import os
import time
import traceback

from utils import chat


if __name__ == "__main__":
    model_name = "gpt-3.5-turbo"
    bpmn_json = open("../data/ccc19_json_repr.txt", "r").read()
    questions = [x.strip() for x in open("../data/ccc19_questions.txt").readlines()]
    model_text_description = open("../data/ccc19.txt", "r").read().strip()

    for index, quest in enumerate(questions):
        data = None
        session = None

        data = {}
        data["parameters"] = {}
        data["parameters"]["model_abstraction"] = "json"
        data["parameters"]["enable_role_prompting"] = True
        data["parameters"]["enable_natural_language_restriction"] = True
        data["parameters"]["enable_chain_of_thought"] = True
        data["parameters"]["enable_process_analysis"] = True
        data["parameters"]["enable_knowledge_injection"] = True

        session = {}
        session["model_name"] = "gpt-4-turbo-preview"
        session["api_key"] = "sk-"

        data["textualRepresentation"] = bpmn_json

        current_answer = open("../data/answers/answer_%d_%s.txt" % (index+1, model_name), "r").read().replace("\n\n", "\n").strip()

        message = []
        message.append("Given a textual description of the process provided by an export (which you should take as ground truth):")
        message.append(model_text_description)
        message.append("And given the following question:")
        message.append(quest)
        message.append("Could you provide a score from 1.0 (minimum quality) to 10.0 (maximum quality) to the quality of the following answer:")
        message.append(current_answer)
        message.append("Try to include a brief explanation on why the answer received the given score.")

        message = "\n\n".join(message)

        target_file = "../data/evaluation/eval_%d_%s.txt" % (index+1, model_name)

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
