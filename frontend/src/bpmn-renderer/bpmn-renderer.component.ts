import {Component, ElementRef, Input, SimpleChanges, ViewChild} from '@angular/core';
import {environment} from "../environments/environment";
/**
 * You may include a different variant of BpmnJS:
 *
 * bpmn-viewer  - displays BPMN diagrams without the ability
 *                to navigate them
 * bpmn-modeler - bootstraps a full-fledged BPMN editor
 */
// @ts-ignore
import * as BpmnJS from 'bpmn-js/dist/bpmn-modeler.development.js';
// @ts-ignore
import * as dagreD3 from 'dagre-d3/dist/dagre-d3.js';
// @ts-ignore
import * as d3 from 'd3';


class CustomWaypoint {
  dictio;
  // @ts-ignore
  $name;
  $model: any;
  $type: any;
  $attrs: any;
  $parent: any;
  $descriptor: any;
  x: any;
  y: any;

  constructor() {
    this.dictio = {};
  }

  get(varname: any) {
    // @ts-ignore
    return this.dictio[varname];
  }

  set(varname: any, varvalue: any) {
    // @ts-ignore
    this.dictio[varname] = varvalue;
  }
}

@Component({
  selector: 'app-bpmn-renderer',
  standalone: true,
  imports: [],
  templateUrl: './bpmn-renderer.component.html',
  styleUrl: './bpmn-renderer.component.scss'
})
export class BpmnRendererComponent {

  @Input()
  bpmnContentBase64: string
    // instantiate BpmnJS with component
    | undefined

  // instantiate BpmnJS with component
  private bpmnJS: BpmnJS;

  // retrieve DOM element reference
  @ViewChild('ref', { static: true }) private el: ElementRef | undefined;

  textualRepresentation = "";
  modelXmlString = "";
  modelSvg = "";

  ngOnInit(){
    // reset_conversation();

    // if (this.bpmnContentBase64) {
    //   const xmlString = atob(this.bpmnContentBase64);
    //   this.renderUpdatedBPMN(xmlString)
    //     .then(() => {
    //       console.log("BPMN diagram rendered with updated layout.");
    //     })
    //     .catch((err: any) => {
    //       console.error("Error rendering BPMN diagram with updated layout:", err);
    //     });
    // }
  }

  ngAfterContentInit(): void {
    // attach BpmnJS instance to DOM element
    this.bpmnJS.attachTo(this.el?.nativeElement);
  }

  ngOnChanges(changes: SimpleChanges) {
    if(changes.hasOwnProperty('bpmnContentBase64')){
      const xmlString = atob(changes['bpmnContentBase64'].currentValue);
      this.renderUpdatedBPMN(xmlString)
        .then(() => {
          console.log("BPMN diagram rendered with updated layout.");
        })
        .catch((err: any) => {
          console.error("Error rendering BPMN diagram with updated layout:", err);
        });
    }

  }

  ngOnDestroy(): void {
    this.bpmnJS.destroy();
  }


  // document.addEventListener("DOMContentLoaded", function () {
  //   reset_conversation();
  //   const bpmnContentBase64 = document
  //     .getElementById("bpmn-container")
  //     .getAttribute("data-bpmn-content");
  //   if (bpmnContentBase64) {
  //     const xmlString = atob(bpmnContentBase64);
  //     renderUpdatedBPMN(xmlString)
  //       .then(() => {
  //         console.log("BPMN diagram rendered with updated layout.");
  //       })
  //       .catch((err) => {
  //         console.error("Error rendering BPMN diagram with updated layout:", err);
  //       });
  //   }
  //   reset_button_listener();
  // });


  async renderUpdatedBPMN(xmlString: any) {
    try {
      xmlString = await this.bpmnLayoutWithDagre(xmlString);
    } catch (err) {

    }

    this.modelXmlString = xmlString;

    const container: any = document.getElementById("bpmn-container");
    container.innerHTML = ""; // This clears out any existing content
    let viewer = new BpmnJS({
      container: container,
    });
    this.bpmnJS = viewer
    try {
      await viewer.importXML(xmlString);

      viewer
        .saveSVG({format: true})
        .then(function (result: any) {
          let modelSvg = result.svg;
          console.log(modelSvg);
          // Use the SVG as needed
        })
        .catch(function (err: any) {
          console.log(err);
        });

      const canvas = viewer.get("canvas");
      canvas.zoom("fit-viewport");

      const elementRegistry = viewer.get("elementRegistry");
      const allElements = elementRegistry.getAll();
      this.textualRepresentation = this.buildTextualRepresentation(allElements, viewer);
      //console.log(textualRepresentation);
      //console.log(modelXmlString);

      const eventBus = viewer.get("eventBus");
      let previousSelection: any[] = [];

      eventBus.on("selection.changed", (event: any) => {
        this.reset_conversation();

        const selectedElements = event.newSelection;
        const modeling = viewer.get("modeling");
        previousSelection.forEach((element) => {
          modeling.setColor(element, {fill: "white"});
        });
        selectedElements.forEach((element: any) => {
          modeling.setColor(element, {fill: "lightblue"});
        });
        previousSelection = selectedElements;

        if (environment.ENABLE_SENDING_SUBMODEL) {
          if (selectedElements.length == 0) {
            const allElements = elementRegistry.getAll();
            this.textualRepresentation = this.buildTextualRepresentation(allElements, viewer);
          } else {
            this.textualRepresentation = this.buildTextualRepresentation(
              selectedElements,
              viewer
            );
          }
        }


        //console.log(textualRepresentation);
      });
      container.addEventListener(
        "wheel",
        function (event: any) {
          event.preventDefault();
          const delta = Math.sign(event.deltaY);
          let zoomLevel = canvas.zoom();
          if (delta < 0) {
            zoomLevel = zoomLevel * 1.1;
          } else {
            zoomLevel = zoomLevel * 0.9;
          }
          canvas.zoom(zoomLevel, "auto");
        },
        {passive: false}
      );
    } catch (err) {
      console.error("Failed to import updated BPMN diagram", err);
    }
  }

  reset_button_listener() {
    // var resetButton = document.getElementById("reset_button");
    // if (resetButton) {
    //   resetButton.addEventListener("click", function () {
    //     reset_conversation();
    //   });
    // }
}

reset_conversation() {
  // axios
  //   .post("/reset_conversation")
  //   .then(function (response) {
  //     console.log(response.data.success);
  //     var chatBox = document.getElementById("chat-box");
  //     // chatBox.innerHTML = "";
  //
  //     $('#chat-history').empty()
  //     sendInitialSystemMessage();
  //   })
  //   .catch(function (error) {
  //     console.error(error);
  //   });
}

buildTextualRepresentation(selectedElements: any, viewer: any) {
  const elementRegistry = viewer.get("elementRegistry");
  let representation = "Selected BPMN Elements and Connections:\n";

  selectedElements.forEach((e: { id: any; }) => {
    const element = elementRegistry.get(e.id);

    let elementDetails;
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

      [
        "sourceRef",
        "targetRef",
        "lanes",
        "processRef",
        "flowNodeRef",
        "$parent",
      ].forEach((relation) => {
        const related = element.businessObject[relation];
        if (related) {
          if (Array.isArray(related)) {
            const ids = related.map((item) => item.id).join(", ");
            properties.push(`${relation}: (${ids})`);
          } else if (related.id) {
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



  renderGraph(
    iterativelyReachedNodes: any,
    nodes: any,
    edgesDict: any,
    nodesep: any,
    edgesep: any,
    ranksep: any,
    targetDivDagre: string,
    desideredWidth: any = null,
    desideredHeight: any = null
  ) {
    const g = new dagreD3.graphlib.Graph().setGraph({});

    for (let n of iterativelyReachedNodes) {
      if (!n.$type.toLowerCase().endsWith("flow")) {
        let name = "" + n.name;
        let isProperName = true;
        if (name.length == 0) {
          name = n.id;
          isProperName = false;
        }
        if (name == "start" || name == "end") {
          isProperName = false;
        }
        if (isProperName && desideredWidth != null) {
          g.setNode(n.id, {
            label: n.name.replaceAll(" ", "\n"),
            width: desideredWidth,
            height: desideredHeight,
          });
        } else if (desideredWidth != null) {
          g.setNode(n.id, {
            label: n.name.replaceAll(" ", "\n"),
            width: Math.min(desideredWidth, desideredHeight) * 0.28,
            height: Math.min(desideredWidth, desideredHeight) * 0.28,
          });
        } else {
          g.setNode(n.id, {
            label: n.name.replaceAll(" ", "\n"),
          });
        }
      }
    }

    for (let n of nodes) {
      if (n.$type.toLowerCase().endsWith("flow")) {
        let source = n.sourceRef.id;
        let target = n.targetRef.id;
        edgesDict[source + "@" + target] = n.id;
        g.setEdge(source, target, {
          label: "",
        });
      }
    }

    g.graph().rankDir = "LR";
    g.graph().nodesep = nodesep;
    g.graph().edgesep = edgesep;
    g.graph().ranksep = ranksep;

    let render = new dagreD3.render();
    let svg = d3.select("#" + targetDivDagre);
    let inner = svg.append("g");
    render(inner, g);

    return g;
  }

  async bpmnLayoutWithDagre(xmlString: any) {
    let targetDivFirstBpmn = "internalCanvas";
    let targetDivDagre = "internalSvg";
    let nodesep = 30;
    let edgesep = 30;
    let ranksep = 85;

    let bpmnViewer = new BpmnJS({
      container: "#" + targetDivFirstBpmn,
    });
    this.bpmnJS = bpmnViewer

    await bpmnViewer.importXML(xmlString);

    let nodes = bpmnViewer._definitions.rootElements[0].flowElements;
    let graphical = bpmnViewer._definitions.diagrams[0].plane.planeElement;
    let graphicalDict = {};
    let edgesDict = {};
    let i = 0;
    while (i < graphical.length) {
      // @ts-ignore
      graphicalDict[graphical[i].bpmnElement.id] = i;
      i++;
    }

    let toVisit = [];
    let iterativelyReachedNodes: any[] = [];

    for (let n of nodes) {
      if (n.$type.toLowerCase().endsWith("startevent")) {
        toVisit.push(n);
        break;
      }
    }

    while (toVisit.length > 0) {
      let el = toVisit.pop();
      if (!iterativelyReachedNodes.includes(el)) {
        iterativelyReachedNodes.push(el);
      }
      if (el.outgoing != null) {
        for (let out of el.outgoing) {
          if (!iterativelyReachedNodes.includes(out.targetRef)) {
            toVisit.push(out.targetRef);
          }
        }
      }
    }

    let g = this.renderGraph(
      iterativelyReachedNodes,
      nodes,
      edgesDict,
      nodesep,
      edgesep,
      ranksep,
      targetDivDagre
    );

    let desideredWidth = 0;
    let desideredHeight = 0;

    for (let nodeId in g._nodes) {
      let node = g._nodes[nodeId];
      let elemStr = node.elem.innerHTML;
      let width = parseInt(elemStr.split('width="')[1].split('"')[0]);
      let height = parseInt(elemStr.split('height="')[1].split('"')[0]);
      desideredWidth = Math.max(desideredWidth, width);
      desideredHeight = Math.max(desideredHeight, height);
    }

    g = this.renderGraph(
      iterativelyReachedNodes,
      nodes,
      edgesDict,
      nodesep,
      edgesep,
      ranksep,
      targetDivDagre,
      desideredWidth * 1.7,
      desideredHeight * 0.87
    );

    for (let nodeId in g._nodes) {
      let node = g._nodes[nodeId];
      let elemStr = node.elem.innerHTML;
      let width = parseInt(elemStr.split('width="')[1].split('"')[0]);
      let height = parseInt(elemStr.split('height="')[1].split('"')[0]);
      // @ts-ignore
      graphical[graphicalDict[nodeId]].bounds.x = node.x - width / 2.0;
      // @ts-ignore
      graphical[graphicalDict[nodeId]].bounds.y = node.y - height / 2.0;
      // @ts-ignore
      graphical[graphicalDict[nodeId]].bounds.height = height;
      // @ts-ignore
      graphical[graphicalDict[nodeId]].bounds.width = width;
    }

    for (let edgeId in g._edgeLabels) {
      let graphEdgeObj = g._edgeObjs[edgeId];
      graphEdgeObj = graphEdgeObj.v + "@" + graphEdgeObj.w;
      let graphEdge = g._edgeLabels[edgeId];
      let edge = g._edgeLabels[edgeId];
      // @ts-ignore
      let graphicalElement = graphical[graphicalDict[edgesDict[graphEdgeObj]]];
      let referenceWaypoint = graphicalElement.waypoint[0];
      graphicalElement.waypoint = [];
      for (let p of edge.points) {
        let waypoint = new CustomWaypoint();
        waypoint.$type = referenceWaypoint.$type;
        waypoint.x = p.x;
        waypoint.y = p.y;
        waypoint.$parent = referenceWaypoint.$parent;
        waypoint.$attrs = referenceWaypoint.$attrs;
        waypoint.$descriptor = referenceWaypoint.$descriptor;
        waypoint.$model = referenceWaypoint.$model;
        waypoint.set("x", p.x);
        waypoint.set("y", p.y);
        graphicalElement.waypoint.push(waypoint);
      }
    }

    let xmlContent = await bpmnViewer.saveXML();

    return xmlContent.xml;
  }


}
