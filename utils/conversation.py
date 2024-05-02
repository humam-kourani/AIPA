from utils.abstraction import get_simplified_xml_abstraction
from utils.prompting import add_prompt_strategies
from llm_configuration import constants
from utils import common


def create_conversation(role="user", parameters=None):
    if parameters is None:
        parameters = {}

    prompt = add_prompt_strategies(parameters=parameters)
    conversation = [create_message(prompt, role=role, parameters=parameters)]
    return conversation


def create_message(message: str, role="user", additional_content=None, additional_content_type: str = "text",
                   parameters=None):
    if parameters is None:
        parameters = {}

    model_abstraction = parameters.get("model_abstraction", constants.MODEL_ABSTRACTION)

    if model_abstraction not in ["svg"]:
        content = message
    else:
        content = [{"type": "text", "text": f'{message}'}]
        if additional_content is not None:
            content.append({"type": additional_content_type, additional_content_type: additional_content})

    message = {"role": role, "content": content}

    return message


def create_process_model_representation(data, parameters=None):
    if parameters is None:
        parameters = {}

    model_abstraction = parameters.get("model_abstraction", constants.MODEL_ABSTRACTION)

    abstraction_message = ""

    if model_abstraction == "json":
        textual_representation = data.get('textualRepresentation', '')
        abstraction_message = create_message(
            f'This is a text describing selected elements of the BPMN as dictionaries: {textual_representation}',
            role="user", parameters=parameters)
    elif model_abstraction == "xml":
        model_xml_string = data.get('modelXmlString', '')

        reduce_xml_size = parameters.get("reduce_xml_size", constants.REDUCE_XML_SIZE)

        if reduce_xml_size:
            model_xml_string = common.reduce_xml_size_using_pm4py(model_xml_string)

        abstraction_message = create_message(
            f"This is a text containing the BPMN 2.0 XML of the process: {model_xml_string}", role="user", parameters=parameters)
    elif model_abstraction == "svg":
        abstraction_message = create_message(f"The following messages attach the BPMN 2.0 visual of the process",
                                             role="user", parameters=parameters)

    return abstraction_message
