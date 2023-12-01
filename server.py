import socket
import threading
import queue
import time


# class KeepAlive(threading.Thread):
#   def __init__(self):
#      super(KeepAlive, self).__init__()
#     self.running = True

# def run(self):
#   while self.running:
#      if time.time() - ka_time > 10:
#         print("40s nebolo ka...")
#        self.stop()

# def stop(self):
#   self.running = False
#  self.join(timeout=0)


class ServerThread:
    def __init__(self, target_function):
        self.target_function = target_function
        # self.args = args

        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self.run)

    def run(self):
        while not self.stop_event.is_set():
            self.target_function()  # (self.args)
        
        return

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join(timeout=0)


class Server:
    def __init__(self):
        self.thread1 = ServerThread(self.recieve)
        self.thread2 = ServerThread(self.keep_alive)
        self.thread3 = ServerThread(self.akcia)
        self.messages = queue.Queue()
        self.clients = []
        self.ka_time = None
        self.addr = None
        self.end = 0
        self.swap = 0

        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(("localhost", 7003))

    def recieve(self):
        while not self.thread1.stop_event.is_set():
            try:
                message, self.addr = self.server.recvfrom(1024)
                message=int.from_bytes(message,byteorder="big")
                print(message)

                if message == 1:  # syn
                    flag=5
                    self.server.sendto(flag.to_bytes(1,byteorder="big"), self.addr)  # ack
                    print(f"Handshake uspesny")
                elif message == 2:  # ka
                    self.ka_time = time.time()
                    flag=3
                    self.server.sendto(flag.to_bytes(1,byteorder="big"), self.addr)  # ack
                    #print("IA")
                elif message == 7:
                    flag=6
                    self.server.sendto(flag.to_bytes(1,byteorder="big"), self.addr)  # fin
                    self.end = 1
                    self.swap = 1
                else:
                    self.messages.put((message, self.addr))
            except:
                pass

    def keep_alive(self):

        while not self.thread1.stop_event.is_set():
            time.sleep(2)
            if self.ka_time is not None and time.time() - self.ka_time > 10:
                print("10s nebolo ka...")
                flag=6
                self.server.sendto(flag.to_bytes(1,byteorder="big"), self.addr) #fin
                self.end = 1


    # server.sendto(6.encode(), addr)  # ak 40s nic ta fin

    def swapf(self):
        flag=7
        self.server.sendto(flag.to_bytes(1,byteorder="big"), self.addr)


    def recieve_file(self, filename):
        with open(filename, "wb"):
            while True:
                data, addr = self.server.recvfrom(4096)
                if not data:
                    break

    def akcia(self):
        while not self.thread3.stop_event.is_set():
            try:
                akcia = input("a) posli subor/b) swap/c) end")
            except:
                print("Zavírame kasíno ! 💔")
                exit()

            if akcia == "a":
                pass
            elif akcia == "b":
                self.swapf()
                self.end = 1
                self.thread1.stop()
                self.thread2.stop()
                self.thread3.stop()
                self.swap = 1
                if self.end == 1:
                    self.server.close()

            elif akcia == "c":
                self.end=1
                return

    def start(self):
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()

        while self.end != 1:
            pass

        self.thread3.stop()
        self.thread2.stop()
        self.thread1.stop()

        if self.end == 1:
            exit(0)

# messages = queue.Queue()
# clients = []

# server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server.bind(("localhost", 9998))

# ka_time = time.time()

# addr = None

# t1 = threading.Thread(target=recieve)
# t2 = threading.Thread(target=broadcast)
# t3 = KeepAlive()

# t1.start()
# t2.start()
# t3.start()
