import sys
from pathlib import Path

sys.path[0] = str(Path(sys.path[0]).parent)

import logging
import socket
import threading

from clientserver5.server.clienthandler import ClientHandler

logging.basicConfig(level=logging.INFO)


class SommenServer(threading.Thread):

    def __init__(self, host, port, messages_queue):
        threading.Thread.__init__(self, name="Thread-Server")
        self.__is_connected = False
        self.host = host
        self.port = port
        # self.init_server(host, port)                #server NIET onmiddellijk initialiseren (via GUI)
        self.messages_queue = messages_queue

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

    def close_server_socket(self):
        if self.serversocket is not None:
            self.serversocket.close()

    # thread-klasse!
    def run(self):
        number_received_message = 0
        try:
            while True:
                self.print_bericht_gui_server("waiting for a new client...")

                # establish a connection
                socket_to_client, addr = self.serversocket.accept()
                self.print_bericht_gui_server(f"Got a connection from {addr}")
                clh = ClientHandler(socket_to_client, self.messages_queue)
                clh.start()
                self.print_bericht_gui_server(
                    f"Current Thread count: {threading.active_count()}."
                )

        except Exception as ex:
            self.print_bericht_gui_server("Serversocket afgesloten")

    def print_bericht_gui_server(self, message):
        self.messages_queue.put(f"Server:> {message}")
