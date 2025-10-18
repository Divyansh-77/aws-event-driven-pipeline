# variables.tf - Defines input variables for our Terraform configuration.
# This makes our code reusable and easy to configure.

variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}