import sys
from pathlib import Path

print(sys.path[0])
sys.path[0] = str(Path(sys.path[0]).parent)
print(sys.path[0])

import threading
from tkinter import *

from gui_server import ServerWindow


def callback():
    # test
    # threads overlopen
    print("Active threads:")
    for thread in threading.enumerate():
        print(f">Thread name is {thread.getName()}.")
    gui_server.afsluiten_server()
    root.destroy()


root = Tk()
root.geometry("600x500")
gui_server = ServerWindow(root)
root.protocol("WM_DELETE_WINDOW", callback)
root.mainloop()
