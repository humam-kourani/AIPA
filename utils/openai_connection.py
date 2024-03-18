from typing import TypeVar

import requests

T = TypeVar('T')

DEV_MODE = True


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

    if DEV_MODE:
        with open('C:\\Users\\kourani\\azure_api_key.txt', 'r') as file:
            azure_api_key = file.read().strip()

        with open('C:\\Users\\kourani\\azure_endpoint.txt', 'r') as file:
            azure_endpoint = file.read().strip()
            from openai import AzureOpenAI
            client = AzureOpenAI(
                api_key=azure_api_key, 
                api_version="2023-05-15",
                azure_endpoint=azure_endpoint
            )
        response = client.chat.completions.create(model=openai_model, messages=messages_payload)
        try:
            new_message = response.choices[0].message.content
            conversation_history.append({"role": "user", "content": new_message})
            print('HIST', conversation_history)
            return new_message, conversation_history
        except Exception as e:
            raise Exception(f"Connection to OpenAI failed! {e}. This is the response: " + str(response))

    else:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json()
        try:
            new_message = response["choices"][0]["message"]["content"]
            conversation_history.append({"role": "user", "content": new_message})
            print('HIST', conversation_history)
            return new_message, conversation_history
        except Exception as e:
            raise Exception(f"Connection to OpenAI failed! {e}. This is the response: " + str(response))

    
