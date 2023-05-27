import threading
import socket
import time
host = socket.gethostbyname(socket.gethostname())
print(host)
port = 59008
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(('192.168.1.108',port)) #must have 1 argument
server.listen()

clients =[]
aliases =[]

#send a boradcast message
def broadcast(message):
    for client in clients:
        client.send(message)

def handleClient(client):
    while True:
        try:
            message = client.recv(1024)#max number need to be recv
            broadcast(message)
        except:
            index = client.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break

#Main function to recv the clients connection
def recieve():
    while True:
        print('Server is running and listening . . . . ')
        client , address = server.accept() # - -- - - - -- - - - -  - - -
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        time.sleep(0.001)
        client.send('you are now connect to chat room'.encode('utf-8'))
        time.sleep(0.001)
        client.send('you are now connected!'.encode('utf-8'))
        time.sleep(0.001)
        thread = threading.Thread(target=handleClient,args=(client,))
        thread.start()

if __name__ == "__main__":
    recieve()