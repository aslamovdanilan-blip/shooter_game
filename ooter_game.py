#Создай собственный Шутер!

from pygame import *
from random import *


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image  = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()    

        if keys[K_LEFT] and self.rect.x >5:
            self.rect.x -=self.speed
        if keys[K_RIGHT]and self.rect.x < win_width - 80  :
            self.rect.x += self.speed

    def fire(self):#при нажатии на пробел б создаём обьекти добавляем его в список(у обьекта при этом своя логика из-за класса)
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top,15, 20, -15)#создаём обькт пули
        bullets.add(bullet)#добавляемсозданный обьект в список спрайтов

class Enemy (GameSprite):
    def update(self):
        self.rect.y+= self.speed
        global lose
        if self.rect.y > win_height:
            self.rect.x  =randint (80, win_width - 80)
            self.rect.y = 0
            lose =lose +1



#класс спрайта - пули
class Bullet(GameSprite):#наследуемся от класса GameSprite, чтобы получить все команды родителя
    #движение врага
    def update(self):#функция которую мы пишем, чтобы задать движение
        self.rect.y += self.speed# меняем у координаты чтобы двигаться вверх
        #исчизает если дайдёт до края
        if self.rect.y < 0:#и если пересикаем 0 координату по у то после кдаляем пулю чтобы не засарять память
            self.kill()#команда удаления
    
        



mixer.init()    
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

font.init()
font1= font.Font(None, 36 )
win = font1.render('YOU WIN!!!!!!!!!!!!!', True, (225,225,225))
loset= font1.render('YOU LOSE!!!!!!!!!!!', True, (180, 0, 0))
font2 =font.Font(None, 36)

goal = 10  
lose = 0
score = 0 
max_lose = 3

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = "ufo.png"
img_bullet = 'bullet.png'




win_height = 700
win_width = 500


display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))                   

ship =Player(img_hero,5, win_height - 100, 80, 100, 10)

monsters =sprite.Group()
for i in range(1,6):
    monster =Enemy (img_enemy, randint(80,win_width- 80), -40, 80,50, randint(1, 5))
    monsters.add(monster)

bullets = sprite.Group()# списак на основе класса Sprite

finish = False

game = True

while game:
    for e in event.get():
        if e.type ==QUIT:
            game = False
        #событие нажатия на пробел 
        elif e.type == KEYDOWN:#если мы нажимаем на кнопку  на клавиатуре
            if e.key == K_SPACE:#на клавиатуре выбираем кнопку прбела
                fire_sound.play()#запускаем звук
                ship.fire()#вызываем функцию файр(которая написанна в классе Player и создаёт пулю)

    
    if not finish:
        window.blit(background, (0, 0))

        text = font2.render('Счёт: ' + str(score), 1, (225, 225, 225))
        window.blit(text, (10,20))

        text_lose  =font2.render('Пропущено: ' + str(lose),1, (225, 225, 225))
        window.blit(text_lose, (10, 50))


        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)

        
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy,randint(80,win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters,False) or lose>=max_lose:
            finiah = True
            window.blit(loset,(200, 200))

        if score == goal:
            finish=True
            window.blit(win, (200,200))

        display.update()
    else:
            finish = False
            score = 0
            lose = 0
            for b in bullets:
                b.kill()
            for m in monsters:
                m.kill()



            time.delay(2000)
            for i in range(1,5):
                monster = Enemy(img_enemy,randint(80,win_width - 80), -40, 80, 50, randint(1,5))
                monsters.add(monster)



        

    
        

    time.delay(50)
