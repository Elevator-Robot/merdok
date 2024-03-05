import json
from http import HTTPStatus

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler.api_gateway import ApiGatewayResolver, Response
from aws_lambda_powertools.event_handler.exceptions import BadRequestError

from aws_lambda_powertools.tracing import Tracer
from database_operations import (
    store_connection,
    delete_connection,
    retrieve_conversation,
    update_conversation,
)
from openai_interface import generate_message, format_prompt


LOGGER: Logger = Logger()

TRACER: Tracer = Tracer()
APP: ApiGatewayResolver = ApiGatewayResolver()


@APP.post("/connect")  # type: ignore
@LOGGER.inject_lambda_context(log_event=True)
def connect(event, context: LambdaContext):
    """Handle connection event."""
    try:
        connection_id = event["requestContext"]["connectionId"]
        user_id = event.get("queryStringParameters", {}).get("userId", "defaultUserId")
        store_connection(connection_id, user_id)
        return {"statusCode": HTTPStatus.OK.value, "body": "Connected."}
    except BadRequestError as err:
        return {"statusCode": HTTPStatus.BAD_REQUEST.value, "body": str(err)}


@APP.post("/disconnect")  # type: ignore
@LOGGER.inject_lambda_context(log_event=True)
def disconnect(event, context: LambdaContext):
    """Handle disconnection event."""
    connection_id = event["requestContext"]["connectionId"]
    delete_connection(connection_id)
    return {"statusCode": HTTPStatus.OK.value, "body": "Disconnected."}


@APP.post("/send-message")  # type: ignore
@LOGGER.inject_lambda_context(log_event=True)
def send_message(event, context: LambdaContext) -> Response[str]:
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
    prompt = format_prompt(
        conversation
    )  # Define your format_prompt function based on your logic

    generated_message = generate_message(prompt)
    conversation.append({"role": "assistant", "content": generated_message})
    update_conversation(user_id, conversation)

    LOGGER.debug(f"userId: {user_id}")
    LOGGER.debug(f"userMessage: {user_message}")
    LOGGER.debug(f"conversation: {conversation}")
    LOGGER.debug(f"prompt: {prompt}")
    LOGGER.debug(f"generatedMessage: {generated_message}")

    return Response(
        status_code=HTTPStatus.OK.value,
        headers={"Content-Type": "application/json"},
        body=json.dumps({"message": generated_message, "conversation": conversation}),
    )
