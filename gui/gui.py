from src import perlin
import math
import numpy
import tkinter as tk


class Gui(tk.Tk):
    SIZE = (1000, 600)
    TITLE = "TITLE"
    class RowColumnRatio: Field = 6; Menu = 1; Up = 6; Bottom = 1

    def __init__(self, *args, **kwargs):
        super(Gui, self).__init__(*args, **kwargs)
        self.set_geometry()

        self.title(self.TITLE)
        self.resizable(0, 0)

        self._gui_skeleton()
        self._build()

    def set_geometry(self):
        x, y = (self.winfo_screenwidth() - self.SIZE[0]) // 2, (self.winfo_screenheight() - self.SIZE[1]) // 4
        w, h = self.SIZE
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.update_idletasks()

    def _gui_skeleton(self):
        self.field = Field(self, bg='red')
        self.field_menu = FieldMenu(self, bg='green')
        self.menu = Menu(self, bg='blue')

        self.field.grid(row=0, column=0, sticky='news')
        self.field_menu.grid(row=0, column=1, sticky='news')
        self.menu.grid(row=1, column=0, columnspan=2, sticky='news')

        self.columnconfigure(0, weight=self.RowColumnRatio.Field)
        self.columnconfigure(1, weight=self.RowColumnRatio.Menu)
        self.rowconfigure(0, weight=self.RowColumnRatio.Up)
        self.rowconfigure(1, weight=self.RowColumnRatio.Bottom)

        self.update_idletasks()

    def _build(self):
        self.field.build()
        self.field_menu.build()
        self.menu.build()


class PopGui(tk.Tk):
    pass


class Field(tk.Frame):
    def __init__(self, *args, **kwargs):
        super(Field, self).__init__(*args, **kwargs)
        self.canvas = tk.Canvas(self, **kwargs)
        self.canvas.pack(expand=True, fill='both')

        self.pack_propagate(0)

    def build(self):
        self.draw_boundary(perlin.Perlin1D().noise(numpy.arange(360))[0])

    def draw_boundary(self, boundary):
        boundary = [(int(math.cos(math.radians(angle)) * self.winfo_width() / 2 * length + self.winfo_width() / 2),
                     int(math.sin(math.radians(angle)) * self.winfo_height() / 2 * length + self.winfo_height() / 2))
                    for angle, length in enumerate(boundary)]
        self.canvas.create_polygon(boundary, fill='', outline='black')


class FieldMenu(tk.Frame):
    def __init__(self, *args, **kwargs):
        super(FieldMenu, self).__init__(*args, **kwargs)

    def build(self):
        pass


class Menu(tk.Frame):
    def __init__(self, *args, **kwargs):
        super(Menu, self).__init__(*args, **kwargs)

    def build(self):
        pass


if __name__ == '__main__':
    gui = Gui()
    gui.mainloop()
