import socket 
from _thread import *
import sys



server= "192.168.1.4" # ipv4 address of my network 
port = 5555 

srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: 
    srv_socket.bind((server, port))

except socket.error as e : 
    str(e)
# listen waiting for 2 players 

srv_socket.listen(2) 
print("waiting for connection, server starting...")

def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""

    # when connected to new connection
    while True:
        try:
            data = conn.recv(2048) # 2048 is amout of information you are going to recive 
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()


while True:
    conn, addr = srv_socket.accept() # store the connection(what is connected) and address
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))