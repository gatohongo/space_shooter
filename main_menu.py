import imageio
import pygame
import sys

from boton import Boton
from font import obtener_font
from elementos import Jugador, Enemigo, Bala, Respuesta, nueva_pregunta, preguntas_mostradas

pygame.init()

# Colores
negro = (0, 0, 0)
blanco = (255, 255, 255)

# Propiedades de la ventana
ANCHO, ALTO = 1080, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Programming Shoot 1.0")
icono = pygame.image.load("assets/imagenes/icon.png")
pygame.display.set_icon(icono)

# Configuración audio
musica_bg = pygame.mixer.Sound("assets/audio/musica_bg.ogg")

# Carga de sonidos
sonido_disparo = pygame.mixer.Sound("assets/audio/disparo.wav")
sonido_impacto = pygame.mixer.Sound("assets/audio/explosion.wav")
sonido_click = pygame.mixer.Sound("assets/audio/click.wav")


def menu_principal():
    # Iniciar la musica de fondo
    musica_bg.play(-1)

    # Iniciar el gif del fondo
    gif = 'assets/imagenes/space.gif'
    gif_frames = imageio.mimread(gif)
    gif_frames_escalados = [
        pygame.transform.scale(pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB"), (ANCHO, ALTO)) for
        frame in gif_frames]

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
        menu_texto = obtener_font(60).render("PROGRAMMING SHOOT 1.0", False, blanco)
        menu_rect = menu_texto.get_rect(center=(540, 100))

        # Dibujar en pantalla el texto y rect creados
        pantalla.blit(menu_texto, menu_rect)

        # Creacion de los botones con atributos heredados de la clase Boton
        boton_jugar = Boton(pygame.image.load("assets/imagenes/rect_salir.png"), (540, 290),
                            "JUGAR", obtener_font(40), blanco, blanco)
        boton_ajustes = Boton(pygame.image.load("assets/imagenes/rect_salir.png"), (540, 410),
                              "AJUSTES", obtener_font(40), blanco, blanco)
        boton_salir = Boton(pygame.image.load("assets/imagenes/rect_salir.png"), (540, 530),
                            "SALIR", obtener_font(40), blanco, blanco)

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


def jugar():
    # Configuración de la pantalla
    pygame.display.set_caption("Juego")
    reloj = pygame.time.Clock()

    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    enemigo_list = pygame.sprite.Group()
    balas = pygame.sprite.Group()

    # Crear Jugador
    jugador = Jugador()
    all_sprites.add(jugador)

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
    fondo_1 = pygame.image.load("assets/imagenes/fondo_juego.png").convert()
    fondo_2 = pygame.image.load("assets/imagenes/fondo_juego.png").convert()
    fondo_1 = pygame.transform.scale(fondo_1, (ANCHO, ALTO))
    fondo_2 = pygame.transform.scale(fondo_2, (ANCHO, ALTO))
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
        pantalla.blit(fondo_2, (0, fondo_y - ALTO))
        pregunta_surface = obtener_font(22).render(pregunta, False, blanco)
        pregunta_rect = pregunta_surface.get_rect(center=(ANCHO // 2, 50))
        pantalla.blit(pregunta_surface, pregunta_rect)

        fondo_y += 3.5  # Velocidad del fondo

        # Resetear fondos cuando salen de la pantalla
        if fondo_y >= ALTO:
            fondo_y = 0

        all_sprites.draw(pantalla)

        pygame.display.flip()

    pygame.quit()


def ajustes():
    musica_bg.stop()
    ejecutando = True

    while ejecutando:
        posicion_mouse = pygame.mouse.get_pos()

        pantalla.fill(blanco)

        ajustes_texto = obtener_font(35).render("Pantalla de ajustes en construccion.", True, negro)
        ajustes_rect = ajustes_texto.get_rect(center=(540, 260))
        pantalla.blit(ajustes_texto, ajustes_rect)

        ajustes_atras = Boton(None, (540, 460),
                              "ATRAS", obtener_font(75), negro, "Green")

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


def game_over():
    musica_bg.stop()
    pantalla.fill("Black")
    sonido_game_over = pygame.mixer.Sound("assets/audio/game_over.wav")
    sonido_game_over.play()

    game_over_texto = obtener_font(80).render("GAME OVER", True, blanco)
    game_over_rect = game_over_texto.get_rect(center=(ANCHO // 2, ALTO // 2))
    pantalla.blit(game_over_texto, game_over_rect)

    pygame.display.flip()

    pygame.time.delay(4000)  # Esperar 2 segundos antes de volver al menú principal
    menu_principal()


def salir():
    pygame.quit()
    sys.exit()


menu_principal()
