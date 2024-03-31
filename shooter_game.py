from pygame import *
from random import randint
from time import time as timer
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
lost = 0
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if (keys[K_LEFT] or keys[K_a]) and self.rect.x>5:
            self.rect.x -= self.speed
        if (keys[K_RIGHT] or keys[K_d]) and self.rect.x< win_width-80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx,self.rect.top,15,20,-10)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            self.speed = randint(1,5)
            lost+=1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()


font.init()
fon = font.Font(None,36)
img_bullet = "buletss.png"
img_bg = 'cosmos.jpg'
img_player = 'roccket.png'
img_enemy = 'nllo.png'

win_width = 700
win_height = 500
ship = Player(img_player,5,win_height-100,80,100,10)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy,randint(80,win_width - 80),
                    -40,80,50,randint(1,3))
    monsters.add(monster)
display.set_caption('Shooter')
window = display.set_mode((win_width,win_height))
bg = transform.scale(image.load(img_bg),(win_width,win_height))
timers = time.Clock()
game = True
finish = False
score = 0
num_fire = 0
rel_fire = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <5 and rel_fire == False:
                    num_fire +=1
                    fire_sound.play()
                    ship.fire()
                if num_fire >=5 and rel_fire == False:
                    last_time = timer()
                    rel_fire = True
    if not finish:
        window.blit(bg,(0,0))
        if rel_fire == True:
            now_time = timer()
            if now_time - last_time <1:
                window.blit(fon.render("reload...", True,(255,255,255)),(325,325))
            else:
                num_fire = 0
                rel_fire = False

        text = fon.render('Рахунок ' + str(score),1,(255,255,255))
        window.blit(text,(10,20))
        text_lose = fon.render('Пропущено ' + str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))
        ship.update()
        monsters.update()
        bullets.update()
        monsters.draw(window)
        bullets.draw(window)
        ship.reset()
        colides = sprite.groupcollide(monsters, bullets, True,True)
        for c in colides:
            score += 1
            monster = Enemy(img_enemy,randint(80,win_width - 80),
                    -40,80,50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship,monsters, False) or lost >= 11:
            finish = True
            window.blit(fon.render("LOSE",True,(255,255,255)),(200,200))
        if score >= 16:
            finish= True
            window.blit(fon.render("WIN",True,(180,0,0)),(200,200))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        for i in bullets:
            i.kill()
        for i in monsters:
            i.kill()
        time.delay(3000)
        for i in range(1,6):
            monster = Enemy(img_enemy,randint(80,win_width - 80),
                    -40,80,50,randint(1,5))
            monsters.add(monster)    
    timers.tick(60)