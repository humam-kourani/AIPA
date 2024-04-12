import os
import base64
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from utils import chat

app = Flask(__name__)
CORS(app, origins=['http://localhost:4200'])
session = {}
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# @app.route("/", methods=['GET', 'POST'])
# def upload_bpmn():
#     return render_template('index.html')

@app.route("/", methods=['GET', 'POST'])
def upload_bpmn():
    if request.method == 'POST':
        file = request.files.get('bpmnFile')
        if file:
            if file.filename.endswith('.bpmn'):

                session.pop('conversation', None)

                bpmn_content = file.read().decode('utf-8')
                bpmn_content_base64 = base64.b64encode(bpmn_content.encode('utf-8')).decode('utf-8')
                return jsonify(success=True, bpmn_content_base64=bpmn_content_base64)
            else:
                # TODO: this is not working
                return jsonify(success=False, error='Unsupported file type. Please upload a .bpmn file.'), 400
        else:
            return render_template('upload.html')
    else:
        return render_template('upload.html')


@app.route('/update-config', methods=['POST'])
def update_config():
    session['model_name'] = request.json['model_name']
    session['api_key'] = request.json['api_key']
    return jsonify({'message': 'Configuration saved successfully'})


@app.route('/chat_with_llm', methods=['POST'])
def chat_with_llm():
    data = request.json

    try:
        new_message = chat.chat_with_llm(data, session=session)
        return jsonify({"response": new_message})
    except Exception as e:
        return jsonify(success=False, error="The following error occured: " + str(e)), 400


@app.route('/reset_conversation', methods=['POST'])
def reset_conversation():
    session.pop('conversation', None)
    return jsonify({"success": "Conversation has been reset"}), 200


@app.route('/test_route', methods=['GET'])
def test_route():
    return jsonify({"message": "hello world"}), 200


if __name__ == "__main__":
    app.secret_key = 'your_secret_key'  # Needed for flash messages to work
    app.run(port=4555, debug=True)
