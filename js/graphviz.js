import "./graphviz.css";
import "./uuid.js";
import { play_success, play_error } from "./audio";

import html from "./graphviz.html";
import { generateUUID } from "./uuid";

//https://github.com/hpcc-systems/hpcc-js-wasm
import { Graphviz } from "@hpcc-js/wasm-graphviz";

function render({ model, el }) {

  function handle_error(error) {
    if (model.get("audio")) play_error(error.message);
    console.log(error);
    //if (model.get("audio")) play_error(error.message);
    model.set("response", {
      status: "error",
      error_message: error.message,
    });
    model.save_changes();
  }

  const _headless = model.get("headless");
  Graphviz.load().then((graphviz) => {
    model.set("response", { status: "ready" });
    model.save_changes();

    if (!_headless) {
      let el2 = document.createElement("div");
      el2.innerHTML = html;
      const uuid = generateUUID();
      el2.id = uuid;
      el.appendChild(el2);
    }

    model.on("change:code_content", () => {
      const dot = model.get("code_content");
      if (!dot) return;

      async function handle_svg(model, graphviz) {
        let svg;
        try {
          svg = await graphviz.dot(dot);
          model.set("svg", svg);
          model.set("response", {status:"completed", svg: svg})
        } catch (error) {
          handle_error(error);
        }
        model.save_changes();
        return svg;
      }

      handle_svg(model, graphviz).then((svg) => {
        if (!_headless) {
          const img_el = el.querySelector('div[title="image-container"]');
          const dot_el = el.querySelector('pre[title="dot-container"]');
          dot_el.innerHTML = dot;
          img_el.innerHTML = "Processing...";
          img_el.innerHTML = svg;
        }
      });
    });
  });
}

export default { render };
