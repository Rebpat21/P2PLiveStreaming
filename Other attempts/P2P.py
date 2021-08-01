from socket import *
import os
import time
import sys
import threading as thread


server_socket = socket(AF_INET, SOCK_STREAM)
server_port = int(sys.argv[1])
server_socket.bind(("", server_port))
server_socket.listen(5)

bit = ""

def byte(bufferByte):
    global bit
    print("Sending: "+bufferByte)
    bufferByte = bit
    
def isRouting(addr, mssg, connection_socket):
    global bit
    while True:
        time.sleep(1)
        try:
            connection_socket.send(bit)
        except:
            print(str(addr)+" closed connection.")
            connection_socket.close()
            break

def routing():
    print("Beginning Routing...")

    while True:
        connection_socket, addr = server_socket.accept()
        mssg = connection_socket.recv(2048).decode()

        threadStart = thread.Thread(target=isRouting, args=(addr, mssg, connection_socket))
        threadStart.start()

routing()