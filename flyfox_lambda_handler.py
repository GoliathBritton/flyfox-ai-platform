
# FLYFOX AI AWS Lambda Handler
import json
import asyncio
from flyfox_quantum_voice_implementation import FlyfoxQuantumVoiceAssistant

async def lambda_handler(event, context):
    """AWS Lambda handler for FLYFOX AI quantum voice calls"""
    
    body = json.loads(event['body'])
    call_type = body.get('type', 'flyfox_quantum_voice')
    
    quantum_assistant = FlyfoxQuantumVoiceAssistant()
    
    if call_type == 'start_call':
        call_session = await quantum_assistant.start_quantum_call(
            body['call_id'], 
            body['initial_message']
        )
        return {
            'statusCode': 200,
            'body': json.dumps(call_session),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    
    elif call_type == 'process_message':
        response = await quantum_assistant.process_quantum_call_message(
            body['call_id'], 
            body['message']
        )
        return {
            'statusCode': 200,
            'body': json.dumps(response),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Invalid call type'}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }

# For local testing
if __name__ == "__main__":
    # Test event
    test_event = {
        'body': json.dumps({
            'type': 'start_call',
            'call_id': 'flyfox_lambda_test_001',
            'initial_message': 'Hello from FLYFOX AI Lambda!'
        })
    }
    
    result = asyncio.run(lambda_handler(test_event, None))
    print(f"Lambda Test Result: {result}")
