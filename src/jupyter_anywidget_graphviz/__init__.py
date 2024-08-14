import importlib.metadata
import pathlib

import anywidget
import traitlets

try:
    __version__ = importlib.metadata.version("jupyter_anywidget_graphviz")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


class Widget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"
    value = traitlets.Int(0).tag(sync=True)


class graphvizWidget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "graphviz.js"
    _css = pathlib.Path(__file__).parent / "static" / "graphviz.css"

    code_content = traitlets.Unicode("").tag(sync=True)
    svg = traitlets.Unicode("").tag(sync=True)

    def set_code_content(self, value):
        self.code_content = value


from .magics import GraphvizAnywidgetMagic

def load_ipython_extension(ipython):
    ipython.register_magics(GraphvizAnywidgetMagic)

from .panel import create_panel

# Launch with custom title as: graphviz_panel("Graphviz")
# Use second parameter for anchor
@create_panel
def graphviz_panel(title=None, anchor=None):
    return graphvizWidget()
