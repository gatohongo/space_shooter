import pygame, sys, imageio
from pygame_boton import Boton

pygame.init()

#Propiedades de la ventana
ancho, alto = 1080, 720
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Shooter Practice 2.0")
icono = pygame.image.load("target.png")
pygame.display.set_icon(icono)

def obtener_font(tamaño):
    return pygame.font.Font("space_invaders.ttf",tamaño)

def jugar():
    print("Juego")

def ajustes():
    print("Ajustes")

def salir():
    print("Salir")

def menu_principal():

    #Inicializacion del fondo
    gif = 'space.gif'
    gif_frames = imageio.mimread(gif)
    gif_frames_escalados = [pygame.transform.scale(pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB"), (ancho, alto)) for frame in gif_frames]

    #Variables de tiempo
    clock = pygame.time.Clock()
    FPS = 60
    indice_frame = 0

    #Ciclo de la ventana
    running = True

    while running:

        #Frame actual del GIF
        frame_actual = gif_frames_escalados[indice_frame]

        #Dibujar el frame actual
        pantalla.blit(frame_actual, (0, 0))

        #Actualizar el indice para la siguiente iteracion
        indice_frame = (indice_frame + 1) % len(gif_frames_escalados)

        #Eventos de mouse
        posicion_mouse = pygame.mouse.get_pos()

        #Creacion del texto principal del menu
        menu_texto = obtener_font(80).render("SPACE SHOOTER", True, "#ffffff")
        menu_rect = menu_texto.get_rect(center=(540,100))

        #Dibujar en pantalla el texto y rect creados
        pantalla.blit(menu_texto, menu_rect)

        #Creacion de los botones con atributos heredados de la clase Boton
        boton_jugar = Boton(imagen=pygame.image.load("rect_salir.png"), posicion=(540,260), texto="JUGAR", font=obtener_font(40), color_principal="#ffffff", color_sobrepuesto="#ffffff")
        boton_ajustes = Boton(imagen=pygame.image.load("rect_salir.png"), posicion=(540,380), texto="AJUSTES", font=obtener_font(40), color_principal="#ffffff", color_sobrepuesto="#ffffff")
        boton_salir = Boton(imagen=pygame.image.load("rect_salir.png"), posicion=(540,500), texto="SALIR", font=obtener_font(40), color_principal="#ffffff", color_sobrepuesto="#ffffff")

        #Ciclo para cambiar color del boton al sobreponer el mouse
        for boton in [boton_jugar, boton_ajustes, boton_salir]:
            boton.cambiar_color(posicion_mouse)
            boton.actualizar(pantalla)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar.obtener_evento(posicion_mouse):
                    jugar()
                if boton_ajustes.obtener_evento(posicion_mouse):
                    ajustes()
                if boton_salir.obtener_evento(posicion_mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

menu_principal()
