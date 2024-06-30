import socket
from models.chain import Chains
from config.config import ChainsConfig, ClientConfig
from utils.clear_console import clear_console
import os


class ConsoleInputs:
    def solicite_int():
        while True:
            try:
                number = input("Ingrese un número entero: ")
                number = 0 if number == "" else int(number)
                return number
            except ValueError:
                print("No es un número entero válido. Intente nuevamente.")

    def set_chain():
        confirm = input("desea agregar una cadena manual (y/any)? ")
        if confirm != "y" and confirm != "yes":
            return None

        chain = input("Ingrese la cadena: ")
        return chain

    def chains_name():
        name = input(
            "Entra en nombre de tu archivo, no escriba nada y presiona enter si quiere usar el nombre default: "
        )
        return name

    def chains_count():
        count = input(
            "ingresa la cantidad de cadenas que tendra tu archivo de cadenas. Si desea calcular automatico escriba 'a' o 'auto'. Si no escribe un numero o ('auto'/'a') entonces se asume que no quiere especificar la cantidad de cadenas, por ejemplo presionando <enter>."
        )
        return count

    def checking(message: str = None):
        if message:
            check = input(f"{message} (y/any): ")
            return True if check == "y" or check == "yes" else False
        else:
            raise ValueError("message debe tener algun valor")


class Client:
    def __init__(
        self,
        server_dir=ClientConfig.DIR,
        server_port=ClientConfig.PORT,
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

            break

    def create_and_send_chains(self) -> bool:
        if ConsoleInputs.checking(
            "Desea crear una nueva lista de cadenas y enviarla al servidor"
        ):
            name = ConsoleInputs.chains_name()
            self.new_chains(name if name != "" else ChainsConfig.DEFAULT_NAME)
            self.generate_chains()
            self.send_from_chains()
            return True
        else:
            return False

    def new_chains(self, filename=ChainsConfig.DEFAULT_NAME):
        self.chains = Chains(name=filename, path=self.base_files_path)
        print(f"Tu archivo llamara {filename}.txt")
        return self.chains

    def generate_chains(self):
        chains_to_autogenerate = ConsoleInputs.solicite_int()
        self.chains.generate_n_chains(chains_to_autogenerate)

        manual_chain = ConsoleInputs.set_chain()
        while manual_chain:
            self.chains.append(manual_chain)
            manual_chain = ConsoleInputs.set_chain()

        return self.chains

    def send_from_chains(self):
        if ConsoleInputs.checking(
            f"Desea crear y enviar el archivo {self.chains.name} al servidor"
        ):
            self.chains.to_file()
            self.send(self.chains.fullpath)

    def send_from_filename(self, filename: str):
        """
        Aqui hay que pasar la extension oligado al filename
        """
        filepath = os.path.sep.join([self.base_files_path, filename])
        self.send(filepath=filepath)

    def send(self, filepath):
        count = ConsoleInputs.chains_count()
        if count == "auto" or count == "a":
            with open(filepath, "rb") as f:
                file_data = f.read()
                count = file_data.count("\n")
        try:
            count = int(count)
        except:
            count = None
        if count:
            print(f"La cantidad de cadenas que se pasara por parametros es {count}")
        else:
            print(f"No se pasara el numero de cadenas por parametros al servidor")
        self.send_file(filepath, count)

    def send_file(self, filepath, count=None):
        # Crear un socket TCP/IP
        if self.protocol == "TCP/IP":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            raise NotImplementedError(
                "No existe implementacion para un protocolo distinto a 'TCP/IP'"
            )

        # Conectar al servidor
        server_address = (self.server_dir, self.server_port)
        print(f"Conectándose a {server_address}")
        sock.connect(server_address)

        try:
            # Enviar el nombre del archivo
            filename = filepath.split("/")[-1]
            sock.sendall(
                str(len(filename)).encode("utf-8")
            )  # Enviar longitud del nombre del archivo
            sock.sendall(filename.encode("utf-8"))  # Enviar nombre del archivo

            # Leer y enviar el contenido del archivo
            with open(filepath, "rb") as f:
                file_data = f.read()
                sock.sendall(file_data)

            print(f"Archivo {filename} enviado correctamente.")
        finally:
            sock.close()
            pass
