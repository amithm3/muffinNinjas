import tkinter as tk
import os
import numpy as np
from src import perlin
from typing import *
from tkinter.filedialog import askopenfilename

if TYPE_CHECKING:
    from .gui import Gui
    from .menu import FielderButton


class Field(tk.Frame):
    FIELDER_SIZE = 3
    FIELDER_FLASH_SIZE_UP = 1
    FIELDER_MAX = 11
    FIELDER_COLOR = 'blue'
    FIELDER_FLASH_COLOR = 'maroon'
    PITCH_SIZE = (5, 20)

    def __init__(self, parent: "Gui", **kwargs):
        super(Field, self).__init__(parent, **kwargs)
        self.canvas = tk.Canvas(self, **kwargs)
        self.canvas.pack(expand=True, fill='both')

        self.pack_propagate(0)

        self.parent = parent
        self.scale = 1

    def build(self):
        boundary_select_but = tk.Button(self, text="Set Boundary", bg="#AAA")
        boundary_select_but.place(x=self.winfo_width() // 2 - boundary_select_but.winfo_reqwidth() // 2,
                                  y=self.winfo_height() // 2 - boundary_select_but.winfo_reqheight() // 2)
        boundary_select_but.bind("<Enter>", lambda event: boundary_select_but.configure(bg="light green"))
        boundary_select_but.bind("<Leave>", lambda event: boundary_select_but.configure(bg="#AAA"))
        boundary_select_but.config(command=lambda: self._cmd_boundary_select(boundary_select_but))

    def tkinterCoordToBoundary(self, x, y):
        return x - self.winfo_width() / 2, -(y - self.winfo_height() / 2)

    def boundaryCoordToTkinter(self, x, y):
        return x + self.winfo_width() / 2, y + self.winfo_height() / 2

    def _cmd_boundary_select(self, boundary_select_but: tk.Button):
        boundary_select_but["state"] = "disabled"
        if os.path.basename(path := os.path.dirname(os.getcwd())) == "muffinNinjas":
            init_path = rf"{path}/assets/fields"
        elif os.path.basename(path := os.getcwd()) == "muffinNinjas":
            init_path = rf"{path}/assets/fields"
        else:
            init_path = ""

        file = askopenfilename(initialdir=init_path)
        boundary_select_but["state"] = "normal"
        if os.path.basename(file) == "random.csv":
            self.draw_boundary(perlin.Perlin1D().noise(np.arange(360))[0])
        elif file == "":
            return
        else:
            if not self.file_to_boundary(file): return

        boundary_select_but.destroy()
        self.parent.field_menu.add_fielders(self.get_random_pos_within_boundary(11))

    def get_random_pos_within_boundary(self, num):
        positions = []
        while len(positions) < num:
            pos = np.random.uniform((-self.canvas.winfo_width() / 2, -self.canvas.winfo_height() / 2),
                                       (self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2), 2)
            if self.cheap_check_if_inside_boundary(*pos): positions.append((int(pos[0]), int(pos[1])))

        return positions

    def cheap_check_if_inside_boundary(self, x, y):
        theta = np.arctan2(y, x)
        theta = int(np.degrees(theta)) + 180
        coords = np.array(self.canvas.coords('field')).reshape([-1, 2]).transpose()
        coords = np.array(self.tkinterCoordToBoundary(*coords)).transpose()

        bound_len = (coords[theta: theta + 2] ** 2).mean()
        pos_len = x ** 2 + y ** 2

        return bound_len > pos_len

    def file_to_boundary(self, path):
        # noinspection PyBroadException
        try:
            self.parent.sim.field.load(path)
        except:
            return False

        boundary = [self.parent.sim.field.boundaryLength(angle) for angle in range(360)]
        self.draw_boundary(boundary)

        return True

    def draw_boundary(self, boundary):
        boundary = np.array(boundary)
        self.canvas.delete("field")
        zoom = min(self.winfo_width() / 2, self.winfo_height() / 2)
        self.scale = zoom / max(boundary)
        boundary *= self.scale
        angles = np.arange(boundary.shape[0])
        boundary = self.boundaryCoordToTkinter(np.sin(np.radians(angles)) * boundary,
                                               -np.cos(np.radians(angles)) * boundary)
        boundary = np.array(boundary).transpose()
        self.canvas.create_polygon(boundary.flatten().tolist(), fill='light green', outline='#000', width=1.5,
                                   tags="field")
        middle = self.boundaryCoordToTkinter(0, 0)
        self.canvas.create_rectangle([middle[0] - self.PITCH_SIZE[0], middle[1] - self.PITCH_SIZE[1],
                                      middle[0] + self.PITCH_SIZE[0], middle[1] + self.PITCH_SIZE[1]], tags="pitch",
                                     fill='sienna2', outline='sienna3')

    def draw_fielder(self, x, y, tag):
        x, y = self.boundaryCoordToTkinter(x, y)
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
