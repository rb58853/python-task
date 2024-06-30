import os
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class ChainConfig:
    INVALIDS_SUBCHAIN = ["aa"]


class ServerConfig:
    BASE_DATA_PATH = os.path.sep.join([os.getcwd(), "data", "server", "chains"])
    DIR = "127.0.0.1"
    PORT: int = 8080
