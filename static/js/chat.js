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
  console.log(postDataContent);

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
