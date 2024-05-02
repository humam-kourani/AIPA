from utils import chat
import os
import time
import traceback


if __name__ == "__main__":
    model_name = "gpt-3.5-turbo"
    bpmn_json = open("../data/ccc19_json_repr.txt", "r").read()
    questions = [x.strip() for x in open("../data/ccc19_questions.txt").readlines()]

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
        session["model_name"] = model_name
        session["api_key"] = "sk-"

        data["textualRepresentation"] = bpmn_json
        data["message"] = quest

        target_file = "../data/answers/answer_%d_%s.txt" % (index+1, model_name)

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
