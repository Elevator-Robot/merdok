import boto3
from datetime import datetime

# Initialize a session using Amazon DynamoDB
session = boto3.Session()

# Initialize DynamoDB resource
dynamodb = session.resource('dynamodb')

# Reference the chat table
chat_table = dynamodb.Table('MerdokStack-ChatTable7A2D1C24-17H1KRCICVODG')

def write_new_chat(chatSessionId, message):
    timestamp = datetime.utcnow().isoformat()
    response = chat_table.put_item(
        Item={
            'chatSessionId': chatSessionId,
            'timestamp': timestamp,
            'message': message
        }
    )
    return response

# Example usage
if __name__ == "__main__":
    chatSessionId = "session123"
    message = "Hello, this is a new chat message!"
    response = write_new_chat(chatSessionId, message)
    print("Write successful:", response)
