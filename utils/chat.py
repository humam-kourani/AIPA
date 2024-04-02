from utils.conversation import create_conversation, create_message, create_process_model_representation
from utils.openai_connection import generate_response_with_history


def chat_with_llm(data, session=None):
    if session is None:
        session = {}

    user_message = data.get('message', '')
    parameters = data.get('parameters', None)
    if parameters is None:
        parameters = {}

    is_first_message = False

    if 'conversation' not in session:
        session['conversation'] = create_conversation(parameters=parameters)
        session['conversation'].append(create_process_model_representation(data, parameters=parameters))
        is_first_message = True

    message = create_message(user_message, role="user", parameters=parameters)
    session['conversation'].append(message)

    new_message, updated_history = generate_response_with_history(data, session, parameters=parameters)
    session['conversation'] = updated_history

    return new_message
