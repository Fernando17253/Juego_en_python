import asyncio

pos = {}
currentId = 0

async def handle_client(reader, writer):
    global currentId, pos
    # ...
    client_id = str(currentId)
    currentId += 1
    pos[client_id] = "0,0"  # Inicializar la posición del jugador con un valor por defecto

    try:
        writer.write(str.encode(client_id))
        await writer.drain()

        while True:
            data = await reader.read(2048)
            if not data:
                break
            reply = data.decode('utf-8')
            print(f"Recibiendo de {client_id}: " + reply)

            # Actualizar la posición para el cliente actual
            pos[client_id] = reply

            # Construir una cadena de datos con la posición de todos los jugadores excepto el actual
            positions_to_send = ';'.join([f"{key}:{value}" for key, value in pos.items() if key != client_id])
            print(f"Enviando a {client_id}: " + positions_to_send)

            # Enviar la cadena de posiciones al cliente actual
            writer.write(positions_to_send.encode())
            await writer.drain()

    except Exception as e:
        print(f"Error en la conexión con el cliente {client_id}: {e}")

    finally:
        # Remover la posición del cliente que se desconecta y cerrar la conexión
        pos.pop(client_id, None)
        writer.close()
        print(f"Conexion cerrada con el cliente {client_id}")

async def main():
    server = await asyncio.start_server(handle_client, '10.10.0.58', 5555)
    async with server:
        await server.serve_forever()

asyncio.run(main())
