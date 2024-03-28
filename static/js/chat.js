function sendMessage() {
    var userMessage = document.getElementById("user_message").value;
    appendMessage("You", userMessage);
    document.getElementById("user_message").value = ""; // Clear input field

    axios.post("/chat_with_llm", { message: userMessage, textualRepresentation: textualRepresentation })
        .then(function (response) {
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
