from utils import chat


if __name__ == "__main__":
    bpmn_json = open("../data/ccc19_json_repr.txt", "r").read()

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
    data["message"] = "Could you produce a list of 20 questions related to the underyling process? Please produce real questions about the process. Accompany each question with a relevance score between 1.0 (minimum confidence on the relevance of the question) to 10.0 (maximum confidence)."
    response1 = chat.chat_with_llm(data, session)
    print(response1)
