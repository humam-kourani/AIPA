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
});
