# lambda_function.py for the Report Generator
# This script is the brain of our second worker.
# It runs on a daily schedule, reads all data from DynamoDB, creates a summary,
# and saves the summary as a CSV file in S3.

import json
import boto3
import os
import csv
from datetime import datetime

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')

# Get table and bucket names from environment variables
TABLE_NAME = os.environ.get('PROCESSED_DATA_TABLE_NAME', 'ProcessedData')
BUCKET_NAME = os.environ.get('DATA_LAKE_BUCKET_NAME') # You'll need to pass this from Terraform
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    This function is triggered daily by an EventBridge schedule.
    """
    print("Report generation started.")

    try:
        # 1. Scan the DynamoDB table to get all items
        # Note: A Scan operation reads every item in a table. For large tables, this can be slow and expensive.
        # For production apps with large tables, consider a different data model or use Query.
        response = table.scan()
        items = response.get('Items', [])
        
        # Handle pagination if the table is large
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))

        if not items:
            print("No data found in DynamoDB. Exiting.")
            return {
                'statusCode': 200,
                'body': json.dumps('No data to report.')
            }

        # 2. Generate a summary (Example: count total records)
        # You can make this much more complex: calculate averages, sums, etc.
        total_records = len(items)
        summary_data = [
            {'metric': 'Total Records Processed', 'value': total_records}
        ]
        
        # 3. Create a CSV report in the Lambda's temporary storage
        tmp_report_path = '/tmp/daily_summary.csv'
        with open(tmp_report_path, mode='w', newline='') as report_file:
            if summary_data:
                writer = csv.DictWriter(report_file, fieldnames=summary_data[0].keys())
                writer.writeheader()
                writer.writerows(summary_data)
        
        # 4. Upload the report to the S3 bucket in a 'reports' folder
        today_str = datetime.utcnow().strftime('%Y-%m-%d')
        report_key = f"reports/summary-{today_str}.csv"
        
        s3_client.upload_file(tmp_report_path, BUCKET_NAME, report_key)

        print(f"Successfully generated report and uploaded to s3://{BUCKET_NAME}/{report_key}")

        return {
            'statusCode': 200,
            'body': json.dumps('Daily summary report generated successfully!')
        }

    except Exception as e:
        print(f"Error generating report: {e}")
        raise e
