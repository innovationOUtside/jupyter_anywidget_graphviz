# jupyter_anywidget_graphviz

Jupyter [`anywidget`](https://github.com/manzt/anywidget) for rendering diagrams from `.dot` language to SVG using Graphviz Wasm ([`hpcc-systems/hpcc-js-wasm`](https://github.com/hpcc-systems/hpcc-js-wasm)).

Install as:

```sh
pip install jupyter_anywidget_graphviz
```

![Example of graphviz anywidget](images/graphviz_anywidget.png)

## Usage

This runs in a browser based Jupyter environment and uses the browser machinery to run the wasm application.

```python
# Import package
from jupyter_anywidget_graphviz import graphviz_panel

# Create a widget panel with a handle
g = graphviz_panel()

# Load magic
%load_ext jupyter_anywidget_graphviz
```

We can now write `dot` code in a magicked code cell (`%%graphviz_magic WIDGET_HANDLE`):

```python
%%graphviz_magic g
  strict graph {
    a -- b
    a -- b
    b -- a [color=blue]
  }
```

The output is previewed in the panel.

Retrieve the SVG diagram as `WIDGET_HANDLE.svg`.

We can display the diagram in the notebook e.g. as:

```python
from IPython.display import SVG

SVG(g.svg)
```
