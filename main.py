import pygame
import random
import math
from pygame import mixer

# Inicializar Pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e icono
pygame.display.set_caption('Invasión Espacial')
icono = pygame.image.load('ovni.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load('fondo.jpeg')

# Musica
mixer.music.load('fondo_sonido.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# Variables del jugador
img_jugador = pygame.image.load('nave-espacial.png')
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# Variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 10
for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load('fantasma.png'))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# Variables bala
img_bala = pygame.image.load('bala.png')
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 2
bala_visible = False

# Puntaje
puntaje = 0
fuente = pygame.font.Font('war_is_over_font.ttf', 32)
texto_x = 10
texto_y = 10

# Texto final de juego
fuente_final = pygame.font.Font('war_is_over_font.ttf', 40)


def texto_final():
    mi_fuente_final = fuente_final.render('HAS PERDIDO', True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (60, 200))


# Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f'PUNTAJE: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 28, y + 10))


# Funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# Funcion enemigo
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# Funcion jugador
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# Loop del juego
se_ejectura = True
while se_ejectura:
    # Imagen de fondo
    pantalla.blit(fondo, (0, 0))
    # Iterar eventos
    for evento in pygame.event.get():
        # Evento para cerrar juego
        if evento.type == pygame.QUIT:
            se_ejectura = False
        # Evento presionar tecla
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('bala_sonido_16b.wav')
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)
        # Evento soltar teclas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Modificar ubicacion jugador
    jugador_x += jugador_x_cambio
    # Mantener jugador dentro de los bordes de ventana
    if jugador_x <= 0:
        jugador_x = 1
    elif jugador_x >= 736:
        jugador_x = 734

    # Modificar ubicacion enemigo
    for e in range(cantidad_enemigos):
        # Fin del juego
        if enemigo_y[e] >= 450:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        enemigo_x[e] += enemigo_x_cambio[e]
        # Mantener enemigo dentro de los bordes de ventana
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.5
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.5
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            colision_sound = mixer.Sound('impacto_boom_16.wav')
            colision_sound.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)
        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x, texto_y)
    # Actualizar todo
    pygame.display.update()
