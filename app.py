import os
import base64

from flask import Flask, request, jsonify, abort, make_response
from flask_cors import CORS
from utils import chat

app = Flask(__name__)
CORS(app)
session_dict = {}
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def __get_session(session_key):
    session = session_dict.get(session_key, None)
    if session is None:
        session = {}
    return session


@app.route("/", methods=['GET', 'POST'])
def upload_bpmn():
    session_key = request.remote_addr + request.user_agent.string
    session = __get_session(session_key)

    if request.method == 'POST':
        file = request.files.get('bpmnFile')
        if file:
            if file.filename.endswith('.bpmn'):
                session.pop('conversation', None)

                session_dict[session_key] = session

                bpmn_content = file.read().decode('utf-8')
                bpmn_content_base64 = base64.b64encode(bpmn_content.encode('utf-8')).decode('utf-8')
                response = make_response(jsonify(success=True, bpmn_content_base64=bpmn_content_base64), 200)
            else:
                # TODO: this is not working
                response = make_response(jsonify(success=False, error='Unsupported file type. Please upload a .bpmn file.'), 400)

            return response
        else:
            abort(500)
    else:
        abort(500)


@app.route('/update-config', methods=['POST'])
def update_config():
    session_key = request.remote_addr + request.user_agent.string
    session = __get_session(session_key)

    session['model_name'] = request.json['model_name']
    session['api_key'] = request.json['api_key']
    session['api_url'] = request.json['api_url']
    session['azure_endpoint'] = request.json['azure_endpoint']

    session_dict[session_key] = session

    response = make_response(jsonify({'some': 'data'}), 200)

    return response


@app.route('/chat_with_llm', methods=['POST'])
def chat_with_llm():
    session_key = request.remote_addr + request.user_agent.string
    session = __get_session(session_key)

    session["session_key"] = session_key

    data = request.json

    try:
        new_message = chat.chat_with_llm(data, session=session)

        session_dict[session_key] = session

        response = make_response(jsonify({"response": new_message}), 200)
    except Exception as e:
        response = make_response(jsonify(success=False, error="The following error occured: " + str(e)), 400)

    return response


@app.route('/reset_conversation', methods=['POST'])
def reset_conversation():
    session_key = request.remote_addr + request.user_agent.string
    session = __get_session(session_key)

    session.pop('conversation', None)

    session_dict[session_key] = session

    response = make_response(jsonify({"success": "Conversation has been reset"}), 200)

    return response


if __name__ == "__main__":
    app.secret_key = 'your_secret_key'  # Needed for flash messages to work
    app.run(host='0.0.0.0', port=4555, debug=True)
