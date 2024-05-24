from typing import TypeVar
from utils.conversation import create_message

import os
import requests

from llm_configuration import constants
from utils import common
from copy import deepcopy
import time

T = TypeVar('T')


class Results:
    LAST_MESSAGES = None
    RESPONSE_JSON = None


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
        raise Exception("Please configure the OpenAI connection!")

    azure_endpoint = session.get('azure_endpoint', '')

    if azure_endpoint:
        from openai import AzureOpenAI

        client = AzureOpenAI(
            api_key=api_key,
            api_version="2023-05-15",
            azure_endpoint=azure_endpoint
        )

        response = client.chat.completions.create(model=openai_model, messages=messages)

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
            "messages": messages,
        }

        Results.LAST_MESSAGES = messages
        for msg in conversation_history:
            if type(msg["content"]) is list:
                for item in msg["content"]:
                    if item["type"] != "text":
                        # set the max tokens property if there are non-textual messages
                        payload["max_tokens"] = constants.MAX_TOKENS_FOR_ADVANC_MSG_TYPES

        complete_url = api_url+"chat/completions"

        response = requests.post(complete_url, headers=headers, json=payload).json()
        Results.RESPONSE_JSON = response

        try:
            response_message = response["choices"][0]["message"]["content"]
        except Exception as e:
            raise Exception(f"Connection to OpenAI failed! This is the response: " + str(response))

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

            current_prompt_file = os.path.join(prompts_dir, str(int(time.time_ns())) + "_" + session_key + ".txt")
            current_response_file = os.path.join(responses_dir, str(int(time.time_ns())) + "_" + session_key + ".txt")

            F = open(current_prompt_file, "w")
            json.dump(Results.LAST_MESSAGES, F)
            F.close()

            F = open(current_response_file, "w")
            json.dump(Results.RESPONSE_JSON, F)
            F.close()

    return response_message, conversation_history
