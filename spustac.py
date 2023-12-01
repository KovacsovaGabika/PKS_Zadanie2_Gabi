import server
import client

import threading


class TheThread:
    def __init__(self, target_function):
        self.target_function = target_function
        # self.args = args

        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run)

    def run(self):
        while not self.stop_event.is_set():
            self.target_function()  # (self.args)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join(timeout=0)


count = 0
volba = 0

while volba != "3":
    if count == 0:
        volba = input("1 server/2 client/3 exit")

    if volba == "1":
        server1 = server.Server()

        server1.start()

        if count == 0:
            server1.prvy_beh = 1

        if server1.swap == 1:
            print("som v ifku")
            server1.thread4.stop()
            volba = "2"

    elif volba == "2":
        client1 = client.Client()

        client1.start()

        if count == 0:
            client1.prvy_beh = 1

        if client1.swap == 1:
            print("som v ifku")
            client1.thread3.stop()
            volba = "1"

    count = 1
