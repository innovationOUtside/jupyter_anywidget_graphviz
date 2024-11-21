import importlib.metadata
import pathlib

import anywidget
import traitlets
import time
import warnings

from IPython.display import display

try:
    __version__ = importlib.metadata.version("jupyter_anywidget_graphviz")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

try:
    from jupyter_ui_poll import ui_events
except:
    warnings.warn(
        "You must install jupyter_ui_poll if you want to return cell responses / blocking waits (not JupyerLite); install necessary packages then restart the notebook kernel:%pip install jupyter_ui_poll",
        UserWarning,
    )

class Widget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = pathlib.Path(__file__).parent / "static" / "widget.css"
    value = traitlets.Int(0).tag(sync=True)


class graphvizWidget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "graphviz.js"
    _css = pathlib.Path(__file__).parent / "static" / "graphviz.css"

    headless = traitlets.Bool(False).tag(sync=True)
    code_content = traitlets.Unicode("").tag(sync=True)
    svg = traitlets.Unicode("").tag(sync=True)
    response = traitlets.Dict().tag(sync=True)

    def __init__(self, headless=False, **kwargs):
        super().__init__(**kwargs)
        self.headless = headless
        self.response = {"status": "initialising"}

    def _wait(self, timeout, conditions=("status", "completed")):
        start_time = time.time()
        with ui_events() as ui_poll:
            while self.response[conditions[0]] != conditions[1]:
                ui_poll(10)
                if timeout and ((time.time() - start_time) > timeout):
                    raise TimeoutError(
                        "Action not completed within the specified timeout."
                    )
                time.sleep(0.1)
        self.response["time"] = time.time() - start_time
        return

    def ready(self, timeout=5):
        self._wait(timeout, ("status", "ready"))

    # Need to guard this out in JupyterLite (definitely in pyodide)
    def blocking_reply(self, timeout=None):
        self._wait(timeout)
        return self.response

    def set_code_content(self, value):
        self.response = {"status": "processing"}
        self.svg = ''
        self.code_content = value

def graphviz_headless():
    widget_ = graphvizWidget(headless=True)
    display(widget_)
    return widget_


def graphviz_inline():
    widget_ = graphvizWidget()
    display(widget_)
    return widget_


from .magics import GraphvizAnywidgetMagic

def load_ipython_extension(ipython):
    ipython.register_magics(GraphvizAnywidgetMagic)

from .panel import create_panel

# Launch with custom title as: graphviz_panel("Graphviz")
# Use second parameter for anchor
@create_panel
def graphviz_panel(title=None, anchor=None):
    return graphvizWidget()
