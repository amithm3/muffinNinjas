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
        self.field = Field(self, bg='gray')
        self.field_menu = FieldMenu(self)
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
    class FielderStat(tk.Toplevel):
        def __init__(self, parent: "FieldMenu", but, **kwargs):
            super().__init__(parent, **kwargs)
            self.focus_force()
            self.overrideredirect(1)
            self.config(takefocus=1)

            stat = but.stat
            for key, val, i in zip(stat.keys(), stat.values(), range(len(stat))):
                if key == 'pos': tk.Label(self, text=f"{key}: {val}").grid(row=0, column=0, columnspan=2)
                else:
                    tk.Label(self, text=f"{key}").grid(row=i, column=0)
                    sv = tk.StringVar(self)
                    sv.trace("w", lambda *_, sv=sv, key=key, but=but: self.ent_to_but(but, key, sv))
                    ent = tk.Entry(self, textvariable=sv)
                    ent.insert('end', f"{val}")
                    ent.grid(row=i, column=1)
            ok_but = tk.Button(self, text="OK", command=lambda: (self.destroy(),))
            ok_but.grid()

            self.sync_windows()

        @staticmethod
        def ent_to_but(but, key, sv):
            print(key)
            but.stat[key] = sv.get()
            print(but.stat)

        def run(self):
            loop_active = True
            while loop_active:
                if self.winfo_exists(): self.after(0, self.update())
                else: break

        def sync_windows(self, event=None):
            if self.winfo_exists():
                x = self.master.master.winfo_x() + 30
                y = self.master.master.winfo_y() + 50
                self.geometry("+%d+%d" % (x, y))

    class BoundarySelect(tk.Toplevel):
        def __init__(self, parent: "Field", **kwargs):
            super().__init__(parent, **kwargs)
            self.focus_force()
            self.overrideredirect(1)
            self.config(takefocus=1)

            gen_ran_bound_but = tk.Button(self, text="Generate Random Boundary")
            chs_fil_bound_but = tk.Button(self, text="Choose Boundary info File")
            ok_but = tk.Button(self, text="OK",
                               command=lambda: (self.destroy(), parent.boundary_selected()), state='disabled')
            cl_but = tk.Button(self, text="CANCEL", command=lambda: (self.destroy(), parent.canvas.delete("field")))

            gen_ran_bound_but.config(command=lambda: (parent.draw_boundary(
                perlin.Perlin1D().noise(numpy.arange(360))[0]), ok_but.config(state='normal')))
            chs_fil_bound_but.config(command=lambda: parent.file_to_boundary(askopenfilename()))

            gen_ran_bound_but.pack(expand=1, fill='both')
            chs_fil_bound_but.pack(expand=1, fill='both')
            ok_but.pack(side='left')
            cl_but.pack(side='right')

            self.sync_windows()

        def run(self):
            loop_active = True
            while loop_active:
                if self.winfo_exists(): self.after(0, self.update())
                else: break

        def sync_windows(self, event=None):
            if self.winfo_exists():
                x = self.master.master.winfo_x() + 30
                y = self.master.master.winfo_y() + 50
                self.geometry("+%d+%d" % (x, y))


class Field(tk.Frame):
    FIELDER_SIZE = 2
    FIELDER_MAX = 11

    def __init__(self, parent: Gui, **kwargs):
        super(Field, self).__init__(parent, **kwargs)
        self.canvas = tk.Canvas(self, **kwargs)
        self.canvas.pack(expand=True, fill='both')

        self.pack_propagate(0)

        self._boundary_selected = False
        self.parent = parent
        self.fielder_seek = 0

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
        self.parent.bind("<Configure>", lambda event: popup.sync_windows(event))
        popup.grab_set()
        popup.run()
        popup.grab_release()
        self.parent.bind("<Configure>", lambda event: None)
        if not self._boundary_selected: boundary_select_but["state"] = "normal"
        else: boundary_select_but.destroy(); self._boundary_selected = False; self.add_fielders_setup()

    def boundary_selected(self):
        self._boundary_selected = True

    def draw_boundary(self, boundary):
        self.canvas.delete("field")
        boundary = [(int(math.cos(math.radians(angle)) * self.winfo_width() / 2 * length + self.winfo_width() / 2),
                     int(math.sin(math.radians(angle)) * self.winfo_height() / 2 * length + self.winfo_height() / 2))
                    for angle, length in enumerate(boundary)]
        self.canvas.create_polygon(boundary, fill='light green', outline='#000', width=1.5, tags="field")

    def file_to_boundary(self, file):
        pass

    def add_fielders_setup(self):
        self.parent.field_menu.show_add_fielder_button()

    def bind_add_fielder(self):
        self.canvas.tag_bind('field', "<Button-1>", lambda event: self.add_fielder(event.x, event.y))
        self.canvas.tag_bind('field', "<Enter>", lambda event: self.canvas.config(cursor="dotbox"))
        self.canvas.tag_bind('field', "<Leave>", lambda event: self.canvas.config(cursor=""))

    def unbind_add_fielder(self):
        self.canvas.tag_bind('field', "<Button-1>", lambda event: None)
        self.canvas.tag_bind('field', "<Enter>", lambda event: self.canvas.config(cursor=""))
        self.canvas.tag_bind('field', "<Leave>", lambda event: self.canvas.config(cursor=""))
        self.canvas.config(cursor="")

    def add_fielder(self, x, y):
        self.unbind_add_fielder()
        self.fielder_seek += 1
        tag = f'f{self.fielder_seek}'
        self.canvas.create_rectangle([x - self.FIELDER_SIZE, y - self.FIELDER_SIZE,
                                      x + self.FIELDER_SIZE, y + self.FIELDER_SIZE],
                                     tags=tag, fill='blue', outline='blue')
        self.parent.field_menu.add_fielder_menu(tag)


# future: merge with field class
class FieldMenu(tk.Frame):
    def __init__(self, parent: Gui, **kwargs):
        super(FieldMenu, self).__init__(parent, **kwargs)

        self.pack_propagate(0)

        self.parent = parent

    def build(self):
        pass

    def show_add_fielder_button(self):
        add_fielder_but = tk.Button(self, text="Add Fielder",
                                    command=lambda: (self.parent.field.bind_add_fielder(),
                                                     self.move_mouse_to_canvas()))
        add_fielder_but.pack(pady=10)

    def move_mouse_to_canvas(self):
        bbox = self.parent.field.canvas.bbox('field')
        x = numpy.random.randint(bbox[0], bbox[2])
        y = numpy.random.randint(bbox[1], bbox[3])
        self.parent.field.event_generate("<Motion>", x=x, y=y, warp=1)

    # noinspection PyTypeChecker
    def add_fielder_menu(self, tag):
        but = tk.Button(self)
        but.tag = tag
        but.config(command=lambda: self.change_fielder_stat(but))
        but.stat = {'pos': self.get_pos_by_tag(but.tag), 'v_max': 8, 'v_throw': 25}
        but.pack(fill='x', pady=5)

    def get_pos_by_tag(self, tag):
        cord = self.parent.field.canvas.coords(tag)

        return (cord[0] + cord[2]) / 2, (cord[1] + cord[3]) / 2

    def change_fielder_stat(self, but):
        popup = PopGui.FielderStat(self, but)
        self.parent.bind("<Configure>", lambda event: popup.sync_windows(event))
        popup.grab_set()
        popup.run()
        popup.grab_release()
        self.parent.bind("<Configure>", lambda event: None)


class Menu(tk.Frame):
    def __init__(self, parent: Gui, **kwargs):
        super(Menu, self).__init__(parent, **kwargs)

        self.parent = parent

    def build(self):
        pass


if __name__ == '__main__':
    gui = Gui()
    gui.mainloop()
