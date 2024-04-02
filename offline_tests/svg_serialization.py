from utils import chat
import pm4py
from tempfile import NamedTemporaryFile


if __name__ == "__main__":
    bpmn = pm4py.read_bpmn("bpmn_models/running-example.bpmn")
    svg_path = NamedTemporaryFile(suffix=".svg")
    svg_path.close()
    svg_path = svg_path.name

    pm4py.save_vis_bpmn(bpmn, svg_path)
    svg_string = open(svg_path, "r").read()

    data = {}
    data["parameters"] = {}
    data["parameters"]["model_abstraction"] = "svg"
    data["parameters"]["enable_role_prompting"] = True
    data["parameters"]["enable_natural_language_restriction"] = True
    data["parameters"]["enable_chain_of_thought"] = True
    data["parameters"]["enable_process_analysis"] = True
    data["parameters"]["enable_knowledge_injection"] = True

    session = {}
    session["model_name"] = "gpt-4-vision-preview"
    session["api_key"] = "sk-"

    data["modelSvg"] = svg_string
    data["message"] = "What are the start activities of the process model?"
    response1 = chat.chat_with_llm(data, session)
    print(response1)

    print("\n\n")

    # a timer needs to be implemented, otherwise the tokens-per-minute are easily exceeded

    #data["message"] = "How confident are you in a scale from 1.0 to 10.0? Can you repeat the original question?"
    #response2 = chat.chat_with_llm(data, session)
    #print(response2)

    print("\n\n")

    print(session["conversation"])
