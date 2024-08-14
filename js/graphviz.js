import "./graphviz.css";
import "./uuid.js";
import html from "./graphviz.html";
import { generateUUID } from "./uuid";

//https://github.com/hpcc-systems/hpcc-js-wasm
import { Graphviz } from "@hpcc-js/wasm-graphviz";

function render({ model, el }) {
  let el2 = document.createElement("div");
  el2.innerHTML = html;
  const uuid = generateUUID();
  el2.id = uuid;
  el.appendChild(el2);

  const img_el = el.querySelector('div[title="image-container"]');
  const dot_el = el.querySelector('div[title="dot-container"]');

  model.on("change:code_content", () => {
    const dot = model.get("code_content");
    dot_el.innerHTML = dot
    img_el.innerHTML = "Processing..."
    Graphviz.load().then((graphviz) => {
      const svg = graphviz.dot(dot);
      img_el.innerHTML = svg;
      model.set("svg", svg);
      model.save_changes();
    });
  });
}

export default { render };
