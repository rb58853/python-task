import socket
from config.config import ServerConfig, logging
from models.chain import Chains
import json
from tqdm import tqdm

""" TODO
- Create a progress bar for received files. To do this, I must first send the size of the data that will be passed through the socket, so that the receiver can receive it and create a progress bar with this information. Similar to what is done with 'END'.
"""


class Server:
    def __init__(self, dir=ServerConfig.DIR, port=ServerConfig.PORT) -> None:
        self.dir = dir
        self.port = port

    def start(self):
        # TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Linking the socket with a specific port
        server_address = (self.dir, self.port)  # IP address and port
        logging.info(f"Starting server on {server_address}")
        sock.bind(server_address)

        # Listening for incoming connections
        sock.listen(1)

        while True:
            logging.info("Waiting connection...")
            connection, client_address = sock.accept()
            try:
                print(f"Connection from {client_address}")

                bytes_recv = ServerConfig.bytes_recv

                file_data = b""
                while True:
                    data = connection.recv(bytes_recv)
                    if not data:
                        break
                    if data.decode()[-3:] == "END":
                        file_data += data[:-3]
                        break
                    file_data += data

                data = json.loads(file_data.decode("utf-8"))
                logging.info(f"File {data['filename']} received successfully.")

                response = self.process_chain(data).encode("utf-8")

                sent_progress_bar = tqdm(
                    total=len(response),
                    desc="Sending response to client",
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                )
                sent_progress_bar.update(bytes_recv)

                bytes_sent = ServerConfig.bytes_sent
                while len(response) > 0:
                    connection.sendall(response[:bytes_sent])
                    response = response[bytes_sent:]
                    sent_progress_bar.update(bytes_sent)
                sent_progress_bar.close()

            finally:
                connection.close()

    def process_chain(self, data):
        chains = Chains(name=data["filename"], chains=data["file_content"].split("\n"))
        chains.evaluate_all_chains()
        return json.dumps({"name": chains.name, "content": str(chains)})
