import socket
from config.config import ServerConfig, logging
import json

class Server:
    def __init__(
        self, dir=ServerConfig.DIR, port=ServerConfig.PORT, protocol="TCP/IP"
    ) -> None:
        self.dir = dir
        self.port = port
        self.protocol = protocol

    def start(self):
        if self.protocol == "TCP/IP":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Enlazar el socket con un puerto específico
        server_address = (self.dir, self.port)  # Dirección IP y puerto
        print(f"Iniciando servidor en {server_address}")
        sock.bind(server_address)

        # Escuchar conexiones entrantes
        sock.listen(1)

        while True:
            print("Esperando conexión...")
            connection, client_address = sock.accept()
            try:
                print(f"Conexión desde {client_address}")

                # Preparar para recibir datos
                file_data = b""
                while True:
                    data = connection.recv(4096)
                    if not data:
                        break
                    file_data += data

                data = json.loads(file_data.decode("utf-8"))
                print(f"Archivo recibido correctamente.")

            finally:
                connection.close()
