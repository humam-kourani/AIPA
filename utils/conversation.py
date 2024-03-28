from typing import List

from utils.prompting import add_prompt_strategies


def create_conversation() -> List[dict[str:str]]:
    prompt = add_prompt_strategies()
    conversation = [{"role": "user", "content": f'{prompt}'}]
    return conversation


def create_message(message: str) -> List[dict[str:str]]:
    return {"role": "user", "content": f'{message}'}
