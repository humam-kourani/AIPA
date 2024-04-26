ENABLE_DEV_MODE = False
DISABLE_LLM_CONNECTION = True

AZURE_API_KEY_PATH = 'azure_api_key.txt'
AZURE_ENDPOINT = 'azure_endpoint.txt'
AZURE_OPENAI_MODEL = 'azure_openai_model.txt'

# can be either 'json', 'xml', 'simplified_xml' (the entire process model is provided for xml and simplified xml), or 'svg' (a picture of the process model is uploaded)
MODEL_ABSTRACTION = "simplified_xml"

ENABLE_ROLE_PROMPTING = True
ENABLE_KNOWLEDGE_INJECTION = True
ENABLE_NATURAL_LANGUAGE_RESTRICTION = True
ENABLE_CHAIN_OF_THOUGHT = True
ENABLE_PROCESS_ANALYSIS = True
ENABLE_FEW_SHOTS_LEARNING = True
ENABLE_NEGATIVE_PROMPTING = True

OPENAI_API_DEFAULT_URL = "https://api.openai.com/v1/"
MAX_TOKENS_FOR_ADVANC_MSG_TYPES = 4096
