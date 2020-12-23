import pygame

pygame.init()
win=pygame.display.set_mode((1000,600))
pygame.display.set_caption("Mannu's games")

walkLeft=[pygame.image.load('L1.png'),pygame.image.load('L2.png'),pygame.image.load('L3.png'),pygame.image.load('L4.png'),pygame.image.load('L5.png'),pygame.image.load('L6.png'),pygame.image.load('L7.png'),pygame.image.load('L8.png'),pygame.image.load('L9.png'),]
walkRight=[pygame.image.load('R1.png'),pygame.image.load('R2.png'),pygame.image.load('R3.png'),pygame.image.load('R4.png'),pygame.image.load('R5.png'),pygame.image.load('R6.png'),pygame.image.load('R7.png'),pygame.image.load('R8.png'),pygame.image.load('R9.png'),]
bg=pygame.image.load('back.png')
stand=pygame.image.load('standing.png')

#initialize

clock=pygame.time.Clock()
bulletsound=pygame.mixer.Sound('bullet.wav')
music=pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

x=800
y=500
width=64
height=64
vel=10
isJump=False
jumpCount=10
left=False
right=False
walkCount=0
standing=True
score=0

hitbox=(x+10,y+8,40,55)
def draw(win):
    global walkCount;global hitbox
    if walkCount + 1 >= 27:
        walkCount=0
    if not standing:
        if left:
            win.blit(walkLeft[walkCount//3],(x,y))
            walkCount+=1
        elif right:
            win.blit(walkRight[walkCount//3],(x,y))
            walkCount+=1
    else:
       if right:
           win.blit(walkRight[0],(x,y))
       else:
           win.blit(walkLeft[0], (x, y))
    hitbox = (x+10,y+8,40,60)
    #pygame.draw.rect(win,(255,0,0),hitbox,2)

def hit():
    global walkCount;global isJump;global jumpCount;global x;global y
    isJump=False
    jumpCount=10
    x=100
    y=500
    walkCount=0
    font3=pygame.font.SysFont('arial',50,True)
    text=font3.render('-5',1,(255,0,0))
    win.blit(text,(250-(text.get_width()/2),200))
    pygame.display.update()
    i=0
    while i<300:
        pygame.time.delay(10)
        i+=1
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                i=301
                pygame.quit()


class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel=8*facing
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)


def reDrawWindow():
    win.blit(bg,(0,0))
    draw(win)
    text=font1.render("Score: "+str(score),1,(0,0,0))
    win.blit(text,(40,40))
    text2 = font2.render("Created by: Mannu", 1, (255, 0, 0))
    win.blit(text2, (750, 40))

    enemy.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


class enemies(object):
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),pygame.image.load('L10E.png'), pygame.image.load('L11E.png'), ]
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),pygame.image.load('R10E.png'), pygame.image.load('R11E.png'), ]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.health=10
        self.visible=True
        self.hitbox = (self.x + 10, self.y + 2, 45, 60)

    def draw(self,win):
        self.moves()
        if self.visible:
            if self.walkCount+1>=33:
                self.walkCount=0
            if self.vel>0:
                win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            pygame.draw.rect(win,(255,0,0),(self.hitbox[0],self.hitbox[1]-20,50,10))
            pygame.draw.rect(win, (0,128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50-(5*(10-self.health)), 10))
            self.hitbox = (self.x + 10, self.y + 2, 45, 60)
           # pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def moves(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1

    def hit(self):
        if self.health>0:
            self.health-=1
        else:
            self.visible=False
        print('hit')


#mainloop
font1=pygame.font.SysFont('arial',40,True)
font2=pygame.font.SysFont('arial',30,True)

enemy=enemies(20,505,64,64,900)
run=True
bullets=[]
shootloop=0
while run:
    clock.tick(27)

    if enemy.visible==True:
        if hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and hitbox[1] + hitbox[3] > enemy.hitbox[1]:
            if  hitbox[0]+ hitbox[2] > enemy.hitbox[0] and hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
                hit()
                score -= 5

    if shootloop>0:
        shootloop+=1
    if shootloop>3:
        shootloop=0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:  #quit the screen
            run=False

    for bullet in bullets:
        if enemy.visible == True:
            if bullet.y- bullet.radius<enemy.hitbox[1]+enemy.hitbox[3] and bullet.y+bullet.radius>enemy.hitbox[1]:
                if bullet.x+bullet.radius>enemy.hitbox[0] and bullet.x-bullet.radius<enemy.hitbox[0]+enemy.hitbox[2]:
                    hitsound = pygame.mixer.music.load('hit.mp3')
                    pygame.mixer.music.play()
                    enemy.hit()
                    score+=1
                    bullets.pop(bullets.index(bullet))

        if bullet.x <1000 and bullet.x>0:
            bullet.x+=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys=pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootloop==0:
        bulletsound.play()
        if left:
            facing=-1
        else:
            facing=1

        if len(bullets)<5 :
            bullets.append(projectile(round(x+width//2),round(y+height//2),7,(0,0,0),facing))
        shootloop=1


    if keys[pygame.K_LEFT] and x>=0+40:    #after and we use the condition that is for boundary
        x-=vel
        left=True
        right=False
        standing=False
    elif keys[pygame.K_RIGHT] and x<=1000-width:
        x+=vel
        left=False
        right=True
        standing=False
    else:
        standing=True
        walkCount=0
    if not(isJump):
        if keys[pygame.K_UP]:
            isJump=True
            left = False
            right = False
            walkCount = 0
    else:
        if jumpCount>=-10:
            neg=1
            if jumpCount<0:
                neg=-1
            y-=(jumpCount**2)*0.5*neg
            jumpCount-=1
        else:
            isJump=False
            jumpCount=10
    reDrawWindow()

pygame.quit()