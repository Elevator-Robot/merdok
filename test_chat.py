import boto3
import requests
import json
import os
from datetime import datetime

# Get the API details from AWS
def get_api_details():
    client = boto3.client('appsync')
    # List GraphQL APIs
    response = client.list_graphql_apis()
    
    # Get the first API (assuming it's our chat API)
    api = response['graphqlApis'][0]
    api_id = api['apiId']
    api_url = api['uris']['GRAPHQL']
    
    # Get API Key
    keys = client.list_api_keys(apiId=api_id)
    api_key = keys['apiKeys'][0]['id']
    
    return api_url, api_key

def send_test_message():
    api_url, api_key = get_api_details()
    
    # GraphQL mutation
    mutation = """
    mutation SendMessage {
        sendMessageToChat(
            chatSessionId: "test-session-1"
            userId: "test-user-1"
            content: "Hello, this is a test message!"
        ) {
            messageId
            chatSessionId
            userId
            content
            timestamp
            isBotResponse
        }
    }
    """
    
    # Headers for the request
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }
    
    # Make the request
    response = requests.post(
        api_url,
        headers=headers,
        json={'query': mutation}
    )
    
    # Print the response
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    send_test_message()
