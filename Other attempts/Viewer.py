from socket import *
import os
import time
import sys
import threading as thread
# from P2P import *

print(sys.argv[1])
print(sys.argv[2])
print(sys.argv[3])
print(sys.argv[4])


server_name = sys.argv[1]
server_port = int(sys.argv[2])
passPort = int(sys.argv[3])
mssg = sys.argv[4]

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

client_socket.send(mssg.encode())

response = client_socket.recv(2048)
print(response.decode())

def passData(response):
    buffer = []
    i = 0
    client_socket.connect(('localhost', passPort))
    while(response):
        print("Sent:"+response.decode())
        buffer.append(response.decode())
        # print(len(buffer))
        if len(buffer) == 10:
            try:
                byte(buffer[i])
                buffer.pop(i)
                i += 1
            except:
                print("An error has occured.")
                exit()
            finally:
                print("Queue could not be passed.")
                buffer.pop(i)

        response = client_socket.recv(2048)


if response.decode() == "Ending":
    print("Stream Closed")
    exit()
elif response.decode() == "Reroute":
    response = client_socket.recv(2048)
    new_server_name = response.decode()
    response = client_socket.recv(2048)
    new_server_port = response.decode()
    client_socket.close()

    # client_socket = socket(AF_INET, SOCK_STREAM)
    # client_socket.connect((new_server_name, int(new_server_port)))

    # threadStart = thread.Thread(target=passData, args=(response, ))
    # threadStart.start()
    

print("Recieving Data...")


while(response):
    print(response.decode())
    response = client_socket.recv(2048)

client_socket.close() 
