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
from Data.GetCountriesHappinesWithBbp import GetCountriesHappinesWithBbp
from Data.Vergelijk2Landen import Vergelijk2Landen
from Data.UserLogin import UserLogin

from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Combobox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import jsonpickle
import tkinter as tk
from tkinter import ttk
import threading

score_range = [
    0,
    0.5,
    1,
    1.5,
    2,
    2.5,
    3,
    3.5,
    4,
    4.5,
    5,
    5.5,
    6,
    6.5,
    7,
    7.5,
    8,
    8.5,
    9,
    9.5,
    10,
]

All_Countries = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "Argentina",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahrain",
    "Bangladesh",
    "Belarus",
    "Belgium",
    "Benin",
    "Bhutan",
    "Bolivia",
    "Bosnia and Herzegovina",
    "Botswana",
    "Brazil",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Chad",
    "Chile",
    "China",
    "Colombia",
    "Congo (Brazzaville)",
    "Congo (Kinshasa)",
    "Costa Rica",
    "Croatia",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Estonia",
    "Ethiopia",
    "Finland",
    "France",
    "Gabon",
    "Georgia",
    "Germany",
    "Ghana",
    "Greece",
    "Guatemala",
    "Guinea",
    "Haiti",
    "Honduras",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Israel",
    "Italy",
    "Ivory Coast",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kosovo",
    "Kuwait",
    "Kyrgyzstan",
    "Latvia",
    "Lebanon",
    "Liberia",
    "Libya",
    "Lithuania",
    "Luxembourg",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Mali",
    "Malta",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Moldova",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Myanmar",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "Norway",
    "Pakistan",
    "Palestinian Territories",
    "Panama",
    "Paraguay",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Qatar",
    "Romania",
    "Russia",
    "Rwanda",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Sierra Leone",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "South Africa",
    "South Korea",
    "Spain",
    "Sri Lanka",
    "Sweden",
    "Switzerland",
    "Syria",
    "Tajikistan",
    "Tanzania",
    "Thailand",
    "Togo",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Uganda",
    "Ukraine",
    "United Kingdom",
    "United States",
    "Uruguay",
    "Uzbekistan",
    "Venezuela",
    "Vietnam",
    "Yemen",
    "Zambia",
    "Zimbabwe",
]

Bbp_range = [
    0,
    0.1,
    0.2,
    0.3,
    0.4,
    0.5,
    0.6,
    0.7,
    0.8,
    0.9,
    1,
    1.1,
    1.2,
    1.3,
    1.4,
    1.5,
    1.6,
    1.7,
    1.8,
    1.9,
    2,
]


class Window(Frame, threading.Thread):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        threading.Thread.__init__(self)
        self.master = master
        while True:
            try:
                if self.makeConnnectionWithServer():
                    break
            except Exception as ex:
                logging.error(f"Foutmelding: {ex}")
                messagebox.showerror("Error", "Could not connect to server")
        self.init_window()
        
        self.start()

    def init_window(self):
        # login window
        self.master.withdraw()
        self.top = tk.Toplevel()
        self.top.title("Login")
        self.top.geometry("300x250")
        Label(self.top, text="Please enter your username, email and password").grid(
            row=0, columnspan=2, padx=(5, 5), pady=(5, 5)
        )
        Label(self.top, text="The Username and password is case sensitive").grid(
            row=1, columnspan=2, padx=(5, 5), pady=(5, 5)
        )
        Label(self.top, text="Username:").grid(
            row=2, column=0, padx=(5, 5), pady=(5, 5)
        )
        self.entry_username = Entry(self.top, width=20)
        Label(self.top, text="Email:").grid(row=3, column=0, padx=(5, 5), pady=(5, 5))
        self.entry_email = Entry(self.top, width=20)
        Label(self.top, text="Password:").grid(
            row=4, column=0, padx=(5, 5), pady=(5, 5)
        )
        self.entry_password = Entry(self.top, width=20, show="*")
        self.entry_username.grid(row=2, column=1, padx=(5, 5), pady=(5, 5))
        self.entry_email.grid(row=3, column=1, padx=(5, 5), pady=(5, 5))
        self.entry_password.grid(row=4, column=1, padx=(5, 5), pady=(5, 5))

        self.requestbutton = Button(self.top, text="Login", command=self.login)
        self.requestbutton.grid(row=5, column=0, padx=(5, 5), pady=(5, 5), columnspan=2)

        self.requestbutton = Button(self.top, text="Register", command=self.register)
        self.requestbutton.grid(row=6, column=0, padx=(5, 5), pady=(5, 5), columnspan=2)

        Grid.rowconfigure(self.top, 7, weight=1)
        Grid.columnconfigure(self.top, 2, weight=1)

        self.master.title("Happines score")
        self.master.geometry("450x500")

        self.pack(fill=BOTH, expand=1)

        # zoeken naar landen tussen een happines range
        Label(
            self, text="Geef de range van happines score waartussen u wil zoeken:"
        ).grid(row=0)

        self.cmb_happinesScoreMin = Combobox(
            self, state="readonly", values=score_range, width=20
        )
        self.cmb_happinesScoreMax = Combobox(
            self, state="readonly", values=score_range, width=20
        )
        self.cmb_happinesScoreMin.current(0)
        self.cmb_happinesScoreMax.current(1)

        self.cmb_happinesScoreMin.grid(
            row=1, column=0, sticky=E + W, padx=(5, 5), pady=(5, 5)
        )
        self.cmb_happinesScoreMax.grid(
            row=2, column=0, sticky=E + W, padx=(5, 5), pady=(5, 0)
        )

        self.requestbutton = Button(
            self, text="Search", command=self.GetCountriesWithHappinesScore
        )
        self.requestbutton.grid(row=3, column=0, padx=(5, 5), pady=(5, 5))

        # land opzoeken om gelukscore te zien
        Label(self, text="Geef een land in om de happines score te zien:").grid(row=4)
        self.cmb_country = Combobox(
            self, state="readonly", values=All_Countries, width=20
        )
        self.cmb_country.current(0)
        self.cmb_country.grid(row=5, column=0, sticky=E + W, padx=(5, 5), pady=(5, 5))

        self.requestbutton = Button(self, text="Search", command=self.GetCountry)
        self.requestbutton.grid(row=6, column=0, padx=(5, 5), pady=(5, 5))

        # landen tussen een bepaalde range van BBP
        Label(
            self,
            text="Geef de range van de BBP invloed op de happines score waartussen u wil zoeken:",
        ).grid(row=7)

        self.cmb_bbpMin = Combobox(self, state="readonly", values=Bbp_range, width=20)
        self.cmb_bbpMax = Combobox(self, state="readonly", values=Bbp_range, width=20)
        self.cmb_bbpMin.current(0)
        self.cmb_bbpMax.current(1)
        self.cmb_bbpMin.grid(row=8, column=0, sticky=E + W, padx=(5, 5), pady=(5, 5))
        self.cmb_bbpMax.grid(row=9, column=0, sticky=E + W, padx=(5, 5), pady=(5, 0))
        self.requestbutton = Button(
            self, text="search", command=self.GetCountriesWithBbp
        )
        self.requestbutton.grid(row=10, column=0, padx=(5, 5), pady=(5, 5))

        # 2 landen opzoeken om te vergelijken
        Label(self, text="Geef 2 landen die u wilt vergelijken:").grid(row=11)

        self.cmb_country1 = Combobox(
            self, state="readonly", values=All_Countries, width=20
        )
        self.cmb_country2 = Combobox(
            self, state="readonly", values=All_Countries, width=20
        )
        self.cmb_country1.current(0)
        self.cmb_country2.current(1)
        self.cmb_country1.grid(row=12, column=0, sticky=E + W, padx=(5, 5), pady=(5, 5))
        self.cmb_country2.grid(row=13, column=0, sticky=E + W, padx=(5, 5), pady=(5, 0))
        self.requestbutton = Button(self, text="search", command=self.Vergelijk2Landen)
        self.requestbutton.grid(row=14, column=0, padx=(5, 5), pady=(5, 5))

        self.requestbutton = Button(self, text="Logout", command=self.Logout)
        self.requestbutton.grid(row=15, column=0, padx=(5, 5), pady=(5, 5))

        Grid.rowconfigure(self, 16, weight=1)
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
        window.geometry("1200x800")

        # tekst widget maken
        text = tk.Text(window, wrap="word", height=20, width=50)
        text.pack(side="left", fill="both", expand=True)

        if not result:  # kijken of het niet leeg is
            text.insert(tk.END, "This country does not exist")
        else:

            scrollbar = tk.Scrollbar(window, command=text.yview)
            scrollbar.pack(side="right", fill="y")
            text.config(yscrollcommand=scrollbar.set)

            text.insert(
                tk.END,
                "\n".join(
                    f"{item[0]} - Happiness Score: {item[1]}" for item in result.Score
                ),
            )

            text.config(state=tk.DISABLED)

            # plot maken
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(
                [item[0] for item in result.Score],
                [item[1] for item in result.Score],
                marker="o",
                linestyle="-",
            )
            ax.set_title(
                f"Evolution of Happiness Score over the Years for {result.Country}"
            )
            ax.set_xlabel("Year")
            ax.set_ylabel("Happiness Score")
            ax.grid(True)

            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        window.mainloop()

    def show_message_box_CountriesByAvgBbp(self, result):
        window = tk.Toplevel()
        window.title("Countries in this BBP range")

        text = tk.Text(window, wrap="word", height=20, width=50)
        text.pack(side="left", fill="y", expand=True)

        if not result.countries:  # kijken of de list niet leeg is
            text.insert(tk.END, "There is no country within this BBP range")
        else:
            scrollbar = tk.Scrollbar(window, command=text.yview)
            scrollbar.pack(side="right", fill="y")
            text.config(yscrollcommand=scrollbar.set)

            text.insert(tk.END, "\n".join(result.countries))

            text.config(state=tk.DISABLED)

    def show_message_box_Compare(self, result):
        window = tk.Toplevel()

        window.title("Comparison of Happiness Scores")

        text = tk.Text(window, wrap="word", height=20, width=50)
        text.pack(side="left", fill="y", expand=True)

        if not result.Comparison:  # kijken of de list niet leeg is
            text.insert(tk.END, "No data available for comparison.")
        else:
            scrollbar = tk.Scrollbar(window, command=text.yview)
            scrollbar.pack(side="right", fill="y")
            text.config(yscrollcommand=scrollbar.set)

            for item in result.Comparison:
                text.insert(
                    tk.END, f"{item[0]} - Year: {item[1]}, Happiness Score: {item[2]}\n"
                )

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
            return True
        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")

    def GetCountriesWithHappinesScore(self):
        try:
            logging.info("Get countries with happines score...")
            happinesScoreMin = float(self.cmb_happinesScoreMin.get())
            happinesScoreMax = float(self.cmb_happinesScoreMax.get())

            self.my_writer_obj.write(f"GetCountriesWithHappinesScore\n")
            data = GetCountriesHappines(happinesScoreMin, happinesScoreMax)
            self.my_writer_obj.write(jsonpickle.encode(data) + "\n")
            self.my_writer_obj.flush()

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")

    def GetCountry(self):
        try:
            logging.info("Get country...")
            country = self.cmb_country.get()

            self.my_writer_obj.write(f"GetCountry\n")
            data = GetCountriesScore(country)
            print(data)
            self.my_writer_obj.write(jsonpickle.encode(data) + "\n")
            self.my_writer_obj.flush()

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")

    def GetCountriesWithBbp(self):
        try:
            logging.info("Get countries with BBP...")
            bbpMin = float(self.cmb_bbpMin.get())
            bbpMax = float(self.cmb_bbpMax.get())

            self.my_writer_obj.write(f"GetCountriesWithBbp\n")
            data = GetCountriesHappinesWithBbp(bbpMin, bbpMax)
            self.my_writer_obj.write(jsonpickle.encode(data) + "\n")
            self.my_writer_obj.flush()

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")

    def Vergelijk2Landen(self):
        try:
            logging.info("Vergelijk 2 landen...")
            country1 = self.cmb_country1.get()
            country2 = self.cmb_country2.get()

            self.my_writer_obj.write(f"CompareCountries\n")
            data = Vergelijk2Landen(country1, country2)
            self.my_writer_obj.write(jsonpickle.encode(data) + "\n")
            self.my_writer_obj.flush()

        except Exception as ex:
            logging.error(f"Foutmelding: {ex}")

    def Logout(self):
        self.master.withdraw()
        self.top.deiconify()

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
            elif "GetCountriesWithBbp" in commando:
                result = jsonpickle.decode(data)
                self.master.after(0, self.show_message_box_CountriesByAvgBbp, result)
            elif "CompareCountries" in commando:
                result = jsonpickle.decode(data)
                self.master.after(0, self.show_message_box_Compare, result)
            elif "UserLogin" in commando:
                result = jsonpickle.decode(data)
                if result.succes:
                    self.master.deiconify()
                    self.top.withdraw()
                else:
                    messagebox.showerror("Error", "Invalid username or password")
            elif "UserRegister" in commando:
                result = jsonpickle.decode(data)
                if result.succes:
                    messagebox.showinfo("Success", "User registered successfully")
                else:
                    messagebox.showerror(
                        "Error", "User already exists or the email is invalid"
                    )
            commando = self.my_writer_obj.readline().rstrip("\n")
            data = self.my_writer_obj.readline().rstrip("\n")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        email = self.entry_email.get()
        email = email.lower()
        self.my_writer_obj.write(f"UserLogin\n")
        data = UserLogin(username, password, email)
        self.my_writer_obj.write(jsonpickle.encode(data) + "\n")
        self.my_writer_obj.flush()

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        email = self.entry_email.get()
        email = email.lower()
        self.my_writer_obj.write(f"UserRegister\n")
        data = UserLogin(username, password, email)
        self.my_writer_obj.write(jsonpickle.encode(data) + "\n")
        self.my_writer_obj.flush()


logging.basicConfig(level=logging.INFO)

root = Tk()
root.geometry("400x300")
app = Window(root)
root.mainloop()
