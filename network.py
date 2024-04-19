import asyncio
import socket

class Network:
    def __init__(self, host="10.10.0.58", port=5555):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        print("Connected to the server")
        
    async def get_player_id(self):
        if not self.writer:
            await self.connect()
        self.writer.write(b'get_id')
        await self.writer.drain()
        data = await self.reader.read(2048)
        return data.decode()

    async def send(self, data):
        try:
            self.writer.write(data.encode())
            await self.writer.drain()
        except Exception as e:
            print(f"Send Error: {e}")
            await self.connect()  # Reconnect and try again
            self.writer.write(data.encode())
            await self.writer.drain()

    async def receive(self):
        data = await self.reader.read(2048)
        return data.decode()

    def close(self):
        if self.writer:
            self.writer.close()
            print("Connection closed")
