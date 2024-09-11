from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

@magics_class
class GraphvizAnywidgetMagic(Magics):
    def __init__(self, shell):
        super(GraphvizAnywidgetMagic, self).__init__(shell)
        self.widget_name = (
            None  # Store the widget variable name as an instance attribute
        )
        self.widget = None

    def _set_widget(self, w_name=""):
        w_name = w_name.strip()
        if w_name:
            self.widget_name = w_name
        self.widget = self.shell.user_ns[self.widget_name]
        # Perhaps add a test that it is a widget type, else None?
        #print(f"graphviz_magic object set to: {self.widget_name}")

    @line_magic
    def setwidget(self, line):
        """Set the object name to be used in subsequent myAnywidget_magic calls."""
        self._set_widget(line)

    @cell_magic
    @magic_arguments()
    @argument('-w', '--widget-name', type=str, help='widget variable name')
    def graphviz_magic(self, line, cell):
        args = parse_argstring(self.graphviz_magic, line)
        if args.widget_name:
            self._set_widget(args.widget_name)
        if self.widget is None :
            print("Error: No widget / widget name set. Use %set_myAnywidget_object first to set the name.")
            return
        elif cell:
            # Get the actual widget
            w = self.widget
            w.set_code_content(cell)

## %load_ext jupyter_anywidget_graphviz
## Usage: %%graphviz_magic x [where x is the widget object ]
