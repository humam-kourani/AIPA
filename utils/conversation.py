from utils.prompting import add_prompt_strategies
from llm_configuration import constants
from typing import Optional


def create_conversation(role="user", parameters=None):
    if parameters is None:
        parameters = {}

    prompt = add_prompt_strategies(parameters=parameters)
    content = [{"type": "text", "text": f'{prompt}'}]
    conversation = [{"role": role, "content": content}]
    return conversation


def create_message(message: str, role="user", additional_content: Optional[str] = None, additional_content_type: str = "text", parameters=None):
    if parameters is None:
        parameters = {}

    content = [{"type": "text", "text": f'{message}'}]

    if additional_content is not None:
        content.append({"type": additional_content_type, additional_content_type: f'{additional_content}'})

    return {"role": role, "content": content}


def create_process_model_representation(data, parameters=None):
    if parameters is None:
        parameters = {}

    model_abstraction = parameters.get("model_abstraction", constants.MODEL_ABSTRACTION)
    abstraction_message = ""

    if model_abstraction == "json":
        textual_representation = data.get('textualRepresentation', '')
        abstraction_message = create_message(
            f'This is a text describing selected elements of the BPMN as dictionaries: {textual_representation}',
            role="user")
    
    return abstraction_message
