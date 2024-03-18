async function renderUpdatedBPMN(xmlString) {
  try {
    xmlString = await bpmnLayoutWithDagre(xmlString);
  } catch (err) {    
  }    
  const container = document.getElementById('bpmn-container');
  container.innerHTML = ''; // This clears out any existing content 
  var viewer = new BpmnJS({
      container: container,
  }); 
  try {
      await viewer.importXML(xmlString);
      var canvas = viewer.get('canvas');
      canvas.zoom('fit-viewport');
      var eventBus = viewer.get('eventBus'); 
      let previousSelection = []; 
      eventBus.on('selection.changed', function(event) {
        const selectedElements = event.newSelection;
        console.log('Selected: ',selectedElements );
        const modeling = viewer.get('modeling');         
        previousSelection.forEach(element => {
            modeling.setColor(element, { fill: 'white' });
        });
        selectedElements.forEach(element => {
            modeling.setColor(element, { fill: 'lightblue'});
        }); 
        previousSelection = selectedElements;

        const textualRepresentation = buildTextualRepresentation(selectedElements, viewer);
        console.log(textualRepresentation);
     });
     container.addEventListener('wheel', function(event) {
      event.preventDefault(); 
      const delta = Math.sign(event.deltaY);
      let zoomLevel = canvas.zoom(); 
      if (delta < 0) {
          zoomLevel = zoomLevel * 1.1;
      } else {
          zoomLevel = zoomLevel * 0.9; 
      }
      canvas.zoom(zoomLevel, 'auto');
    }, { passive: false }); 
  } catch (err) {
      console.error('Failed to import updated BPMN diagram', err);
  }
} 

function reset_button_listener() {
    var resetButton = document.getElementById("reset_button");
    if (resetButton) {
        resetButton.addEventListener("click", function() {
            axios.post("/reset_conversation")
            .then(function(response) {
                console.log(response.data.success);
                var chatBox = document.getElementById("chat-box");
                chatBox.innerHTML = "";  
            })
            .catch(function(error) {
                console.error(error);
            });
        });
    }
}

function buildTextualRepresentation(selectedElements, viewer) {
    const elementRegistry = viewer.get('elementRegistry');
    let representation = "Selected BPMN Elements and Connections:\n";
  
    selectedElements.forEach(e => {
        const element = elementRegistry.get(e.id);

        if (element.businessObject) {
            let properties = [];
            // console.log("Non-enumerable keys:");
            // Object.getOwnPropertyNames(element.businessObject).forEach(key => {
            //     console.log(key);
            // });
            

            for (const [key, value] of Object.entries(element.businessObject)) {
                
                if (value !== null && value !== "") {
                    properties.push(`${key}: ${value}`);
                }                           
            }

            ['sourceRef', 'targetRef', 'lanes', 'processRef', 'flowNodeRef', '$parent'].forEach((relation) => {
                const related = element.businessObject[relation];
                if (related) {
                    if (Array.isArray(related)) { // For arrays (like 'lanes'), list all IDs
                        const ids = related.map(item => item.id).join(", ");
                        properties.push(`${relation}: (${ids})`);
                    } else if (related.id) { // For single objects, just append the ID
                        properties.push(`${relation}: ${related.id}`);
                    }
                }
            });

            if (properties.length > 0) {
                elementDetails = `{ ${properties.join(", ")} }`;
            }
        }

        representation += `- ${elementDetails}\n`;
    });
  
    return representation;
}

document.addEventListener('DOMContentLoaded', function() {
  const bpmnContentBase64 = document.getElementById('bpmn-container').getAttribute('data-bpmn-content');
  if (bpmnContentBase64) {
      const xmlString = atob(bpmnContentBase64); 
      renderUpdatedBPMN(xmlString).then(() => {
          console.log('BPMN diagram rendered with updated layout.');
      }).catch(err => {
          console.error('Error rendering BPMN diagram with updated layout:', err);
      });
  }
  reset_button_listener();
 
});
