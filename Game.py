import pygame
import random
from network import Network
import asyncio
import threading

# Definir colores
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Tamaño de la pantalla y bloques
ANCHO = 800
ALTO = 600
TAM_BLOQUE = 20

def start_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

new_loop = asyncio.new_event_loop()
t = threading.Thread(target=start_asyncio_loop, args=(new_loop,))
t.start()

class Gusano:
    def __init__(self, id, start_pos):
        self.id = id
        self.segmentos = [start_pos]
        self.direccion = 'RIGHT'
        self.score = 0

    async def mover(self):
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

def parse_positions(data_str):
    player_positions = {}
    try:
        # Divide la cadena de datos por ";" para obtener los datos de cada jugador.
        players_data = data_str.split(';')
        for player_data in players_data:
            # Divide cada sección por ":" para separar el id del jugador de sus coordenadas.
            player_id, position = player_data.split(':')
            # Divide las coordenadas por "," y convierte los valores a enteros.
            x, y = map(float, position.split(','))
            player_positions[int(player_id)] = (int(x), int(y))
    except ValueError as e:
        print(f"Error parsing position data: {data_str} - {e}")

    return player_positions

async def main():
    pygame.init()
    pantalla = pygame.display.set_mode([ANCHO, ALTO])
    n = Network()
    await n.connect()

    id = await n.get_player_id()
    gusano = Gusano(int(id), (ANCHO / 2, ALTO / 2))
    gusano_oponente = Gusano(1 - int(id), (ANCHO / 2, ALTO / 2 + TAM_BLOQUE))

    manzana = Manzana()
    reloj = pygame.time.Clock()
    running = True

    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    gusano.direccion = 'UP'
                elif evento.key == pygame.K_DOWN:
                    gusano.direccion = 'DOWN'
                elif evento.key == pygame.K_LEFT:
                    gusano.direccion = 'LEFT'
                elif evento.key == pygame.K_RIGHT:
                    gusano.direccion = 'RIGHT'

        await asyncio.gather(
            gusano.mover(),
            update_game_state(n, gusano, gusano_oponente)
        )

        pantalla.fill(NEGRO)
        gusano.dibujar(pantalla)
        gusano_oponente.dibujar(pantalla)
        manzana.dibujar(pantalla)
        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()

async def update_game_state(network, gusano, gusano_oponente):
    # Enviar la posición actual del gusano al servidor.
    await network.send(f"{gusano.id}:{gusano.segmentos[0][0]},{gusano.segmentos[0][1]}")

    # Recibir los datos de las posiciones de los oponentes desde el servidor.
    opponent_data = await network.receive()
    
    # Parsear la cadena de posiciones recibida en un diccionario de posiciones.
    player_positions = parse_positions(opponent_data)
    
    # Actualizar la posición del oponente si la nueva posición está disponible.
    if gusano_oponente.id in player_positions:
        gusano_oponente.segmentos[0] = player_positions[gusano_oponente.id]

# To run the asyncio program
if __name__ == "__main__":
    asyncio.run(main())
