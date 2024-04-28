import os
import pickle
import sys
import threading
from tkinter import messagebox
import jsonpickle
import hashlib
import numpy as np
import pandas as pd
import uuid
import datetime
from pathlib import Path
import matplotlib.pyplot as plt
import csv

from werkzeug import Client


class ClientHandler(threading.Thread):
    numbers_clienthandlers = 0

    def __init__(self, socketclient, messages_queue, par_dataset):
        threading.Thread.__init__(self)
        self.socketclient = socketclient
        self.client_io_obj = self.socketclient.makefile(mode="rw")
        self.messages_queue = messages_queue
        self.id = ClientHandler.numbers_clienthandlers

        ClientHandler.numbers_clienthandlers += 1
        self.dataset = par_dataset

    def getDataLogin(self):
        self.container = self.database.get_container_client(self.container_name)
        query = "SELECT * FROM c"
        items = self.container.query_items(query, enable_cross_partition_query=True)
        for item in items:
            try:
                self.people_list.append(
                    Client(
                        naam=item["naam"],
                        email=item["email"],
                        wachtwoord=item["wachtwoord"],
                    )
                )
            except Exception as e:
                self.bericht_servergui(f"Error: {e}")
        print(list(self.people_list))

    def run(self):
        io_stream_client = self.socketclient.makefile(mode="rw")
        print("Started & waiting...")
        try:
            commando = io_stream_client.readline().rstrip("\n")
            data = io_stream_client.readline().rstrip("\n")
            obj = None
            while commando != "CLOSE":
                if commando == "GetCountriesWithHappinesScore":
                    self.bericht_servergui("GetCountriesWithHappinesScore")
                    obj = jsonpickle.decode(data)

                    countries = self.search_countries_by_happiness_score(
                        obj.HappinessMin, obj.HappinessMax
                    )
                    obj.countries = countries

                elif commando == "GetCountry":
                    self.bericht_servergui("GetCountry")
                    obj = jsonpickle.decode(data)
                    score = self.search_country_by_name(obj.Country)
                    obj.Score = score

                elif commando == "GetCountriesWithBbp":
                    self.bericht_servergui("GetCountriesWithBbp")
                    obj = jsonpickle.decode(data)
                    countries = self.search_countries_by_avg_gdp_range(
                        obj.BbpMin, obj.BbpMax
                    )
                    obj.countries = countries
                elif commando == "CompareCountries":
                    self.bericht_servergui("CompareCountries")
                    obj = jsonpickle.decode(data)
                    comparison = self.compare_countries_happiness(
                        obj.Country1, obj.Country2
                    )
                    obj.Comparison = comparison

                elif commando == "UserLogin":
                    self.bericht_servergui("UserLogin")
                    obj = jsonpickle.decode(data)
                    if self.check_user_credentials(
                        obj.username, obj.email, obj.password, "users.csv"
                    ):
                        obj.succes = True
                    else:
                        obj.succes = False
                elif commando == "UserRegister":
                    self.bericht_servergui("UserRegister")
                    obj = jsonpickle.decode(data)
                    obj.succes = self.add_user_to_csv(
                        obj.username, obj.email, obj.password, "users.csv"
                    )

                self.client_io_obj.write(commando + "\n")
                self.client_io_obj.write(jsonpickle.encode(obj) + "\n")
                self.client_io_obj.flush()

                commando = io_stream_client.readline().rstrip("\n")
                data = io_stream_client.readline().rstrip("\n")

        except Exception as e:
            self.bericht_servergui(f"Error: {e}")

    def bericht_servergui(self, message):
        self.messages_queue.put(f"CLH {self.id}:> {message}")

    def search_countries_by_happiness_score(self, min_score, max_score):

        # zorgen dat min_score < max_score
        if min_score > max_score:
            min_score, max_score = max_score, min_score

        # gemiddelde hapinnes score berekenen per land
        average_scores_per_country = self.dataset.groupby("Country")[
            "Happiness Score"
        ].mean()

        # Filteren op min en max score
        filtered_countries = average_scores_per_country[
            (average_scores_per_country >= min_score)
            & (average_scores_per_country <= max_score)
        ]

        return filtered_countries.index.tolist()

    def search_country_by_name(self, country_name):
        # filteren op land
        filtered_df = self.dataset[self.dataset["Country"] == country_name]

        filtered_df = filtered_df[["Year", "Happiness Score"]]

        score_per_year = [
            (row["Year"], row["Happiness Score"])
            for index, row in filtered_df.iterrows()
        ]

        return score_per_year

    def search_countries_by_avg_gdp_range(self, min_avg_gdp, max_avg_gdp):
        # zorgen dat min_avg_gdp < max_avg_gdp
        if min_avg_gdp > max_avg_gdp:
            min_avg_gdp, max_avg_gdp = max_avg_gdp, min_avg_gdp
        # gemiddelde bbp berekenen per land
        avg_gdp_per_country = self.dataset.groupby("Country")[
            "Economy (GDP per Capita)"
        ].mean()

        # filteren op min en max bbp
        filtered_countries = avg_gdp_per_country[
            (avg_gdp_per_country >= min_avg_gdp) & (avg_gdp_per_country <= max_avg_gdp)
        ]

        # namen van de landen in een list steken
        countries_within_avg_gdp_range = filtered_countries.index.tolist()

        return countries_within_avg_gdp_range

    def compare_countries_happiness(self, country1, country2):

        # Filteren op land
        country1_data = self.dataset[self.dataset["Country"] == country1]
        country2_data = self.dataset[self.dataset["Country"] == country2]

        comparison_df = pd.concat([country1_data, country2_data])

        comparison_df = comparison_df[["Country", "Year", "Happiness Score"]]

        comparison_list = comparison_df.values.tolist()

        return comparison_list

    def check_user_credentials(self, username, email, password, csvfile):
        with open(csvfile, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (
                    row["user"] == username
                    and row["email"] == email
                    and row["password"] == password
                ):
                    return True
        return False

    def is_valid_email(self, email):
        return "@" in email and "." in email

    def email_exists_in_csv(self, email, csvfile):
        with open(csvfile, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["email"] == email:
                    return True
        return False

    def add_user_to_csv(self, username, email, password, csvfile):
        # controleren als het email valid is
        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return False
        # controleren als ge gebruiker al bestaat
        if self.email_exists_in_csv(email, csvfile):
            return False

        fieldnames = [
            "user",
            "email",
            "password",
            "ScoreRangeOperaties",
            "SearchCountryOperaties",
            "BBPOperaties",
            "CompareOperaties",
        ]
        new_user_data = {
            "user": username,
            "email": email,
            "password": password,
            "ScoreRangeOperaties": "0",
            "SearchCountryOperaties": "0",
            "BBPOperaties": "0",
            "CompareOperaties": "0",
        }
        with open(csvfile, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            # als de file leeg is headers toevoegen
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(new_user_data)
        return True
