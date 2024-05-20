import sys
import imageio
import pygame
import random

from boton import Boton
from elementos import Jugador, Enemigo, Explosion, Bala, Respuesta, nueva_pregunta, preguntas_mostradas
from font import obtener_font

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

sonido_fx = [sonido_disparo, sonido_impacto, sonido_click]


def menu_principal():
    pygame.display.set_caption("Programming Shoot 1.0")
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
    explosion_group = pygame.sprite.Group()
    balas = pygame.sprite.Group()

    # Añadir corazones y inicializar vidas
    corazon_og = pygame.image.load("assets/imagenes/heart.png").convert_alpha()
    corazon = pygame.transform.scale(corazon_og, (100, 100))
    corazones = [corazon] * 4
    vidas = 4

    # Inicializar puntaje
    puntaje = 0

    # Crear Jugador
    jugador = Jugador()
    all_sprites.add(jugador)

    # Pregunta inicial
    pregunta, respuestas, respuesta_correcta = nueva_pregunta(preguntas_mostradas=preguntas_mostradas)

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
                if event.key == pygame.K_SPACE:
                    sonido_disparo.play()  # Sonido de disparo
                    bala = Bala(jugador.rect.centerx, jugador.rect.top)
                    all_sprites.add(bala)
                    balas.add(bala)
                elif event.key == pygame.K_ESCAPE:
                    pausa()

        # Actualizar sprites
        jugador.update()
        all_sprites.update()

        # Verificar colisión bala-enemigo y respuesta correcta
        colisiones = pygame.sprite.groupcollide(enemigo_list, balas, False, True)
        for enemigo, balas_enemigo in colisiones.items():
            for bala in balas_enemigo:
                if enemigo.respuesta == respuesta_correcta:
                    explosion = Explosion(enemigo.rect.centerx,
                                          enemigo.rect.centery)  # Crea la explosión en la posición del enemigo
                    explosion_group.add(explosion)
                    sonido_impacto.play()
                    puntaje += 100

                    # Pasa a la siguiente pregunta
                    pregunta, respuestas, respuesta_correcta = nueva_pregunta(preguntas_mostradas)
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

                else:
                    try:
                        explosion = Explosion(enemigo.rect.centerx,
                                              enemigo.rect.centery)  # Crea la explosión en la posición del enemigo
                        explosion_group.add(explosion)
                        sonido_impacto.play()
                        corazones.pop()
                        vidas += -1

                        # Pasa a la siguiente pregunta
                        pregunta, respuestas, respuesta_correcta = nueva_pregunta(preguntas_mostradas)

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

                    except IndexError:
                        game_over()

        # Colisiones jugador-enemigo
        golpe1 = pygame.sprite.spritecollide(jugador, enemigo_list, False, pygame.sprite.collide_mask)
        if golpe1:
            explosion = Explosion(enemigo1.rect.centerx,
                                  enemigo1.rect.centery)  # Crea la explosión en la posición del enemigo
            explosion_group.add(explosion)
            sonido_impacto.play()
            vidas += -1

            if vidas <= 0:
                game_over()

            else:
                # Reiniciar la posicion del jugador y los enemigos
                jugador.rect.centerx = ANCHO // 2
                jugador.rect.bottom = ALTO - 50
                for enemigo in enemigo_list:
                    enemigo.rect.x = random.randrange(ANCHO - enemigo.rect.width)
                    enemigo.rect.y = random.randrange(-ALTO, -10)

                # Eliminar un corazón de la lista
                corazones.pop()

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
        pregunta_surface = obtener_font(20).render(pregunta, False, blanco)
        pregunta_rect = pregunta_surface.get_rect(center=(ANCHO // 2, 50))
        pantalla.blit(pregunta_surface, pregunta_rect)

        fondo_y += 3.5  # Velocidad del fondo

        # Resetear fondos cuando salen de la pantalla
        if fondo_y >= ALTO:
            fondo_y = 0

        # Mostrar vidas
        for i, corazon in enumerate(corazones):
            pantalla.blit(corazon, (ANCHO - 80 - (i * 45), ALTO - 75))

        explosion_group.update()  # Actualiza las explosiones
        explosion_group.draw(pantalla)
        all_sprites.draw(pantalla)

        # Mostrar puntaje
        texto_puntaje = obtener_font(40).render(str(puntaje).zfill(4), False, "Green")
        pantalla.blit(texto_puntaje, (10, 670))

        pygame.display.flip()

    pygame.quit()


def pausa():
    pygame.display.set_caption("Pausa")

    # Guardar volumen original
    volumen_original_musica = musica_bg.get_volume()
    volumen_original_efectos = sonido_fx[0].get_volume()

    barra_musica_pos = int(volumen_original_musica * 300)
    barra_efectos_pos = int(volumen_original_efectos * 300)

    while True:
        posicion_mouse = pygame.mouse.get_pos()
        texto_salir = Boton(None, (120, 25),
                            "SALIR AL MENU", obtener_font(25), blanco, "Green")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if texto_salir.obtener_evento(posicion_mouse):
                    sonido_click.play()  # Sonido de click
                    musica_bg.stop()
                    menu_principal()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.display.set_caption("Juego")
                return  # Salir de la función de pausa

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si el clic fue en la barra de volumen de música
                if ANCHO / 2.7 <= event.pos[0] <= ANCHO / 2.7 + 300 and 430 <= event.pos[1] <= 470:
                    barra_musica_pos = event.pos[0] - ANCHO / 2.7
                    musica_bg.set_volume(barra_musica_pos / 300.0)
                # Verificar si el clic fue en la barra de volumen de efectos
                elif ANCHO / 2.7 <= event.pos[0] <= ANCHO / 2.7 + 300 and 530 <= event.pos[1] <= 570:
                    barra_efectos_pos = event.pos[0] - ANCHO / 2.7
                    for sonido in sonido_fx:
                        sonido.set_volume(barra_efectos_pos / 300.0)

        # Crear una superficie semitransparente para la pausa
        superficie_pausa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        superficie_pausa.fill((0, 0, 0))

        # Dibujar la barra de volumen de música
        pygame.draw.rect(superficie_pausa, (155, 155, 155), (ANCHO / 2.7, 430, barra_musica_pos, 40))

        # Dibujar la barra de volumen de efectos
        pygame.draw.rect(superficie_pausa, (155, 155, 155), (ANCHO / 2.7, 530, barra_efectos_pos, 40))

        # Mostrar el texto de pausa
        texto_pausa = obtener_font(40).render("PAUSADO", False, (255, 255, 255))
        texto_rect = texto_pausa.get_rect(center=(ANCHO / 2, 200))
        superficie_pausa.blit(texto_pausa, texto_rect)

        # Mostrar texto sonidos
        texto_musica = obtener_font(30).render("MUSICA", False, (255, 255, 255))
        texto_fx = obtener_font(30).render("FX", False, (255, 255, 255))
        texto_musica_rect = texto_musica.get_rect(center=(ANCHO / 3.7, 450))
        texto_fx_rect = texto_fx.get_rect(center=(ANCHO / 3.5, 550))
        superficie_pausa.blit(texto_musica, texto_musica_rect)
        superficie_pausa.blit(texto_fx, texto_fx_rect)

        # Mostrar texto salir al menu
        texto_salir.cambiar_color(posicion_mouse)
        texto_salir.actualizar(superficie_pausa)

        pantalla.blit(superficie_pausa, (0, 0))
        pygame.display.flip()  # Actualiza la pantalla


def ajustes():
    pygame.display.set_caption("Ajustes")
    musica_bg.stop()
    ajustes = True

    # Guardar volumen original
    volumen_original_musica = musica_bg.get_volume()
    volumen_original_efectos = sonido_fx[0].get_volume()

    barra_musica_pos = int(volumen_original_musica * 300)
    barra_efectos_pos = int(volumen_original_efectos * 300)

    while ajustes:
        posicion_mouse = pygame.mouse.get_pos()
        texto_salir = Boton(None, (120, 25),
                            "VOLVER", obtener_font(25), blanco, "Green")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if texto_salir.obtener_evento(posicion_mouse):
                    sonido_click.play()  # Sonido de click
                    musica_bg.stop()
                    menu_principal()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Verificar si el clic fue en la barra de volumen de música
                if ANCHO / 2.7 <= event.pos[0] <= ANCHO / 2.7 + 300 and 430 <= event.pos[1] <= 470:
                    barra_musica_pos = event.pos[0] - ANCHO / 2.7
                    musica_bg.set_volume(barra_musica_pos / 300.0)
                # Verificar si el clic fue en la barra de volumen de efectos
                elif ANCHO / 2.7 <= event.pos[0] <= ANCHO / 2.7 + 300 and 530 <= event.pos[1] <= 570:
                    barra_efectos_pos = event.pos[0] - ANCHO / 2.7
                    for sonido in sonido_fx:
                        sonido.set_volume(barra_efectos_pos / 300.0)

        # Crear una superficie semitransparente para la pausa
        superficie_pausa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        superficie_pausa.fill((0, 0, 0))

        # Dibujar la barra de volumen de música
        pygame.draw.rect(superficie_pausa, (155, 155, 155), (ANCHO / 2.7, 430, barra_musica_pos, 40))

        # Dibujar la barra de volumen de efectos
        pygame.draw.rect(superficie_pausa, (155, 155, 155), (ANCHO / 2.7, 530, barra_efectos_pos, 40))

        # Mostrar el texto de pausa
        texto_pausa = obtener_font(40).render("PAUSADO", False, (255, 255, 255))
        texto_rect = texto_pausa.get_rect(center=(ANCHO / 2, 200))
        superficie_pausa.blit(texto_pausa, texto_rect)

        # Mostrar texto sonidos
        texto_musica = obtener_font(30).render("MUSICA", False, (255, 255, 255))
        texto_fx = obtener_font(30).render("FX", False, (255, 255, 255))
        texto_musica_rect = texto_musica.get_rect(center=(ANCHO / 3.7, 450))
        texto_fx_rect = texto_fx.get_rect(center=(ANCHO / 3.5, 550))
        superficie_pausa.blit(texto_musica, texto_musica_rect)
        superficie_pausa.blit(texto_fx, texto_fx_rect)

        # Mostrar texto salir al menu
        texto_salir.cambiar_color(posicion_mouse)
        texto_salir.actualizar(superficie_pausa)

        pantalla.blit(superficie_pausa, (0, 0))
        pygame.display.update()  # Actualiza la pantalla


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
