from openai import OpenAI as openai
from os import environ

class DragonChatHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def send_message(self, message, model="text-davinci-003"):
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a knight in the kingdom of Larion. You are questing to defeat the dragon and save the kingdom."
                },
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

    def start_conversation(self, initial_message):
        return self.send_message(initial_message)

    def continue_conversation(self, message):
        return self.send_message(message)

if __name__ == "__main__":
    api_key = environ.get("OPENAI_API_KEY")
    if api_key:
        chat_handler = DragonChatHandler(api_key)
        initial_message = "You are a knight in the kingdom of Larion. You are questing to defeat the dragon and save the kingdom."
        chat_handler.start_conversation(initial_message)
    else:
        print("Please set the OPENAI_API_KEY environment variable")
