from functools import wraps
from sidecar import Sidecar
from IPython.display import display


# Create a decorator to simplify panel autolaunch
# First parameter on decorated function is optional title
# Second parameter on decorated function is optional anchor location
# Via Claude.ai
def create_panel(widget_class):
    @wraps(widget_class)
    def wrapper(title=None, anchor="split-right"):
        if title is None:
            title = f"{widget_class.__name__[:-6]} Output"  # Assuming widget classes end with 'Widget'

        widget_ = widget_class()
        widget_.sc = Sidecar(title=title, anchor=anchor)

        with widget_.sc:
            display(widget_)

        # Add a close method to the widget
        def close():
            widget_.sc.close()

        widget_.close = close

        return widget_
        # We can then close the panel as sc.

    return wrapper
