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

def parse_position(position_str):
    """
    Converts a position string formatted as 'x,y' into a tuple (x, y).
    
    Args:
    position_str (str): The position string to parse.

    Returns:
    tuple: The parsed position as a tuple (int, int), or (0, 0) if there is an error.
    """
    try:
        x, y = position_str.split(',')
        return (int(x), int(y))
    except ValueError:
        print("Error parsing position data")
        return (0, 0)

def main():
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO, ALTO])

    n = Network()
    id = int(n.get_player_id())
    gusano = Gusano(id, (ANCHO / 2, ALTO / 2))
    gusano_oponente = Gusano(1 - id, (ANCHO / 2, ALTO / 2 + TAM_BLOQUE))

    manzana = Manzana()
    reloj = pygame.time.Clock()

    running = True
    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            elif evento.type is pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    gusano.direccion = 'UP'
                elif evento.key == pygame.K_DOWN:
                    gusano.direccion = 'DOWN'
                elif evento.key == pygame.K_LEFT:
                    gusano.direccion = 'LEFT'
                elif evento.key == pygame.K_RIGHT:
                    gusano.direccion = 'RIGHT'

        gusano.mover()
        
        # Send the current position of the gusano to the server
        n.send(f"{gusano.id}:{gusano.segmentos[0][0]},{gusano.segmentos[0][1]}")

        # Receive the updated position of the opponent from the server
        opponent_data = n.receive()
        opponent_pos = parse_position(opponent_data)
        if opponent_pos:
            gusano_oponente.segmentos[0] = opponent_pos

        gusano_oponente.mover()

        pantalla.fill(NEGRO)
        gusano.dibujar(pantalla)
        gusano_oponente.dibujar(pantalla)
        manzana.dibujar(pantalla)
        pygame.display.flip()
        reloj.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
