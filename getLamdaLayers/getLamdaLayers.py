import boto3
import os
from dotenv import load_dotenv
load_dotenv("../.env") 

# Crdentials for aws lambda
aws_access_key =  os.getenv("aws_access_key")
aws_secret_key = os.getenv("aws_secret_key")
region_name = os.getenv("region_name")

# Create an instance for lamda conection
lambda_client = boto3.client('lambda', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region_name)



def list_versions_of_layer(layer_name):
    try:
        response = lambda_client.list_layer_versions(LayerName=layer_name) # Obtain the information of the layer

        total_functions_by_version = {}  #Dicctionary to save the total of functions by version

        with open('report.txt', 'w') as file:
            for version in response['LayerVersions']:
                file.write(f"Layer: {layer_name}\n")
                file.write(f"Version: {version['Version']}\n")
                file.write(f"Arn: {version['LayerVersionArn']}\n")

                func_paginator = lambda_client.get_paginator('list_functions')
                total_functions = 0  # Counter of functions
                for func_page in func_paginator.paginate():
                    for function in func_page['Functions']:
                        if 'Layers' in function:
                            for function_layer in function['Layers']:
                                if function_layer['Arn'] == version['LayerVersionArn']:
                                    file.write(f"Lamda function associated: {function['FunctionName']}\n")
                                    total_functions += 1
                                    break

                file.write("-" * 30 + "\n")
                total_functions_by_version[version['Version']] = total_functions  

        # Final resume in the file
        with open('report.txt', 'a') as file:
            file.write(f"Resume:\n")
            for version, total_functions in total_functions_by_version.items():
                file.write(f"Version {version}: {total_functions} functions\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    layer_name = "production_config"
    list_versions_of_layer(layer_name)