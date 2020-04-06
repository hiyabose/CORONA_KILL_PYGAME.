import pygame
import random
import math
from pygame import mixer


#initialise the pygame
pygame.init()

#creating a screen
screen = pygame.display.set_mode((800, 600))

#adding a background
bg = pygame.image.load('city.jpg')

#background sound
mixer.music.load('background.wav')
mixer.music.play(-1)  #-1 is used to play music continously

#title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space.png')
pygame.display.set_icon(icon)

#player
playerimg = pygame.image.load('003-cracker.png')
playerX = 370
playerY = 480
pXchange = 0


#enemy
enemyimg = []
enemyX = []
enemyY = []
eXchange = []
eYchange = []
no_of_enm = 6

for i in range (no_of_enm):
    enemyimg.append( pygame.image.load('006-coronavirus.png'))
    #to create enemy in random places
    enemyX.append(random.randint (0,736))
    enemyY.append(random.randint (50,150))
    eXchange.append(2)
    eYchange.append(40)


#bullet
bulletimg = pygame.image.load('001-fire.png')
bulletX = 0
bulletY = 480
bXchange = 0
bYchange = 10
bulletstate ="ready"

#score
score =0
font = pygame.font.Font('freesansbold.ttf',33)

textX =10
textY = 10

#game over
over = pygame.font.Font('freesansbold.ttf',64)

def showscore(x,y):
    sc = font.render("Score :" + str(score),True,(0,0,0))
    screen.blit(sc, (x,y))


def game_over(x,y):
    ov= over.render("GAME OVER!",True,(0,0,0))
    screen.blit(ov, (200,250))
    
def player(x,y):
    screen.blit(playerimg, (x,y))   #it is used to draw image on the screen
    

def enemy(x,y,i):
    screen.blit(enemyimg[i], (x,y))   #it is used to draw image on the screen
    
def fire_bullet(x,y):
    global bulletstate
    bulletstate = "fire"
    screen.blit(bulletimg,(x+16,y+10))
    


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY - bulletY,2))
    if distance < 27:
        return True
    else:
        return False
#Game loop
running = True
while running:
    #screen color
    screen.fill((0,0,0))
    #background
    screen.blit(bg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            

        #if keystroke is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pXchange= -5
            if event.key ==pygame.K_RIGHT:
                pXchange = 5
            if event.key ==pygame.K_SPACE:
                if bulletstate is "ready":
                    s= mixer.Sound('laser.wav')
                    s.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key ==pygame.K_RIGHT:
                pXchange = 0
            
    
    #to call the player
    playerX += pXchange

    #setting boundaries
    if playerX <=0:
        playerX = 0
    elif playerX >= 736:
        playerX =736

    #setting boundary for enemy
    for i in range (no_of_enm):

        #game over
        if enemyY[i] > 440 :
            for j in range(no_of_enm):
                enemyY[j] = 3000

                
            game_over(200,250)
            break

            
        enemyX[i] += eXchange[i]
        if enemyX[i] <= 0:
            eXchange[i] = 2
            enemyY[i] += eYchange[i]
        elif enemyX[i] >= 736:
            eXchange[i] = -2
            enemyY[i] += eYchange[i]
        #collision
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)    
        if collision:
            c= mixer.Sound('explosion.wav')
            c.play()
            bulletY = 480
            bulletstate = "ready"
            score +=50
            #print(score)
            enemyX[i] = random.randint (0,736)
            enemyY[i] = random.randint (50,150)

            
        enemy(enemyX[i], enemyY[i],i)    

    #BULLET MOVEMENT
    if bulletY <= 0:
        bulletY = 480
        bulletstate = "ready"
        
    if bulletstate is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bYchange

   

        
    player(playerX, playerY)
    showscore(textX, textY)
   
    pygame.display.update()
    

