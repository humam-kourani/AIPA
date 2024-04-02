from utils.prompting import add_prompt_strategies


def create_conversation(role="user", parameters=None):
    if parameters is None:
        parameters = {}

    prompt = add_prompt_strategies(parameters=parameters)
    content = [{"type": "text", "text": f'{prompt}'}]
    conversation = [{"role": role, "content": content}]
    return conversation


def create_message(message: str, role="user", parameters=None):
    if parameters is None:
        parameters = {}

    content = [{"type": "text", "text": f'{message}'}]
    return {"role": role, "content": content}


def create_process_model_representation(data, parameters=None):
    if parameters is None:
        parameters = {}

    textual_representation = data.get('textualRepresentation', '')
    return create_message(
        f'This is a text describing selected elements of the BPMN as dictionaries: {textual_representation}',
        role="user")
