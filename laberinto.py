import pygame
import random
import sys
import time

# Dimensiones del laberinto
ANCHO = 1000
ALTO = 800

# Dimensiones de las celdas del laberinto
CELDA = 15

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Inicializar pygame
pygame.init()

# Configurar la ventana del juego
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Laberinto")

# Fuente para el texto del botón
fuente = pygame.font.Font(None, 30)

# Variables globales
filas = (ALTO - CELDA) // CELDA
columnas = ANCHO // CELDA
laberinto = [[1] * columnas for _ in range(filas)]
ruta_encontrada = False
ruta = []
inicio_tiempo = 0
fin_tiempo = 0

def dibujar_cronometro(tiempo):
    texto_cronometro = fuente.render("Tiempo: {} s".format(tiempo), True, NEGRO)
    pantalla.blit(texto_cronometro, (20, 20))

def generar_laberinto():
    # Inicializar el laberinto con todas las paredes
    for fila in range(filas):
        for columna in range(columnas):
            laberinto[fila][columna] = 1

    # Punto de partida
    fila_actual = random.randrange(1, filas, 2)
    columna_actual = random.randrange(1, columnas, 2)
    laberinto[fila_actual][columna_actual] = 0

    # Pila para realizar backtracking
    pila = [(fila_actual, columna_actual)]

    while pila:
        vecinos = []

        # Buscar vecinos no visitados
        if fila_actual >= 2 and laberinto[fila_actual - 2][columna_actual] == 1:
            vecinos.append((-2, 0))
        if fila_actual <= filas - 3 and laberinto[fila_actual + 2][columna_actual] == 1:
            vecinos.append((2, 0))
        if columna_actual >= 2 and laberinto[fila_actual][columna_actual - 2] == 1:
            vecinos.append((0, -2))
        if columna_actual <= columnas - 3 and laberinto[fila_actual][columna_actual + 2] == 1:
            vecinos.append((0, 2))

        if vecinos:
            dx, dy = random.choice(vecinos)
            nueva_fila = fila_actual + dx
            nueva_columna = columna_actual + dy
            laberinto[nueva_fila][nueva_columna] = 0
            laberinto[fila_actual + dx // 2][columna_actual + dy // 2] = 0
            pila.append((nueva_fila, nueva_columna))
            fila_actual = nueva_fila
            columna_actual = nueva_columna
        else:
            fila_actual, columna_actual = pila.pop()

    # Marcar la entrada y la salida del laberinto
    laberinto[1][0] = 0
    laberinto[filas - 2][columnas - 1] = 0


def resolver_laberinto(fila, columna):
    global ruta_encontrada

    if fila < 0 or fila >= filas or columna < 0 or columna >= columnas:
        return False

    if laberinto[fila][columna] != 0 and laberinto[fila][columna] != 2:
        return False

    if laberinto[fila][columna] == 2:
        return False

    laberinto[fila][columna] = 2
    dibujar_laberinto()
    time.sleep(0.05)  # Retardo para visualizar paso a paso

    if fila == filas - 2 and columna == columnas - 1:
        ruta_encontrada = True
        return True

    if resolver_laberinto(fila, columna + 1):
        return True
    if resolver_laberinto(fila + 1, columna):
        return True
    if resolver_laberinto(fila, columna - 1):
        return True
    if resolver_laberinto(fila - 1, columna):
        return True

    laberinto[fila][columna] = 3
    dibujar_laberinto()
    time.sleep(0.05)  # Retardo para visualizar paso a paso

    return False




def dibujar_laberinto():
    pantalla.fill(BLANCO)
    for fila in range(filas):
        for columna in range(columnas):
            if laberinto[fila][columna] == 1:
                pygame.draw.rect(pantalla, NEGRO, (columna * CELDA, fila * CELDA, CELDA, CELDA))
            elif laberinto[fila][columna] == 0:
                pygame.draw.rect(pantalla, BLANCO, (columna * CELDA, fila * CELDA, CELDA, CELDA))
            elif laberinto[fila][columna] == 2:
                pygame.draw.rect(pantalla, VERDE, (columna * CELDA, fila * CELDA, CELDA, CELDA))
            elif laberinto[fila][columna] == 3:
                pygame.draw.rect(pantalla, ROJO, (columna * CELDA, fila * CELDA, CELDA, CELDA))
    
            if ruta_encontrada and laberinto[fila][columna] == 2:
                pygame.draw.rect(pantalla, AZUL, (columna * CELDA, fila * CELDA, CELDA, CELDA))
                
    pygame.display.flip()



def dibujar_ruta(ruta):
    for fila, columna in ruta:
        pygame.draw.rect(pantalla, AZUL, (columna * CELDA, fila * CELDA, CELDA, CELDA))
    pygame.display.update()


def dibujar_botones():
    pygame.draw.rect(pantalla, ROJO, (10, ALTO - 110, 100, 50))
    pygame.draw.rect(pantalla, AZUL, (120, ALTO - 110, 100, 50))
    texto_generar = fuente.render("Generar", True, BLANCO)
    texto_resolver = fuente.render("Resolver", True, BLANCO)
    pantalla.blit(texto_generar, (20, ALTO - 105))
    pantalla.blit(texto_resolver, (130, ALTO - 105))


generar_laberinto()
dibujar_laberinto()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if 10 <= pos[0] <= 110 and ALTO - 110 <= pos[1] <= ALTO - 60:
                    generar_laberinto()
                    dibujar_laberinto()
                    ruta_encontrada = False
                    inicio_tiempo = 0
                    fin_tiempo = 0
                    ruta.clear()
                elif 120 <= pos[0] <= 220 and ALTO - 110 <= pos[1] <= ALTO - 60:
                    if not ruta_encontrada:
                        resolver_laberinto(1, 0)
                        inicio_tiempo = time.time()
                        fin_tiempo = time.time()
                        dibujar_ruta(ruta)
    
    dibujar_botones()
    if inicio_tiempo > 0 and fin_tiempo > 0:
        tiempo_transcurrido = round(fin_tiempo - inicio_tiempo, 2)
        dibujar_cronometro(tiempo_transcurrido)
    pygame.display.update()
