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


# function to convert the postion to int and return it as tuples 
def read_pos(str):
        str = str.split(",")
        return int(str[0]), int(str[1])
    
# convert the postion to string 
def make_pos(tup):
        return str(tup[0]) + ", " + str(tup[1])

# hold position of players 
pos = [(0,0),(100,100)]

def threaded_client(conn,player):
    # send id when we are connected 
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""

    # when connected to new connection
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())# 2048 is amout of information you are going to recive 
            pos[player] = data 
            

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: ", reply)
                print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()


currentplayer =0 

while True:
    conn, addr = srv_socket.accept() # store the connection(what is connected) and address
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,currentplayer))
    currentplayer+=1