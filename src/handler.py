import json
from aws_lambda_powertools import Logger
from database_operations import (
    store_connection,
    delete_connection,
    retrieve_conversation,
    update_conversation,
)
from openai_interface import generate_message, format_prompt


logger = Logger(service="assistant")


@logger.inject_lambda_context(log_event=True)
def connect(event, context):
    """Handle connection event."""
    connection_id = event["requestContext"]["connectionId"]
    user_id = event.get("queryStringParameters", {}).get("userId", "defaultUserId")
    store_connection(connection_id, user_id)
    return {"statusCode": 200}


@logger.inject_lambda_context(log_event=True)
def disconnect(event, context):
    """Handle disconnection event."""
    connection_id = event["requestContext"]["connectionId"]
    delete_connection(connection_id)
    return {"statusCode": 200}


@logger.inject_lambda_context(log_event=True)
def send_message(event, context):
    """Handle send_message event."""
    user_id = event.get("userId", "defaultUserId")
    body = json.loads(event.get("body", "") or "{}")
    user_message = body.get("message", "")

    default_conversation = [
        {
            "role": "system",
            "content": "You are Brigh, the Goddess of Invention, in the Pathfinder universe. You are a benevolent deity known for your wisdom, creativity, and guidance. You are the Dungeon Master guiding a user through a grand campaign that spans multiple planes of existence in the Pathfinder universe. The user relies on your advice and guidance to navigate the challenges they encounter. Your tone is confident, creative, and enlightening, with a touch of divine authority. You are not just narrating the story; you are weaving it and influencing the course of events. Remember to provide rich descriptions of the environments, engage in role-play with the user, and manage the mechanics of the game.",  # noqa: E501
            # ... rest of the message
        }
    ]
    conversation = retrieve_conversation(user_id, default_conversation)
    conversation.append({"role": "user", "content": user_message})
    prompt = format_prompt(conversation)  # Define your format_prompt function based on your logic

    generated_message = generate_message(prompt)
    conversation.append({"role": "assistant", "content": generated_message})
    update_conversation(user_id, conversation)

    logger.debug(f"userId: {user_id}")
    logger.debug(f"userMessage: {user_message}")
    logger.debug(f"conversation: {conversation}")
    logger.debug(f"prompt: {prompt}")
    logger.debug(f"generatedMessage: {generated_message}")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": generated_message, "conversation": conversation}),
    }
