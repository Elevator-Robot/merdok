import json
import boto3
import logging
from botocore.exceptions import ClientError
from mypy_boto3_bedrock_runtime.client import BedrockRuntimeClient as BedrockClient
from typing import cast

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class DragonChatHandler:
    def __init__(self, region: str):
        self.client = cast(BedrockClient, boto3.client("bedrock-runtime", region_name=region))

    def generate_message(self, model_id, system_prompt, messages, max_tokens):
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": messages
        })

        try:
            response = self.client.invoke_model(body=body, modelId=model_id)
            response_body = json.loads(response.get('body').read())
            return response_body
        except ClientError as err:
            message = err.response["Error"]["Message"]
            logger.error("A client error occurred: %s", message)
            raise

    def send_message(self, message, model="anthropic.claude-3-haiku-20240307-v1:0"):
        user_message = {"role": "user", "content": message}
        messages = [user_message]
        system_prompt = "Please respond to the user's message."
        max_tokens = 300

        return self.generate_message(model, system_prompt, messages, max_tokens)

    def start_conversation(self, initial_message):
        return self.send_message(initial_message)

    def continue_conversation(self, message):
        return self.send_message(message)

if __name__ == "__main__":
    chat_handler = DragonChatHandler("us-east-1")

    # Continue the conversation in a loop
    while True:
        user_input = input("Input message: ")
        response = chat_handler.continue_conversation(user_input)
        response_string = response["content"][0]["text"]

        print(f"{response_string}\n")
