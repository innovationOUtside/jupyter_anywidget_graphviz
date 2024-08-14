from IPython.core.magic import Magics, magics_class, cell_magic


@magics_class
class GraphvizAnywidgetMagic(Magics):
    def __init__(self, shell):
        super(GraphvizAnywidgetMagic, self).__init__(shell)

    @cell_magic
    def graphviz_magic(self, line, cell):
        obj_name = line.strip()
        if cell:
            w = self.shell.user_ns[obj_name]
            w.set_code_content(cell)

## %load_ext jupyter_anywidget_graphviz
## Usage: %%graphviz_magic x [where x is the widget object ]
