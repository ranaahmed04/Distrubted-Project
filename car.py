import pygame
import sys
pygame.init()

WIDTH,HEIGHT= 800,600
FBS=60

Window=pygame.display.set_mode((WIDTH,HEIGHT))
#to add caption 
pygame.display.set_caption("Car Racing Game")

#time module 

# to make game has the same spped on all computers regarding processor speed
#object to trace time 
clock1=pygame.time.Clock() 


#to load images 
Car1=pygame.image.load("images/car1.jpg")
GRASS =pygame.image.load("images/grass.jpg")
YELLOWSTRIP=pygame.image.load("images/yellow_strip.jpg")
STRIP=pygame.image.load("images/strip.jpg")


def background():
    Window.blit(GRASS,(0,0))
    Window.blit(GRASS,(700,0))
    Window.blit(YELLOWSTRIP,(400,0))
    Window.blit(YELLOWSTRIP,(400,100))
    Window.blit(YELLOWSTRIP,(400,200))
    Window.blit(YELLOWSTRIP,(400,300))
    Window.blit(YELLOWSTRIP,(400,400))
    Window.blit(YELLOWSTRIP,(400,500))
    Window.blit(YELLOWSTRIP,(400,600))
    Window.blit(STRIP,(120,0))
    Window.blit(STRIP,(680,0))

def car(x,y): 
    Window.blit(Car1,(x,y))


def game_loop():

    run = True
    car_width=56
    CarWidth,CarHeight=400,470 
    X_change = 0
    while run:
       
        for event in pygame.event.get():
            if event.type ==pygame.QUIT: # if we press quit button the widow close
             pygame.quit()
             run=False
             sys.exit()
        
        #to move in x-ycoordinate(logic for pressing key)
        if event.type==pygame.KEYDOWN: #while pressing any key
            if event.key==pygame.K_LEFT:
                X_change=-5
            if event.key==pygame.K_RIGHT:
                X_change=5
        #logic for removing key 
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    X_change=0

        CarWidth+=X_change


        #change backgrounf color to grey
        Window.fill((119,119,119))  
        background()
        #calling car function
        car(CarWidth,CarHeight)
        

         # to update what i draw to display on screen
        pygame.display.update() 
        clock1.tick(FBS)

game_loop()



