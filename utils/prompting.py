from llm_configuration import constants


def add_prompt_strategies(parameters=None):
    if parameters is None:
        parameters = {}

    model_abstraction = parameters.get("model_abstraction", constants.MODEL_ABSTRACTION)

    enable_role_prompting = parameters.get("enable_role_prompting", constants.ENABLE_ROLE_PROMPTING)
    enable_natural_language_restriction = parameters.get("enable_natural_language_restriction",
                                                         constants.ENABLE_NATURAL_LANGUAGE_RESTRICTION)
    enable_chain_of_thought = parameters.get("enable_chain_of_thought", constants.ENABLE_CHAIN_OF_THOUGHT)
    enable_process_analysis = parameters.get("enable_process_analysis", constants.ENABLE_PROCESS_ANALYSIS)
    enable_knowledge_injection = parameters.get("enable_knowledge_injection", constants.ENABLE_KNOWLEDGE_INJECTION)
    enable_few_shots_learning = parameters.get("enable_few_shots_learning", constants.ENABLE_FEW_SHOTS_LEARNING)
    enable_negative_prompting = parameters.get("enable_negative_prompting", constants.ENABLE_NEGATIVE_PROMPTING)

    prompt = ''

    if enable_role_prompting:
        role_prompt = role_prompting()
        prompt += role_prompt

    if enable_natural_language_restriction:
        nlp_restriction = natural_language_restriction()
        prompt += nlp_restriction

    if enable_chain_of_thought:
        ch_of_thought = chain_of_thoughts()
        prompt += ch_of_thought

    if enable_process_analysis:
        proc_anal = process_analysis()
        prompt += proc_anal

    if enable_knowledge_injection:
        know_inj = knowledge_injection()
        prompt += know_inj

    if model_abstraction == "json":
        if enable_few_shots_learning:
            few_shots = few_shots_learning_json()
            prompt += few_shots
        if enable_negative_prompting:
            negative_prompt = negative_prompting_json()
            prompt += negative_prompt

    return prompt


def role_prompting():
    return "- Your role: you are an expert in business process modeling and BPMN. I will give you a textual representation of a full BPMN model or only selected elements of a BPMN (e.g., a set of tasks and flows) and ask you questions about the process. You are supposed to answer the question based on your understanding of the provided model.\n\n"


def knowledge_injection():
    return """
- Business Process Model and Notation (BPMN) is a standardized graphical notation for modeling business processes. It enables precise modeling, covering simple tasks to complex inter-organizational interactions. Key BPMN elements include:

1. **Flow Objects**: These are the main graphical elements to define behavior in a BPMN diagram.
   - **Events**: Represent something that happens during the course of a process. There are Start, Intermediate, and End events.
   - **Activities**: Work that is performed within a process. Activities can be Tasks (atomic activities) or Sub-Processes (which can be broken down into finer levels of detail).
   - **Gateways**: Control the flow of the process, determining branching, forking, merging, and joining of paths based on data or events.

2. **Connecting Objects**: These define the flow or relationship between Flow Objects.
   - **Sequence Flows**: Determine activities' order.
   - **Message Flows**:  Show messages between participants.
   - **Associations**: Link information, like text annotations, to Flow Objects.

3. **Swimlanes**: Organizational tools used to categorize activities within a process.
   - **Pools**: Represent major participants in a process, typically entire organizations or large departments.
   - **Lanes**: Break down Pools into smaller roles or responsibilities.

4. **Artifacts**: Provide additional information about the process.
   - **Data Objects**: Show how data is required or produced by activities.
   - **Groups**: Visually separate diagram parts without affecting the sequence flow.
   - **Text Annotations**: Offer explanations or extra information about parts of the model.

5. **Choreographies and Collaborations**: Illustrate interactions between business entities.
   - **Choreographies**: Define the expected behavior between two or more business participants.
   - **Collaborations**: Show relationships and message exchanges between two or more distinct processes or participants.\n\n\n"""


def natural_language_restriction():
    return "- Please answer in natural language, so that any user not familiar with the BPMN standard can understand your answer without any technical knowledge; i.e., avoid technical terms like Task, Gate, flow, lane, etc.; rather use natural language to describe the behavior of the underlying process.\n\n"


def chain_of_thoughts():
    return "- Where possible, please share the chain of thoughts or reasoning behind your answers. This helps in understanding not just what you think, but also how you arrived at that conclusion, providing a richer insight into your analytical process, all while remaining based on the process flow without using any technical terms.\n\n"


def process_analysis():
    return "- Where possible, discuss the advantages and disadvantages of the process/subprocess/path in question. A balanced analysis will provide a more comprehensive understanding of its efficacy and areas for areas for improvement.\n\n"


process_textual_representation_json = """Selected BPMN Elements and Connections:
- { $type: bpmn:Collaboration, id: Collaboration_1y0blh3, participants: [object Object],[object Object],[object Object], messageFlows: [object Object],[object Object],[object Object],[object Object],[object Object],[object Object], $parent: Definitions_1 }
- { $type: bpmn:Participant, id: Participant_1x9zkso, name: credit scoring frontend (bank), processRef: Process_1, $parent: Collaboration_1y0blh3 }
- { $type: bpmn:Participant, id: Participant_0e81yis, name: credit scoring (bank), processRef: Process_0hiditg, $parent: Collaboration_1y0blh3 }
- { $type: bpmn:Task, id: Task_16winvj, name: request credit score, $parent: Process_0hiditg }
- { $type: bpmn:ExclusiveGateway, id: ExclusiveGateway_0e5en8h, name: score received?, $parent: Process_0hiditg }
- { $type: bpmn:ExclusiveGateway, id: ExclusiveGateway_0e5en8h, name: score received?, $parent: Process_0hiditg }
- { $type: bpmn:IntermediateCatchEvent, id: IntermediateCatchEvent_0a8iz14, name: credit score received, eventDefinitions: [object Object], $parent: Process_0hiditg }
- { $type: bpmn:IntermediateCatchEvent, id: IntermediateCatchEvent_0a8iz14, name: credit score received, eventDefinitions: [object Object], $parent: Process_0hiditg }
- { $type: bpmn:ExclusiveGateway, id: ExclusiveGateway_11dldcm, $parent: Process_0hiditg }
- { $type: bpmn:Task, id: Task_1fzfxey, name: send credit score, $parent: Process_0hiditg }
- { $type: bpmn:EndEvent, id: EndEvent_0rp5trg, name: scoring request handled, eventDefinitions: , $parent: Process_0hiditg }
- { $type: bpmn:EndEvent, id: EndEvent_0rp5trg, name: scoring request handled, eventDefinitions: , $parent: Process_0hiditg }
- { $type: bpmn:StartEvent, id: StartEvent_1els7eb, name: scoring request received, eventDefinitions: [object Object], $parent: Process_0hiditg }
- { $type: bpmn:StartEvent, id: StartEvent_1els7eb, name: scoring request received, eventDefinitions: [object Object], $parent: Process_0hiditg }
- { $type: bpmn:Task, id: Task_0l942o9, name: report delay, $parent: Process_0hiditg }
- { $type: bpmn:Participant, id: Participant_1xfb3ml, name: scoring service, processRef: Process_1dc1p3b, $parent: Collaboration_1y0blh3 }
- { $type: bpmn:StartEvent, id: StartEvent_0o849un, name: scoring request received, eventDefinitions: [object Object], $parent: Process_1dc1p3b }
- { $type: bpmn:StartEvent, id: StartEvent_0o849un, name: scoring request received, eventDefinitions: [object Object], $parent: Process_1dc1p3b }
- { $type: bpmn:Task, id: Task_1r15hqs, name: compute credit score (level 1), $parent: Process_1dc1p3b }
- { $type: bpmn:Task, id: Task_04l4kzo, name: send result, $parent: Process_1dc1p3b }
- { $type: bpmn:ExclusiveGateway, id: ExclusiveGateway_0rtdod4, name: score available?, $parent: Process_1dc1p3b }
- { $type: bpmn:ExclusiveGateway, id: ExclusiveGateway_0rtdod4, name: score available?, $parent: Process_1dc1p3b }
- { $type: bpmn:ExclusiveGateway, id: ExclusiveGateway_125lzox, $parent: Process_1dc1p3b }
- { $type: bpmn:EndEvent, id: EndEvent_0khk0tq, name: scoring request handled, eventDefinitions: , $parent: Process_1dc1p3b }
- { $type: bpmn:EndEvent, id: EndEvent_0khk0tq, name: scoring request handled, eventDefinitions: , $parent: Process_1dc1p3b }
- { $type: bpmn:Task, id: Task_1hd2ybe, name: compute credit score (level 2), $parent: Process_1dc1p3b }
- { $type: bpmn:Task, id: Task_07vbn2i, name: send credit score, $parent: Process_1dc1p3b }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_0rrtx7k, sourceRef: StartEvent_1els7eb, targetRef: Task_16winvj, $parent: Process_0hiditg }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_06b4pjd, sourceRef: Task_16winvj, targetRef: ExclusiveGateway_0e5en8h, $parent: Process_0hiditg }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_14gfddm, name: no, sourceRef: ExclusiveGateway_0e5en8h, targetRef: Task_0l942o9, $parent: Process_0hiditg }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_14gfddm, name: no, sourceRef: ExclusiveGateway_0e5en8h, targetRef: Task_0l942o9, $parent: Process_0hiditg }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_08fsgff, sourceRef: Task_0l942o9, targetRef: IntermediateCatchEvent_0a8iz14, $parent: Process_0hiditg }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_1i1amgb, sourceRef: IntermediateCatchEvent_0a8iz14, targetRef: ExclusiveGateway_11dldcm, $parent: Process_0hiditg }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_0upas8x, name: yes, sourceRef: ExclusiveGateway_0e5en8h, targetRef: ExclusiveGateway_11dldcm, $parent: Process_0hiditg }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_0upas8x, name: yes, sourceRef: ExclusiveGateway_0e5en8h, targetRef: ExclusiveGateway_11dldcm, $parent: Process_0hiditg }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_12a77en, sourceRef: ExclusiveGateway_11dldcm, targetRef: Task_1fzfxey, $parent: Process_0hiditg }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_1nyeozm, sourceRef: Task_1fzfxey, targetRef: EndEvent_0rp5trg, $parent: Process_0hiditg }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_158pur5, sourceRef: StartEvent_0o849un, targetRef: Task_1r15hqs, $parent: Process_1dc1p3b }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_049ghuo, sourceRef: Task_1r15hqs, targetRef: Task_04l4kzo, $parent: Process_1dc1p3b }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_04a402p, sourceRef: Task_04l4kzo, targetRef: ExclusiveGateway_0rtdod4, $parent: Process_1dc1p3b }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_154teg7, name: no, sourceRef: ExclusiveGateway_0rtdod4, targetRef: Task_1hd2ybe, $parent: Process_1dc1p3b }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_154teg7, name: no, sourceRef: ExclusiveGateway_0rtdod4, targetRef: Task_1hd2ybe, $parent: Process_1dc1p3b }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_1o0d2v1, sourceRef: Task_1hd2ybe, targetRef: Task_07vbn2i, $parent: Process_1dc1p3b }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_1xqy47o, sourceRef: Task_07vbn2i, targetRef: ExclusiveGateway_125lzox, $parent: Process_1dc1p3b }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_0t0wbx3, sourceRef: ExclusiveGateway_125lzox, targetRef: EndEvent_0khk0tq, $parent: Process_1dc1p3b }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_0jh32vv, name: yes, sourceRef: ExclusiveGateway_0rtdod4, targetRef: ExclusiveGateway_125lzox, $parent: Process_1dc1p3b }
- { $type: bpmn:SequenceFlow, id: SequenceFlow_0jh32vv, name: yes, sourceRef: ExclusiveGateway_0rtdod4, targetRef: ExclusiveGateway_125lzox, $parent: Process_1dc1p3b }
- { $type: bpmn:MessageFlow, id: MessageFlow_1pkfls0, sourceRef: Participant_1x9zkso, targetRef: StartEvent_1els7eb, $parent: Collaboration_1y0blh3 }
- { $type: bpmn:MessageFlow, id: MessageFlow_1m6362g, sourceRef: Task_0l942o9, targetRef: Participant_1x9zkso, $parent: Collaboration_1y0blh3 }
- { $type: bpmn:MessageFlow, id: MessageFlow_1i21wes, sourceRef: Task_1fzfxey, targetRef: Participant_1x9zkso, $parent: Collaboration_1y0blh3 }
- { $type: bpmn:MessageFlow, id: MessageFlow_1mm30jd, sourceRef: Task_16winvj, targetRef: StartEvent_0o849un, $parent: Collaboration_1y0blh3 }
- { $type: bpmn:MessageFlow, id: MessageFlow_13j4vf5, sourceRef: Task_04l4kzo, targetRef: Task_16winvj, $parent: Collaboration_1y0blh3 }
- { $type: bpmn:MessageFlow, id: MessageFlow_1nttl77, sourceRef: Task_07vbn2i, targetRef: IntermediateCatchEvent_0a8iz14, $parent: Collaboration_1y0blh3 }"""

examples_json = [
    {
        "input": "How does the bank start the credit scoring process?",
        "output_good": "A bank clerk uses their software to request a credit score for a customer, which kicks off the process in the banking system to communicate with the credit protection agency.",
        "output_bad": "The bank initiates a BPMN Collaboration, invoking a Participant Process via a MessageFlow to the Schufa service for a credit scoring Event."
    },
    {
        "input": "What happens after the bank sends a scoring request to the agency?",
        "output_good": "The agency quickly performs an initial credit scoring. If possible, this result is sent back immediately to the bank's system and shown to the clerk.",
        "output_bad": "Upon receipt of the scoring request, an IntermediateCatchEvent is triggered, leading to an immediate execution of a Task for level 1 scoring, conditioned by an ExclusiveGateway."
    },
    {
        "input": "What occurs if the initial credit scoring doesn’t give an immediate result?",
        "output_good": "The agency informs the bank's system about the delay and starts a more detailed scoring. The bank's system then notifies the clerk about the delay, asking them to check back later.",
        "output_bad": "If the initial scoring doesn't resolve, a conditional ExclusiveGateway routes the flow to a delay notification Task, subsequently initializing a level 2 scoring Sub-Process."
    },
    {
        "input": "How is the clerk informed of the final credit scoring result?",
        "output_good": "Once the detailed scoring is completed and the result is sent back to the bank's system, it is displayed on the clerk's software for review.",
        "output_bad": "The final scoring outcome, after processing through a sequence of EventBasedGateways and Task executions, is programmatically dispatched to the initiating Participant's frontend interface."
    },
    {
        "input": "What does the bank do if the credit score is delayed?",
        "output_good": "The bank's system displays a message to the clerk about the delay, and as soon as the final score is ready, it notifies the clerk to check the result.",
        "output_bad": "In the event of a scoring delay, an IntermediateCatchEvent captures the timeout, activating a Task to update the UI component of the clerk's software module with a delay notification."
    }
]


def few_shots_learning_json():
    res = "- Let us consider the following textual representaion of an example process:\n"
    res += process_textual_representation_json + "\n\n"
    res += "- These are example pairs of input and expected output:\n"
    for i in range(len(examples_json)):
        res += f"Input {i}: {examples_json[i]['input']}\n"
        res += f"Expected output {i}: {examples_json[i]['output_good']}\n"
    res += "\n\n"
    return res


def negative_prompting_json():
    res = "- Now, I will give you example bad outputs for the same example questions, so you try to avoid such outputs:\n"
    for i in range(len(examples_json)):
        res += f"Bad output for question {i}: {examples_json[i]['output_bad']}\n"
    res += "\n\n"
    return res
