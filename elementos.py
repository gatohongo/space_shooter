import pygame
import random
from font import obtener_font

ANCHO = 1080
ALTO = 720
blanco = (255, 255, 255)
preguntas_mostradas = []
vidas = 4
pantalla_juego = pygame.display.set_mode((ANCHO, ALTO))
explosion_imgs = [pygame.image.load("assets/imagenes/explosion_1.png"),
                  pygame.image.load("assets/imagenes/explosion_2.png"),
                  pygame.image.load("assets/imagenes/explosion_3.png"),
                  pygame.image.load("assets/imagenes/explosion_4.png"),
                  pygame.image.load("assets/imagenes/explosion_5.png"),
                  pygame.image.load("assets/imagenes/explosion_6.png"),
                  pygame.image.load("assets/imagenes/explosion_7.png")]


# Clase del Jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Carga la imagen original
        self.image_original = pygame.image.load("assets/imagenes/nave1.png").convert_alpha()
        # Escala la imagen original a las nuevas dimensiones
        self.image = pygame.transform.scale(self.image_original, (150, 138))
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 50
        self.speed_x = 0
        self.vidas = 4

    def update(self):
        self.speed_x = 0
        tecla_oprimida = pygame.key.get_pressed()
        if tecla_oprimida[pygame.K_LEFT]:
            self.speed_x = -4
        if tecla_oprimida[pygame.K_RIGHT]:
            self.speed_x = 4
        self.rect.x += self.speed_x
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.left < 0:
            self.rect.left = 0


# Clase del Enemigo
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, nueva_respuesta):
        super().__init__()
        self.imagen_original = pygame.image.load("assets/imagenes/enemigo.png").convert_alpha()
        self.image = pygame.transform.scale(self.imagen_original, (110, 98))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-ALTO, -10)
        self.speedy = random.uniform(1, 1.5)
        self.speedx = random.choice([-1, 1]) * random.uniform(1, 3)  # Velocidad aleatoria en x
        self.respuesta = nueva_respuesta

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # Rebotar en los bordes de la pantalla
        if self.rect.left < 0 or self.rect.right > ANCHO:
            self.speedx *= -1  # Invertir la dirección en x

        if self.rect.top > ALTO:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-ALTO, -10)
            self.speedy = random.uniform(1, 1.5)
            self.speedx = random.uniform(1, 1.5)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image_index = 0
        self.image_original = explosion_imgs[self.image_index]
        self.image = pygame.transform.scale(self.image_original, (120, 108))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.animation_speed = 0.2  # Velocidad de animación de la explosión
        self.last_update = pygame.time.get_ticks()
        self.lifetime = 2000  # Duración de la explosión en milisegundos (1 segundos)

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.image_index += 1
            if self.image_index >= len(explosion_imgs):
                self.kill()  # Eliminar la explosión después de mostrar todas las imágenes
            else:
                self.image = explosion_imgs[self.image_index]

        # Restar el tiempo transcurrido desde la última actualización al tiempo de vida de la explosión
        self.lifetime -= now - self.last_update
        if self.lifetime <= 0:
            self.kill()  # Eliminar la explosión si el tiempo de vida restante es menor o igual a cero


# Clase de la Bala
class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.imagen_original = pygame.image.load("assets/imagenes/shot.png").convert_alpha()
        self.image = pygame.transform.scale(self.imagen_original, (60, 60))
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
    def __init__(self, text, nuevo_enemigo):
        super().__init__()
        self.text = text
        self.font = obtener_font(17)
        self.image = self.font.render(text, False, blanco)
        self.rect = self.image.get_rect()
        self.enemy = nuevo_enemigo

    def update(self):
        self.rect.centerx = self.enemy.rect.centerx
        self.rect.centery = self.enemy.rect.centery + 60


# Función para generar una nueva pregunta y respuestas
def nueva_pregunta(preguntas_mostradas):
    preguntas = [
        "¿Que palabra clave se utiliza en Python para definir una funcion?",
        "¿Cual es la funcion que se utiliza para imprimir en la consola en Python?",
        "¿Cual es el resultado de 2 + 3 * 4?",
        "¿Que es una lista?",
        "¿Que es un diccionario en Python?",
        "¿Cual es el operador para comparar igualdad en Python?",
        "¿Que hace el metodo .append() en una lista?",
        "¿Que es un bucle for?",
        "¿Cual es el tipo de dato que puede contener varios elementos en Python?",
        "¿Que funcion se utiliza para obtener la longitud de una lista en Python?",
        "¿Que operador se utiliza para concatenar dos cadenas en Python?",
        "¿Cual es la palabra clave que se utiliza para definir una condicion en Python?",
        "¿Nombre del bucle que se ejecuta mientras una condicion sea verdadera en Python?",
        "¿Cual es el operador de exponenciacion en Python?"
    ]
    respuestas_correctas = [
        ["def", "define", "func", "function"],
        ["print()", "display()", "show()", "console.log()"],
        ["14", "18", "20", "11"],
        ["Conjunto de elementos", "Texto largo", "Indice numerico", "Codigo de error"],
        ["Coleccion de pares clave-valor", "Libro de definiciones", "Lista ordenada", "Serie numerica"],
        ["==", "=", "!=", "<>"],
        ["Agrega un elemento", "Elimina un elemento", "Reemplaza un elemento", "Ordena la lista"],
        ["Iteracion de elementos", "Lista de funciones", "Expresion matematica", "Estructura condicional"],
        ["lista", "array", "conjunto", "colección"],
        ["len()", "length()", "longitud()", "size()"],
        ["+", "concat()", "append()", "add()"],
        ["if", "else", "elif", "condición"],
        ["while", "for", "loop", "ciclo"],
        ["**", "^", "exp()", "exp"]
    ]

    # Verificar si se han mostrado todas las preguntas
    if len(preguntas_mostradas) >= len(preguntas):
        preguntas_mostradas.clear()

    # Obtener una pregunta no mostrada
    pregunta_nueva = random.choice([pregunta for pregunta in preguntas if pregunta not in preguntas_mostradas])
    indice_pregunta = preguntas.index(pregunta_nueva)

    # Agregar la pregunta a las preguntas mostradas
    preguntas_mostradas.append(pregunta_nueva)

    # Obtener respuestas correspondientes
    opciones_respuesta = respuestas_correctas[indice_pregunta]
    respuesta_correcta_valida = opciones_respuesta[0]  # La primera respuesta es la correcta
    random.shuffle(opciones_respuesta)

    return pregunta_nueva, opciones_respuesta, respuesta_correcta_valida
