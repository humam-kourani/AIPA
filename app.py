import copy
import os
import base64
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from utils.conversation import create_conversation, create_message

from utils.openai_connection import generate_response_with_history


app = Flask(__name__)
session = {}
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['model_name'] = request.form.get('model_name')
        session['api_key'] = request.form.get('api_key')
        try:
            response, conversation = generate_response_with_history(create_conversation(), session['api_key'], session['model_name'])
            session['initial_conversation_without_model'] = conversation
            session.pop('conversation', None)
            session.pop('initial_conversation', None)
            return render_template('upload.html')
        except Exception as e:
            flash(str(e), 'error')
    return render_template("configure_openai.html")
    

@app.route("/upload_bpmn", methods=['GET', 'POST'])
def upload_bpmn():
    if request.method == 'POST':
        file = request.files.get('bpmnFile')
        if file:
            if file.filename.endswith('.bpmn'):
                bpmn_content = file.read().decode('utf-8')
                bpmn_content_base64 = base64.b64encode(bpmn_content.encode('utf-8')).decode('utf-8')
                session.pop('conversation', None)
                return render_template('upload.html', bpmn_content_base64=bpmn_content_base64)
            else:
                flash('Unsupported file type. Please upload a .bpmn file.', 'error')
        else:
            return render_template('upload.html')
    else:
        return redirect("/")
    
@app.route('/chat_with_llm', methods=['POST'])
def chat_with_llm():
    if 'initial_conversation_without_model' not in session:
        return redirect("/index")

    data = request.json
    
    if 'conversation' not in session:
        textual_representation = data.get('textualRepresentation', '')
        session['conversation'] = copy.deepcopy(session['initial_conversation_without_model'])
        session['conversation'].append(create_message(f'This is a text describing selected elements of the BPMN as dictionaries: {textual_representation}'))

    user_message = data.get('message', '')
    session['conversation'].append({"role": "user", "content": user_message})

    api_key = session['api_key']
    openai_model = session['model_name']

    try:
        new_message, updated_history = generate_response_with_history(session['conversation'], api_key, openai_model)
        session['conversation'] = updated_history 
        print(updated_history)
        return jsonify({"response": new_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/reset_conversation', methods=['POST'])
def reset_conversation():
    session.pop('conversation', None)
    return jsonify({"success": "Conversation has been reset"}), 200

    


if __name__ == "__main__":
    app.secret_key = 'your_secret_key'  # Needed for flash messages to work
    app.run(port=4555, debug=True)
