import socket
from models.chain import Chains
from config.config import ChainsConfig, ClientConfig, logging
from utils.clear_console import clear_console
import os
import json
from tqdm import tqdm

""" TODO
- Create a progress bar for received files. To do this, I must first send the size of the data that will be passed through the socket, so that the receiver can receive it and create a progress bar with this information. Similar to what is done with 'END'.
"""

class ConsoleInputs:
    def solicite_int(message="Enter an integer: "):
        while True:
            try:
                number = input(f"> {message}")
                number = None if number == "" else int(number)
                return number
            except ValueError:
                print(f"< '{number}' is not an integer. Try again.")

    def set_chain():
        confirm = input("> Do you want to add a string manually? (y/any)? ")
        if confirm != "y" and confirm != "yes":
            return None

        chain = input("> Write the string here: ")
        return chain

    def set_name():
        name = input(
            "> Enter the name of your file, just press <enter> if you want to use the default name: "
        )
        return name if name != "" else None

    def checking(message: str = None):
        if message:
            check = input(f"> {message} (y/any)? ")
            return True if check == "y" or check == "yes" else False
        else:
            raise ValueError("message must have any value")


class Client:
    """
    ## `Client`
    Client responsible for sending files to the server. It also handles creating and saving strings, as well as storing information received from the server. To start the client, run the `start` function.

    ### inputs
    - `server_dir`: server address to which it should connect. Default: `ClientConfig.DIR`.
    - `server_port`: server port number to which it should connect. Default: `ClientConfig.PORT`.
    - `files_path`: location where generated string files by the client will be saved. Default: `ClientConfig.BASE_DATA_PATH`
    - `responses_path`: location where server response files will be saved. Default: `ClientConfig.BASE_RESPONSE_DATA_PATH`
    """

    def __init__(
        self,
        server_dir=ClientConfig.DIR,
        server_port: int = ClientConfig.PORT,
        files_path=ClientConfig.BASE_DATA_PATH,
        responses_path=ClientConfig.BASE_RESPONSE_DATA_PATH,
    ) -> None:

        self.server_dir = server_dir
        self.server_port = server_port
        self.base_files_path = files_path
        self.base_response_data_path = responses_path

        self.chains: Chains = self.new_chains()

    def start(self):
        """
        ## `start`
        Initialize the client and execute a loop to create or send strings to the server.
        """
        clear_console()
        while True:
            if self.create_and_send_chains():
                print("\n\n")
                continue
            if self.send_from_filename():
                print("\n\n")
                continue

            logging.info("Client closed")
            break

    def create_and_send_chains(self) -> bool:
        if ConsoleInputs.checking(
            "Do you want to create a new list of strings and send it to the server?"
        ):
            name = ConsoleInputs.set_name()
            self.new_chains(name if name else ChainsConfig.DEFAULT_NAME)
            self.generate_chains()
            self.send_from_chains()
            return True
        return False

    def new_chains(self, filename=ChainsConfig.DEFAULT_NAME):
        self.chains = Chains(name=filename, path=self.base_files_path)
        logging.info(f"Your file will be named {filename}{ChainsConfig.EXT}")
        return self.chains

    def generate_chains(self):
        chains_to_autogenerate = ConsoleInputs.solicite_int(
            "How many strings would you like to add? "
        )
        if chains_to_autogenerate:
            self.chains.generate_n_chains(chains_to_autogenerate)
        else:
            self.chains.generate_n_chains()

        manual_chain = ConsoleInputs.set_chain()
        while manual_chain:
            self.chains.append(manual_chain)
            manual_chain = ConsoleInputs.set_chain()

        return self.chains

    def send_from_chains(self):
        logging.info(
            f"The file {self.chains.name} has been created and will be sent to the server."
        )
        self.chains.to_file()
        return self.send(self.chains.fullpath)

    def send_from_filename(self):
        if ConsoleInputs.checking(
            f"Do you want to send an existing file to the server? The file must be located at address '{self.base_files_path}' and can only select files with extension '{ChainsConfig.EXT}'."
        ):

            name = ConsoleInputs.set_name()
            filename = name if name else ChainsConfig.DEFAULT_NAME
            if filename[-(len(ChainsConfig.EXT)) :] != ChainsConfig.EXT:
                filename += ChainsConfig.EXT

            filepath = os.path.sep.join([self.base_files_path, filename])
            return self.send(filepath=filepath)
        return False

    def send(self, filepath):
        if not os.path.exists(filepath):
            logging.error(f"The file {filepath} does not exist.")
            return False

        self.send_file(filepath)
        return True

    def send_file(self, filepath):
        # Creating a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to server
        server_address = (self.server_dir, self.server_port)
        logging.info(f"Connecting to {server_address}")
        sock.connect(server_address)

        try:
            with open(filepath, "rb") as f:
                file_data = f.read().decode("utf-8")

            data = {}
            data["filename"] = filepath.split(os.path.sep)[-1]
            data["file_content"] = file_data
            data = json.dumps(data).encode("utf-8")

            bytes_sent = ClientConfig.bytes_sent
            progress_bar = tqdm(
                total=len(data),
                desc="Sending data to server",
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            )

            # send data with progress
            while len(data) > 0:
                sock.sendall(data[:bytes_sent])
                data = data[bytes_sent:]
                progress_bar.update(bytes_sent)

            progress_bar.close()

            end_message = "END".encode()
            sock.sendall(end_message)
            logging.info("File sent successfully.")

            response_data = b""

            bytes_recv = ClientConfig.bytes_recv
            while True:
                data = sock.recv(bytes_recv)
                if not data:
                    break
                response_data += data

            try:
                logging.info(
                    f"A file with the server's response has been created in {self.create_response_file(response_data)}."
                )
            except:
                logging.error(
                    f"The file with the server's response has not been created."
                )

        except Exception as e:
            logging.error(f"The process did not execute correctly: {e}")
        finally:
            sock.close()

    def create_response_file(self, data):
        """ """
        dirpath = self.base_response_data_path
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        data = json.loads(data.decode("utf-8"))
        filename = data["name"]
        data = data["content"]
        filepath = os.path.sep.join([dirpath, filename])

        with open(filepath, "w") as file:
            file.write(data)
        return filepath
