ENABLE_DEV_MODE = False

AZURE_API_KEY_PATH = 'azure_api_key.txt'
AZURE_ENDPOINT = 'azure_endpoint.txt'
AZURE_OPENAI_MODEL = 'azure_openai_model.txt'

# can be either 'json', 'xml' (the entire process model is provided), or 'svg' (a picture of the process model is uploaded)
MODEL_ABSTRACTION = "json"


DEFAULT_ENABLE_PROMPT_STRATEGIES = True
ENABLE_ROLE_PROMPTING = DEFAULT_ENABLE_PROMPT_STRATEGIES
ENABLE_KNOWLEDGE_INJECTION = DEFAULT_ENABLE_PROMPT_STRATEGIES
ENABLE_NATURAL_LANGUAGE_RESTRICTION = DEFAULT_ENABLE_PROMPT_STRATEGIES
ENABLE_CHAIN_OF_THOUGHT = DEFAULT_ENABLE_PROMPT_STRATEGIES
ENABLE_PROCESS_ANALYSIS = DEFAULT_ENABLE_PROMPT_STRATEGIES
ENABLE_FEW_SHOTS_LEARNING = DEFAULT_ENABLE_PROMPT_STRATEGIES
ENABLE_NEGATIVE_PROMPTING = DEFAULT_ENABLE_PROMPT_STRATEGIES

OPENAI_API_DEFAULT_URL = "https://api.openai.com/v1/"
MAX_TOKENS_FOR_ADVANC_MSG_TYPES = 4096
