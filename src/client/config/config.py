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
    # Default name for chains file
    DEFAULT_NAME = "chains"

    # Extension for chains file
    EXT = ".txt"

    # Range for spaces count in a chain
    SPACES_RANGE = (3, 5)

    # Invalid positions for a space in a chain
    INVALID_SPACES_INDEX = [0, -1]

    # Min distance between spaces in a chain
    SPACES_MIN_DISTANCE = 1

    # Regular expression for valid characters in a chain
    VALID_CHARACTERS = r"^[a-zA-Z0-9 ]+$"

    # Characters that can be selected to form the chain
    CHOISED_CHARACTERS = (
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    )

    # Range of the lenght that a chain must have
    CHAIN_RANGE = (50, 100)

    # Default number of chains to create
    CHAINS_DEFAULT_COUNT = 1000000


class ClientConfig:
    # Path to dir data for create chains
    BASE_DATA_PATH = os.path.sep.join([base_path, "data", "client", "chains"])

    # Path to dir data for create server response file
    BASE_RESPONSE_DATA_PATH = os.path.sep.join(
        [base_path, "data", "client", "responses"]
    )

    # Dir socket to connect
    DIR = "127.0.0.1"

    # Port socket to connect
    PORT: int = 8080

    bytes_recv = 1024 * 1024
    bytes_sent = 1024 * 1024
