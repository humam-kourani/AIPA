from utils import chat
import os

DATASET = "ccc19"
REQUIRED_ABSTRACTION = "simplified_xml"

if __name__ == "__main__":
    json_repr_file = "../data/"+DATASET+"/json_repr.txt"
    bpmn_xml_file = "../bpmn_models/ccc19.bpmn"

    bpmn_xml = open(bpmn_xml_file, "r").read()
    bpmn_json = None

    if os.path.exists(json_repr_file):
        bpmn_json = open(json_repr_file, "r").read()

    data = {}
    data["parameters"] = {}
    data["parameters"]["enable_role_prompting"] = True
    data["parameters"]["enable_natural_language_restriction"] = True
    data["parameters"]["enable_chain_of_thought"] = True
    data["parameters"]["enable_process_analysis"] = True
    data["parameters"]["enable_knowledge_injection"] = True

    session = {}
    session["model_name"] = "gpt-4-turbo-preview"
    session["api_key"] = "sk-"

    data["parameters"]["model_abstraction"] = REQUIRED_ABSTRACTION
    data["modelXmlString"] = bpmn_xml
    if bpmn_json is not None and bpmn_json:
        data["textualRepresentation"] = bpmn_json

    data["message"] = "Could you produce a list of 20 questions related to the underyling process? Please produce real questions about the process. Accompany each question with a relevance score between 1.0 (minimum confidence on the relevance of the question) to 10.0 (maximum confidence)."
    response1 = chat.chat_with_llm(data, session)
    print(response1)
