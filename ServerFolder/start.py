import sys
from pathlib import Path

# print(sys.path[0]) #test
sys.path[0] = str(Path(sys.path[0]).parent)  # Hier aanpassen
print(sys.path[0])

import logging
import threading
from tkinter import *

from ServerFolder.gui_server import ServerWindow

logging.basicConfig(level=logging.DEBUG)


def callback():
    # even controleren overlopen van actieve threads wanneer window gesloten wordt
    logging.debug("Active threads:")
    for thread in threading.enumerate():
        logging.debug(f">Thread name is {thread.getName()}.")
    root.destroy()


root = Tk()
root.geometry("600x500")
gui_server = ServerWindow(root)
root.protocol("WM_DELETE_WINDOW", callback)
root.mainloop()
