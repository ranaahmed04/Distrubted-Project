import random
from time import sleep
import socket

import threading
import time
import pygame
import redis
#import my_database


host = '192.168.1.104'
port = 42008

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((host,port))
lock = threading.Lock()
GlobalMessage = ''
IsChange = "No Change"
myPosition = 800 * 0.45
players =['','','','','','']
myPlayerNumber = 0
gameDisplay = None
clock = None
#***************************** Recieve Thread *************************************
def clientRecieve():
    global PlayerTitle
    global myPosition 
    global Guests
    global IsChange
    global GlobalMessage
    global dict
    global myPlayerNumber
    global players
    global clock
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            playerNum = message[:-1]
            go = message[8:10]

            #player1
            #player2
            #..etc
            if playerNum == "player":
                with lock:
                    PlayerTitle = message
                    myPlayerNumber = int(PlayerTitle[-1])
                    if myPlayerNumber > 1:
                        for i in range(myPlayerNumber-1):
                            p = Player(name=f"player{i+1}",car_img=pygame.image.load(f'./img/car{i+1}.png'),x_pos=800*0.45,y_pos=600*0.8)
                            players[i]=p

                    print("You are --> "+ PlayerTitle)

            elif message == "Check":
                client.send('Ack'.encode('utf-8'))

            #New player1 has connected to the game
            elif message[0:3] == "New":
                with lock:
                    #message[4:11] == player1
                    Guests = message[12:]
                    print("Guestes ++ : "+ Guests)
                    p = Player(name=f"player{len(eval(Guests))}",car_img=pygame.image.load(f'./img/car{len(eval(Guests))}.png'),x_pos=800*0.45,y_pos=600*0.8)
                    players[len(eval(Guests))-1]=p
                    print(players)
                    time.sleep(0.01)
                    #create object and append in array of objects

            elif message[0:6] == "Update":
                with lock:
                    Guests = message[7:]
                    print(Guests)
                    time.sleep(0.01)
            elif message[0:8] == "Gameover":
                for i in range(len(eval(Guests))):
                    if (players[i].name == message[-7:]) and (players[i].name != PlayerTitle):
                        print(f"{message[-7:]} is defeated")
                        with lock:
                            font = pygame.font.SysFont("lucidaconsole", 14)
                            text = font.render(f"{message[-7:]} is defeated", True, (255,255,255))
                            gameDisplay.blit(text, (600, 420)) 
                            pygame.display.update()
                            clock.tick(60)
                            sleep(1)
                            players[i].X_Position = 800*0.45



                        

            #player1 Go Left
            #player1 Go Right
            elif go == "Go":
                print(message)
                if PlayerTitle != message[0:7]:
                    with lock:
                        #get player name and change the x coordinates of this player
                        n = message[6:7]
                        n = int(n)
                        GlobalMessage = message
                        IsChange = "Change"
                        if message[11:12] == 'L':
                            players[n-1].X_Position -= 50
                        elif message[11:12] == 'R':
                            players[n-1].X_Position += 50

            else:
                print(message)
                
        except Exception as e:
            print('Error From Client Recieve ! : ' + e)
            client.close()
            break
#***************************** End - Recieve Thread *************************************
'''''
def sendChat():
    while True:
        try:
            m_chat = f'chat ---- {PlayerTitle}: {input("")}'
            client.send(f'{m_chat}'.encode('utf-8'))
        except Exception as e:
            print(f"Excpetion happen from Sender Chat {e} " + PlayerTitle )
            break
'''''

class Player:
    def __init__(self, name, car_img, x_pos, y_pos):
        self.name = name
        self.car_img = car_img
        self.X_Position = x_pos
        self.Y_Position = y_pos
        self.crashed = False

#playerName = client.recv(1024).decode('utf-8')
class CarRacing(threading.Thread):
    global Guests
    global PlayerTitle
    global myPlayerNumber
    global gameDisplay
    global players

    def __init__(self):
        global clock
        threading.Thread.__init__(self)
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        clock = pygame.time.Clock()
        self.gameDisplay = None

        self.initialize()

    def initialize(self):

        # enemy_car
        #self.enemy_car = pygame.image.load('./img/enemy_car_1.png')
        #self.enemy_car_startx = random.randrange(310, 450)
        #self.enemy_car_starty = -600
        #self.enemy_car_speed = 5
        #self.enemy_car_width = 49
        #self.enemy_car_height = 100
        #my_database.StoreDatabase(PlayerTitle,self.carImg,self.car_x_coordinate,self.crashed)
        
        p = Player(name=PlayerTitle,car_img=pygame.image.load(f'./img/car{myPlayerNumber}.png'),x_pos=800*0.45,y_pos=600*0.8)
        players[myPlayerNumber-1]=p
        # Background
        self.bgImg = pygame.image.load("./img/back_ground.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0

    def car(self,x,y):
        time.sleep(0.01)
        for i in range(len(eval(Guests))):
         #   dataset = my_database.Getdatabase(f"player{i+1}")
          #  print(dataset)
           # self.gameDisplay.blit(dataset[0], (dataset[1], 600*0.8))
            gameDisplay.blit(players[i].car_img, (players[i].X_Position,y))

    def racing_window(self):
        global gameDisplay
        global myPosition
        gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        with lock:
            myPosition = 800 * 0.45
        client.send(f"StartAgain-['{PlayerTitle}','{myPosition}','{players[myPlayerNumber-1].car_img}']".encode('utf-8'))
        pygame.display.set_caption('Car Dodge')
        self.run_car()

    def run_car(self):
        global IsChange
        global gameDisplay
        global clock
        '''''
        time.sleep(3)
        thread_chat = threading.Thread(target=sendChat)
        thread_chat.start()
        '''''

        # lama a5osh b player 3 lazm y3ml object l player 1 w player 2 beltrteb
        # 3shan y3mlhom append beltrteb
        # must change this while to be generic for my car and all other cars
        # implement function for restarting after gameover
        while not players[myPlayerNumber-1].crashed:
            
            #with lock:
             #   if IsChange == "Change":    
              #      players[myPlayerNumber-1].X_Position = myPosition
               #     IsChange = "No Change" 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    players[myPlayerNumber-1].crashed = True
                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_LEFT):
                        with lock:
                            players[myPlayerNumber-1].X_Position -= 50
                            client.send((f'{PlayerTitle} Go Left{players[myPlayerNumber-1].X_Position}').encode('utf-8'))
                        print ("CAR X COORDINATES: %s" % players[myPlayerNumber-1].X_Position)
                    if (event.key == pygame.K_RIGHT):
                        with lock:
                            players[myPlayerNumber-1].X_Position += 50
                            client.send(f'{PlayerTitle} Go Right{players[myPlayerNumber-1].X_Position}'.encode('utf-8'))
                        print ("CAR X COORDINATES: %s" % players[myPlayerNumber-1].X_Position)
                    print ("x: {x}, y: {y}".format(x=players[myPlayerNumber-1].X_Position, y=players[myPlayerNumber-1].Y_Position))

            gameDisplay.fill(self.black)
            self.back_ground_raod()
            '''
            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.enemy_car_starty += self.enemy_car_speed
            
            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.randrange(310, 450)
            '''
            self.car(players[myPlayerNumber-1].X_Position,players[myPlayerNumber-1].Y_Position)
            self.highscore(self.count)
            self.count += 1
            '''''
            if (self.count % 100 == 0):
                self.enemy_car_speed += 1
                self.bg_speed = 1
            
            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.car_x_coordinate > self.enemy_car_startx and self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width or self.car_x_coordinate + self.car_width > self.enemy_car_startx and self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = True
                    self.display_message("Game Over !!!")
            '''''
            if players[myPlayerNumber-1].X_Position < 310 or players[myPlayerNumber-1].X_Position > 460:
                players[myPlayerNumber-1].crashed = True
                client.send(f'Gameover-{PlayerTitle}'.encode('utf-8'))
                self.display_message("Game Over !!!")

            pygame.display.update()
            with lock:
                clock.tick(60)

    def display_message(self, msg):
        
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, (255, 255, 255))
        gameDisplay.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        self.display_credit()
        pygame.display.update()
        with lock:
            clock.tick(60)
        sleep(1)
        car_racing.initialize()
        car_racing.racing_window()

    def back_ground_raod(self):
        gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def highscore(self, count):
        font = pygame.font.SysFont("arial", 20)
        text = font.render("Score : " + str(count), True, self.white)
        gameDisplay.blit(text, (0, 0))

    def display_credit(self):
        font = pygame.font.SysFont("lucidaconsole", 14)
        text = font.render("Thanks for playing!", True, self.white)
        gameDisplay.blit(text, (600, 520))

if __name__ == '__main__':

    thread = threading.Thread(target=clientRecieve)
    thread.start()
    time.sleep(1)
    car_racing = CarRacing()
    car_racing.start()

    #root = tk.Tk()
    #chatroom = ChatRoom(root)
    #chatroom.start()
    car_racing.racing_window()
    print("from main i'm here - - - - - - - - - - - -  * * * * * * *")
    #root.mainloop()





    
    



