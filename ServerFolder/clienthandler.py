import os
import pickle
import sys
import threading
import jsonpickle
import hashlib
import numpy as np
import pandas as pd
import uuid
import datetime
from pathlib import Path

from werkzeug import Client

# VSC Compatibility
# print(sys.path[0])  # test
# sys.path[0] = str(Path(sys.path[0]).parent)  # Hier aanpassen
# print(sys.path[0])


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
                    print("GetCountriesWithHappinesScore")
                    obj = jsonpickle.decode(data)

                    countries = self.search_countries_by_happiness_score(
                        obj.HappinessMin, obj.HappinessMax
                    )
                    obj.countries = countries

                elif commando == "GetCountry":
                    print("GetCountry")
                    obj = jsonpickle.decode(data)
                    country = self.search_country_by_name(obj.Country)
                    obj.Country = country

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

        # Calculate the average happiness score across the 5 years for each country
        average_scores_per_country = self.dataset.groupby("Country")[
            "Happiness Score"
        ].mean()

        # Filter countries based on average happiness score range
        filtered_countries = average_scores_per_country[
            (average_scores_per_country >= min_score)
            & (average_scores_per_country <= max_score)
        ]

        return filtered_countries.index.tolist()

    def search_country_by_name(self, country_name):
        # Filter DataFrame based on country name
        filtered_df = self.dataset[self.dataset["Country"] == country_name]

        # Selecting only 'Year' and 'Happiness Score' columns
        filtered_df = filtered_df[["Year", "Happiness Score"]]

        # Converting DataFrame to a list of tuples
        score_per_year = [
            (row["Year"], row["Happiness Score"])
            for index, row in filtered_df.iterrows()
        ]

        return score_per_year
