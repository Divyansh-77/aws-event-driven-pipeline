# Automated Serverless Data Pipeline on AWS

<p align="center">
  <img src="https://img.shields.io/badge/AWS-Serverless-FF9900?logo=amazonaws&style=for-the-badge" alt="AWS Serverless">
  <img src="https://img.shields.io/badge/Terraform-IaC-7B42BC?logo=terraform&style=for-the-badge" alt="Terraform IaC">
  <img src="https://img.shields.io/badge/GitHub_Actions-CI/CD-2088FF?logo=githubactions&style=for-the-badge" alt="GitHub Actions CI/CD">
  <img src="https://img.shields.io/badge/Python-3.9-3776AB?logo=python&style=for-the-badge" alt="Python 3.9">
</p>

<p align="center">
  <img src="https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/YOUR_REPO/deploy.yml?branch=main&style=flat-square&logo=github" alt="CI/CD Pipeline Status">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="License: MIT">
</p>

This project demonstrates a fully automated, event-driven, and serverless data processing pipeline built on Amazon Web Services (AWS). The entire infrastructure is managed using **Terraform** (Infrastructure as Code) and deployed automatically via a **CI/CD pipeline** using GitHub Actions.

The pipeline is designed to ingest raw sales data from CSV files, process it, and store it in a structured NoSQL database for analysis, all without managing a single server.

---

## 🏛️ Architecture Diagram

The architecture is designed for scalability, cost-efficiency, and minimal operational overhead. The flow of data is entirely event-driven.

![Architecture Diagram](images/architecture.png)

---

## 🚀 Key Features

* **Event-Driven:** The entire pipeline is triggered automatically by an event (a file upload to S3), making it highly responsive.
* **Fully Serverless:** No servers to provision, manage, or patch. This follows AWS best practices, leading to significant cost savings (pay-per-use) and reduced operational burden.
* **Infrastructure as Code (IaC):** The entire AWS infrastructure is defined as code using Terraform. This ensures consistent, repeatable, and version-controlled environments.
* **Automated CI/CD:** A complete GitHub Actions workflow automates the process of building, packaging, and deploying the infrastructure and Lambda code on every `git push`.
* **Scalability & Resilience:** Leverages managed AWS services (S3, Lambda, DynamoDB) that scale automatically and are inherently highly available.
* **Cost-Effective:** By using serverless components, you only pay for the exact compute time and storage used. **All services used fall within the AWS Free Tier** for typical development usage.

---

## 🛠️ Technology Stack

<p align="center">
  <a href="https://aws.amazon.com/"><img src="https://img.shields.io/badge/AWS-232F3E?logo=amazonaws&logoColor=white&style=for-the-badge" alt="AWS"></a>
  <a href="https://aws.amazon.com/s3/"><img src="https://img.shields.io/badge/S3-569A31?logo=amazons3&logoColor=white&style=for-the-badge" alt="Amazon S3"></a>
  <a href="https://aws.amazon.com/lambda/"><img src="https://img.shields.io/badge/Lambda-FF9900?logo=awslambda&logoColor=white&style=for-the-badge" alt="AWS Lambda"></a>
  <a href="https://aws.amazon.com/dynamodb/"><img src="https://img.shields.io/badge/DynamoDB-4053D6?logo=amazondynamodb&logoColor=white&style=for-the-badge" alt="Amazon DynamoDB"></a>
  <a href="https://aws.amazon.com/eventbridge/"><img src="https://img.shields.io/badge/EventBridge-C54030?logo=amazoneventbridge&logoColor=white&style=for-the-badge" alt="Amazon EventBridge"></a>
  <a href="https://aws.amazon.com/cloudwatch/"><img src="https://img.shields.io/badge/CloudWatch-FF4F8B?logo=amazoncloudwatch&logoColor=white&style=for-the-badge" alt="Amazon CloudWatch"></a>
  <a href="https://www.terraform.io/"><img src="https://img.shields.io/badge/Terraform-7B42BC?logo=terraform&logoColor=white&style=for-the-badge" alt="Terraform"></a>
  <a href="https://github.com/features/actions"><img src="https://img.shields.io/badge/GitHub_Actions-2088FF?logo=githubactions&logoColor=white&style=for-the-badge" alt="GitHub Actions"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white&style=for-the-badge" alt="Python"></a>
</p>

* **Cloud Provider:** **AWS (Amazon Web Services)**
* **Core Services:**
    * **Amazon S3:** For object storage (data ingestion and reporting).
    * **AWS Lambda:** For serverless compute (data processing logic).
    * **Amazon DynamoDB:** For a fully managed NoSQL database.
    * **Amazon EventBridge:** For scheduled, cron-based triggers.
    * **Amazon CloudWatch:** For logging, monitoring, and debugging.
    * **AWS IAM:** For secure access management and permissions.
* **Infrastructure as Code:** **Terraform**
* **CI/CD:** **GitHub Actions**
* **Programming Language:** **Python 3.9** (for Lambda functions)

---

## ⚙️ How It Works (End-to-End Flow)

1.  **Trigger:** A user uploads a `.csv` file into the `sales_data/` folder in the S3 bucket.
2.  **Event Notification:** S3 detects the new object and automatically sends an event notification to the `data-processor` AWS Lambda function.
3.  **Processing:** The Lambda function is invoked. Its Python script reads the CSV file, parses each row, and writes the structured data as individual items into the DynamoDB table.
4.  **Storage:** The processed data is now securely stored in DynamoDB, ready for querying.
5.  **Scheduled Reporting (Daily):** An Amazon EventBridge rule runs on a daily schedule (cron job), triggering the `report-generator` Lambda. This function scans DynamoDB, generates a summary report, and saves it to a separate S3 bucket.

---

## 📁 Project Structure

├── .github/workflows/ │ ├── deploy.yml # GitHub Actions workflow for deployment │ └── destroy.yml # GitHub Actions workflow for cleanup ├── src/ │ ├── data_processor/ │ │ └── lambda_function.py # Python code for processing data │ └── report_generator/ │ └── lambda_function.py # Python code for generating reports ├── terraform/ │ ├── main.tf # Core Terraform configuration │ ├── variables.tf # Input variables │ └── provider.tf # AWS provider configuration └── sales_data.csv # Sample input data file
 
 ---

## 🔧 Setup and Deployment

This project is designed for fully automated deployment.

### Prerequisites

* An AWS Account with appropriate permissions.
* A GitHub Account.
* An **IAM Role in AWS** that GitHub Actions can assume (OpenID Connect - OIDC). This is the most secure and modern way (no long-lived `AWS_ACCESS_KEY_ID` needed).

### Configuration

1.  **Fork this Repository:** Create your own copy.
2.  **Configure GitHub Secrets:** In your forked repository, go to `Settings > Secrets and variables > Actions` and add the following secrets:
    * `AWS_REGION`: The AWS region to deploy to (e.g., `us-east-1`).
    * `AWS_IAM_ROLE_ARN`: The ARN of the IAM Role that GitHub Actions will assume.

### Deployment

The deployment is triggered automatically by a `git push` to the `main` branch (unless you use `[skip ci]`).

1.  Clone your forked repository.
2.  Make any desired changes (e.g., in the `terraform` or `src` directory).
3.  Commit and push the changes:
    ```bash
    git add .
    git commit -m "My first commit"
    git push origin main
    ```
4.  Go to the **"Actions"** tab in your GitHub repository to monitor the deployment workflow.

---

## 💡 Usage (Demonstration)

Once the `deploy` workflow is successful:

1.  Navigate to the **Amazon S3** console.
2.  Find the bucket named `sales-pipeline-data-<...>`
3.  Navigate into the `sales_data/` folder.
4.  Upload the provided `sales_data.csv` file.
5.  Navigate to the **Amazon DynamoDB** console.
6.  Open the table named `sales-pipeline-data-table-<...>` and explore its items. The data from the CSV will appear within the seconds.

---

## 🧹 Cleanup: Avoiding AWS Bills (₹0 Goal)

**This is the most important step to avoid all AWS bills.**

To prevent ongoing charges, you **must** destroy all created resources when you are finished.

A `destroy` workflow has been configured for this purpose.

1.  In your GitHub repository, go to the **"Actions"** tab.
2.  On the left, click on the **"Destroy AWS Infrastructure"** workflow.
3.  Click the **"Run workflow"** dropdown button and then click the green **"Run workflow"** button.

This will trigger a job that runs `terraform destroy`, safely removing all AWS resources created by this project, ensuring you pay **₹0**.
