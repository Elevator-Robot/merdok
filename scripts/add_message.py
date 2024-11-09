import uuid
from datetime import datetime, timezone
from typing import Any, Dict

import boto3


class MessageSender:
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(table_name)

    def send_message(
        self, conversation_id: str, content: str, sender: str
    ) -> Dict[str, Any]:
        """
        Add a new message to a conversation
        """
        message = {
            "conversationId": conversation_id,
            "id": str(uuid.uuid4()),
            "content": content,
            "sender": sender,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        self.table.put_item(Item=message)
        return message


if __name__ == "__main__":
    message_sender = MessageSender(
        "MerdokStack-MessagesTable05B58A27-7A4GD0OPXJW5"
    )
    message = message_sender.send_message(
        "b2eb0531-a6aa-4c7d-81bb-74f41d99a199", "Are you alive?", "Bob"
    )
    print(message)
