from typing import TypeVar
from utils.conversation import create_message

import os
import requests

from llm_configuration import constants
from utils import common
from copy import deepcopy
import time
import re
import json

T = TypeVar('T')


class Results:
    LAST_MESSAGES = None
    RESPONSE_JSON = None


def strip_non_unicode_characters(text):
    # Define a pattern that matches all valid Unicode characters.
    pattern = re.compile(r'[^\u0000-\uFFFF]', re.UNICODE)
    # Replace characters not matching the pattern with an empty string.
    cleaned_text = pattern.sub('', text)
    cleaned_text = cleaned_text.encode('cp1252', errors='ignore').decode('cp1252')

    return cleaned_text


def serialize_completion(completion):
    return {
        "id": completion.id,
        "choices": [
            {
                "finish_reason": choice.finish_reason,
                "index": choice.index,
                "message": {
                    "content": choice.message.content,
                    "role": choice.message.role,
                    "function_call": {
                        "arguments": json.loads(
                            choice.message.function_call.arguments) if choice.message.function_call and choice.message.function_call.arguments else None,
                        "name": choice.message.function_call.name
                    } if choice.message and choice.message.function_call else None
                } if choice.message else None
            } for choice in completion.choices
        ],
        "created": completion.created,
        "model": completion.model,
        "object": completion.object,
        "system_fingerprint": completion.system_fingerprint,
        "usage": {
            "completion_tokens": completion.usage.completion_tokens,
            "prompt_tokens": completion.usage.prompt_tokens,
            "total_tokens": completion.usage.total_tokens
        }
    }


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
    session_key = parameters.get("session_key", "")

    svg_string = data.get('modelSvg', '')
    json_repr = data.get('textualRepresentation', '')

    if False:
        F = open("svg_string.txt", "w")
        F.write(svg_string)
        F.close()

        F = open("json_repr.txt", "w")
        F.write(json_repr)
        F.close()

    if model_abstraction == "svg":
        additional_content = {"url": common.get_png_url_from_svg(svg_string, parameters=parameters)}
        additional_content_type = "image_url"

        conversation_history = deepcopy(conversation_history)

        conversation_history[-1]["content"].append(
            {"type": additional_content_type, additional_content_type: additional_content})

    if merge_all_messages_in_one:
        messages = [{"role": "user", "content": "\n\n".join(x["content"] for x in conversation_history)}]
    else:
        messages = conversation_history

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
        raise Exception("The OpenAI connection is not configured. Please configure the OpenAI connection")

    azure_endpoint = session.get('azure_endpoint', '')

    if azure_endpoint:
        from openai import AzureOpenAI

        client = AzureOpenAI(
            api_key=api_key,
            api_version="2023-05-15",
            azure_endpoint=azure_endpoint
        )

        response = client.chat.completions.create(model=openai_model, messages=messages)
        Results.LAST_MESSAGES = messages
        Results.RESPONSE_JSON = serialize_completion(response)

        try:
            response_message = response.choices[0].message.content
        except Exception as e:
            raise Exception(response['error']['message'])

    else:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": openai_model,
            "messages": messages,
        }

        Results.LAST_MESSAGES = messages
        for msg in conversation_history:
            if type(msg["content"]) is list:
                for item in msg["content"]:
                    if item["type"] != "text":
                        # set the max tokens property if there are non-textual messages
                        payload["max_tokens"] = constants.MAX_TOKENS_FOR_ADVANC_MSG_TYPES

        complete_url = api_url + "chat/completions"

        response = requests.post(complete_url, headers=headers, json=payload).json()
        Results.RESPONSE_JSON = response

        try:
            response_message = response["choices"][0]["message"]["content"]
        except Exception as e:
            raise Exception(response['error']['message'])

    response_message = strip_non_unicode_characters(response_message)
    conversation_history.append(create_message(response_message, role="system", parameters=parameters))

    if session_key is not None and session_key:
        if constants.ENABLE_SESSION_RECORDINGS:
            logging_dir = constants.SESSION_RECORDINGS_DIR
            if not os.path.exists(logging_dir):
                os.mkdir(logging_dir)
            prompts_dir = os.path.join(logging_dir, "prompts")
            responses_dir = os.path.join(logging_dir, "responses")

            if not os.path.exists(prompts_dir):
                os.mkdir(prompts_dir)

            if not os.path.exists(responses_dir):
                os.mkdir(responses_dir)

            current_prompt_file = os.path.join(prompts_dir, str(int(time.time_ns())) + "_" + re.sub(r'[^a-zA-Z0-9]', '',
                                                                                                    session_key) + ".txt")
            current_response_file = os.path.join(responses_dir,
                                                 str(int(time.time_ns())) + "_" + re.sub(r'[^a-zA-Z0-9]', '',
                                                                                         session_key) + ".txt")

            F = open(current_prompt_file, "w")
            json.dump(Results.LAST_MESSAGES, F)
            F.close()

            F = open(current_response_file, "w")
            json.dump(Results.RESPONSE_JSON, F)
            F.close()

    return response_message, conversation_history
