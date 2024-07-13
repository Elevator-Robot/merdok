from os import environ
import json
import boto3
from mypy_boto3_bedrock_runtime.client import BedrockRuntimeClient as BedrockClient
from typing import cast

class DragonChatHandler:
    def __init__(self, api_key: str, secret_key: str, region: str):
        self.client = cast(BedrockClient, boto3.client(
            "bedrock-runtime",
            aws_access_key_id=api_key,
            aws_secret_access_key=secret_key,
            region_name=region
        ))

    def send_message(self, message, model="anthropic.claude-3-haiku-20240307-v1:0"):
        response = self.client.invoke_model(
            accept="application/json",
            modelId=model,
            body=json.dumps({
                "input": message,
                "parameters": {
                    "system": "You are a knight in the kingdom of Larion. You are questing to defeat the dragon and save the kingdom."
                }
            })
        )

    def start_conversation(self, initial_message):
        return self.send_message(initial_message)

    def continue_conversation(self, message):
        return self.send_message(message)

if __name__ == "__main__":
    api_key = environ.get("AWS_ACCESS_KEY_ID")
    secret_key = str(environ.get("AWS_SECRET_ACCESS_KEY"))
    print(f"API Key: {api_key}")
    print(f"Secret Key: {secret_key}")
    if api_key:
        chat_handler = DragonChatHandler(api_key, secret_key, "us-east-1")
        initial_message = "You are a knight in the kingdom of Larion. You are questing to defeat the dragon and save the kingdom."
        chat_handler.start_conversation(initial_message)
    else:
        print("Please set the AWS_ACCESS_KEY_ID environment variable")
