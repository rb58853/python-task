import os
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class ChainsConfig:
    DEFAULT_NAME = "chains"
    EXT = ".txt"

    SPACES_RANGE = (3, 5)
    INVALID_SPACES_INDEX = [0, -1]
    SPACES_MIN_DISTANCE = (
        1  # Valor 1 es equivalente a que no pueden haber espacios consecutivos
    )

    VALID_CHARACTERS = r"^[a-zA-Z0-9 ]+$"
    CHOISED_CHARACTERS = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    )

    CHAIN_RANGE = (50, 100)
    CHAINS_COUNT = 1000000


class ClientConfig:
    BASE_DATA_PATH = os.path.sep.join([os.getcwd(), "data", "client", "chains"])
    DIR = "127.0.0.1"
    PORT: int = 8080
