from socket import *
import os
import time
import sys
import queue
import threading as thread

q = queue.Queue(15)

def Client():
    global q

    time.sleep(1)
    print("Client side started.")

    server_name = sys.argv[1]
    server_port = int(sys.argv[2])
    mssg = sys.argv[4]

    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect((server_name, server_port))
    except:
        print("Connection could not be established.")
        exit()

    client_socket.send(mssg.encode())

    response = client_socket.recv(2048)
    # print(response.decode())

    if response.decode() == "Ending":
        print("Stream Closed")
        exit()
    elif response.decode() == "Reroute":
        # Recieves new ip
        response = client_socket.recv(2048)
        new_server_name = response.decode()
        # Recieves new Port
        response = client_socket.recv(2048)
        new_server_port = response.decode()
        print("Rerouting to "+new_server_name+", "+new_server_port)
        new_server_port = int(new_server_port)

        client_socket.close()

        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((new_server_name, new_server_port))

        response = client_socket.recv(2048)

    while(response):
        time.sleep(0.1)
        print(response.decode())
        # Buffer(response)
        q.put(response)
        if q.full():
            q.get()

        response = client_socket.recv(2048)
    

def isRelay(addr, connection_socket):
    global q

    print("Connecting, please wait...")
    first = True
    if first:
        time.sleep(10)
        first = False
    while True:
        while q:
            time.sleep(1)
            try:
                bit = q.get()
                # print(str(bit))
                connection_socket.send(bit)
                # print("Sent: "+bit)
            except:
                print(str(addr)+" closed or lost connection.")
                exit()



def Server():
    time.sleep(1)
    other_server_port = int(sys.argv[3])
    print("Server started with port: "+str(other_server_port))

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("", other_server_port))
    server_socket.listen(5)

    while True:
        connection_socket, addr = server_socket.accept()
        # mssg = connection_socket.recv(2048).decode()

        print("Established connection with: "+str(addr))

        threadStart = thread.Thread(target=isRelay, args=(addr, connection_socket))
        threadStart.start()

    connection_socket.close()

clientThread = thread.Thread(target=Client, args=())
serverThread = thread.Thread(target=Server, args=())

clientThread.start()
serverThread.start()

# print("end")
