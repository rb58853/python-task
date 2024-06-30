import socket
from models.chain import Chains


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

    def chains_count():
        count = input(
            "ingresa la cantidad de cadenas que tendra tu archivo de cadenas. Si desea calcular automatico escriba 'a' o 'auto'. Si no escribe un numero o ('auto'/'a') entonces se asume que no quiere especificar la cantidad de cadenas, por ejemplo presionando <enter>."
        )
        return count


class Client:
    def __init__(self, server_dir, server_port, base_files_path) -> None:
        self.server_dir = server_dir
        self.server_port = server_port
        self.base_files_path = base_files_path

    def generate_chains(self, filename="chains.txt"):
        chains = Chains()
        chains_to_autogenerate = ConsoleInputs.solicite_int()
        chains.generate_n_chains(chains_to_autogenerate)

        manual_chain = ConsoleInputs.set_chain()
        while manual_chain:
            chains.append(manual_chain)
            manual_chain = ConsoleInputs.set_chain()

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

        self.send_file(filepath, count)

    def send_file(self, filepath, count=None):
        # Crear un socket TCP/IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
