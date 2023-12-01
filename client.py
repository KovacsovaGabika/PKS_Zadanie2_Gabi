import queue
import socket
import threading
import random
import time


class ClientThread:
    def __init__(self, target_function):
        self.target_function = target_function

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


class Client:
    def __init__(self):
        self.thread1 = ClientThread(self.recieve)
        self.thread2 = ClientThread(self.keep_alive)
        self.thread3 = ClientThread(self.akcia)
        self.messages = queue.Queue()
        self.end = 0
        self.swap = 0
        self.akcia = None
        self.prvy_beh = 0

        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client.bind(("localhost", random.randint(8000, 9000)))

    def recieve(self):
        while True:
            try:
                message, _ = self.client.recvfrom(1024)
                self.messages.put(message.decode())

                if message.decode() == "00000111":
                    self.swap = 1
                    self.end = 1
                    #self.thread1.stop()
                    #self.thread2.stop()
                    self.prvy_beh = 1
                    #self.thread3.stop()

                    if self.end == 1:
                        self.client.close()

            except:
                pass

    def handshake(self):
        self.client.sendto("00000001".encode(), ("localhost", 7003))  # syn
        message, _ = self.client.recvfrom(1024)
        if message.decode() == "00000101":
            return 1
        return 0

    def keep_alive(self):
        while True:
            time.sleep(1)
            self.client.sendto("00000010".encode(), ("localhost", 7003))  # ka
            print("KA")

    def swapf(self):
        self.client.sendto("00000111".encode(), ("localhost", 7003))

    def akcia(self):
        while True:

            self.akcia = input("a) posli subor/b) swap/c) end")
            if self.akcia == "a":
                pass
            elif self.akcia == "b":
                self.swapf()
                self.end = 1
                self.thread1.stop()
                self.thread2.stop()
                #self.thread3.stop()
                self.swap = 1
                if self.end == 1:
                    self.client.close()

            else:
                #self.thread3.stop()
                break

    def start(self):
        if self.prvy_beh == 0:
            if self.handshake() == 1:
                print(f"Handshake uspesny")

        self.thread1.start()
        self.thread2.start()
        self.thread3.start()

        ending_condition = self.messages.get()
        while ending_condition != "00000110":
            ending_condition = self.messages.get()

        self.end = 1
        self.thread1.stop()
        self.thread2.stop()
        self.thread3.stop()

        if self.end == 1:
            self.client.close()
