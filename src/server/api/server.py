import socket
from config.config import ServerConfig, logging
from models.chain import Chains
import json

class Server:
    def __init__(self, dir=ServerConfig.DIR, port=ServerConfig.PORT) -> None:
        self.dir = dir
        self.port = port

    def start(self):
        # TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Linking the socket with a specific port
        server_address = (self.dir, self.port)  # IP address and port
        print(f"Starting server on {server_address}")
        sock.bind(server_address)

        # Listening for incoming connections
        sock.listen(1)

        while True:
            print("Waiting connection...")
            connection, client_address = sock.accept()
            try:
                print(f"Connection from {client_address}")

                file_data = b""
                while True:
                    data = connection.recv(4096)
                    if not data:
                        break
                    if data.decode()[-3:] == "END":
                        temp = data[:-3]
                        file_data += data[:-3]
                        break
                    file_data += data

                data = json.loads(file_data.decode("utf-8"))
                logging.info(f"File {data['filename']} received successfully.")

                response = self.process_chain(data).encode("utf-8")
                connection.sendall(response)

            finally:
                connection.close()

    def process_chain(self, data):
        chains = Chains(name=data["filename"], chains=data["file_content"].split("\n"))
        chains.evaluate_all_chains()
        return json.dumps({"name": chains.name, "content": str(chains)})
