'Script elaborated by Alejandro Forero'
#Changue de runtimes in the bottom of this script

import boto3
from tqdm import tqdm
aws_access_key = 'access key'
aws_secret_key = 'secret key'
region_name = 'us-east-1'

lambda_client = boto3.client('lambda', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region_name)

# Lists to store function names
functionNames = []
functionsNotUpdated = []
functionsUpdated = []

# Function to list Lambda functions by runtime and update them to a new runtime
def list_lamdas_per_version(runtime, newRuntime):
    try:
        # Open a file to save the report
        with open('report.txt', 'w') as file: 
            # Create a paginator for Lambda functions
            func_paginator = lambda_client.get_paginator('list_functions')
            total_functions = 0
            # Initialize a progress bar for reading functions
            with tqdm(total=204, desc="Reading functions") as pbar:
                for func_page in func_paginator.paginate():
                    for function in func_page['Functions']:
                        # Check if the function matches the runtime and naming convention
                        if function['Runtime'] == runtime and function['FunctionName'].startswith('development_'):
                            # Append the function name to the list
                            functionNames.append(function['FunctionName'])
                            total_functions += 1
                            pbar.update(1)
            # Close the file
            file.close()
        
        # Initialize a progress bar for updating functions
        with tqdm(total=total_functions, desc="Updating functions...") as pbar: # Progress bar
            for functionName in functionNames:
                # Update the Lambda function configuration
                response = lambda_client.update_function_configuration(
                    FunctionName=functionName,
                    Runtime=newRuntime
                )
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    pbar.update(1)
                    functionsUpdated.append(functionName)
                    print(f"Function {functionName} updated successfully")
                else:
                    print(f"Function {functionName} not updated")
                    functionsNotUpdated.append(functionName)
                    
        # Create a report
        with open('report.txt', 'a') as file:
            file.write("## Functions not updated\n")
            file.write("---\n")
            file.write(f'### Total functions not updated: {len(functionsNotUpdated)}\n\n')
            for functionNotUpdated in functionsNotUpdated:
                file.write(f"- {functionNotUpdated}\n")
            file.write('## Functions updated\n')
            file.write("---\n")
            file.write(f'### Total functions updated: {len(functionsUpdated)}\n\n')
            for functionUpdated in functionsUpdated:
                file.write(f"- {functionUpdated}\n")
            
            file.close()
            
    except Exception as e:
        print(e)

if __name__ == "__main__":
    # Specify the source and target runtimes
    runtime = "nodejs14.x"
    newRuntime = "nodejs18.x"
    list_lamdas_per_version(runtime, newRuntime)  