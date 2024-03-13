import os
import base64
import openai
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from utils.conversation import create_conversation

from utils.openai_connection import generate_response_with_history


app = Flask(__name__)
session = {}
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model_name = request.form.get('model_name')
        api_key = request.form.get('api_key')
        try:
            response, conversation = generate_response_with_history(create_conversation(), api_key, model_name)
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
                return render_template('upload.html', bpmn_content_base64=bpmn_content_base64)
            else:
                flash('Unsupported file type. Please upload a .bpmn file.', 'error')
        else:
            return render_template('upload.html')
    else:
        return redirect("/")



if __name__ == "__main__":
    app.secret_key = 'your_secret_key'  # Needed for flash messages to work
    app.run(port=4555, debug=True)
