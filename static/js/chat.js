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


$( document ).ready(function() {
  $("#chatButton").click(sendMessageMock)

  $("#dotFalling").css("display", "none");
})

function sendMessageMock() {
  let userMessage = $('#chatInput').val();
  $('#chatInput').val('')
  addUserMessageToChatbox(userMessage)

  $("#dotFalling").css("display", "block");

  // setTimeout(function () {
  //   console.log('I will run after 2 seconds');
  //   let responseMessage = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus quis ipsum pharetra nunc ultrices viverra ac quis justo. Duis ut suscipit ligula. Nunc sagittis gravida lorem ac vulputate. Praesent eu blandit ante. Mauris eleifend dui a arcu tincidunt porttitor."
  //   addResponseMessageToChatbox(responseMessage)
  //   $("#dotFalling").css("display", "none");
  // }, 3000);
  // var responseMessage = response.data.response;
  // addResponseMessageToChatbox(responseMessage)

  let postDataContent = {
    message: userMessage 
  };

  axios.post("/chat_with_llm", postDataContent)
    .then(function(response) {
      var llmResponse = response.data.response;

      addResponseMessageToChatbox(llmResponse);
    })
    .catch(function(error) {
      console.error("Error fetching the response:", error);
      addResponseMessageToChatbox("Sorry, there was an error processing your message.");
    })
    .finally(function() {
      $("#dotFalling").css("display", "none");
    });
}

function addUserMessageToChatbox(userMessage){

  $("#chat-history").append('<li class="clearfix">\n' +
        '   <div class="message-data">\n' +
          '   <p class="send"> ' + userMessage + ' </p>\n' +
          '   <img src="static/assets/human.png" alt="avatar" class="avatar">\n' +
          ' </div>\n' +
        '</li>');
    var d = $('#chat-history-parent');
    d.scrollTop(d.prop("scrollHeight"));
    
    
}

function addResponseMessageToChatbox(responseMessage){
  $("#chat-history").append('<li class="clearfix">\n' +
    '   <div class="message-data">\n' +
      '   <img src="static/assets/robot.png" alt="avatar" class="avatar">\n' +
      '   <p class="receive">' + responseMessage + '</p>\n' +
      ' </div>\n' +
    '   </li>');

  var d = $('#chat-history-parent');
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
  var initialMessage = "Hello! I am your AI assistant. How may I assist you with the uploaded BPMN model?";
  addResponseMessageToChatbox(initialMessage);
}
