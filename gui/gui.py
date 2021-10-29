import perlin
import math
import numpy
import tkinter as tk
from tkinter.filedialog import askopenfilename


class Gui(tk.Tk):
    SIZE = (750, 600)
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
        self.field = Field(self)
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


class PopGui:
    class BoundarySelect(tk.Toplevel):
        def __init__(self, parent: "Field", **kwargs):
            super().__init__(parent, **kwargs)
            self.focus_force()

            gen_ran_bound_but = tk.Button(self, text="Generate Random Boundary")
            chs_fil_bound_but = tk.Button(self, text="Choose Boundary info File")
            ok_but = tk.Button(self, text="OK",
                               command=lambda: (self.destroy(), parent.boundary_selected()), state='disabled')
            cl_but = tk.Button(self, text="CANCEL", command=lambda: (self.destroy(), parent.canvas.delete("field")))

            gen_ran_bound_but.config(command=lambda: (parent.draw_boundary(
                perlin.Perlin1D().noise(numpy.arange(360))[0]), ok_but.config(state='normal')))

            gen_ran_bound_but.pack(expand=1, fill='both')
            chs_fil_bound_but.pack(expand=1, fill='both')
            ok_but.pack(side='left')
            cl_but.pack(side='right')

        def run(self):
            loop_active = True
            while loop_active:
                if self.winfo_exists(): self.after(0, self.update())
                else: break


class Field(tk.Frame):
    def __init__(self, parent, **kwargs):
        super(Field, self).__init__(parent, **kwargs)
        self.canvas = tk.Canvas(self, **kwargs)
        self.canvas.pack(expand=True, fill='both')

        self.pack_propagate(0)

        self._boundary_selected = False

    def build(self):
        boundary_select_but = tk.Button(self, text="Set Boundary", bg="#AAA")
        boundary_select_but.place(x=self.winfo_width() // 2 - boundary_select_but.winfo_reqwidth() // 2,
                                  y=self.winfo_height() // 2 - boundary_select_but.winfo_reqheight() // 2)
        boundary_select_but.bind("<Enter>", lambda event: boundary_select_but.configure(bg="light green"))
        boundary_select_but.bind("<Leave>", lambda event: boundary_select_but.configure(bg="#AAA"))
        boundary_select_but.config(command=lambda: self._on_boundary_select(boundary_select_but))

    def _on_boundary_select(self, boundary_select_but: tk.Button):
        boundary_select_but["state"] = "disabled"
        popup = PopGui.BoundarySelect(self)
        popup.geometry(f"+{self.winfo_rootx()}+{self.winfo_rooty()}")
        popup.grab_set()
        popup.run()
        popup.grab_release()
        if not self._boundary_selected: boundary_select_but["state"] = "normal"
        else: boundary_select_but.destroy(); self._boundary_selected = False

    def boundary_selected(self):
        self._boundary_selected = True

    def draw_boundary(self, boundary):
        self.canvas.delete("field")
        boundary = [(int(math.cos(math.radians(angle)) * self.winfo_width() / 2 * length + self.winfo_width() / 2),
                     int(math.sin(math.radians(angle)) * self.winfo_height() / 2 * length + self.winfo_height() / 2))
                    for angle, length in enumerate(boundary)]
        self.canvas.create_polygon(boundary, fill='light green', outline='#777', width=3.5, tags="field")
        self.canvas.create_polygon(boundary, fill='light green', outline='#000', width=1.5, tags="field")


class FieldMenu(tk.Frame):
    def __init__(self, parent, **kwargs):
        super(FieldMenu, self).__init__(parent, **kwargs)

    def build(self):
        pass


class Menu(tk.Frame):
    def __init__(self, parent, **kwargs):
        super(Menu, self).__init__(parent, **kwargs)

    def build(self):
        pass


if __name__ == '__main__':
    gui = Gui()
    gui.mainloop()
