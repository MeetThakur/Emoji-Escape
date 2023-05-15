import pygame
import sys
from pygame.locals import *
import random as r
import time


#basic info
clock = pygame.time.Clock()
pygame.init()
gameState = 2
score = -6

#fonts
scorefont = pygame.font.Font("font/Pixeltype.ttf",50)
overfont = pygame.font.Font("font/Pixeltype.ttf",200)
endfont = pygame.font.Font("font/Pixeltype.ttf",50)

#Screen Dimensions
HEIGHT = 740
WIDTH = 1366


#Keyboard Keys Check
RightKey = False
LeftKey = False
UpKey = False
DownKey = False

#state images
startImg = pygame.image.load("images/start.png")
helpImg= pygame.image.load("images/help.jpg")
overImg = pygame.image.load("images/over.png")
pauseImg = pygame.image.load("images/pause.png")


#main window
screen = pygame.display.set_mode((WIDTH,HEIGHT),RESIZABLE)
pygame.display.set_caption("Emoji Mania")
bg = pygame.image.load("images/bg.jpg")

#score File
with open("high.txt","r") as ScoreFile:
    highscore = ScoreFile.read()
    



#player settings
playerHieght = 70
playerWidth = 70
playerX = 300
playerY = 300
playerSpeed = 8

class Player(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/chr.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(playerHieght,playerWidth))
        self.rect = self.image.get_rect(center = (playerX,playerY))
    def Movement(self):
        if RightKey and self.rect.right<=1366:
            self.rect.right += playerSpeed
        if LeftKey and self.rect.left>=0: 
            self.rect.left -= playerSpeed
        if UpKey and self.rect.top>=0:
            self.rect.top -= playerSpeed
        if DownKey and self.rect.bottom <=740:
            self.rect.bottom +=  playerSpeed
    def shield(self):
        if shieldUsed:
            self.image = pygame.image.load("images/chrShield.png").convert_alpha()
            self.image = pygame.transform.scale(self.image,(playerHieght,playerWidth))
        if not shieldUsed:
            self.image = pygame.image.load("images/chr.png").convert_alpha()
            self.image = pygame.transform.scale(self.image,(playerHieght,playerWidth))
    def update(self):
        self.Movement()
        self.shield()




#character defination
player = pygame.sprite.GroupSingle()
player.add(Player())











#enemy images
enemyimage1 = pygame.image.load("images/enemy1.png")
enemyimage2 = pygame.image.load("images/enemy2.png")
enemyimage3 = pygame.image.load("images/enemy3.png")

#Enemy Settings
EnemySpeed = 6
EnemyMaxSpeed = 10
EnemyColors = ["red","blue","green"]
enemyHeight = 120
enemyWidth = 150


class Enemy(pygame.sprite.Sprite):
    def __init__(self,color):
        super().__init__()
        if color == "red":          
            self.image = pygame.transform.scale(enemyimage1,(80,80)).convert_alpha()
        elif color == "green":
            self.image = pygame.transform.scale(enemyimage2,(80,80)).convert_alpha()
        elif color == "blue":
            self.image = pygame.transform.scale(enemyimage3,(80,80)).convert_alpha()
        self.rect = self.image.get_rect(center = (-111,500))
        self.EnemySpeed = 5
    def Movement(self):
        global score,Tscore,EnemySpeed,EnemyMaxSpeed
        if gameState == 1:
            if score>100:
                EnemyMaxSpeed = score//10
            if self.rect.left>=-100:
                self.rect.left -= self.EnemySpeed
            else:
                self.rect.right = 1400
                self.rect.top = r.randint(0,720)
                self.EnemySpeed = r.randint(5,EnemyMaxSpeed)
                score += 1
                tnum = 5
                Tscore = score
            while len(enemies.sprites()) < 6:
                enemies.add(Enemy(r.choice(EnemyColors)))
        elif gameState == 0 or gameState == 2:
            EnemyMaxSpeed = 20
            self.kill()
            while len(enemies.sprites()) < 6:
                enemies.add(Enemy(r.choice(EnemyColors)))
            score = -6


    def update(self):
        self.Movement()


#making Enemies
enemies = pygame.sprite.Group()
enemies.add(Enemy("red"))
enemies.add(Enemy("red"))
enemies.add(Enemy("blue"))
enemies.add(Enemy("blue"))
enemies.add(Enemy("green"))
enemies.add(Enemy("green"))












fire = False
knifePos = (100,100)
makeKnife = True

knifeSpeed = 20

class KnifePower(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/knife.png")
        self.image = pygame.transform.scale(self.image,(60,60))
        self.rect = self.image.get_rect(right = 0)
    def shoot(self):
        global fire,makeKnife,KnifeCount
        if fire == True and makeKnife == True and KnifeCount != 0:
            self.rect.center = knifePos
            fire = False
            makeKnife = False
            KnifeCount -= 1
        if self.rect.right != 0:
            self.rect.right += knifeSpeed
        if self.rect.left > 1370:
            self.kill()
            makeKnife = True
        if gameState == 0:
            self.kill()
            makeKnife = True
        if knifeGroup.sprite is not None:
            if pygame.sprite.spritecollide(knifeGroup.sprite,enemies,True):
                self.kill()
                enemies.add(Enemy(r.choice(EnemyColors)))
                makeKnife = True

    def update(self):
        self.shoot()


knifeGroup = pygame.sprite.GroupSingle()
knifeGroup.add(KnifePower())









KnifeCount = 2 #default Knife Count
ShieldCount = 1 #DEFAULT SHIELD COUNT
spawn = True #to check if if Powerup is Already Spawned or Not
shieldUsed = False #checks for user input
shieldActivated = False 
LivesCount = 0


class PowerUps(pygame.sprite.Sprite):
    def __init__(self,pwr):
        super().__init__()
        if pwr == "knife":
            self.power = "knife"
            self.image = pygame.image.load("images/knife.png")
            self.image = pygame.transform.scale(self.image,(50,50))
            self.rect = self.image.get_rect(right = -50)
        if pwr == "shield":
            self.power = "shield"
            self.image = pygame.image.load("images/shield.png")
            self.image = pygame.transform.scale(self.image,(50,50))
            self.rect = self.image.get_rect(right = -50)
        if pwr == "heart":
            self.power = "heart"
            self.image = pygame.image.load("images/heart.png")
            self.image = pygame.transform.scale(self.image,(50,50))
            self.rect = self.image.get_rect(right = -50)

    def spawn(self):
        global KnifeCount,ShieldCount,spawn,shieldUsed
        if score%20 == 0 and score>1 and spawn == True:
            self.rect.center = (r.randint(50,600),r.randint(50,600))
            spawn = False
        if gameState == 0 or gameState == 2:
            self.rect.right = 0
            spawn = True


    def ability(self):
        global KnifeCount,ShieldCount,spawn,shieldUsed,LivesCount
        if pygame.sprite.spritecollide(player.sprite,Powers,True):
            if self.power == "knife":
                KnifeCount += 1
                Powers.add(PowerUps(r.choice(pList)))
                spawn = True
                self.kill()
            if self.power == "shield":
                ShieldCount += 1
                Powers.add(PowerUps(r.choice(pList)))
                spawn = True
                self.kill()
            if self.power == "heart":
                LivesCount += 1
                Powers.add(PowerUps(r.choice(pList)))
                spawn = True
                self.kill()
        if shieldUsed == True:
            if score == shieldScore + 20:
                shieldUsed = False
                


    def update(self):
        self.spawn()
        self.ability()

pList = ["heart","shield","knife","knife","knife","knife","shield","heart","knife","shield"]
Powers = pygame.sprite.Group()
Powers.add(PowerUps(r.choice(pList)))



#collions between Player and Enemy
def collions():
    global LivesCount
    if pygame.sprite.spritecollide(player.sprite,enemies,False) and shieldUsed == False:
        if LivesCount > 0:
            LivesCount -= 1
            pygame.sprite.spritecollide(player.sprite,enemies,True)

            return 1
        else:
            return 0
    else: 
        return 1





knifeImg = pygame.image.load("images/knife.png").convert_alpha()
knifeImg = pygame.transform.scale(knifeImg,(35,35))
KnifeRect = knifeImg.get_rect(center = (60,35))

ShieldImg = pygame.image.load("images/shield.png").convert_alpha()
ShieldImg = pygame.transform.scale(ShieldImg,(35,35))
ShieldRect = ShieldImg.get_rect(center = (200,35))

HeartImg = pygame.image.load("images/heart.png").convert_alpha()
HeartImg = pygame.transform.scale(HeartImg,(35,35))
HeartRect = HeartImg.get_rect(center = (340,35))


#display During Game
def displayStats():
    global KnifeRect,ShieldRect,HeartRect
    scoreD = scorefont.render(f'Score: {score}',False,(0,0,0))
    scoreR = scoreD.get_rect(center = (650,50))

    Kcount = scorefont.render(f'x {KnifeCount}',False,(0,0,0))
    KcountRect = Kcount.get_rect(center = (100,40))

    Scount = scorefont.render(f'x {ShieldCount}',False,(0,0,0))
    ScountRect = Scount.get_rect(center = (240,40))
    
    Lcount = scorefont.render(f'x {LivesCount}',False,(0,0,0))
    LcountRect = Lcount.get_rect(center = (390,40))
    

    screen.blit(scoreD,scoreR)

    screen.blit(Kcount,KcountRect)
    screen.blit(knifeImg,KnifeRect)

    screen.blit(Scount,ScountRect)
    screen.blit(ShieldImg,ShieldRect)

    screen.blit(Lcount,LcountRect)
    screen.blit(HeartImg,HeartRect)
    screen.blit(scoreD,scoreR)

    return score



#Score After Dying
def endScore():
    scoreD = scorefont.render(f'Your Score: {Tscore}',False,(0,0,0))
    scoreR = scoreD.get_rect(center = (650,600))
    screen.blit(scoreD,scoreR)
    highscoreD = scorefont.render(f'High Score: {highscore}',False,(0,0,0))
    highscoreR = highscoreD.get_rect(center = (650,650))
    screen.blit(highscoreD,highscoreR)



#active window
def window():
    screen.blit(bg,(0,0))
    player.draw(screen)
    enemies.draw(screen)
    knifeGroup.draw(screen)
    Powers.draw(screen)
    score = displayStats()


#main Loop
while  True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    RightKey = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                RightKey = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                LeftKey = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                LeftKey = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                UpKey = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                UpKey = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                DownKey = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                DownKey = False



        if pygame.mouse.get_pressed()[0] and KnifeCount!= 0 and gameState == 1:
            knifePos = player.sprite.rect.center
            if len(knifeGroup.sprites()) == 0:
                knifeGroup.add(KnifePower())
            fire = True


        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and KnifeCount!= 0 and gameState == 1:
            knifePos = player.sprite.rect.center
            if len(knifeGroup.sprites()) == 0:
                knifeGroup.add(KnifePower())
            fire = True



        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT and ShieldCount !=0 and gameState == 1:
            shieldScore = score
            shieldUsed = True
            ShieldCount -= 1


        if pygame.mouse.get_pressed()[2] and ShieldCount != 0 and gameState == 1:
            shieldScore = score
            shieldUsed = True
            ShieldCount -= 1



        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and (gameState==0 or gameState ==2 or gameState==4):
            gameState = 1
            Tscore = 0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            gameState = 2

        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB and gameState == 2:
            gameState = 3

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and gameState == 1:
            gameState = 4


    if gameState ==1: #main game
        window()
        player.update()
        enemies.update()
        knifeGroup.update()
        Powers.update()
        gameState = collions()
        pygame.mouse.set_visible(False)




    elif gameState== 0:#game Over State
        with open("high.txt","w") as ScoreFile:
            if int(highscore) < Tscore:
                highscore = Tscore
            ScoreFile.write(str(highscore))
        enemies.draw(screen)
        screen.blit(overImg,(0,0))
        enemies.update()
        knifeGroup.update() 
        Powers.update()
        KnifeCount = 2
        ShieldCount = 1
        LivesCount = 0
        pygame.mouse.set_visible(True)
        endScore()

    elif gameState == 2: #main menu
        screen.blit(startImg,(0,0))
        pygame.mouse.set_visible(True)
        enemies.update()
        knifeGroup.update() 
        Powers.update()
        KnifeCount = 2
        ShieldCount = 1
        LivesCount = 0


    elif gameState== 3: #help
        screen.blit(helpImg,(0,0))
        pygame.mouse.set_visible(True)

    elif gameState ==4: #paused game
        screen.blit(pauseImg,(0,0))
        pygame.mouse.set_visible(True)

    #fps
    clock.tick(60)
    pygame.display.update()



