import boto3
import requests
import json
import os
from datetime import datetime

# Cognito Pool constants
USER_POOL_ID = 'us-east-1_jq7L9L7CH'
CLIENT_ID = 'your-client-id'  # You'll need to add your app client ID
TEST_USERNAME = 'your-test-username'
TEST_PASSWORD = 'your-test-password'

def get_cognito_token():
    """Get authentication token from Cognito"""
    client = boto3.client('cognito-idp')
    
    try:
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': TEST_USERNAME,
                'PASSWORD': TEST_PASSWORD
            },
            ClientId=CLIENT_ID
        )
        return response['AuthenticationResult']['IdToken']
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        raise

def get_api_details():
    """Get AppSync API URL"""
    client = boto3.client("appsync")
    response = client.list_graphql_apis()
    
    # Get the first API (assuming it's our chat API)
    api = response["graphqlApis"][0]
    api_url = api["uris"]["GRAPHQL"]
    
    return api_url

def send_test_message():
    api_url = get_api_details()
    token = get_cognito_token()

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

    # Headers for the request with Cognito token
    headers = {
        "Content-Type": "application/json",
        "Authorization": token
    }

    # Make the request
    response = requests.post(api_url, headers=headers, json={"query": mutation})

    # Print the response
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    send_test_message()
