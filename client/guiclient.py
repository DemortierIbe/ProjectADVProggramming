# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import sys
from pathlib import Path

print(sys.path[0])  # test
sys.path[0] = str(Path(sys.path[0]).parent)  # Hier aanpassen
print(sys.path[0])


import logging
import socket
from tkinter import *

from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Combobox

import jsonpickle
import tkinter as tk
from tkinter import ttk


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.makeConnnectionWithServer()

    def init_window(self):
        # Maak een lijst met de opties
        options = ["downloads", "rating", "number of reviews"]

        # Maak een combobox
        combo_box = ttk.Combobox(root, values=options)

        # Stel de huidige waarde van de combobox in op de eerste optie ("downloads")
        combo_box.current(0)

        # Plaats de combobox op rij 1 en kolom 2
        combo_box.grid(row=0, column=1)
        Label(self, text="Sort by").grid(row=1, column=0)

        self.requestbutton = Button(root, text="Request", command=self.request)
        self.requestbutton.grid(row=2, column=0, columnspan=2, pady=(5, 5), padx=(5, 5))

        Grid.rowconfigure(self, 3, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

    def makeConnnectionWithServer(self):
        try:
            logging.info("Making connection with server...")
            # get local machine name
            host = socket.gethostname()
            port = 9999
            self.socket_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # connection to hostname on the port.
            self.socket_to_server.connect((host, port))
            self.my_writer_obj = self.socket_to_server.makefile(mode="rw")
            logging.info("Open connection with server succesfully")
        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")

    def request(self):
        try:
            logging.info("Requesting data from server...")
            # Send request to server
            self.my_writer_obj.write(f"request")
            self.my_writer_obj.flush()
            # Receive data from server
            data = self.my_writer_obj.readline().rstrip("\n")
            self.my_writer_obj.flush()
            logging.info(f"Received data from server: {data}")
            # Convert data to Som object
            som = jsonpickle.decode(data)
            # Print data
            logging.info(f"Som object: {som}")
        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")


logging.basicConfig(level=logging.INFO)

root = Tk()
root.geometry("400x300")
app = Window(root)
root.mainloop()
