from typing import TypeVar
from utils.conversation import create_message

import importlib.resources
import os
import requests

from llm_configuration import constants


T = TypeVar('T')


def generate_response_with_history(session, api_key, openai_model) -> str:
    """
    Generates a response from the LLM using the conversation history.

    :param session: Session dictionary
    :param api_key: OpenAI API key
    :param openai_model: OpenAI model to be used
    :return: The content of the LLM response
    """

    conversation_history = session["conversation"] # The conversation history

    if constants.ENABLE_DEV_MODE:
        from openai import AzureOpenAI

        with importlib.resources.path("llm_configuration", constants.AZURE_API_KEY_PATH) as path:
            if os.path.exists(path):
                azure_api_key = open(path, 'r').read().strip()
            else:
                raise Exception(str(path) + " (AZURE_API_KEY_PATH) does not exist!")

        with importlib.resources.path("llm_configuration", constants.AZURE_ENDPOINT) as path:
            if os.path.exists(path):
                azure_endpoint = open(path, 'r').read().strip()
            else:
                raise Exception(str(path) + " (AZURE_ENDPOINT) does not exist!")

        client = AzureOpenAI(
            api_key=azure_api_key,
            api_version="2023-05-15",
            azure_endpoint=azure_endpoint
        )

        response = client.chat.completions.create(model=openai_model, messages=conversation_history)

        try:
            response_message = response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Connection to OpenAI failed! This is the response: " + str(response))

    else:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": openai_model,
            "messages": conversation_history,
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json()

        try:
            response_message = response["choices"][0]["message"]["content"]
        except Exception as e:
            raise Exception(f"Connection to OpenAI failed! This is the response: " + str(response))

    conversation_history.append(create_message(response_message, role="system"))
    return response_message, conversation_history
