function sendMessage() {
    var userMessage = document.getElementById("user_message").value;
    appendMessage("You", userMessage);
    document.getElementById("user_message").value = ""; // Clear input field

    axios.post("/chat_with_llm", { message: userMessage, textualRepresentation: textualRepresentation })
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

$(document).ready(function () {
    $("#sidebar").mCustomScrollbar({
        theme: "minimal"
    });

    $('#dismiss, .overlay').on('click', function () {
        // hide sidebar
        $('#sidebar').removeClass('active');
        // hide overlay
        $('.overlay').removeClass('active');
    });

    $('#sidebarCollapse').on('click', function () {
        // open sidebar
        $('#sidebar').addClass('active');
        // fade in the overlay
        $('.overlay').addClass('active');
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });
});
