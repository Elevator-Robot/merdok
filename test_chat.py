import boto3
import requests
import json
import os
import dotenv

dotenv.load_dotenv()

# Cognito Pool constants
USER_POOL_ID = "us-east-1_jq7L9L7CH"
CLIENT_ID = "q9ql4rmsu26d7tskkc8a9bm17"
TEST_USERNAME = os.getenv("COGNITO_USERNAME")
TEST_PASSWORD = os.getenv("COGNITO_PASSWORD")


def get_cognito_token():
    """Get authentication token from Cognito"""
    client = boto3.client("cognito-idp")

    try:
        response = client.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",  # valid options: [ADMIN_NO_SRP_AUTH, ADMIN_USER_PASSWORD_AUTH, USER_SRP_AUTH, REFRESH_TOKEN_AUTH, REFRESH_TOKEN, CUSTOM_AUTH, USER_PASSWORD_AUTH, USER_AUTH]
            AuthParameters={"USERNAME": TEST_USERNAME, "PASSWORD": TEST_PASSWORD},
            ClientId=CLIENT_ID,
        )
        return response["AuthenticationResult"]["IdToken"]
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
    
    # Debug prints
    print(f"API URL: {api_url}")
    print(f"Token (first 50 chars): {token[:50]}...")
    
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
        "Authorization": f"Bearer {token}"
    }
    
    # Debug prints
    print("Headers:", json.dumps(headers, indent=2))
    
    # Make the request
    response = requests.post(api_url, headers=headers, json={"query": mutation})
    
    # Debug response
    print(f"Response Status Code: {response.status_code}")
    print("Response Headers:", json.dumps(dict(response.headers), indent=2))

    # Print the response
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    send_test_message()
