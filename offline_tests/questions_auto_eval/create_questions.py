from utils import chat
import os

DATASET = "ccc19"
REQUIRED_ABSTRACTION = "simplified_xml"
ENABLE_PROMPTING_STRATEGIES = True
MERGE_ALL_MESSAGES_IN_ONE = REQUIRED_ABSTRACTION is not "svg"
OPENAI_API_URL = "https://api.openai.com/v1/"
#OPENAI_API_URL = "http://137.226.117.70:11434/v1/"
#OPENAI_API_URL = "https://api.deepinfra.com/v1/openai/"

if __name__ == "__main__":
    json_repr_file = "../data/"+DATASET+"/json_repr.txt"
    svg_repr_file = "../data/" + DATASET + "/svg_string.txt"
    bpmn_xml_file = "../bpmn_models/ccc19.bpmn"

    bpmn_xml = open(bpmn_xml_file, "r").read()
    bpmn_json = None
    bpmn_svg = None

    if os.path.exists(json_repr_file):
        bpmn_json = open(json_repr_file, "r").read()

    if os.path.exists(svg_repr_file):
        bpmn_svg = open(svg_repr_file, "r").read()

    data = {}
    data["parameters"] = {}
    data["parameters"]["enable_role_prompting"] = ENABLE_PROMPTING_STRATEGIES
    data["parameters"]["enable_natural_language_restriction"] = ENABLE_PROMPTING_STRATEGIES
    data["parameters"]["enable_chain_of_thought"] = ENABLE_PROMPTING_STRATEGIES
    data["parameters"]["enable_process_analysis"] = ENABLE_PROMPTING_STRATEGIES
    data["parameters"]["enable_knowledge_injection"] = False
    data["parameters"]["enable_few_shots_learning"] = ENABLE_PROMPTING_STRATEGIES
    data["parameters"]["enable_negative_prompting"] = ENABLE_PROMPTING_STRATEGIES

    data["parameters"]["merge_all_messages_in_one"] = MERGE_ALL_MESSAGES_IN_ONE

    session = {}
    session["model_name"] = "gpt-4o"
    session["api_key"] = "sk-"
    session["api_url"] = OPENAI_API_URL

    data["parameters"]["model_abstraction"] = REQUIRED_ABSTRACTION
    data["modelXmlString"] = bpmn_xml
    if bpmn_json is not None and bpmn_json:
        data["textualRepresentation"] = bpmn_json
    if bpmn_svg is not None and bpmn_svg:
        data["modelSvg"] = bpmn_svg

    data["message"] = "Could you produce a list of 20 questions related to the underyling process? Please produce real questions about the process. Accompany each question with a relevance score between 1.0 (minimum confidence on the relevance of the question) to 10.0 (maximum confidence)."
    response1 = chat.chat_with_llm(data, session)
    print(response1)
