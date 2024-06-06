import os
import time
import traceback

from utils import chat


DATASET = "ccc19"
REQUIRED_ABSTRACTION = "simplified_xml"
ENABLE_PROMPTING_STRATEGIES = True
MERGE_ALL_MESSAGES_IN_ONE = REQUIRED_ABSTRACTION is not "svg"
OPENAI_API_URL = "https://api.openai.com/v1/"
#OPENAI_API_URL = "http://137.226.117.70:11434/v1/"
#OPENAI_API_URL = "https://api.deepinfra.com/v1/openai/"

if __name__ == "__main__":
    model_name = "gpt-4o"  # model that answered the questions

    json_repr_file = "../data/"+DATASET+"/json_repr.txt"
    svg_repr_file = "../data/" + DATASET + "/svg_string.txt"
    bpmn_xml_file = "../bpmn_models/ccc19.bpmn"
    ground_truth_file = "../data/"+DATASET+"/ground_truth.txt"
    questions_ground_truth = "../data/"+DATASET+"/ground_truth/"

    bpmn_xml = open(bpmn_xml_file, "r").read()
    bpmn_json = None
    bpmn_svg = None
    model_text_description = None

    if os.path.exists(json_repr_file):
        bpmn_json = open(json_repr_file, "r").read()

    if os.path.exists(svg_repr_file):
        bpmn_svg = open(svg_repr_file, "r").read()

    if os.path.exists(ground_truth_file):
        model_text_description = open(ground_truth_file, "r").read().strip()

    questions = [x.strip() for x in open("../data/"+DATASET+"/questions.txt", encoding="utf-8").readlines()]

    for index, quest in enumerate(questions):
        target_file = "../data/"+DATASET+"/evaluation/eval_%d_%s.txt" % (index+1, model_name.replace("/", "").replace(":", ""))

        question_ground_truth_file = os.path.join(questions_ground_truth, "ground_truth_%d.txt" % (index+1))
        question_ground_truth = None

        current_answer_file = "../data/"+DATASET+"/answers/answer_%d_%s.txt" % (index+1, model_name.replace("/", "").replace(":", ""))

        if os.path.exists(question_ground_truth_file):
            question_ground_truth = open(question_ground_truth_file, "r").read().strip()

        if os.path.exists(current_answer_file) and not os.path.exists(target_file):
            data = None
            session = None

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
            session["model_name"] = "gpt-4o" # evaluation model (not the one that answered the questions!)
            session["api_key"] = "sk-"
            session["api_url"] = OPENAI_API_URL

            data["parameters"]["model_abstraction"] = REQUIRED_ABSTRACTION
            data["modelXmlString"] = bpmn_xml
            if bpmn_json is not None and bpmn_json:
                data["textualRepresentation"] = bpmn_json
            if bpmn_svg is not None and bpmn_svg:
                data["modelSvg"] = bpmn_svg

            current_answer = open(current_answer_file, "r").read().replace("\n\n", "\n").strip()

            message = []
            if model_text_description is not None and model_text_description:
                message.append("Given a textual description of the process provided by an export (which you should take as ground truth):")
                message.append(model_text_description)
            message.append("And given the following question:")
            message.append(quest)

            if question_ground_truth is not None and question_ground_truth:
                message.append("And the following answer given by an human, which you should consider as correct:")
                message.append(question_ground_truth)

            message.append("Could you provide a score from 1.0 (minimum quality) to 10.0 (maximum quality) to the quality of the following answer:")
            message.append(current_answer)
            message.append("Try to include a brief explanation on why the answer received the given score.")

            message = "\n\n".join(message)

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
