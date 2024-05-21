import os
import time
import traceback

from utils import chat


DATASET = "ccc19"
REQUIRED_ABSTRACTION = "simplified_xml"
ENABLE_PROMPTING_STRATEGIES = True
MERGE_ALL_MESSAGES_IN_ONE = False
OPENAI_API_URL = "https://api.openai.com/v1/"

if __name__ == "__main__":
    model_name = "gpt-4o"  # model that answered the questions

    json_repr_file = "../data/"+DATASET+"/json_repr.txt"
    bpmn_xml_file = "../bpmn_models/ccc19.bpmn"
    ground_truth_file = "../data/"+DATASET+"/ground_truth.txt"

    bpmn_xml = open(bpmn_xml_file, "r").read()
    bpmn_json = None
    model_text_description = None

    if os.path.exists(json_repr_file):
        bpmn_json = open(json_repr_file, "r").read()

    if os.path.exists(ground_truth_file):
        model_text_description = open(ground_truth_file, "r").read().strip()

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
        data["parameters"]["enable_few_shots_learning"] = ENABLE_PROMPTING_STRATEGIES
        data["parameters"]["enable_negative_prompting"] = ENABLE_PROMPTING_STRATEGIES

        data["parameters"]["merge_all_messages_in_one"] = MERGE_ALL_MESSAGES_IN_ONE

        session = {}
        session["model_name"] = "gpt-4o" # evaluation model (not the one that answered the questions!)
        session["api_key"] = "sk-"
        session["api_url"] = OPENAI_API_URL

        data["parameters"]["model_abstraction"] = REQUIRED_ABSTRACTION
        data["modelXmlString"] = bpmn_xml
        if bpmn_json is not None and bpmn_json:
            data["textualRepresentation"] = bpmn_json

        current_answer = open("../data/"+DATASET+"/answers/answer_%d_%s.txt" % (index+1, model_name), "r").read().replace("\n\n", "\n").strip()

        message = []
        if model_text_description is not None and model_text_description:
            message.append("Given a textual description of the process provided by an export (which you should take as ground truth):")
            message.append(model_text_description)
        message.append("And given the following question:")
        message.append(quest)
        message.append("Could you provide a score from 1.0 (minimum quality) to 10.0 (maximum quality) to the quality of the following answer:")
        message.append(current_answer)
        message.append("Try to include a brief explanation on why the answer received the given score.")

        message = "\n\n".join(message)

        target_file = "../data/"+DATASET+"/evaluation/eval_%d_%s.txt" % (index+1, model_name)

        if not os.path.exists(target_file):
            while True:
                try:
                    data["message"] = message
                    response1 = chat.chat_with_llm(data, session)
                    print("\n\n")
                    print(message)
                    print("\n\n")
                    print(response1)

                    F = open(target_file, "w")
                    F.write(response1)
                    F.close()

                    break
                except:
                    traceback.print_exc()
                    time.sleep(60)
