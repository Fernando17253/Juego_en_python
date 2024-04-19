import pygame
import random
import threading
import time
from network import Network

# Definir colores
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Tamaño de la pantalla
ANCHO = 800
ALTO = 600

# Tamaño de los bloques
TAM_BLOQUE = 20

class Gusano(threading.Thread):
    def __init__(self, id, start_pos):
        threading.Thread.__init__(self)
        self.id = id
        self.segmentos = [start_pos]
        self.direccion = 'RIGHT'
        self.score = 0

    def mover(self):
        cabeza = self.segmentos[0]
        if self.direccion == 'UP':
            nueva_cabeza = (cabeza[0], (cabeza[1] - TAM_BLOQUE) % ALTO)
        elif self.direccion == 'DOWN':
            nueva_cabeza = (cabeza[0], (cabeza[1] + TAM_BLOQUE) % ALTO)
        elif self.direccion == 'LEFT':
            nueva_cabeza = ((cabeza[0] - TAM_BLOQUE) % ANCHO, cabeza[1])
        elif self.direccion == 'RIGHT':
            nueva_cabeza = ((cabeza[0] + TAM_BLOQUE) % ANCHO, cabeza[1])
        self.segmentos.insert(0, nueva_cabeza)
        self.segmentos.pop()

    def dibujar(self, pantalla):
        color = VERDE if self.id == 0 else AZUL
        for segmento in self.segmentos:
            pygame.draw.rect(pantalla, color, [segmento[0], segmento[1], TAM_BLOQUE, TAM_BLOQUE])

class Manzana:
    def __init__(self):
        self.posicion = (random.randrange(0, ANCHO - TAM_BLOQUE, TAM_BLOQUE), random.randrange(0, ALTO - TAM_BLOQUE, TAM_BLOQUE))

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, ROJO, [self.posicion[0], self.posicion[1], TAM_BLOQUE, TAM_BLOQUE])

def main():
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO, ALTO])
    n = Network()
    id = int(n.id)
    gusano1 = Gusano(0, (ANCHO / 2, ALTO / 2))
    gusano2 = Gusano(1, (ANCHO / 2, ALTO / 2 + TAM_BLOQUE))
    if id == 1:
        gusano1, gusano2 = gusano2, gusano1
    gusano1.start()
    gusano2.start()
    manzana = Manzana()
    reloj = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w:
                    gusano1.direccion = 'UP'
                elif evento.key == pygame.K_s:
                    gusano1.direccion = 'DOWN'
                elif evento.key == pygame.K_a:
                    gusano1.direccion = 'LEFT'
                elif evento.key == pygame.K_d:
                    gusano1.direccion = 'RIGHT'
                elif evento.key == pygame.K_UP:
                    gusano2.direccion = 'UP'
                elif evento.key == pygame.K_DOWN:
                    gusano2.direccion = 'DOWN'
                elif evento.key == pygame.K_LEFT:
                    gusano2.direccion = 'LEFT'
                elif evento.key == pygame.K_RIGHT:
                    gusano2.direccion = 'RIGHT'
        # Actualización de posición basada en teclado hecho aquí
        gusano1.mover()
        gusano2.mover()

        # Enviar la posición del gusano local al servidor y recibir la posición del otro gusano
        respuesta = n.send(f"{gusano1.id}:{gusano1.segmentos[0][0]},{gusano1.segmentos[0][1]}")
        # La respuesta contiene la nueva posición del otro gusano
        pos = respuesta.split(":")[1].split(",")

        #gusano2.segmentos[0] = (int(pos[0]), int(pos[1]))

        gusano2.segmentos[0] = (int(float(pos[0])), int(float(pos[1])))

        pantalla.fill(NEGRO)

        gusano1.dibujar(pantalla)
        gusano2.dibujar(pantalla)

        if gusano1.segmentos[0] == manzana.posicion:
            gusano1.segmentos.append(gusano1.segmentos[-1])
            gusano1.score += 1
            manzana.posicion = manzana.posicion

        if gusano2.segmentos[0] == manzana.posicion:
            gusano2.segmentos.append(gusano2.segmentos[-1])
            gusano2.score += 1
            manzana.posicion = manzana.posicion

        manzana.dibujar(pantalla)

        # Enviar información de la posición de los jugadores al servidor
        n.send(f"{gusano1.id}:{gusano1.segmentos[0][0]},{gusano1.segmentos[0][1]}")
        n.send(f"{gusano2.id}:{gusano2.segmentos[0][0]},{gusano2.segmentos[0][1]}")

        pygame.display.flip()
        reloj.tick(10)

if __name__ == "__main__":
    main()