import tkinter as tk
import numpy as np
import os
import threading as td
from typing import *
from .pop_gui import FielderStat
from ..simulation.fielder import Fielder
from tkinter.filedialog import askdirectory

if TYPE_CHECKING: from .gui import Gui


class FieldMenu(tk.Frame):
    def __init__(self, parent: "Gui", **kwargs):
        super(FieldMenu, self).__init__(parent, **kwargs)

        self.pack_propagate(0)

        self.parent = parent

    def build(self):
        but_batsman = tk.Button(self, text="Set Batsman \n Data", command=lambda: self.load_batsman_data())
        but_batsman.pack(fill='x', pady=5, padx=5)

        rate_but = tk.Button(self, text='rate', command=lambda: self.rate())
        rate_but.pack(side='bottom')

    def add_fielders(self, positions):
        for i, pos in zip(range(self.parent.field.FIELDER_MAX), positions):
            tag = f'f{i}'
            self.parent.field.draw_fielder(pos[0], pos[1], tag)
            FielderButton(self, tag).pack(fill='x', pady=5, padx=5)

    def move_mouse_to_canvas(self):
        bbox = self.parent.field.canvas.bbox('field')
        while True:
            pos = np.random.uniform((bbox[0], bbox[1]), (bbox[2], bbox[3]), 2)
            w, h = self.parent.field.canvas.winfo_width() / 2, self.parent.field.canvas.winfo_height() / 2
            if self.parent.field.cheap_check_if_inside_boundary(pos[0] - w, pos[1] - h): break
        self.parent.field.canvas.event_generate("<Motion>", x=pos[0], y=pos[1], warp=1)

    def get_pos_by_tag(self, tag):
        cord = self.parent.field.canvas.coords(tag)
        cord = self.parent.field.tkinterCoordToBoundary((cord[0] + cord[2]) / 2, (cord[1] + cord[3]) / 2)
        cord = cord[0] / self.parent.field.scale, cord[1] / self.parent.field.scale
        return cord

    def change_fielder_stat(self, but):
        popup = FielderStat(self, but)
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

    def load_batsman_data(self):
        if os.path.basename(path := os.path.dirname(os.getcwd())) == "muffinNinjas":
            init_path = rf"{path}/assets/players"
        elif os.path.basename(path := os.getcwd()) == "muffinNinjas":
            init_path = rf"{path}/assets/players"
        else:
            init_path = ""

        folder_path = askdirectory(initialdir=init_path)
        self.parent.sim.inputBatsManData(folder_path)

    def rate(self):
        thread = td.Thread(target=lambda: print(self.parent.sim.rate()))
        thread.daemon = True
        thread.start()


class FielderButton(tk.Button):
    def __init__(self, parent: "FieldMenu", tag, **kwargs):
        super(FielderButton, self).__init__(parent, text=tag, **kwargs)

        self.tag = tag
        self.parent = parent
        self.stat = {'pos': self.parent.get_pos_by_tag(self.tag), 'v_max': 8, 'v_throw': 25}
        self.fielder = Fielder(**self.stat)
        self.parent.parent.sim.addFielder(self.fielder)

        self.bind("<Enter>", lambda event, tags=self.tag: self.parent.parent.field.flash_fielder(tags))
        self.bind("<Leave>", lambda event, tags=self.tag: self.parent.parent.field.unFlash_fielder(tags))

        self.config(command=lambda: self.parent.change_fielder_stat(self))

    def update_pos(self):
        self.stat.update([('pos', self.parent.get_pos_by_tag(self.tag))])

    def update_fielder(self):
        self.fielder.update_stat(**self.stat)
