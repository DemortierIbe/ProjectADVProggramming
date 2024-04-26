# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import sys
from pathlib import Path

print(sys.path[0])  # test
sys.path[0] = str(Path(sys.path[0]).parent)  # Hier aanpassen
print(sys.path[0])


import logging
import socket
from tkinter import *
from Data.GetCountriesHappines import GetCountriesHappines
from Data.GetCountriesScore import GetCountriesScore

from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Combobox

import jsonpickle
import tkinter as tk
from tkinter import ttk
import threading


class Window(Frame, threading.Thread):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        threading.Thread.__init__(self)
        self.master = master
        self.init_window()
        self.makeConnnectionWithServer()
        self.start()

    def init_window(self):
        # changing the title of our master widget
        self.master.title("Happines score")
        self.master.geometry("800x600")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # zoeken naar landen tussen een happines range
        Label(
            self, text="Geef de range van happines score waartussen je wil zoeken:"
        ).grid(row=0)

        self.entry_happinesScore1 = Entry(self, width=20)
        self.entry_happinesScore2 = Entry(self, width=20)

        self.entry_happinesScore1.grid(
            row=1, column=0, sticky=E + W, padx=(5, 5), pady=(5, 5)
        )
        self.entry_happinesScore2.grid(
            row=2, column=0, sticky=E + W, padx=(5, 5), pady=(5, 0)
        )

        self.requestbutton = Button(
            self, text="Search", command=self.GetCountriesWithHappinesScore
        )
        self.requestbutton.grid(row=3, column=0, padx=(5, 5), pady=(5, 5))

        # land opzoeken om gelukscore te zien
        Label(self, text="Geef een land in om de happines score te zien:").grid(row=4)
        self.entry_country = Entry(self, width=20)
        self.entry_country.grid(row=5, column=0, sticky=E + W, padx=(5, 5), pady=(5, 5))

        self.requestbutton = Button(
            self, text="Search country", command=self.GetCountry
        )
        self.requestbutton.grid(row=6, column=0, padx=(5, 5), pady=(5, 5))

        Grid.rowconfigure(self, 8, weight=1)
        Grid.columnconfigure(self, 1, weight=1)

    def show_message_box_CountriesByHappiness(self, result):
        window = tk.Toplevel()
        window.title("Countries with Happiness Score")

        text = tk.Text(window, wrap="word", height=20, width=50)
        text.pack(side="left", fill="y", expand=True)

        # Check if the list of countries is empty
        if not result.countries:
            text.insert(tk.END, "There is no country within this happiness score range")
        else:
            # Create a Scrollbar widget
            scrollbar = tk.Scrollbar(window, command=text.yview)
            scrollbar.pack(side="right", fill="y")
            text.config(yscrollcommand=scrollbar.set)

            # Insert the data into the Text widget
            text.insert(tk.END, "\n".join(result.countries))

            # Disable text editing
            text.config(state=tk.DISABLED)

    def show_message_box_Score(self, result):
        window = tk.Toplevel()
        window.title("Countries with Happiness Score")

        text = tk.Text(window, wrap="word", height=20, width=50)
        text.pack(side="left", fill="y", expand=True)

        # Check if the list of countries is empty
        if not result:
            text.insert(tk.END, "This country does not exist")
        else:
            # Create a Scrollbar widget
            scrollbar = tk.Scrollbar(window, command=text.yview)
            scrollbar.pack(side="right", fill="y")
            text.config(yscrollcommand=scrollbar.set)

            # Insert the data into the Text widget
            text.insert(
                tk.END,
                "\n".join(
                    f"{item[0]} - Happiness Score: {item[1]}" for item in result.Country
                ),
            )

            # Disable text editing
            text.config(state=tk.DISABLED)

        window.mainloop()

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

    def GetCountriesWithHappinesScore(self):
        try:
            logging.info("Get countries with happines score...")
            happinesScore1 = float(self.entry_happinesScore1.get())
            happinesScore2 = float(self.entry_happinesScore2.get())

            self.my_writer_obj.write(f"GetCountriesWithHappinesScore\n")
            data = GetCountriesHappines(happinesScore1, happinesScore2)
            self.my_writer_obj.write(jsonpickle.encode(data) + "\n")
            self.my_writer_obj.flush()

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")

    def GetCountry(self):
        try:
            logging.info("Get country...")
            country = self.entry_country.get()

            self.my_writer_obj.write(f"GetCountry\n")
            data = GetCountriesScore(country)
            print(data)
            self.my_writer_obj.write(jsonpickle.encode(data) + "\n")
            self.my_writer_obj.flush()

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")

    def run(self):
        commando = self.my_writer_obj.readline().rstrip()
        data = self.my_writer_obj.readline().rstrip()
        while commando != "CLOSE":
            if "GetCountriesWithHappinesScore" in commando:
                result = jsonpickle.decode(data)
                self.master.after(0, self.show_message_box_CountriesByHappiness, result)
            elif "GetCountry" in commando:
                result = jsonpickle.decode(data)
                self.master.after(0, self.show_message_box_Score, result)
            commando = self.my_writer_obj.readline().rstrip("\n")
            data = self.my_writer_obj.readline().rstrip("\n")


logging.basicConfig(level=logging.INFO)

root = Tk()
root.geometry("400x300")
app = Window(root)
root.mainloop()
