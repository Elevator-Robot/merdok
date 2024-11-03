import json
import uuid
from datetime import datetime
import boto3

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Get the table name from environment variables or use a default for now
    table = dynamodb.Table('ChatTable')
    
    if 'arguments' in event:
        # Handle GraphQL mutations/queries
        field = event.get('info', {}).get('fieldName')
        
        if field == 'startNewChatSession':
            return handle_start_new_chat_session(event, table)
    
    return {
        'statusCode': 400,
        'body': json.dumps('Invalid request')
    }

def handle_start_new_chat_session(event, table):
    # Extract userId from arguments
    user_id = event['arguments']['userId']
    
    # Generate a unique chat session ID
    chat_session_id = str(uuid.uuid4())
    
    # Get current timestamp in ISO format
    timestamp = datetime.utcnow().isoformat()
    
    # Create chat session item
    chat_session = {
        'chatSessionId': chat_session_id,
        'userId': user_id,
        'createdAt': timestamp
    }
    
    # Save to DynamoDB
    table.put_item(Item=chat_session)
    
    # Return the chat session object matching the GraphQL schema
    return chat_session
