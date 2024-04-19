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

# Define the font size for score display
FONT_SIZE = 28

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

def draw_score(display, score, position, color=(255, 255, 255)):
    font = pygame.font.Font(None, FONT_SIZE)
    text = font.render(f'Score: {score}', True, color)
    display.blit(text, position)

def main():
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO, ALTO])
    pygame.font.init()
    n = Network()
    id = int(n.id)
    gusanos = [Gusano(0, (ANCHO / 2, ALTO / 2)), Gusano(1, (ANCHO / 2, ALTO / 2 + TAM_BLOQUE))]
    gusanos[id], gusanos[1-id] = gusanos[1-id], gusanos[id]
    for gusano in gusanos:
        gusano.start()
    manzana = Manzana()
    reloj = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_w:
                    gusano.direccion = 'UP'
                elif evento.key == pygame.K_s:
                    gusano.direccion = 'DOWN'
                elif evento.key == pygame.K_a:
                    gusano.direccion = 'LEFT'
                elif evento.key == pygame.K_d:
                    gusano.direccion = 'RIGHT'
                elif evento.key == pygame.K_UP:
                    gusanos.direccion = 'UP'
                elif evento.key == pygame.K_DOWN:
                    gusanos.direccion = 'DOWN'
                elif evento.key == pygame.K_LEFT:
                    gusanos.direccion = 'LEFT'
                elif evento.key == pygame.K_RIGHT:
                    gusanos.direccion = 'RIGHT'
        # Actualización de posición basada en teclado hecho aquí
        #gusano1.mover()
        #gusano2.mover()
        for i, gusano in enumerate(gusanos):
            gusano.mover()
            # Send and update positions using your network logic
            # Check for apple collision
            if gusano.segmentos[0] == manzana.posicion:
                gusano.segmentos.append(gusano.segmentos[-1])
                gusano.score += 1
                manzana.posicion = (random.randrange(0, ANCHO - TAM_BLOQUE, TAM_BLOQUE), random.randrange(0, ALTO - TAM_BLOQUE, TAM_BLOQUE))

        # Enviar la posición del gusano local al servidor y recibir la posición del otro gusano
        #respuesta = n.send(f"{gusano1.id}:{gusano1.segmentos[0][0]},{gusano1.segmentos[0][1]}")
        # La respuesta contiene la nueva posición del otro gusano
        #pos = respuesta.split(":")[1].split(",")

        #gusano2.segmentos[0] = (int(pos[0]), int(pos[1]))

        #gusano2.segmentos[0] = (int(float(pos[0])), int(float(pos[1])))

        pantalla.fill(NEGRO)

        #gusano1.dibujar(pantalla)
        #gusano2.dibujar(pantalla)
        for gusano in gusanos:
            gusano.dibujar(pantalla)
        manzana.dibujar(pantalla)
        draw_score(pantalla, gusanos[0].score, (50, 50))
        draw_score(pantalla, gusanos[1].score, (ANCHO - 150, 50), AZUL)

        #if gusano1.segmentos[0] == manzana.posicion:
            #gusano1.segmentos.append(gusano1.segmentos[-1])
            #gusano1.score += 1
            #manzana.posicion = (random.randrange(0, ANCHO - TAM_BLOQUE, TAM_BLOQUE), random.randrange(0, ALTO - TAM_BLOQUE, TAM_BLOQUE))

        #if gusano2.segmentos[0] == manzana.posicion:
            #gusano2.segmentos.append(gusano2.segmentos[-1])
            #gusano2.score += 1
            #manzana.posicion = (random.randrange(0, ANCHO - TAM_BLOQUE, TAM_BLOQUE), random.randrange(0, ALTO - TAM_BLOQUE, TAM_BLOQUE))

        #manzana.dibujar(pantalla)

        # Enviar información de la posición de los jugadores al servidor
        #n.send(f"{gusano1.id}:{gusano1.segmentos[0][0]},{gusano1.segmentos[0][1]}")
        #n.send(f"{gusano2.id}:{gusano2.segmentos[0][0]},{gusano2.segmentos[0][1]}")

        pygame.display.flip()
        reloj.tick(10)

if __name__ == "__main__":
    main()