from utils import chat
import os
import time
import traceback


DATASET = "ccc19"
REQUIRED_ABSTRACTION = "simplified_xml"
ENABLE_PROMPTING_STRATEGIES = True
MERGE_ALL_MESSAGES_IN_ONE = False
OPENAI_API_URL = "https://api.openai.com/v1/"

if __name__ == "__main__":
    model_name = "gpt-4o"

    json_repr_file = "../data/"+DATASET+"/json_repr.txt"
    bpmn_xml_file = "../bpmn_models/ccc19.bpmn"

    bpmn_xml = open(bpmn_xml_file, "r").read()
    bpmn_json = None

    if os.path.exists(json_repr_file):
        bpmn_json = open(json_repr_file, "r").read()

    questions = [x.strip() for x in open("../data/"+DATASET+"/questions.txt").readlines()]

    for index, quest in enumerate(questions):
        data = None
        session = None

        data = {}
        data["parameters"] = {}
        data["parameters"]["enable_role_prompting"] = ENABLE_PROMPTING_STRATEGIES
        data["parameters"]["enable_natural_language_restriction"] = ENABLE_PROMPTING_STRATEGIES
        data["parameters"]["enable_chain_of_thought"] = ENABLE_PROMPTING_STRATEGIES
        data["parameters"]["enable_process_analysis"] = ENABLE_PROMPTING_STRATEGIES
        data["parameters"]["enable_knowledge_injection"] = ENABLE_PROMPTING_STRATEGIES

        data["parameters"]["merge_all_messages_in_one"] = MERGE_ALL_MESSAGES_IN_ONE

        session = {}
        session["model_name"] = model_name
        session["api_key"] = "sk-"
        session["api_url"] = OPENAI_API_URL

        data["parameters"]["model_abstraction"] = REQUIRED_ABSTRACTION
        data["modelXmlString"] = bpmn_xml
        if bpmn_json is not None and bpmn_json:
            data["textualRepresentation"] = bpmn_json

        data["message"] = quest

        target_file = "../data/"+DATASET+"/answers/answer_%d_%s.txt" % (index+1, model_name)

        if not os.path.exists(target_file):
            while True:
                try:
                    print("\n\n")
                    print(quest)
                    response1 = chat.chat_with_llm(data, session)
                    print(response1)

                    F = open(target_file, "w")
                    F.write(response1)
                    F.close()

                    break
                except:
                    traceback.print_exc()
                    time.sleep(60)
