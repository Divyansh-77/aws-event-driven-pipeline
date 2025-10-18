# lambda_function.py for the Data Processor
# This Python script is the brain of our first worker.
# It reads a CSV file from S3, processes it, and saves the data to DynamoDB.

import json
import boto3
import os
import csv
import uuid
from urllib.parse import unquote_plus

# Initialize AWS clients outside the handler for better performance (reuse connections).
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
# Get the DynamoDB table name from an environment variable set by Terraform (best practice).
TABLE_NAME = os.environ.get('PROCESSED_DATA_TABLE_NAME', 'ProcessedData')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    """
    This function is triggered when a file is uploaded to the S3 bucket.
    """
    print("Received event:", json.dumps(event))

    try:
        # 1. Get the bucket and file name from the event
        s3_record = event['Records'][0]['s3']
        bucket_name = s3_record['bucket']['name']
        # Handle spaces or special characters in file names
        key = unquote_plus(s3_record['object']['key'])

        print(f"Processing file: s3://{bucket_name}/{key}")

        # 2. Download the CSV file from S3 to a temporary location in Lambda
        tmp_file_path = f"/tmp/{key.split('/')[-1]}"
        s3_client.download_file(bucket_name, key, tmp_file_path)

        # 3. Read the CSV and write each row to DynamoDB
        with open(tmp_file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            # Use batch_writer for efficient bulk writes to DynamoDB
            with table.batch_writer() as batch:
                for row in csv_reader:
                    # Generate a unique ID for each record
                    row['record_id'] = str(uuid.uuid4())
                    
                    # You might want to add more data cleaning/transformation here
                    # For example, converting strings to numbers, validating data, etc.
                    print("Putting item:", row)
                    batch.put_item(Item=row)

        print(f"Successfully processed {key} and stored data in DynamoDB.")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Data processed successfully!')
        }

    except Exception as e:
        print(f"Error processing file: {e}")
        # It's important to raise the error to let AWS know the invocation failed.
        # This can be useful for setting up redrive policies or alerts.
        raise e
