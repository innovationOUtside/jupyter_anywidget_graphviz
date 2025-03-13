# jupyter_anywidget_graphviz

Jupyter [`anywidget`](https://github.com/manzt/anywidget) for rendering diagrams from `.dot` language to SVG using Graphviz Wasm ([`hpcc-systems/hpcc-js-wasm`](https://github.com/hpcc-systems/hpcc-js-wasm)).

Demo: [JupyterLite Demo](https://innovationoutside.github.io/jupyter_anywidget_graphviz/lab/index.html?path=jupyter_graphviz_anywidget_example.ipynb)

Install as:

```sh
pip install jupyter_anywidget_graphviz
```

![Example of graphviz anywidget](images/graphviz_anywidget.png)

## Usage

*See examples in `jupyter_graphviz_anywidget_example.ipynb`*

This runs in a browser based Jupyter environment and uses the browser machinery to run the wasm application.

```python
# Import package
from jupyter_anywidget_graphviz import graphviz_headless, graphviz_panel, graphviz_inline

# Create a headless widget
# - works in: Jupyter Lab, Jupyter Notebook, VS Code
g = graphviz_headless()

# Inline mode
# Preview output as cell output from initialising cell
# - works in: Jupyter Lab, Jupyter Notebook, VS Code
# g = graphviz_inline()

# Create a widget panel with a handle
# - uses jupyter sidecar (Jupyter Lab only)
#g = graphviz_panel()

# Load magic
%load_ext jupyter_anywidget_graphviz
```

We can now write `dot` code in a magicked code cell (`%%graphviz_magic WIDGET_HANDLE`):

```python
%%graphviz_magic -w g
  strict graph {
    a -- b
    a -- b
    b -- a [color=blue]
  }
```

The `-w / --widget-name` setting can be used to set the widget within the magic and it does not need to be passed again.

Use the `-e / --embed` flag or the `-t / --timeout TIMEOUT_IN_S` switch to render the output SVG as cell output (not JupyterLite / marimo).

The widget can also be set via line magic: `%setwidget g`

The output is previewed in the UI panel, if rendered.

Retrieve the SVG diagram as `WIDGET_HANDLE.svg`.

We can also display the diagram manually in the notebook e.g. as:

```python
from IPython.display import SVG

SVG(g.svg)
```

In its base form, the way the Jupyter event loop runs means we can't directly generate an output from the magic cell. However, setting the `-e/--embed` flag, or setting a timeout `-t/--timeout SECONDS` (default 5s), we can force a blocking action on the cell that waits for the asynchronous graphviz object to return the generated SVG, and then render it.

The `.blocking_reply()` method on the object will also block until the response status is set to *completed*.

If you set `g.audio = True`, error messages will be spoken alound using browser text to speech.

### Headless example

```python
from jupyter_anywidget_graphviz import (
    graphviz_headless,
)

class graphVizSVG:
    def __init__(self, svg: str):
        self.svg = svg
    def _repr_svg_(self):
        return self.svg

g = graphviz_headless()
dot = """
  strict graph {
    a -- b
    a -- c
    b -- a [color=red]
  }
"""
g.set_code_content(dot)
g.blocking_reply()

graphVizSVG(g.svg)
```

### Running in marimo

The reactivity is a bit off, but it can eventually getg there if you let things settle then force particular cells to re-run: [example marimo notebook](https://marimo.app/?slug=y2q0gj)

## Alternative solutions

[viz.js](https://viz-js.com/) [[repo](https://github.com/mdaines/viz-js)] also seems to offer in browser graphviz rendering. [`KrunkZhou/jupyterlab-viz-krunk`](https://github.com/KrunkZhou/jupyterlab-viz-krunk) is a JupyterLab extension (untested) that seems to support backticked ` ```graphviz ` blocks in markdown cells.

Here'a an alternative `anywidget` using the same `graphviz` wasm package from @basnijholt: https://github.com/pipefunc/graphviz-anywidget


# Other (predominantly, ouseful) sideloading wasm anywidgets

See the GitHup topc tag: [`jupyter-wasm-anywidget-extension`](https://github.com/topics/jupyter-wasm-anywidget-extension)
