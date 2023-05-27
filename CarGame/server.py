import threading
import socket
import time
host = '192.168.1.108'
port = 59050

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((host,port)) #must have 1 argument
server.listen()



clients =[]
aliases =[]

#send a boradcast message
def broadcast(message):
    for client in clients:
        client.send(message)
def broadcast_ExceptSender(message,index_ToSkip):
    for i,client in clients:
        if i == index_ToSkip:
            pass
        else:
            client.send(message)

def handleClient(client):
    while True:
        try:
            message = client.recv(1024)#max number need to be recv
            if message[8:10] == "Go":
                broadcast_ExceptSender(message,int(message[6:7])-1)
            else:
                broadcast(message)
        except:
            clients.remove(client)
            client.close()
            break

#Main function to recv the clients connection
def recieve():
    PlayerName = []
    global index 
    index = 0
    while True:
        print('Server is running and listening . . . . <<------------------->> ')
        client , address = server.accept()
        print("Server is already conneted with someone - - -")
        PlayerName.append(f"player{index + 1}")
        print(f'connection is established with {str(address)}')
        clients.append(client)
        time.sleep(1)
        client.send(f'{PlayerName[index]}'.encode('utf-8'))
        time.sleep(0.001)
        broadcast(f'New {PlayerName[index]} has connected to the chat room'.encode('utf-8'))
        time.sleep(0.001)
        client.send('you are now connect to chat room'.encode('utf-8'))
        time.sleep(0.001)
        client.send('you are now connected!'.encode('utf-8'))
        index = index +1
        thread = threading.Thread(target=handleClient,args=(client,))
        thread.start()



if __name__ == "__main__":
    recieve()