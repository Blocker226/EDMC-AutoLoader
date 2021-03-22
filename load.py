#  EDMC AutoLoader V1.0
#  Copyright (c) 2020 Blocker226. Released under GNU GPL 3.0
#  repo link

import logging
import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from typing import Optional

import myNotebook as nB
from config import appname, config

PLUGIN_NAME = "AutoLoader"
PLACEHOLDER_MSG = "Nothing Configured."

logger = logging.getLogger(f"{appname}.{PLUGIN_NAME}")


class AutoLoader:
    def __init__(self) -> None:
        self.lb = None
        self.raw_list: Optional[tk.StringVar] = tk.StringVar(value=str(config.get('auto_loader_list')))
        logger.debug("EDMC AutoLoader raw list: " + self.raw_list.get())
        if self.raw_list.get():
            logger.debug("Data found, initialising...")
            self.load_list = self.raw_list.get().split("\n")
        else:
            logger.debug("No existing data found.")
            self.load_list = []

    def refresh_list(self) -> None:
        self.lb.delete(0, tk.END)
        if not self.load_list:
            self.lb.insert(0, "Nothing Configured.")
            return
        for e in self.load_list:
            self.lb.insert(tk.END, e)

    def add_program(self):
        new_program = tk.filedialog.askopenfilename(initialdir="/", title="Select Program", filetypes=[
            ("exe Files", "*.exe"), ("All Files", "*.*")])
        if new_program not in self.load_list:
            self.load_list.append(new_program)
            logger.debug("Added item " + new_program)
            self.refresh_list()

    def del_program(self) -> None:
        if self.lb.get(self.lb.curselection()):
            logger.debug("Deleting item " + self.lb.curselection())
            self.load_list.remove(self.lb.get(self.lb.curselection()))
        self.refresh_list()

    def run_programs(self) -> bool:
        if not self.load_list:
            logger.info("No data, AutoLoader idling.")
            return False
        logger.info("AutoLoader running.")
        for e in self.load_list:
            try:
                logger.info("Executing " + e)
                subprocess.Popen(e, cwd=os.path.dirname(e))
            except Exception as exception:
                logger.error(exception)
                logger.info("Removing invalid entry " + e)
                self.load_list.remove(e)
        logger.info("AutoLoader finished launching.")
        return True

    def on_load(self) -> str:
        logger.info("EDMC AutoLoader loaded.")
        self.run_programs()
        return PLUGIN_NAME

    def on_unload(self) -> None:
        """
        on_unload is called by plugin_stop below.
        It is the last thing called before EDMC shuts down. Note that blocking code here will hold the shutdown process.
        """
        self.on_preferences_closed("", False)

    def setup_preferences(self, parent: nB.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
        current_row = 0
        frame = nB.Frame(parent)
        frame.grid_columnconfigure(0, weight=1)

        nB.Label(frame, text="Load List").grid(padx=10, pady=(10, 0), row=current_row, sticky="w")
        current_row += 1

        self.lb = tk.Listbox(frame)
        self.lb.grid(padx=10, pady=8, row=current_row, sticky="nsew")

        self.refresh_list()

        current_row += 1
        button_frame = nB.Frame(frame)
        button_frame.grid(row=current_row)
        nB.Button(button_frame, text="Add", command=self.add_program).grid(row=0, column=0)
        nB.Button(button_frame, text="Delete", command=self.del_program).grid(row=0, column=1)
        nB.Button(button_frame, text="Launch All", command=self.run_programs).grid(row=0, column=2)
        current_row += 1
        nB.Label(frame, text="EDMC Autoloader v0.1 by CMDR Blocker226").grid(padx=10, pady=(10, 0),
                                                                             row=current_row, sticky="w")

        return frame

    def on_preferences_closed(self, cmdr: str, is_beta: bool) -> None:
        if self.load_list:
            logger.info("Saving " + str(len(self.load_list)) + " items to preferences.")
            config.set('auto_loader_list', '\n'.join(self.load_list))


al = AutoLoader()


def plugin_start3(plugin_dir: str) -> str:
    return al.on_load()


def plugin_stop() -> None:
    return al.on_unload()


def plugin_prefs(parent: nB.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
    return al.setup_preferences(parent, cmdr, is_beta)


def prefs_changed(cmdr: str, is_beta: bool) -> None:
    return al.on_preferences_closed(cmdr, is_beta)


# def plugin_app(parent: tk.Frame) -> Optional[tk.Frame]:
#     return al.setup_main_ui(parent)
