# llm_pm
Process Mining with LLMs 

## Running the app locally 
1. Clone the repo locally
2. Setup virtual Python environment: `python -m venv venv`
3. Activate your virtual environment:
    * For Windows: `venv\Scripts\activate`
    * For Linux: `source venv/bin/activate`
4. Install the necessary requirements: `pip install -r requirements.txt`
5. Start the app server via `python app.py`
6. You can access the app at `http://127.0.0.1:4555/`

## Available abstractions
The user can select between the 'json', 'xml', and 'svg' abstractions in the configuration.

If the 'svg' abstraction is selected, then the 'gpt-4-vision-preview' model should be used,
and ImageMagick should be installed and added to the system path.
