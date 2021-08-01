from socket import *
import os
import time
import sys
import threading as thread

# Connections contains all addresses for ease of checking if connection is new.
connections = []
# Tracker contains address of pier host, number of connections.
tracker = []
count = 0

print(sys.argv[1])

server_socket = socket(AF_INET, SOCK_STREAM)
server_port = int(sys.argv[1])
server_socket.bind(("", server_port))
server_socket.listen(5)


def redirect(addr, connection_socket):
    global connections
    global tracker
    global server_port

    count = 0
    for viewers in tracker:
        redirectAddr, connected = viewers
        ip, port = redirectAddr
        # print(ip)
        if connected == 1:
            count += 1
            continue
        else:
            text = "Reroute"
            connection_socket.send(text.encode())
            newPort = (server_port+(len(connections)-1))
            newPort = str(newPort)
            # print(newPort)
            print("Rerouting: "+str(addr)+" to ("+str(ip)+", "+str(newPort)+")")
            connection_socket.send(ip.encode())
            connection_socket.send(newPort.encode())
            connected += 1
            tracker.insert(count, (redirectAddr, connected))
            print()
            print(str(redirectAddr)+" Now has "+str(connected)+" connection(s).")
            connection_socket.close()
            break


def trackerAdd(addr, connection_socket):
    global connections
    global tracker

    connections.append(addr)
    print("Appended: "+str(addr)+" as connection #: "+str(len(connections)))
    tracker.append((addr, 0))

    if (len(connections) >= 2):
        redirect(addr, connection_socket)


def trackerRemove(addr):
    global connections
    global tracker

    for viewers in tracker:
        redirectAddr, connected = viewers
        if addr == redirectAddr:
            connected = connected - 1
            tracker.insert(count, (redirectAddr, connected))
            print(str(redirectAddr)+" Now has "+str(connected)+" connection(s).")


def isStreaming(mssg, addr, connection_socket):
    global connections

    if addr not in connections:
        trackerAdd(addr, connection_socket)
    i = 0
    # l = f.read(2048)
    while True:
        time.sleep(1)
        try:
            connection_socket.send(("Byte "+str(i)).encode())
        except:
            print(str(addr)+" closed or lost connection.")
            # trackerRemove(addr)
            connection_socket.close()
            break
        i += 1


def stream():
    # f = open("Test.txt", 'rb')
    print("Stream Starting...")

    while True:
        connection_socket, addr = server_socket.accept()
        mssg = connection_socket.recv(2048).decode()
        # print("Yes!")
        if mssg == "End":
            print("Stream Closed")
            connection_socket.send("Ending".encode())
            break
        threadStart = thread.Thread(target=isStreaming, args=(mssg, addr, connection_socket))
        threadStart.start()
    # f.close()
    connection_socket.close()


stream()
