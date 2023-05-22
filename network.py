import socket 


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.4" 
        self.port = 5555
        self.addr = (self.server, self.port)
        self.POS = self.connect() # when i connect i want to return the start postion of each client to the others 
       

    def getPos(self):
        return self.POS

    def connect(self):
        try:
         self.client.connect(self.addr)
         return self.client.recv(2048).decode()
        

        except:
           pass 



    #
    def send(self, data):
      try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
      except socket.error as e:
           print(e)


           
