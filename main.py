import pygame
from random import randint
pygame.init()


win_w = 600
win_h = 480
FPS = 40

# pygame.mixer_music.load("space.ogg")
# pygame.mixer_music.set_volume(0.1)
# pygame.mixer_music.play(-1)

fire_snd = pygame.mixer.Sound("fire.ogg")
# 
bullet_img = pygame.image.load("bullet.png")


class GameSprite:
    def __init__(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image
    
    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Pers(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed

    def move(self, key_left, key_right):
        k = pygame.key.get_pressed()
        if k[key_right]:
            if self.rect.right <= win_w:
                self.rect.x += self.speed 
        elif k[key_left]:
            if self.rect.left >= 0:
                self.rect.x -= self.speed

    def shoot(self):
        # fire_snd.play()
        b = Bullet(self.rect.centerx-7, self.rect.y, 15, 20, bullet_img, 4)

class Enemy(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        # self.direction = direction
        # self.x2 = x2
        # self.x1 = x
    
    def move(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= win_h:
            lost += 1
            print(lost)
            self.rect.x = randint(0, win_w - self.rect.w)
            self.rect.y = randint(-500, -self.rect.h)
            self.speed = randint(1, 3)

bullets = []
class Bullet(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        bullets.append(self)
    
    def move(self):
        self.rect.y -= self.speed
        if self.rect.y <= -20:
            bullets.remove(self)
    
font1 = pygame.font.SysFont("Arial", 20)
font2 = pygame.font.SysFont("Arial", 50)

window = pygame.display.set_mode((win_w, win_h))
pygame.display.set_caption("Shooter 0.1")
clock = pygame.time.Clock()

background = pygame.image.load("galaxy.jpg")
background = pygame.transform.scale(background, (win_w, win_h))
window.blit(background, (0, 0))

rocket_img = pygame.image.load("rocket.png")
rocket = Pers(330, 400, 50, 60, rocket_img, 5)

enemy_img = pygame.image.load("ufo.png")

enemies = []
for i in range(5):
    enemy = Enemy(randint(0, win_w-50), randint(-500, 0), 70, 40, enemy_img, randint(1, 3))
    enemies.append(enemy)

score = 0
lost = 0
game = True
finish = False
while game:
    if not finish:
        window.blit(background, (0, 0))
        rocket.update()
        rocket.move(pygame.K_a, pygame.K_d)
        for enemy in enemies:
            enemy.update()
            enemy.move()
            if rocket.rect.colliderect(enemy.rect):
                finish = True
                game_over = font2.render("Game Over", True, (255, 0, 0))
            for bullet in bullets:
                if bullet.rect.colliderect(enemy.rect):
                    score += 1
                    print(score)
                    enemy.rect.x, enemy.rect.y = randint(0, win_w-50), randint(-500, 0)
                    bullets.remove(bullet)

        for bullet in bullets:
            bullet.update()
            bullet.move()
        if lost >= 3:
            finish = True
            game_over = font2.render("Game Over", True, (255, 0, 0))
    else:
        window.blit(game_over, (200,200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and finish:
            finish = False
            lost = 0
            score = 0
            rocket.rect.x, rocket.rect.y = 300, 400
            for enemy in enemies:
                enemy.rect.x, enemy.rect.y = randint(0, win_w-50), randint(-500, 0)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not finish:
            rocket.shoot()
    propusk = font1.render("Пропущено: "+str(lost), True, (255, 255, 255))
    window.blit(propusk, (10,10))
    killed = font1.render("Вбито: "+str(score), True, (255, 255, 255))
    window.blit(killed, (10,30))
    pygame.display.update()
    clock.tick(FPS)