var bpmnContent = "{{ bpmn_content_base64 }}";
        var viewer = new BpmnJS({ container: '#bpmn-container' });
        viewer.importBpmnDiagram(atob(bpmnContent));

        function sendMessage() {
            var userMessage = document.getElementById("user_message").value;
            appendMessage("You", userMessage);
            document.getElementById("user_message").value = ""; // Clear input field
        
            // Send user message to server and get response
            axios.post("/chat_with_llm", { message: userMessage })
                .then(function (response) {
                    var llmResponse = response.data.response;
                    appendMessage("LLM", llmResponse);
                })
                .catch(function (error) {
                    console.error(error);
                });
        }

        function appendMessage(sender, message) {
            var chatBox = document.getElementById("chat-box");
            var messageElement = document.createElement("div");
            messageElement.innerHTML = "<strong>" + sender + ":</strong> " + message;
            chatBox.appendChild(messageElement);
            chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
        }