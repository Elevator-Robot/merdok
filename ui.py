import streamlit as st
import boto3
from mypy_boto3_bedrock_runtime import BedrockRuntimeClient


# Initialize AWS Bedrock client
# client: BedrockRuntimeClient = boto3.client('bedrock-runtime') # type: ignore

# st.title("Dungeon Master")

# def send_message_to_bedrock(message):
#     response = client.converse_stream(
#         modelId="bedrock-aws",
#         messages=[
#             {
#                 'type': 'message',
#                 'content': message
#             }
#         ]
#     )
#     return response['messages'][0]['content']

# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# with st.form(key='chat_form'):
#     user_input = st.text_input("You: ", "")
#     submit_button = st.form_submit_button(label='Send')


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
