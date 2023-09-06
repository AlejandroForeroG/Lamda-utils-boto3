## General Summary
This repository contains three utility scripts for working with AWS Lambda and its layers. Each script addresses a specific task related to Lambda function management and associated layers. Below, details are provided for each individual script, including its purpose and usage.
---
**Prerequisites**
- AWS credentials stored in a .env file.
- Python 3.x installed.
- Required Python libraries (boto3, dotenv).
  
### Script 1: Lambda Runtime Updater
This script allows you to update the runtime environment of AWS Lambda functions that meet certain criteria, making it easier to migrate functions to new runtime versions.

**Usage**
- Specify the source and target runtimes within the script.
- The script will generate a report in report.txt with details about updated and non-updated functions.

### Script 2: Lambda Layer Version Inspector
This script inspects AWS Lambda layers and gathers information about their versions and associated functions. It simplifies the process of identifying functions that use specific layers.


**Usage**
- The script will inspect the specified layer, list its versions, and document associated functions in a report in report.txt.

### Script 3: Lambda Layer Updater
This script updates AWS Lambda functions by adding a new layer version. It streamlines the process of updating functions to include new layers.


**Usage**
- Configure your AWS credentials in the .env file.
- Modify the script with details of the existing layer and the new layer.

The script will identify functions using the existing layer and update their configuration to include the new layer.
