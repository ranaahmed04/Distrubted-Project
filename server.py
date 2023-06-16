import threading
import socket
import time
#import redis

host = '172.31.21.94'
port = 3008
#my_database = redis.Redis(host=host,port=port,db=0)


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((host,port)) #must have 1 argument
server.listen()

lock = threading.Lock()

clients=[] #ip address of each one

guests=[] #naming of each one .. player1, player2 .. etc



def check(): 
    for i,client in clients:
        client.send("Check".encode('utf-8'))
        time.sleep(0.0001)
        try:
            
            time.sleep(0.001)
            Re = client.recv(1024).decode('utf-8')
            if(Re == "Ack"):
                pass
            else:
                client.remove(client)
                guests.remove(f'player{i}')
                client.close()
                print(guests)
                broadcast(f'Update {guests}'.encode('utf-8'))               
        except:
            client.remove(client)
            guests.remove(f'player{i}')
            client.close()
            print(guests)
            broadcast(f'Update {guests}'.encode('utf-8')) 
def broadcast_ExceptSender(message,index_ToSkip):
    for i,client in clients:
        if i == index_ToSkip:
            pass
        else:
            client.send(message)
def broadcast(message):
    for client in clients:
        client.send(message)
def handleClient(client):
    while True:
        try:
            message = client.recv(1024)#max number need to be recv
            broadcast(message)
        except:
            clients.remove(client)
            client.close()
            break
#send a broadcast message

#Main function to recv the clients connection
def recieve():
    x = 360
    img = "image"
    PlayerName = []
    global index 
    index = 0
    while True:
        print('Server is running and listening . . . . <<------------------->> ')
        client , address = server.accept()

        PlayerName.append(f"player{index + 1}")

        time.sleep(0.4)
        #check()
        print(f'connection is established with {str(address)}')
        clients.append(client)
        time.sleep(0.4)
        
        client.send(f'{PlayerName[index]}'.encode('utf-8'))
        
        time.sleep(0.4)

        guests.append(PlayerName[index])
        print(guests)
        broadcast(f'New {PlayerName[index]} {guests}'.encode('utf-8'))
        time.sleep(0.7)
        client.send('you are now connected!'.encode('utf-8'))
        #my_database.set(f"player{index+1}",f"['{x}','{img}']")
        time.sleep(0.4)
        client.send('StartPlay'.encode('utf-8'))
        index = index +1
        time.sleep(0.4)
        thread = threading.Thread(target=handleClient,args=(client,))
        thread.start()



if __name__ == "__main__":
    recieve()