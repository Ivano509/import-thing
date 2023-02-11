from pygame import *
from time import time as timer
from random import randint
font.init()
mixer.init()
clock = time.Clock()
font1 = font.Font(None, 80)
font2 =font.Font(None,35)
rel_time =False
lost = 0
goal=50
num_fire = 0
win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption('SpaceFight')
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
background = transform.scale(image.load('galaxy.jpg'),(win_width,win_height))
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound =mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))







class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.x = randint(100,win_width-100)
            self.rect.y = 0
            lost = lost+1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 :
            self.kill()


bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()
for m in range (1,6):
    monster = Enemy('ufo.png',randint(100,win_width-100),-35,80,50,randint(1,6))    
    monsters.add(monster)



score = 0
finish = False
run = True
player = Player('rocket.png', 5, win_height - 100, 80, 100,10)
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key==K_SPACE:
                if num_fire <5 and rel_time == False:
                    num_fire +=1
                    fire_sound.play()
                    player.fire()
                if num_fire >=5 and rel_time == False:
                    last_time = timer()
                    rel_time =True
                    

                    
                

                
    if not finish:
        if rel_time == True:
            now_time = timer()
            if now_time - last_time <3:
                reload = font2.render('Wait,reload',1,(230,0,0))
                window.blit(reload,(360,460))
            else:
                num_fire = 0
                rel_time =False
        collides = sprite.groupcollide(monsters, bullets, True, True)
        if sprite.spritecollide(player,asteroids,False) or lost >= 5 :
            finish = True
            window.blit(lose, (200, 200))
        for c in collides:
           score = score + 1
           monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
        if sprite.spritecollide(player,monsters,False) or lost >= 5 :
            finish = True
            window.blit(lose, (200, 200))
        if score >= goal:
           finish = True
           window.blit(win, (200, 200))
        if sprite.groupcollide(monsters,bullets,True,True):
            pass
        
            

        window.blit(background,(0, 0))
        text = font2.render('Счет'+ str(score),1,(255,255,255))
        text_lose = font2.render('Пропущено'+ str(lost),1,(255,255,255))
        window.blit(text,(10,20))
        window.blit(text_lose,(10,50))
        bullets.update()
        bullets.draw(window)
        monsters.update()
        asteroids.update()
        asteroids.draw(window)
        monsters.draw(window)
        player.update()
        player.reset()  
        display.update()
    else:
       finish = False
       score = 0
       lost = 0
       for b in bullets:
           b.kill()
       for m in monsters:
           m.kill()


       time.delay(3000)
       for i in range(1, 6):
           monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
       for i in range(1, 6):
           asteroid = Enemy('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           asteroids.add(asteroid)
    if finish == True:
        window.blit(win,(30,40))
    time.delay(50)



