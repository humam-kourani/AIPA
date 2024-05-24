from utils import chat, openai_connection
import os
import time
import json
import traceback


DATASET = "ccc19"
REQUIRED_ABSTRACTION = "simplified_xml"
ENABLE_PROMPTING_STRATEGIES = True
MERGE_ALL_MESSAGES_IN_ONE = REQUIRED_ABSTRACTION is not "svg"
OPENAI_API_URL = "https://api.openai.com/v1/"
#OPENAI_API_URL = "http://137.226.117.70:11434/v1/"
#OPENAI_API_URL = "https://api.deepinfra.com/v1/openai/"

if __name__ == "__main__":
    model_name = "gpt-4o"

    json_repr_file = "../data/"+DATASET+"/json_repr.txt"
    svg_repr_file = "../data/"+DATASET+"/svg_string.txt"
    bpmn_xml_file = "../bpmn_models/ccc19.bpmn"

    bpmn_xml = open(bpmn_xml_file, "r").read()
    bpmn_json = None
    bpmn_svg = None

    if os.path.exists(json_repr_file):
        bpmn_json = open(json_repr_file, "r").read()

    if os.path.exists(svg_repr_file):
        bpmn_svg = open(svg_repr_file, "r").read()

    questions = [x.strip() for x in open("../data/"+DATASET+"/questions.txt", encoding="utf-8").readlines()]

    for index, quest in enumerate(questions):
        data = None
        session = None

        data = {}
        data["parameters"] = {}
        data["parameters"]["enable_role_prompting"] = ENABLE_PROMPTING_STRATEGIES
        data["parameters"]["enable_natural_language_restriction"] = ENABLE_PROMPTING_STRATEGIES
        data["parameters"]["enable_chain_of_thought"] = ENABLE_PROMPTING_STRATEGIES
        data["parameters"]["enable_process_analysis"] = ENABLE_PROMPTING_STRATEGIES
        data["parameters"]["enable_knowledge_injection"] = False
        data["parameters"]["enable_few_shots_learning"] = False
        data["parameters"]["enable_negative_prompting"] = False

        data["parameters"]["merge_all_messages_in_one"] = MERGE_ALL_MESSAGES_IN_ONE

        session = {}
        session["model_name"] = model_name
        session["api_key"] = "sk-"
        session["api_url"] = OPENAI_API_URL

        data["parameters"]["model_abstraction"] = REQUIRED_ABSTRACTION
        data["modelXmlString"] = bpmn_xml
        if bpmn_json is not None and bpmn_json:
            data["textualRepresentation"] = bpmn_json
        if bpmn_svg is not None and bpmn_svg:
            data["modelSvg"] = bpmn_svg

        data["message"] = quest

        m_name = model_name.replace("/", "").replace(":", "")

        target_file = "../data/"+DATASET+"/answers/answer_%d_%s.txt" % (index+1, m_name)
        ex_time_file = "../data/"+DATASET+"/ex_time/ex_time_%d_%s.txt" % (index+1, m_name)
        response_file = "../data/"+DATASET+"/responses/response_%d_%s.txt" % (index+1, m_name)
        prompt_file = "../data/"+DATASET+"/prompts/prompt_%d_%s.txt" % (index+1, m_name)

        if not os.path.exists(target_file):
            while True:
                try:
                    print("\n\n")
                    print(quest)
                    t0 = time.time()
                    response1 = chat.chat_with_llm(data, session)
                    t1 = time.time()
                    print(response1)

                    F = open(target_file, "w")
                    F.write(response1)
                    F.close()

                    F = open(ex_time_file, "w")
                    F.write("%.2f" % (t1-t0))
                    F.close()

                    F = open(response_file, "w")
                    json.dump(openai_connection.Results.RESPONSE_JSON, F)
                    F.close()

                    F = open(prompt_file, "w")
                    json.dump(openai_connection.Results.LAST_MESSAGES, F)
                    F.close()

                    break
                except:
                    traceback.print_exc()
                    time.sleep(60)
