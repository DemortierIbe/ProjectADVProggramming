# https://pythonprogramming.net/python-3-tkinter-basics-tutorial/
import logging
import socket
from queue import Queue
from threading import Thread
from tkinter import *
import sys
import os
from pathlib import Path

# print(sys.path[0])  # test
# sys.path[0] = str(Path(sys.path[0]).parent)  # Hier aanpassen
# print(sys.path[0])
from ServerFolder.server import Server


class ServerWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.server = None
        self.thread_listener_queue = None
        self.init_messages_queue()

    # Creation of init_window
    def init_window(self):
        # changing the title of our master widget
        self.master.title("Server")
        self.master.geometry("700x600")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        Label(self, text="Log-berichten server:").grid(row=0)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.lstnumbers = Listbox(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstnumbers.yview)

        self.lstnumbers.grid(row=1, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=1, column=1, sticky=N + S)

        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.lst_connectedclients = Listbox(self)
        self.scrollbar.config(command=self.lst_connectedclients.yview)
        self.lst_connectedclients.grid(row=2, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=2, column=1, sticky=N + S)

        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.lst_showallclients = Listbox(self)
        self.scrollbar.config(command=self.lst_showallclients.yview)
        self.lst_showallclients.grid(row=3, column=0, sticky=N + S + E + W)
        self.scrollbar.grid(row=3, column=1, sticky=N + S)

        self.lbl_scorerangeoperaties = Label(
            self, text="Scorerange operaties: {}"
        ).grid(row=4, column=0)
        self.lbl_searchcountryoperaties = Label(
            self, text="Searchcountry operaties: {}"
        ).grid(row=5, column=0)
        self.lbl_bbpoperaties = Label(self, text="Bbp operaties: {}").grid(
            row=6, column=0
        )
        self.lbl_compareoperaties = Label(self, text="Compare operaties: {}").grid(
            row=7, column=0
        )

        self.btn_text = StringVar()
        self.btn_text.set("Start server")
        self.buttonServer = Button(
            self, textvariable=self.btn_text, command=self.start_stop_server
        )

        self.buttonServer.grid(
            row=8,
            column=0,
            columnspan=2,
            pady=(5, 5),
            padx=(5, 5),
            sticky=N + S + E + W,
        )

        Grid.rowconfigure(self, 1, weight=1)
        Grid.columnconfigure(self, 0, weight=1)

    def start_stop_server(self):
        if self.server is not None:
            self.__stop_server()
        else:
            self.__start_server()

    def __stop_server(self):
        self.server.stop_server()
        self.server = None
        logging.info("Server stopped")
        self.btn_text.set("Start server")

    def __start_server(self):
        self.server = Server(socket.gethostname(), 9999, self.messages_queue)
        self.server.init_server()
        self.server.start()  # in thread plaatsen!
        logging.info("Server started")
        self.btn_text.set("Stop server")

    def init_messages_queue(self):
        self.messages_queue = Queue()
        self.thread_listener_queue = Thread(
            target=self.print_messsages_from_queue,
            name="Queue_listener_thread",
            daemon=True,
        )
        self.thread_listener_queue.start()

    def print_messsages_from_queue(self):
        message = self.messages_queue.get()
        previous_handlers = set()
        while message != "CLOSE_SERVER":
            self.lst_connectedclients.delete(0, END)
            handlers = self.server.get_online_users()
            for handler in handlers:
                self.lst_connectedclients.insert(END, handler)
            usersinfo = self.server.get_user_data_from_csv("users.csv")
            self.lst_showallclients.delete(0, END)
            for user in usersinfo:
                self.lst_showallclients.insert(END, user)
            self.update_operaties_sum()
            self.lstnumbers.insert(END, message)
            self.messages_queue.task_done()
            message = self.messages_queue.get()
            previous_handlers.update(handlers)

    def update_operaties_sum(self):
        self.lbl_scorerangeoperaties = Label(
            self,
            text=f"Scorerange operaties: {str(self.server.get_sum_score_range_operaties('users.csv'))}",
        ).grid(row=4, column=0)
        self.lbl_searchcountryoperaties = Label(
            self,
            text=f"Searchcountry operaties: {str(self.server.get_sum_search_country_operaties('users.csv'))}",
        ).grid(row=5, column=0)
        self.lbl_bbpoperaties = Label(
            self,
            text=f"Bbp operaties: {str(self.server.get_sum_bbp_operaties('users.csv'))}",
        ).grid(row=6, column=0)
        self.lbl_compareoperaties = Label(
            self,
            text=f"Compare operaties: {str(self.server.get_sum_compare_operaties('users.csv'))}",
        ).grid(row=7, column=0)
