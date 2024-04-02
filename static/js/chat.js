function sendMessage() {
  var userMessage = document.getElementById("user_message").value;
  appendMessage("You", userMessage);
  document.getElementById("user_message").value = ""; // Clear input field

  let postDataContent = {
    message: userMessage,
    textualRepresentation: textualRepresentation,
    modelXmlString: modelXmlString,
    modelSvg: modelSvg,
  };

  parameters = {};

  // it is possible to customize the parameters
  //parameters["model_abstraction"] = "json";
  //parameters["enable_role_prompting"] = true;
  //parameters["enable_natural_language_restriction"] = true;
  //parameters["enable_chain_of_thought"] = true;
  //parameters["enable_process_analysis"] = true;
  //parameters["enable_knowledge_injection"] = true;

  // only available for the JSON abstraction.
  // Their value is not considered for the other abstractions.
  //parameters["enable_few_shots_learning"] = true;
  //parameters["enable_negative_prompting"] = true;

  postDataContent["parameters"] = parameters;

  axios.post("/chat_with_llm", postDataContent).then(function (response) {
    var llmResponse = response.data.response;
    appendMessage("LLM", llmResponse);
  });
}

function appendMessage(sender, message) {
  var chatBox = document.getElementById("chat-box");
  var messageElement = document.createElement("div");
  messageElement.innerHTML = "<strong>" + sender + ":</strong> " + message;
  chatBox.appendChild(messageElement);
  chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
}
