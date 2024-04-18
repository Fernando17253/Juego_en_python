import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "10.10.0.36"  # IP del servidor
        self.port = 5555
        self.addr = (self.host, self.port)
        self.player_id = None
        self.connected = False  # Estado de la conexión

    def connect(self):
        if not self.connected:
            try:
                self.client.connect(self.addr)
                self.connected = True
                print("Connected to the server")
            except socket.error as e:
                print(f"Error connecting to the server: {e}")
                return str(e)

    def get_player_id(self):
        """
        Connect to the server and get the player ID.
        :return: str
        """
        if not self.connected:
            self.connect()
        try:
            self.player_id = self.client.recv(2048).decode()
            return self.player_id
        except socket.error as e:
            print(f"Error receiving data: {e}")
            return str(e)

    def send(self, data):
        """
        Send data to the server and receive a reply.
        :param data: str
        :return: str
        """
        if not self.connected:
            response = self.connect()
            if response is not None:
                return response  # Return error if connection failed
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            print(f"Error sending/receiving data: {e}")
            return str(e)

    def close(self):
        """
        Close the socket connection to the server.
        """
        if self.connected:
            try:
                self.client.close()
                self.connected = False
                print("Connection closed")
            except socket.error as e:
                print(f"Error closing the connection: {e}")
