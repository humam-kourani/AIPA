from typing import List


def create_conversation() -> List[dict[str:str]]:
    prompt = "You are an expert in BPMN. I will give you a BPMN model and ask you questions about it. Please only answer in natural language so any one not familiar with BPMNs can understand the underlying process flow; i.e., do not mention any technical terms like Task, Gate, flow, etc."
    conversation = [{"role": "user", "content": f'{prompt}'}]
    return conversation


def create_message(message: str) -> List[dict[str:str]]:
    return {"role": "user", "content": f'{message}'}
