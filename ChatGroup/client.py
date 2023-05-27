import threading
import socket

host = '127.0.0.1'
print(host)
port = 59008


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('192.168.1.108',port))
alias = input('choose an alias >> ')


def clientRecieve():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break

def clientSend():
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode('utf-8'))
        
recieveThread = threading.Thread(target=clientRecieve)
recieveThread.start()

sendThread = threading.Thread(target=clientSend)
sendThread.start()