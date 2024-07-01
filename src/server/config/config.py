import os
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
base_path = os.getcwd()
base_path = (
    base_path
    if base_path.split(os.path.sep)[-1] == "python-task"
    else os.path.sep.join(
        [
            dir
            for dir in base_path.split(os.path.sep)
            if dir != "src" and dir != "client"
        ]
    )
)


class ChainsConfig:
    INVALIDS_SUBCHAIN = ["aa"]
    NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

class ServerConfig:
    BASE_DATA_PATH = os.path.sep.join([os.getcwd(), "data", "server", "chains"])
    DIR = "127.0.0.1"
    PORT: int = 8080
