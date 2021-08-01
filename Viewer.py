from socket import *
import os
import time
import sys
import queue
import threading as thread

q = queue.Queue(15)

backup_server_name = ""
backup_server_port = ""

def Client():
    global q
    global backup_server_name
    global backup_server_port

    time.sleep(0.1)
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

    response = client_socket.recv(2048).decode()
    print(response)

    if response == "Ending":
        print("Stream Closed")
        exit()
    elif response == "Reroute":
        # Recieves new ip
        new_server_name = client_socket.recv(2048).decode()
        # Recieves new Port
        new_server_port = client_socket.recv(2048).decode()
        print()
        backup_server_name = new_server_name
        backup_server_port = new_server_port
        print("==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==")
        print("Rerouting to "+new_server_name+", "+new_server_port)
        # server_port = int(server_port)

        client_socket.close()

        client_socket = socket(AF_INET, SOCK_STREAM)
        print(new_server_name)
        print(new_server_port)

        client_socket.connect((new_server_name, int(new_server_port)-1))

    print("Fallback ip: "+backup_server_name)
    print("Fallback port: "+backup_server_port)

    backup_server_name = client_socket.recv(2048)
    backup_server_port = client_socket.recv(2048)

    response = client_socket.recv(2048).decode()


    while(response):
        time.sleep(0.1)
        print("Response: "+response)
        # Buffer(response)
        q.put(response)
        
        if q.full():
            q.get()

        try:
            response = client_socket.recv(2048).decode()
        except:
            print("Lost connection, rerouting.")
            client_socket.close()
            client_socket = socket(AF_INET, SOCK_STREAM)
            
            print("Fallback ip: "+backup_server_name)
            print("Fallback port: "+backup_server_port)

            client_socket.connect((backup_server_name, int(backup_server_port)))
            print("Connecting to: ("+backup_server_name+", "+backup_server_port+")")
            # client_socket.send("".encode())


def isRelay(addr, connection_socket):
    global q

    print(backup_server_name)
    print(backup_server_port)

    print("Connecting, please wait...")
    connection_socket.send(backup_server_name.encode())
    # other_server_port = backup_server_port
    time.sleep(1)
    connection_socket.send(backup_server_port.encode())
    time.sleep(9)


    while True:
        while q:
            time.sleep(1)
            try:
                bit = q.get()
                # print(str(bit))
                connection_socket.send(bit.encode())
                # print("Sent: "+bit)
            except:
                print(str(addr)+" closed or lost connection.")
                exit()


def Server():

    other_server_port = int(sys.argv[3])

    time.sleep(1)
    print("Server started with port: "+str(other_server_port))

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(("", other_server_port))
    server_socket.listen(5)

    while True:
        connection_socket, addr = server_socket.accept()
        # mssg = connection_socket.recv(2048).decode()

        print("Establishing connection with: "+str(addr))
        # time.sleep(10)
        threadStart = thread.Thread(target=isRelay, args=(addr, connection_socket))
        threadStart.start()

    connection_socket.close()


clientThread = thread.Thread(target=Client, args=())
serverThread = thread.Thread(target=Server, args=())

clientThread.start()
serverThread.start()

# print("end")
