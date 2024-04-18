import pygame
import random
from network import Network

# Definir colores
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Tamaño de la pantalla y bloques
ANCHO = 800
ALTO = 600
TAM_BLOQUE = 20

class Gusano:
    def __init__(self, id, start_pos):
        self.id = id
        self.segmentos = [start_pos]
        self.direccion = 'RIGHT'
        self.score = 0

    def mover(self):
        cabeza = self.segmentos[0]
        x_offset = y_offset = 0
        if self.direccion == 'UP': y_offset = -TAM_BLOQUE
        elif self.direccion == 'DOWN': y_offset = TAM_BLOQUE
        elif self.direccion == 'LEFT': x_offset = -TAM_BLOQUE
        elif self.direccion == 'RIGHT': x_offset = TAM_BLOQUE
        nueva_cabeza = ((cabeza[0] + x_offset) % ANCHO, (cabeza[1] + y_offset) % ALTO)
        self.segmentos.insert(0, nueva_cabeza)
        self.segmentos.pop()

    def dibujar(self, pantalla):
        color = VERDE if self.id == 0 else AZUL
        for segmento in self.segmentos:
            pygame.draw.rect(pantalla, color, [segmento[0], segmento[1], TAM_BLOQUE, TAM_BLOQUE])

class Manzana:
    def __init__(self):
        self.posicion = (random.randrange(0, ANCHO, TAM_BLOQUE), random.randrange(0, ALTO, TAM_BLOQUE))

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, ROJO, [self.posicion[0], self.posicion[1], TAM_BLOQUE, TAM_BLOQUE])

def main():
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO, ALTO])
    n = Network()
    id = int(n.id)  # Asumiendo que `id` es un atributo de `Network`
    gusano = Gusano
