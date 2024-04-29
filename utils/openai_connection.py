from typing import TypeVar
from utils.conversation import create_message

import importlib.resources
import os
import requests

from llm_configuration import constants
from utils import common
from copy import deepcopy

T = TypeVar('T')


def generate_response_with_history(data, session, parameters=None) -> str:
    """
    Generates a response from the LLM using the conversation history.

    :param data: Data provided to the service
    :param session: Session dictionary
    :param parameters: Optional parameters
    :return: The content of the LLM response
    """
    if parameters is None:
        parameters = {}

    conversation_history = session["conversation"]  # The conversation history
    model_abstraction = parameters.get("model_abstraction", constants.MODEL_ABSTRACTION)
    merge_all_messages_in_one = parameters.get("merge_all_messages_in_one", constants.MERGE_ALL_MESSAGES_IN_ONE)

    if model_abstraction == "svg":
        svg_string = data.get('modelSvg', '')
        additional_content = {"url": common.get_png_url_from_svg(svg_string, parameters=parameters)}
        additional_content_type = "image_url"

        conversation_history = deepcopy(conversation_history)

        conversation_history[-1]["content"].append(
            {"type": additional_content_type, additional_content_type: additional_content})

    #print(conversation_history)

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

        with importlib.resources.path("llm_configuration", constants.AZURE_OPENAI_MODEL) as path:
            if os.path.exists(path):
                openai_model = open(path, 'r').read().strip()
            else:
                raise Exception(str(path) + " (AZURE_OPENAI_MODEL) does not exist!")

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
        try:
            openai_model = session['model_name']
            api_key = session['api_key']
            api_url = session.get('api_url', '')

            if api_url is not None and api_url:
                if not api_url.endswith("/"):
                    api_url += "/"
            else:
                api_url = constants.OPENAI_API_DEFAULT_URL
        except:
            raise Exception("Please configure the OpenAI connection!")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        if merge_all_messages_in_one:
            messages = [{"role": "user", "content": "\n\n".join(x["content"] for x in conversation_history)}]
        else:
            messages = conversation_history

        payload = {
            "model": openai_model,
            "messages": messages,
        }

        for msg in conversation_history:
            if type(msg["content"]) is list:
                for item in msg["content"]:
                    if item["type"] != "text":
                        # set the max tokens property if there are non-textual messages
                        payload["max_tokens"] = constants.MAX_TOKENS_FOR_ADVANC_MSG_TYPES

        complete_url = api_url+"chat/completions"

        response = requests.post(complete_url, headers=headers, json=payload).json()

        try:
            response_message = response["choices"][0]["message"]["content"]
        except Exception as e:
            raise Exception(f"Connection to OpenAI failed! This is the response: " + str(response))

    conversation_history.append(create_message(response_message, role="system", parameters=parameters))
    return response_message, conversation_history
