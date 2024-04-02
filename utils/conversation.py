from typing import List

from utils.prompting import add_prompt_strategies


def create_conversation(role="user") -> List[dict[str:str]]:
    prompt = add_prompt_strategies()
    conversation = [{"role": role, "content": [{"type": "text", "text": f'{prompt}'}]}]
    return conversation


def create_message(message: str, role="user") -> List[dict[str:str]]:
    return {"role": role, "content": [{"type": "text", "text": f'{message}'}]}
