import boto3
import requests
from requests_aws4auth import AWS4Auth # type: ignore

def query_graphql_api():
    url = "https://47aypigcbzgzlousfetzpdjn2e.appsync-api.us-east-1.amazonaws.com/graphql"
    query = """
    query {
        listMessages(chatSessionId: "session123") {
            messageId
            chatSessionId
            userId
            content
            timestamp
            isBotResponse
        }
    }
    """

    # Get temporary AWS credentials from the current session
    session = boto3.Session()
    credentials = session.get_credentials().get_frozen_credentials()
    region = 'us-east-1'

    # Set up AWS4Auth for signing requests using AWS_IAM
    auth = AWS4Auth(credentials.access_key,
                    credentials.secret_key,
                    region,
                    'appsync',
                    session_token=credentials.token)

    # Make the signed request
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, auth=auth, json={'query': query}, headers=headers)

    # Check response
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed to run by returning code of {response.status_code}. {response.text}")

# Run the query
result = query_graphql_api()
print(result)
