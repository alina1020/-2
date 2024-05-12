from pygame import *
from random import randint
from time import time as timer

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Sooter')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))
mixer.init()
mixer.music.load('c44488ffb8db67a.mp3')
mixer.music.play()   
fire_sound = mixer.Sound('fire.ogg')
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)

lost = 0
scor = 0
life = 3
max_lost = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()              
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        global lost
        global scor
        if self.rect.y > win_width:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1
 
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    
 
display.set_caption('Шутер')
player = Player("rocket.png", 5, 420, 80, 100, 10)          
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png',randint(80,620) , -40, 80, 50, randint(1, 5))
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy('asteroid.png',randint(80,620) , -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)
bullets = sprite.Group()    


clock = time.Clock()
FPS = 60
finish = False
game = True
rel_time = False
num_fire = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True       
    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False    
        collides = sprites_list = sprite.groupcollide(monsters, bullets, True, True)        
        for i in collides:
            scor = scor + 1
            monster = Enemy('ufo.png',randint(80,620) , -40, 80, 50, randint(1, 5))   
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life = life - 1
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
        if scor >= 10:
            finish = False
            window.blit(win, (200, 200))   
        text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text_scor = font2.render('Счёт:' + str(scor), 1, (255, 255, 255))     
        window.blit(text_scor, (10, 20))
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0) 
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life,  (650, 10))            
    display.update()
    clock.tick(FPS)     