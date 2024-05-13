import pygame, sys, imageio, random
from boton import Boton

pygame.init()

# Propiedades de la ventana
ancho, alto = 1080, 720
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Programming Shoot 1.0")
icono = pygame.image.load("assets/imagenes/target.png")
pygame.display.set_icon(icono)

# Configuración audio
musica_bg = pygame.mixer.music.load("assets/audio/musica_bg.ogg")
musica_bg.play()

# Carga de sonidos
sonido_disparo = pygame.mixer.Sound("assets/audio/disparo.wav")
sonido_impacto = pygame.mixer.Sound("assets/audio/explosion.wav")
sonido_click = pygame.mixer.Sound("assets/audio/click.wav")


def obtener_font(tamaño):
    return pygame.font.Font("assets/font/space_invaders.ttf", tamaño)

def game_over():
    pantalla.fill("Black")
    sonido_game_over = pygame.mixer.Sound("assets/audio/game_over.wav")
    sonido_game_over.play()
    sonido

    game_over_texto = obtener_font(80).render("GAME OVER", True, "White")
    game_over_rect = game_over_texto.get_rect(center=(ancho // 2, alto // 2))
    pantalla.blit(game_over_texto, game_over_rect)

    pygame.display.flip()

    pygame.time.delay(2000)  # Esperar 2 segundos antes de volver al menú principal
    menu_principal()

def jugar():
    # Colores
    negro = (0, 0, 0)
    blanco = (255, 255, 255)

    # Configuración de la pantalla
    pygame.display.set_caption("Juego")
    reloj = pygame.time.Clock()

    # Clase del Jugador
    class Jugador(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("assets/imagenes/jugador.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.centerx = ancho // 2
            self.rect.bottom = alto - 50
            self.speed_x = 0

        def update(self):
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
        def __init__(self, respuesta):
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
        def __init__(self, text, enemy):
            super().__init__()
            self.text = text
            self.font = pygame.font.Font(None, 24)
            self.image = self.font.render(text, True, blanco)
            self.rect = self.image.get_rect()
            self.enemy = enemy

        def update(self):
            self.rect.centerx = self.enemy.rect.centerx
            self.rect.centery = self.enemy.rect.centery + 40

    # Función para generar una nueva pregunta y respuestas
    def nueva_pregunta():
        preguntas = [
            "¿Qué palabra clave se utiliza en Python para definir una función?",
            "¿Cuál es la función que se utiliza para imprimir en la consola en Python?",
            "¿Cuál es el resultado de 2 + 3 * 4?",
            "¿Qué es una lista?",
            "¿Qué es un diccionario en Python?",
            "¿Cuál es el operador para comparar igualdad en Python?",
            "¿Qué hace el método .append() en una lista?",
            "¿Qué es un bucle for?"

        ]
        respuestas_correctas = [
            ["def", "define", "func", "fuction"],
            ["print()", "display()", "show()", "console.log()"],
            ["14", "18", "20", "11"],
            ["Conjunto de elementos", "Texto largo", "indice numérico", "Código de error"],
            ["Colección de pares clave-valor", "Libro de definiciones", "Lista ordenada", "Serie numérica"],
            ["==", "=", "!=", "<>"],
            ["Agrega un elemento", "Elimina un elemento", "Reemplaza un elemento", "Ordena la lista"],
            ["Iteración de elementos", "Lista de funciones", "Expresión matemática", "Estructura condicional"]
        ]

        # Verificar si se han mostrado todas las preguntas
        if len(preguntas_mostradas) == len(preguntas):
            pygame.quit()  # Cerrar el juego si se han mostrado todas las preguntas
        else:
            # Obtener una pregunta no mostrada
            pregunta_nueva = random.choice([pregunta for pregunta in preguntas if pregunta not in preguntas_mostradas])
            indice_pregunta = preguntas.index(pregunta_nueva)

            # Agregar la pregunta a las preguntas mostradas
            preguntas_mostradas.append(pregunta_nueva)

            # Obtener respuestas correspondientes
            respuestas = respuestas_correctas[indice_pregunta]
            respuesta_correcta = respuestas[0]  # La primera respuesta es la correcta
            random.shuffle(respuestas)

            return pregunta_nueva, respuestas, respuesta_correcta

    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    enemigo_list = pygame.sprite.Group()
    balas = pygame.sprite.Group()

    # Crear Jugador
    jugador = Jugador()
    all_sprites.add(jugador)

    # Preguntas mostradas
    preguntas_mostradas = []

    # Pregunta inicial
    pregunta, respuestas, respuesta_correcta = nueva_pregunta()

    # Crear Enemigos y sus respuestas asociadas
    for respuesta in respuestas:
        nuevo_enemigo = Enemigo(respuesta)
        all_sprites.add(nuevo_enemigo)
        enemigo_list.add(nuevo_enemigo)
        respuesta_sprite = Respuesta(respuesta, nuevo_enemigo)
        all_sprites.add(respuesta_sprite)

    # Imagenes de fondo
    fondo_1 = pygame.image.load("assets/imagenes/fondo_juego.jpg").convert()
    fondo_2 = pygame.image.load("assets/imagenes/fondo_juego.jpg").convert()
    fondo_1 = pygame.transform.scale(fondo_1, (ancho, alto))
    fondo_2 = pygame.transform.scale(fondo_2, (ancho, alto))
    fondo_y = 0  # Initial vertical position of the background

    iniciar = True
    while iniciar:
        reloj.tick(60)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                iniciar = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    iniciar = False
                elif event.key == pygame.K_SPACE:
                    sonido_disparo.play()  # Sonido de disparo
                    bala = Bala(jugador.rect.centerx, jugador.rect.top)
                    all_sprites.add(bala)
                    balas.add(bala)

        # Actualizar sprites
        jugador.update()
        all_sprites.update()

        # Verificar colisión bala-enemigo y respuesta correcta
        colisiones = pygame.sprite.groupcollide(enemigo_list, balas, False, True)
        for enemigo, balas_enemigo in colisiones.items():
            for bala in balas_enemigo:
                if enemigo.respuesta == respuesta_correcta:
                    sonido_impacto.play()  # Sonido de impacto
                    # Pasa a la siguiente pregunta
                    pregunta, respuestas, respuesta_correcta = nueva_pregunta()
                    # Elimina todos los enemigos actuales y crea nuevos con las nuevas respuestas
                    enemigo_list.empty()
                    all_sprites.empty()
                    balas.empty()
                    for respuesta in respuestas:
                        nuevo_enemigo = Enemigo(respuesta)
                        all_sprites.add(nuevo_enemigo)
                        enemigo_list.add(nuevo_enemigo)
                        respuesta_sprite = Respuesta(respuesta, nuevo_enemigo)
                        all_sprites.add(respuesta_sprite)
                    # Agrega de nuevo al jugador
                    all_sprites.add(jugador)

        # Colisiones jugador-enemigo
        golpe1 = pygame.sprite.spritecollide(jugador, enemigo_list, False, pygame.sprite.collide_mask)
        if golpe1:
            game_over()

        # Colisiones enemigos-enemigos
        colisiones_enemigos = pygame.sprite.groupcollide(enemigo_list, enemigo_list, False, False)
        for enemigo1, enemigos_colisionados in colisiones_enemigos.items():
            for enemigo2 in enemigos_colisionados:
                if enemigo1 != enemigo2:
                    if enemigo1.rect.colliderect(enemigo2.rect):
                        # Cambiar la dirección de enemigo1
                        enemigo1.speedx *= -1
                        # Cambiar la dirección de enemigo2
                        enemigo2.speedx *= -1
                        # Ajustar la posición en x
                        enemigo1.rect.x += enemigo1.speedx
                        enemigo2.rect.x += enemigo2.speedx

        # Dibujar fondos y pregunta
        pantalla.fill(negro)
        pantalla.blit(fondo_1, (0, fondo_y))
        pantalla.blit(fondo_2, (0, fondo_y - alto))
        pregunta_surface = pygame.font.Font(None, 36).render(pregunta, True, blanco)
        pregunta_rect = pregunta_surface.get_rect(center=(ancho // 2, 50))
        pantalla.blit(pregunta_surface, pregunta_rect)

        fondo_y += 3.5  # Velocidad del fondo

        # Resetear fondos cuando salen de la pantalla
        if fondo_y >= alto:
            fondo_y = 0

        all_sprites.draw(pantalla)

        pygame.display.flip()

    pygame.quit()

def ajustes():
    ejecutando = True

    while ejecutando:
        posicion_mouse = pygame.mouse.get_pos()

        pantalla.fill("white")

        ajustes_texto = obtener_font(35).render("Pantalla de ajustes en construccion.", True, "Black")
        ajustes_rect = ajustes_texto.get_rect(center=(540, 260))
        pantalla.blit(ajustes_texto, ajustes_rect)

        ajustes_atras = Boton(imagen=None, posicion=(540, 460),
                            texto="ATRAS", font=obtener_font(75), color_principal="Black", color_sobrepuesto="Green")

        ajustes_atras.cambiar_color(posicion_mouse)
        ajustes_atras.actualizar(pantalla)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ajustes_atras.obtener_evento(posicion_mouse):
                    sonido_click.play()  # Sonido de click
                    menu_principal()

        pygame.display.update()

def salir():
    print("Salir")

def menu_principal():

    # Inicializacion del fondo
    gif = 'assets/imagenes/space.gif'
    gif_frames = imageio.mimread(gif)
    gif_frames_escalados = [pygame.transform.scale(pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB"), (ancho, alto)) for frame in gif_frames]

    # Variables de tiempo
    clock = pygame.time.Clock()
    FPS = 60
    indice_frame = 0

    # Ciclo de la ventana
    running = True

    while running:

        # Frame actual del GIF
        frame_actual = gif_frames_escalados[indice_frame]

        # Dibujar el frame actual
        pantalla.blit(frame_actual, (0, 0))

        # Actualizar el indice para la siguiente iteracion
        indice_frame = (indice_frame + 1) % len(gif_frames_escalados)

        # Eventos de mouse
        posicion_mouse = pygame.mouse.get_pos()

        # Creacion del texto principal del menu
        menu_texto = obtener_font(80).render("SPACE SHOOTER", True, "#ffffff")
        menu_rect = menu_texto.get_rect(center=(540, 100))

        # Dibujar en pantalla el texto y rect creados
        pantalla.blit(menu_texto, menu_rect)

        # Creacion de los botones con atributos heredados de la clase Boton
        boton_jugar = Boton(imagen=pygame.image.load("assets/imagenes/rect_salir.png"), posicion=(540, 260), texto="JUGAR",
                            font=obtener_font(40), color_principal="#ffffff", color_sobrepuesto="#ffffff")
        boton_ajustes = Boton(imagen=pygame.image.load("assets/imagenes/rect_salir.png"), posicion=(540, 380),
                              texto="AJUSTES", font=obtener_font(40), color_principal="#ffffff",
                              color_sobrepuesto="#ffffff")
        boton_salir = Boton(imagen=pygame.image.load("assets/imagenes/rect_salir.png"), posicion=(540, 500),
                            texto="SALIR", font=obtener_font(40), color_principal="#ffffff", color_sobrepuesto="#ffffff")

        # Ciclo para cambiar color del boton al sobreponer el mouse
        for boton in [boton_jugar, boton_ajustes, boton_salir]:
            boton.cambiar_color(posicion_mouse)
            boton.actualizar(pantalla)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.obtener_evento(posicion_mouse):
                    sonido_click.play()  # Sonido de click
                    jugar()
                if boton_ajustes.obtener_evento(posicion_mouse):
                    sonido_click.play()  # Sonido de click
                    ajustes()
                if boton_salir.obtener_evento(posicion_mouse):
                    sonido_click.play()  # Sonido de click
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

menu_principal()
