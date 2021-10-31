import numpy as np

from src import perlin
import os
from src.simulator import Simulator

import math
import numpy
import tkinter as tk
from src.fielder import Fielder
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

        self.sim = Simulator()

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
        def __init__(self, parent: "FieldMenu", but: "FielderButton", **kwargs):
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
                    sv.trace("w", lambda *_, svv=sv, keyy=key, bot=but: self.ent_to_but(bot, keyy, svv))
                    ent = tk.Entry(self, textvariable=sv)
                    ent.insert('end', f"{val}")
                    ent.grid(row=i, column=1)
            row = self.grid_size()[1]
            ok_but = tk.Button(self, text="OK",
                               command=lambda: (self.destroy(), parent.parent.field.unFlash_fielder(but.tag)))
            ok_but.grid(row=row, column=0)
            change_pos_but = tk.Button(self, text="Change Position",
                                       command=lambda: (parent.parent.field.bind_change_fielder(but), self.destroy(),
                                                        parent.disable(), parent.move_mouse_to_canvas()))
            change_pos_but.grid(row=row, column=1)

            self.sync_windows()

        @staticmethod
        def ent_to_but(but: "FielderButton", key, sv):
            but.stat[key] = sv.get()
            but.update_fielder()

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
    FIELDER_SIZE = 3
    FIELDER_FLASH_SIZE_UP = 1
    FIELDER_MAX = 11
    FIELDER_COLOR = 'blue'
    FIELDER_FLASH_COLOR = 'maroon'
    PITCH_SIZE = (20, 5)

    def __init__(self, parent: Gui, **kwargs):
        super(Field, self).__init__(parent, **kwargs)
        self.canvas = tk.Canvas(self, **kwargs)
        self.canvas.pack(expand=True, fill='both')

        self.pack_propagate(0)

        self.parent = parent

    def build(self):
        boundary_select_but = tk.Button(self, text="Set Boundary", bg="#AAA")
        boundary_select_but.place(x=self.winfo_width() // 2 - boundary_select_but.winfo_reqwidth() // 2,
                                  y=self.winfo_height() // 2 - boundary_select_but.winfo_reqheight() // 2)
        boundary_select_but.bind("<Enter>", lambda event: boundary_select_but.configure(bg="light green"))
        boundary_select_but.bind("<Leave>", lambda event: boundary_select_but.configure(bg="#AAA"))
        boundary_select_but.config(command=lambda: self._cmd_boundary_select(boundary_select_but))

    def _cmd_boundary_select(self, boundary_select_but: tk.Button):
        boundary_select_but["state"] = "disabled"
        if os.path.basename(path := os.path.dirname(os.getcwd())) == "muffinNinjas":
            init_path = rf"{path}/assets/fields"
        elif os.path.basename(path := os.getcwd()) == "muffinNinjas": init_path = rf"{path}/assets/fields"
        else: init_path = ""

        file = askopenfilename(initialdir=init_path)
        boundary_select_but["state"] = "normal"
        if os.path.basename(file) == "random.csv": self.draw_boundary(perlin.Perlin1D().noise(np.arange(360))[0])
        elif file == "": return
        else:
            if not self.file_to_boundary(file): return

        boundary_select_but.destroy()
        self.parent.field_menu.add_fielders(self.get_random_pos_within_boundary(11))

    def get_random_pos_within_boundary(self, num):
        positions = []
        while len(positions) < num:
            pos = numpy.random.uniform((-self.canvas.winfo_width() / 2, -self.canvas.winfo_height() / 2),
                                       (self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2), 2)
            if self.cheap_check_if_inside_boundary(*pos): positions.append((int(pos[0]), int(pos[1])))

        return positions

    def cheap_check_if_inside_boundary(self, x, y):
        theta = numpy.arctan(y / x)
        theta = int(np.degrees(theta))
        if y < 0 and x < 0: theta += 180
        if y < 0 < x: theta += 360
        if y > 0 > x: theta += 180
        coords = numpy.array(self.canvas.coords('field')).reshape([-1, 2]) - [self.canvas.winfo_width() / 2,
                                                                              self.canvas.winfo_height() / 2]

        bound_len = (coords[theta: theta + 2] ** 2).sum() / 2
        pos_len = x**2 + y**2
        return bound_len > pos_len and not np.isclose(bound_len, pos_len, rtol=0.09)

    def file_to_boundary(self, path):
        # noinspection PyBroadException
        try:
            self.parent.sim.field.load(path)
        except:
            return False

        boundary = [self.parent.sim.field.boundaryLength(angle) for angle in range(360)]
        self.draw_boundary(np.array(boundary) / max(boundary))

        return True

    def draw_boundary(self, boundary):
        self.canvas.delete("field")
        boundary = [(int(math.cos(math.radians(angle)) * self.winfo_width() / 2 * length + self.winfo_width() / 2),
                     int(math.sin(math.radians(angle)) * self.winfo_height() / 2 * length + self.winfo_height() / 2))
                    for angle, length in enumerate(boundary)]
        self.canvas.create_polygon(boundary, fill='light green', outline='#000', width=1.5, tags="field")
        boundary = np.array(boundary)
        middle = boundary.mean(axis=0)
        self.canvas.create_rectangle([middle[0] - self.PITCH_SIZE[0], middle[1] - self.PITCH_SIZE[1],
                                      middle[0] + self.PITCH_SIZE[0], middle[1] + self.PITCH_SIZE[1]], tags="pitch",
                                     fill='sienna2', outline='sienna3')

    def draw_fielder(self, x, y, tag):
        x += self.canvas.winfo_width() / 2
        y += self.canvas.winfo_height() / 2
        self.canvas.create_rectangle([x - self.FIELDER_SIZE, y - self.FIELDER_SIZE,
                                      x + self.FIELDER_SIZE, y + self.FIELDER_SIZE],
                                     tags=tag, fill=self.FIELDER_COLOR, outline=self.FIELDER_COLOR)

    def bind_change_fielder(self, but):
        self.canvas.tag_bind('field', "<Button-1>", lambda event: self.change_fielder_pos(but, event.x, event.y))
        self.canvas.tag_bind('field', "<Enter>", lambda event: self.canvas.config(cursor="dotbox"))
        self.canvas.tag_bind('field', "<Leave>", lambda event: self.canvas.config(cursor=""))

    def unbind_change_fielder(self):
        self.canvas.tag_bind('field', "<Button-1>", lambda event: None)
        self.canvas.tag_bind('field', "<Enter>", lambda event: self.canvas.config(cursor=""))
        self.canvas.tag_bind('field', "<Leave>", lambda event: self.canvas.config(cursor=""))
        self.canvas.config(cursor="")

    def change_fielder_pos(self, but: "FielderButton", x, y):
        self.unbind_change_fielder()
        self.canvas.coords(but.tag, [x - self.FIELDER_SIZE - self.FIELDER_FLASH_SIZE_UP,
                                     y - self.FIELDER_SIZE - self.FIELDER_FLASH_SIZE_UP,
                                     x + self.FIELDER_SIZE + self.FIELDER_FLASH_SIZE_UP,
                                     y + self.FIELDER_SIZE + self.FIELDER_FLASH_SIZE_UP])
        self.unFlash_fielder(but.tag)
        but.update_pos()
        but.update_fielder()
        self.parent.field_menu.enable()

    def flash_fielder(self, tag):
        self.canvas.itemconfig(tag, fill=self.FIELDER_FLASH_COLOR, outline=self.FIELDER_FLASH_COLOR)
        coords = self.canvas.coords(tag)
        self.canvas.coords(tag, [coords[0] - self.FIELDER_FLASH_SIZE_UP, coords[1] - self.FIELDER_FLASH_SIZE_UP,
                                 coords[2] + self.FIELDER_FLASH_SIZE_UP, coords[3] + self.FIELDER_FLASH_SIZE_UP])

    def unFlash_fielder(self, tag):
        self.canvas.itemconfig(tag, fill=self.FIELDER_COLOR, outline=self.FIELDER_COLOR)
        coords = self.canvas.coords(tag)
        self.canvas.coords(tag, [coords[0] + self.FIELDER_FLASH_SIZE_UP, coords[1] + self.FIELDER_FLASH_SIZE_UP,
                                 coords[2] - self.FIELDER_FLASH_SIZE_UP, coords[3] - self.FIELDER_FLASH_SIZE_UP])


class FieldMenu(tk.Frame):
    def __init__(self, parent: Gui, **kwargs):
        super(FieldMenu, self).__init__(parent, **kwargs)

        self.pack_propagate(0)

        self.parent = parent

    def build(self):
        pass

    def add_fielders(self, positions):
        for i, pos in zip(range(self.parent.field.FIELDER_MAX), positions):
            tag = f'f{i}'
            self.parent.field.draw_fielder(pos[0], pos[1], tag)
            FielderButton(self, tag).pack(fill='x', pady=5)

    def move_mouse_to_canvas(self):
        bbox = self.parent.field.canvas.bbox('field')
        while True:
            pos = numpy.random.uniform((bbox[0], bbox[1]), (bbox[2], bbox[3]), 2)
            w, h = self.parent.field.canvas.winfo_width() / 2, self.parent.field.canvas.winfo_height() / 2
            if self.parent.field.cheap_check_if_inside_boundary(pos[0] - w, pos[1] - h): break
        self.parent.field.canvas.event_generate("<Motion>", x=pos[0], y=pos[1], warp=1)

    def get_pos_by_tag(self, tag):
        cord = self.parent.field.canvas.coords(tag)
        return (cord[0] + cord[2]) / 2, (cord[1] + cord[3]) / 2

    def change_fielder_stat(self, but):
        popup = PopGui.FielderStat(self, but)
        self.parent.bind("<Configure>", lambda event: popup.sync_windows(event))
        but.bind("<Leave>", lambda event, tag=but.tag: None)
        popup.grab_set()
        popup.run()
        popup.grab_release()
        self.parent.bind("<Configure>", lambda event: None)
        but.bind("<Leave>", lambda event, tag=but.tag: self.parent.field.unFlash_fielder(tag))

    def disable(self):
        self.grid_forget()

    def enable(self):
        self.grid(row=0, column=1, sticky='news')


class Menu(tk.Frame):
    def __init__(self, parent: Gui, **kwargs):
        super(Menu, self).__init__(parent, **kwargs)

        self.parent = parent

    def build(self):
        pass


class FielderButton(tk.Button):
    def __init__(self, parent: "FieldMenu", tag, **kwargs):
        super(FielderButton, self).__init__(parent, **kwargs)

        self.tag = tag
        self.parent = parent
        self.stat = {'pos': self.parent.get_pos_by_tag(self.tag), 'v_max': 8, 'v_throw': 25}
        self.fielder = Fielder(**self.stat)

        self.bind("<Enter>", lambda event, tags=self.tag: self.parent.parent.field.flash_fielder(tags))
        self.bind("<Leave>", lambda event, tags=self.tag: self.parent.parent.field.unFlash_fielder(tags))

        self.config(command=lambda: self.parent.change_fielder_stat(self))

    def update_pos(self):
        self.stat.update([('pos', self.parent.get_pos_by_tag(self.tag))])

    def update_fielder(self):
        self.fielder.update_stat(**self.stat)


if __name__ == '__main__':
    gui = Gui()
    gui.mainloop()
