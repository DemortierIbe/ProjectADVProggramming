import sys
from pathlib import Path

sys.path[0] = str(Path(sys.path[0]).parent)

import threading


class ClientHandler(threading.Thread):

    numbers_clienthandlers = 0

    def __init__(self, socketclient, messages_queue):
        threading.Thread.__init__(self)
        # connectie with client
        self.socket_to_client = socketclient
        # message queue -> link to gui server
        self.messages_queue = messages_queue
        # id clienthandler
        self.id = ClientHandler.numbers_clienthandlers
        ClientHandler.numbers_clienthandlers += 1

    def run(self):
        io_stream_client = self.socket_to_client.makefile(mode="rw")

        self.print_bericht_gui_server("Started & waiting...")
        commando = io_stream_client.readline().rstrip("\n")
        while commando != "CLOSE":
            getal1 = io_stream_client.readline().rstrip("\n")
            self.print_bericht_gui_server(f"Number 1: {getal1}")
            getal2 = io_stream_client.readline().rstrip("\n")
            self.print_bericht_gui_server(f"Number 2: {getal2}")

            sum = int(getal1) + int(getal2)

            io_stream_client.write(f"{sum}\n")
            io_stream_client.flush()
            self.print_bericht_gui_server(f"Sending sum {sum} back")

            commando = io_stream_client.readline().rstrip("\n")

        self.print_bericht_gui_server("Connection with client closed...")
        self.socket_to_client.close()

    def print_bericht_gui_server(self, message):
        self.messages_queue.put(f"CLH {self.id}:> {message}")
