import importlib.metadata
import pathlib

import anywidget
import traitlets
import time
import warnings

import platform
import logging

PLATFORM = platform.system().lower()

from IPython.display import display

try:
    __version__ = importlib.metadata.version("jupyter_anywidget_graphviz")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"

try:
    from jupyter_ui_poll import ui_events

    WAIT_AVAILABLE = True
except:
    warnings.warn(
        "You must install jupyter_ui_poll if you want to return cell responses / blocking waits (not JupyerLite); install necessary packages then restart the notebook kernel:%pip install jupyter_ui_poll"
    )
    WAIT_AVAILABLE = False


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
    audio = traitlets.Bool(False).tag(sync=True)

    def __init__(self, headless=False, **kwargs):
        super().__init__(**kwargs)
        self.prefer_use_blocking = PLATFORM != "emscripten" 
        self.headless = headless
        self.response = {"status": "initialising"}
        self.previous_dot = ''

    def _wait(self, timeout, conditions=("status", "completed")):
        if not WAIT_AVAILABLE or conditions[0] not in self.response:
            # No wait condition available
            logging.warning("No wait available. Are you in a pyodide environment?")
            return
        start_time = time.time()
        with ui_events() as ui_poll:
            while (self.response[conditions[0]] != conditions[1]) & (
                self.response["status"] != "error"
            ):
                ui_poll(10)
                if timeout and ((time.time() - start_time) > timeout):
                    raise TimeoutError(
                        "Action not completed within the specified timeout."
                    )
                time.sleep(0.1)
        if self.response["status"] == "error":
            warnings.warn(self.response["error_message"])
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
        # if value == self.previous_dot:
        #    self.response = {"status": "completed"}
        #    return
        self.svg = ""
        self.code_content = ""
        self.code_content = value
        self.previous_dot = value

    def render(self, dot, autorespond=None, timeout=5):
        # The autorespond will try to wait
        self.set_code_content(dot)
        autorespond = self.prefer_use_blocking if autorespond is None else autorespond
        if autorespond:
            timeout = timeout if timeout > 0 else 5
            response = self.blocking_reply(timeout)
            return response


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
