from typing import List


def create_conversation() -> List[dict[str:str]]:
    prompt = "You are an expert in BPMN. I will give you a BPMN model and ask you questions about it."
    conversation = [{"role": "user", "content": f'{prompt}'}]
    return conversation
