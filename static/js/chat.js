function sendMessage() {
  let userMessage = $("#chatInput").val();
  $("#chatInput").val("");
  addUserMessageToChatbox(userMessage);

  $("#dotFalling").css("display", "block");

  let postDataContent = {
    message: userMessage,
    textualRepresentation: textualRepresentation,
    modelXmlString: modelXmlString,
    modelSvg: modelSvg,
  };

  parameters = {};

  console.log(postDataContent);

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

  axios
    .post("/chat_with_llm", postDataContent)
    .then(function (response) {
      var llmResponse = response.data.response;

      addResponseMessageToChatbox(llmResponse);
    })
    .catch(function (error) {
      console.error("Error fetching the response:", error);
      addResponseMessageToChatbox(
        "Sorry, there was an error processing your message."
      );
    })
    .finally(function () {
      $("#dotFalling").css("display", "none");
    });
}

$(document).ready(function () {
  //$("#chatButton").click(sendMessage)

  const input = document.getElementById('chatInput');

  // Add an event listener to detect keydown events
  input.addEventListener('keydown', function(event) {
      // Check if the key pressed is the Enter key
      if (event.key === "Enter") {
          event.preventDefault();
          sendMessage();
      }
  });

  $("#dotFalling").css("display", "none");
});

function addUserMessageToChatbox(userMessage) {
  $("#chat-history").append(
    '<li class="clearfix">\n' +
      '   <div class="message-data">\n' +
      '   <p class="send"> ' +
      userMessage +
      " </p>\n" +
      '   <img src="static/assets/human.png" alt="avatar" class="avatar">\n' +
      " </div>\n" +
      "</li>"
  );
  var d = $("#chat-history-parent");
  d.scrollTop(d.prop("scrollHeight"));
}

function addResponseMessageToChatbox(responseMessage) {
  $("#chat-history").append(
    '<li class="clearfix">\n' +
      '   <div class="message-data">\n' +
      '   <img src="static/assets/robot.png" alt="avatar" class="avatar">\n' +
      '   <p class="receive">' +
      responseMessage +
      "</p>\n" +
      " </div>\n" +
      "   </li>"
  );

  var d = $("#chat-history-parent");
  d.scrollTop(d.prop("scrollHeight"));
}

function appendMessage(sender, message) {
  var chatBox = document.getElementById("chat-box");
  var messageElement = document.createElement("div");
  messageElement.innerHTML = "<strong>" + sender + ":</strong> " + message;
  chatBox.appendChild(messageElement);
  chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
}

function sendInitialSystemMessage() {
  var initialMessage =
    "Hello! I am your AI assistant. How may I assist you with the uploaded BPMN model?";
  addResponseMessageToChatbox(initialMessage);
}
