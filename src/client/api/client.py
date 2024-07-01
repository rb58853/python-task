import socket
from models.chain import Chains
from config.config import ChainsConfig, ClientConfig, logging
from utils.clear_console import clear_console
import os
import codecs
import json


class ConsoleInputs:
    def solicite_int(message="Ingrese un número entero: "):
        while True:
            try:
                number = input(f"> {message}")
                number = None if number == "" else int(number)
                return number
            except ValueError:
                print(
                    f"< '{number}' No es un número entero válido. Intente nuevamente."
                )

    def set_chain():
        confirm = input("> Desea agregar una cadena manual (y/any)? ")
        if confirm != "y" and confirm != "yes":
            return None

        chain = input("> Escriba la cadena: ")
        return chain

    def set_name():
        name = input(
            "> Entra el nombre de tu archivo, no escriba nada y presiona enter si quiere usar el nombre default: "
        )
        return name if name != "" else None

    def checking(message: str = None):
        if message:
            check = input(f"> {message} (y/any)? ")
            return True if check == "y" or check == "yes" else False
        else:
            raise ValueError("message debe tener algun valor")


class Client:
    def __init__(
        self,
        server_dir=ClientConfig.DIR,
        server_port: int = ClientConfig.PORT,
        base_files_path=ClientConfig.BASE_DATA_PATH,
        protocol="TCP/IP",
    ) -> None:
        self.server_dir = server_dir
        self.server_port = server_port
        self.base_files_path = base_files_path
        self.chains: Chains = self.new_chains()
        self.protocol = "TCP/IP"

    def start(self):
        clear_console()
        while True:
            if self.create_and_send_chains():
                continue
            if self.send_from_filename():
                continue

            logging.info("Client closed")
            break

    def create_and_send_chains(self) -> bool:
        if ConsoleInputs.checking(
            "Desea crear una nueva lista de cadenas y enviarla al servidor"
        ):
            name = ConsoleInputs.set_name()
            self.new_chains(name if name else ChainsConfig.DEFAULT_NAME)
            self.generate_chains()
            self.send_from_chains()
            return True
        return False

    def new_chains(self, filename=ChainsConfig.DEFAULT_NAME):
        self.chains = Chains(name=filename, path=self.base_files_path)
        print(f"< Tu archivo llamara {filename}{ChainsConfig.EXT}")
        return self.chains

    def generate_chains(self):
        chains_to_autogenerate = ConsoleInputs.solicite_int(
            "Cuantas cadena desea agregar? "
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
            f"Se ha creado el archivo {self.chains.name} y sera enviado al servidor"
        )
        self.chains.to_file()
        return self.send(self.chains.fullpath)

    def send_from_filename(self):
        if ConsoleInputs.checking(
            f"Desea enviar un archivo existente al servidor. El archivo debe estar en la direccion '{self.base_files_path}' y solo puede seleccionar archivos con extension '{ChainsConfig.EXT}'"
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
            logging.error(f"El archivo {filepath} no existe")
            return False

        self.send_file(filepath)
        return True

    def send_file(self, filepath):
        # Crear un socket TCP/IP
        if self.protocol == "TCP/IP":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            raise NotImplementedError(
                "No existe implementacion para un protocolo distinto a 'TCP/IP'"
            )

        # Conectar al servidor
        server_address = (self.server_dir, self.server_port)
        logging.info(f"Conectándose a {server_address}")
        sock.connect(server_address)

        try:
            with open(filepath, "rb") as f:
                file_data = f.read().decode("utf-8")

            data = {}
            data["filename"] = filepath.split(os.path.sep)[-1]
            data["file_content"] = file_data
            data = json.dumps(data).encode("utf-8")
            sock.sendall(data)

            logging.info("Archivo enviado correctamente.")

            response_data = b""
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                response_data += data
            logging.info("Respuesta recibida correctamente.")
            self.create_response_file()
        except:
            logging.error("Archivo no enviado.")
        finally:
            sock.close()

    def create_response_file(data, dirpath=ClientConfig.BASE_RESPONSE_DATA_PATH):
        data = json.loads(data.decode("utf-8"))
        filename = data["name"]
        data = data["content"]
        filepath = os.path.sep.join([dirpath, filename])
        with open(filepath, "w") as file:
            file.write(data)
        return filepath
