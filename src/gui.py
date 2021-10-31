from .simulation.simulator import Simulator
from .field import Field
from .menu import FieldMenu

import tkinter as tk


class Gui(tk.Tk):
    SIZE = (700, 600)
    TITLE = "TITLE"
    class ColumnRatio: Field = 6; Menu = 1

    def __init__(self, *args, **kwargs):
        super(Gui, self).__init__(*args, **kwargs)
        self.set_geometry()

        self.title(self.TITLE)
        self.resizable(0, 0)

        self._gui_skeleton()
        self._build()

        self.sim = Simulator()

    def set_geometry(self):
        x, y = (self.winfo_screenwidth() - self.SIZE[0]) // 2, (self.winfo_screenheight() - self.SIZE[1]) // 4
        w, h = self.SIZE
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.update_idletasks()

    def _gui_skeleton(self):
        self.field = Field(self, bg='gray')
        self.field_menu = FieldMenu(self)

        self.field.grid(row=0, column=0, sticky='news')
        self.field_menu.grid(row=0, column=1, sticky='news')

        self.columnconfigure(0, weight=self.ColumnRatio.Field)
        self.columnconfigure(1, weight=self.ColumnRatio.Menu)
        self.rowconfigure(0, weight=1)

        self.update_idletasks()
        self.update()

    def _build(self):
        self.field.build()
        self.field_menu.build()
