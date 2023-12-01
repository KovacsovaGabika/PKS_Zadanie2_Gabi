import server
import client

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
