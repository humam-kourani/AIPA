from utils import chat


if __name__ == "__main__":
    bpmn_xml = open("bpmn_models/running-example.bpmn").read()

    data = {}
    data["parameters"] = {}
    data["parameters"]["model_abstraction"] = "xml"
    data["parameters"]["enable_role_prompting"] = True
    data["parameters"]["enable_natural_language_restriction"] = True
    data["parameters"]["enable_chain_of_thought"] = True
    data["parameters"]["enable_process_analysis"] = True
    data["parameters"]["enable_knowledge_injection"] = True

    session = {}
    session["model_name"] = "gpt-4-turbo-preview"
    session["api_key"] = "sk-"

    data["modelXmlString"] = bpmn_xml
    data["message"] = "What are the start activities of the process model?"
    response1 = chat.chat_with_llm(data, session)
    print(response1)

    print("\n\n")

    data["message"] = "How confident are you in a scale from 1.0 to 10.0? Can you repeat the original question?"
    response2 = chat.chat_with_llm(data, session)
    print(response2)

    print("\n\n")

    print(session["conversation"])
