import "./graphviz.css";
import "./uuid.js";
import html from "./graphviz.html";
import { generateUUID } from "./uuid";

//https://github.com/hpcc-systems/hpcc-js-wasm
import { Graphviz } from "@hpcc-js/wasm-graphviz";

function render({ model, el }) {
  const _headless = model.get("headless");
  Graphviz.load().then((graphviz) => {
    if (!_headless) {
      let el2 = document.createElement("div");
      el2.innerHTML = html;
      const uuid = generateUUID();
      el2.id = uuid;
      el.appendChild(el2);
    }

    model.on("change:code_content", () => {
      const dot = model.get("code_content");

      function handle_svg(model, graphviz) {
        const svg = graphviz.dot(dot);
        model.set("svg", svg);
        model.save_changes();
        return svg;
      }

      if (!_headless) {
        const img_el = el.querySelector('div[title="image-container"]');
        const dot_el = el.querySelector('pre[title="dot-container"]');
        dot_el.innerHTML = dot;
        img_el.innerHTML = "Processing...";
        const svg = handle_svg(model, graphviz);
        img_el.innerHTML = svg;
      } else {
        handle_svg(model, graphviz);
      }
    });
  });
}

export default { render };
