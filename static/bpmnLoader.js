document.addEventListener('DOMContentLoaded', function() {
  var container = document.getElementById('bpmn-container');
  var bpmnModeler = new BpmnJS({
      container: container
  });

  var encodedBpmnContent = container.getAttribute('data-bpmn-content');
  var bpmnXml = atob(encodedBpmnContent);

  if (bpmnXml && bpmnXml.trim().length > 0) {
    try {
      bpmnModeler.importXML(bpmnXml);
      bpmnModeler.get("canvas").zoom("fit-viewport");
    } catch (err) {
      console.log(err.message, err.warnings);
    }
  }
});

document.getElementById('yourFormId').addEventListener('submit', function(e) {
  e.preventDefault(); // Prevent the default form submission
  const modelName = document.getElementById('model_name').value;
  const apiKey = document.getElementById('api_key').value;

  // Prepare data to send to your server
  const formData = new FormData();
  formData.append('model_name', modelName);
  formData.append('api_key', apiKey);

  // Send data to your Flask backend
  fetch("{{ url_for('index') }}", {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      alert('Error: ' + data.message); // Display error message
    } else {
      // Handle success (e.g., redirect or display success message)
      console.log('Success:', data);
    }
  })
  .catch((error) => {
    console.error('Error:', error);
  });
});
