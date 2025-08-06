# FLYFOX AI AWS Lambda Deployment Script
import boto3
import zipfile
import os

def deploy_flyfox_lambda():
    """Deploy FLYFOX AI quantum voice calling to AWS Lambda"""
    
    # Create deployment package
    with zipfile.ZipFile('flyfox_quantum_voice.zip', 'w') as zipf:
        zipf.write('flyfox_lambda_handler.py')
        zipf.write('flyfox_quantum_voice_implementation.py')
        # Add other dependencies as needed
    
    # Deploy to AWS Lambda
    lambda_client = boto3.client('lambda')
    
    try:
        response = lambda_client.create_function(
            FunctionName='flyfox-quantum-voice-assistant',
            Runtime='python3.11',
            Handler='flyfox_lambda_handler.lambda_handler',
            Role='arn:aws:iam::YOUR_ACCOUNT:role/lambda-role',
            Code={'ZipFile': open('flyfox_quantum_voice.zip', 'rb').read()},
            Environment={
                'Variables': {
                    'OPENAI_API_KEY': 'your-openai-key',
                    'DYNEX_API_KEY': 'your-dynex-key',
                    'FLYFOX_AI_BRANDED': 'true'
                }
            }
        )
        print(f"FLYFOX AI Lambda deployed: {response['FunctionArn']}")
        return True
    except Exception as e:
        print(f"Lambda deployment failed: {e}")
        return False

if __name__ == "__main__":
    deploy_flyfox_lambda()
