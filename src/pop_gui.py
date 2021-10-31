import tkinter as tk
from typing import *

if TYPE_CHECKING:
    from .menu import FieldMenu, FielderButton


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
                vcmd = (self.register(self.validateIntegerEntry), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
                ent = tk.Entry(self, textvariable=sv, validate="key", validatecommand=vcmd)
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
        if key == 'pos': but.stat[key] = sv.get()
        else: but.stat[key] = int(sv.get())
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

    @staticmethod
    def validateIntegerEntry(*args):
        if args[4] == ' ': return False
        try:
            int(args[2])
            return True
        except ValueError:
            return False
