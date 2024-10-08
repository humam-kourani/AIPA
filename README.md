# AIPA
AI-Powered Process Analyst 

## Running the app locally 
1. Clone the repo locally
2. Setup virtual Python environment: `python -m venv venv`
3. Activate your virtual environment:
    * For Windows: `.venv\Scripts\activate`
    * For Linux: `source venv/bin/activate`
4. Install the necessary requirements: `pip install -r requirements.txt`
5. Start the app server via `python app.py`
6. You can access the app at `http://127.0.0.1:4555/`

### Running the frontend
1. Prerequisites:
   - Install node and angular-cli:
     - node: https://nodejs.org/en
     - angular-cli: https://angular.io/cli
2. Go to the folder: ./frontend
3. Install npm dependencies: `npm install`
4. Run the frontend application: `npm run start`
5. You can access the frontend application at: `http://localhost:4200/`

### Running both frontend and backend using a single script (Windows)
1. Prerequisites:
   - Prerequisites defined in the last two sections also apply here
   - Requirements are automatically installed by this script and these steps can be skipped here:
     - `pip install -r requirements.txt`
     - `npm install`
2. Go to the folder: ./build_scripts
3. Execute the script: `.\run_aipa_windows.ps1`

## Configure Angular CLI's Development Server
Run `ng serve --host 0.0.0.0`

## Available abstractions
The user can select between the 'json', 'xml', and 'svg' abstractions in the configuration.

If the 'svg' abstraction is selected, then the 'gpt-4-vision-preview' model should be used,
and ImageMagick should be installed and added to the system path.
