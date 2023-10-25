"""
Lincoln Lyon
Project 2
Pygame: Galaga Recreation (sort of)

9/22/23
CSSE, Guillaume, Tri 1, Per 1
"""

import pygame
import time
import random

#initiates pygame backround programs and sets up all variables
pygame.init()
screen = pygame.display.set_mode((350,450))
Scolor = (3, 3, 3)
Pcolor = (24, 150, 5)
lWall = False
rWall = False
uWall = False
dWall = False
timeS = 0
timeE = 0
score = 0
timeAS = 0
speed = 1

allMissiles = []
allAsteroids = []



#defines the player size and starting position
player = pygame.Rect((155,350,40,50))
Pos = [155,350]
print("Click the screen and then you can use wasd to move.")
print("Press P to shoot and try to destroy the asteroids before they hit you or your home planet.")
print("If the screen is bugged stop and re-run the code.")

#Creates an asteriod
class Asteroid:
    def __init__(self,pos):
        self.rect = pygame.Rect((pos,0,25,25))
        
    #checks if the asteroid has hit the bottom of the screen or the player.
    def bScreen(stuff):
        return (stuff.rect.y >= 450)
        
    def hitP(stuff):
        return (stuff.rect.colliderect(player))
        
    #Allows the asteroid position to be updateable on the screen
    def redraw(self):
        pygame.draw.rect(screen,(166, 164, 164),self.rect)



#Creates a projectile from the player
class Missile:
    def __init__(self,Xpos,Ypos):
        self.rect = pygame.Rect((Xpos+15,Ypos,10,10))
        self.redraw()
        
    #Checks if this Missile has reached the top of the screen or hit an asteroid.
    def tScreen(stuff):
        return (stuff.rect.y <= 0)
    def hitA(stuff):
        return (stuff.rect.collidelist(allAsteroids))
        
    #Allows the missile position to be updateable on screen
    def redraw(self):
        pygame.draw.rect(screen,(224, 203, 61),self.rect)

#Creates a Lose Game screen if you lose that shows the score.
def LoseGame(score):
    global running
    global pygame
    global screen
    allMissiles.clear()
    allAsteroids.clear()
    screen.fill((0,0,0))
    pygame.font.init()
    end_screen_text = pygame.font.SysFont("Comic Sans MS", 30)
    end_screen = end_screen_text.render("You Lose, your final score is " + str(score) + ".", False, (255,255,255))
    screen.blit(end_screen, (20,225))
    running = False
    pygame.display.update()
    x = True
    while x:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                x = False

#Creates a Win screen if you win.
def WinGame():
    global running
    global pygame
    global screen
    allMissiles.clear()
    allAsteroids.clear()
    screen.fill((0,0,0))
    pygame.font.init()
    end_screen_text = pygame.font.SysFont("Comic Sans MS", 30)
    end_screen = end_screen_text.render("Congradulations you Win.", False, (255,255,255))
    screen.blit(end_screen, (0,225))
    running = False
    pygame.display.update()
    x = True
    while x:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                x = False
    

# Loop over allMissiles, update their positions. (done)
# check for collisions on each (done)
# destroy missile if necessary (done)
# destroy asteriod if necessary (done)
# set up when you lose the game (done)
def updateP():
    x = len(allMissiles)
    for i in range(x):
        Mcurrent = allMissiles[i-1]
        Mcurrent.rect.move_ip(0,-3)
        whatHit = Mcurrent.hitA()
        if(Mcurrent.tScreen()):
            allMissiles.remove(Mcurrent)
        elif(whatHit >= 0):
            global score
            score += 1
            allAsteroids.remove(allAsteroids[whatHit])
            allMissiles.remove(Mcurrent)
    
    y = len(allAsteroids)
    for i in range(y):
        Acurrent = allAsteroids[i-1]
        Acurrent.rect.move_ip(0,1)
        if(Acurrent.bScreen()):
            allAsteroids.remove(Acurrent)
            LoseGame(score)
        elif(Acurrent.hitP()):
            LoseGame(score)
    
    #Waits a small amount of time between spawning asteroids
    global timeAS
    if(timeAS == 0):
        timeAS = time.time()
    if(time.time() >= timeAS+1.25):
        a = Asteroid(random.randrange(50,300))
        allAsteroids.append(a)
        timeAS = 0
    
    #If you get 50 you win
    if(score >= 50):
        WinGame()


#Gives the player a second to get ready to start
time.sleep(1)
running = True
while running:
    
    #updates the entity positions on the screen
    screen.fill(Scolor)
    pygame.draw.rect(screen,(24, 150, 5),player)
    x = len(allMissiles)
    y = len(allAsteroids)
    for i in range(x):
        allMissiles[i-1].redraw()
    for i in range(y):
        allAsteroids[i-1].redraw()
    
    
    key = pygame.key.get_pressed()
    
    #Changes the speed and difficulty when you get farther through the game.
    if(score <= 19):
        speed = 1
    elif(score == 20):
        speed = 2
    elif(score == 40):
        speed = 3
    elif(score == 45):
        speed == 4
    
    if(speed == 1):
        time.sleep(0.0035)
    elif(speed == 2):
        time.sleep(0.0025)
    elif(speed == 3):
        time.sleep(0.001)
    elif(speed == 4):
        time.sleep(0.00075)
    
    #When a button is pressed if it is one that I have defined it moves the player.
    if(key[pygame.K_w] and uWall == False):
        player.move_ip(0,-1)
        Pos[1] = Pos[1]-1
    if(key[pygame.K_a] and lWall == False):
        player.move_ip(-1,0)
        Pos[0] = Pos[0]-1
    if(key[pygame.K_s] and dWall == False):
        player.move_ip(0,1)
        Pos[1] = Pos[1]+1
    if(key[pygame.K_d] and rWall == False):
        player.move_ip(1,0)
        Pos[0] = Pos[0]+1
    #Spawns a missile
    if(key[pygame.K_p] and time.time() >= timeS + 0.375):
        timeS = time.time()
        m = Missile(Pos[0],Pos[1])
        allMissiles.append(m)
    
    
        
    #Checks to see if the player is touching a wall
    if(Pos[0] <= 0):
        lWall = True
    else:
        lWall = False
    if(Pos[0] >= 310):
        rWall = True
    else:
        rWall = False
    if(Pos[1] <= 0):
        uWall = True
    else:
        uWall = False
    if(Pos[1] >= 400):
        dWall = True
    else:
        dWall = False
    
    #Updates the projectiles
    updateP()
    
    
    #Quits the program if trying to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Lets the window and backround programs load before running the code in the loop again.
    pygame.display.flip()
    pygame.display.update()
pygame.quit()