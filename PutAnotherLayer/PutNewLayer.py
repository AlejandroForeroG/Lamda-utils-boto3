import boto3
import os
from dotenv import load_dotenv
load_dotenv() 

# Crdentials for aws lambda
aws_access_key =  os.getenv("aws_access_key")
aws_secret_key = os.getenv("aws_secret_key")
region_name = os.getenv("region_name")

lambda_client = boto3.client('lambda', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region_name)

def list_of_lambdas(layer_name, version_name, new_layer_name):

    try:
        # Get the specified layer version
        response = lambda_client.get_layer_version(LayerName=layer_name, VersionNumber=version_name)
        
        # Get the specified new layer version
        new_layer = lambda_client.get_layer_version(LayerName=new_layer_name, VersionNumber=newLayerVersion)
        
        functionArray = []

        # Print the ARN of the new layer
        print(new_layer['LayerVersionArn'])

        # Create a paginator to list functions
        func_paginator = lambda_client.get_paginator('list_functions')

        for func_page in func_paginator.paginate():  # Iterate over pages of functions
            for function in func_page['Functions']:  # Iterate over functions in the page
                if 'Layers' in function:  # Check if the function has layers
                    for function_layer in function['Layers']:
                        if function_layer['Arn'] == response['LayerVersionArn']:
                            # Add the function ARN to the array
                            functionArray.append(str(function['FunctionArn']))

        for functionArn in functionArray:
            print(functionArn)
            partsFunction = functionArn.split(':')
            nameFunction = partsFunction[6]

            # Update the configuration of the lambda function
            try:
                lambda_client.update_function_configuration(
                    FunctionName=functionArn,
                    Layers=[response['LayerVersionArn'], new_layer['LayerVersionArn']]
                )
                print(f"Layer {new_layer['LayerVersionArn']} added to function {nameFunction} progress: {functionArray.index(functionArn)+1}/{len(functionArray)}")
            except Exception as e:
                print("There was an error:", e)
                break

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    layer_name = "development_config"
    version_name = 80
    new_layer_name = "mobo-config-dev-central"
    newLayerVersion = 7
    list_of_lambdas(layer_name, version_name, new_layer_name)
