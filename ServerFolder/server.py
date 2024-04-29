import csv
import os
import pandas as pd
import sys
from pathlib import Path
import threading
import socket
import logging
import numpy as np


from ServerFolder.clienthandler import ClientHandler

# create a socket object
logging.info("Creating serversocket...")
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# get local machine name
host = socket.gethostname()
ip = socket.gethostbyname(host)

port = 3520

# bind to the port
serversocket.bind((host, port))


class Server(threading.Thread):
    def __init__(self, host, port, messages_queue):
        threading.Thread.__init__(self, name="Thread-Server", daemon=True)
        self.serversocket = None
        self.__is_connected = False
        self.host = host
        self.port = port
        self.messages_queue = messages_queue

    def data_preprocessen(self):

        logging.info("Data preprocessed")
        self.print_bericht_gui_server("Data preprocessed")
        return pd.read_csv("merged_dataset.csv")

    @property
    def is_connected(self):
        return self.__is_connected

    def init_server(self):
        # create a socket object
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(5)
        self.__is_connected = True
        self.print_bericht_gui_server("SERVER STARTED")
        self.dataset = self.data_preprocessen()

    def stop_server(self):
        if self.serversocket is not None:
            self.serversocket.close()
            self.serversocket = None
            self.__is_connected = False
            logging.info("Serversocket closed")

    # thread-klasse!
    def run(self):
        try:
            while True:
                self.print_bericht_gui_server("waiting for a new client...")
                # establish a connection
                socket_to_client, addr = self.serversocket.accept()
                logging.info(f"Got a connection from {addr}")
                self.print_bericht_gui_server(f"Got a connection from {addr}")
                clh = ClientHandler(socket_to_client, self.messages_queue, self.dataset)
                clh.start()
                logging.info(f"Client handler started")
                self.print_bericht_gui_server(
                    f"Current Thread count: {threading.active_count()}."
                )

        except Exception as ex:
            self.print_bericht_gui_server("Serversocket afgesloten")

    def print_bericht_gui_server(self, message):
        self.messages_queue.put(f"Server:> {message}")

    def get_online_users(self) -> list[ClientHandler]:
        handlers = []
        for handler in threading.enumerate():
            if isinstance(handler, ClientHandler):
                handlers.append(handler)
        return handlers

    def get_user_data_from_csv(self, csvfile):
        user_data_list = []
        with open(csvfile, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_data = {
                    "user": row["user"],
                    "ScoreRangeOperaties": int(row["ScoreRangeOperaties"]),
                    "SearchCountryOperaties": int(row["SearchCountryOperaties"]),
                    "BBPOperaties": int(row["BBPOperaties"]),
                    "CompareOperaties": int(row["CompareOperaties"]),
                }
                user_data_list.append(user_data)
        return user_data_list
