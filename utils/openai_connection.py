from typing import Callable, List, TypeVar, Any
import requests

T = TypeVar('T')


def generate_response_with_history(conversation_history, api_key, openai_model) -> str:
    """
    Generates a response from the LLM using the conversation history.

    :param conversation_history: The conversation history to be included
    :param api_key: OpenAI API key
    :param openai_model: OpenAI model to be used
    :return: The content of the LLM response
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages_payload = []
    for message in conversation_history:
        messages_payload.append({
            "role": message["role"],
            "content": [
                {
                    "type": "text",
                    "text": message["content"]
                }
            ]
        })

    payload = {
        "model": openai_model,
        "messages": messages_payload,
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json()

    try:
        new_message = response["choices"][0]["message"]["content"]
        conversation_history.append({"role": "user", "content": new_message})
        return new_message, conversation_history
    except Exception as e:
        raise Exception("Connection to OpenAI failed! This is the response: " + str(response))
