import pygame
import random

# Clase del Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self, ancho, alto):
        super().__init__()
        self.image = pygame.image.load("assets/imagenes/jugador.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = ancho // 2
        self.rect.bottom = alto - 50
        self.speed_x = 0

    def update(self, ancho, alto): 
        self.speed_x = 0
        tecla_oprimida = pygame.key.get_pressed()
        if tecla_oprimida[pygame.K_LEFT]:
            self.speed_x = -4
        if tecla_oprimida[pygame.K_RIGHT]:
            self.speed_x = 4
        self.rect.x += self.speed_x
        if self.rect.right > ancho:
            self.rect.right = ancho
        if self.rect.left < 0:
            self.rect.left = 0

# Clase del Enemigo
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, respuesta, ancho, alto):
        super().__init__()
        self.image = pygame.image.load("assets/imagenes/enemigo.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ancho - self.rect.width)
        self.rect.y = random.randrange(-alto, -10)
        self.speedy = random.uniform(1, 1.5)
        self.speedx = random.choice([-1, 1]) * random.uniform(1, 3)  # Velocidad aleatoria en x
        self.respuesta = respuesta

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # Rebotar en los bordes de la pantalla
        if self.rect.left < 0 or self.rect.right > ancho:
            self.speedx *= -1  # Invertir la dirección en x

        if self.rect.top > alto:
            self.rect.x = random.randrange(ancho - self.rect.width)
            self.rect.y = random.randrange(-alto, -10)
            self.speedy = random.uniform(1, 1.5)
            self.speedx = random.uniform(1, 1.5)

# Clase de la Bala
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/imagenes/laser.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Clase de la Respuesta
class Respuesta(pygame.sprite.Sprite):
    def __init__(self, text, enemy, color_texto):
        super().__init__()
        self.text = text
        self.font = pygame.font.Font(None, 24)
        self.image = self.font.render(text, True, color_texto)
        self.rect = self.image.get_rect()
        self.enemy = enemy

    def update(self):
        self.rect.centerx = self.enemy.rect.centerx
        self.rect.centery = self.enemy.rect.centery + 40
