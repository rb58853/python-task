import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class ChainsConfig:
    # Invalid Substrings for All Letter Sizes, Lowercase or Uppercase
    INVALIDS_SUBCHAIN = ["aa"]

    # Numbers definition
    NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


class ServerConfig:
    # server dir
    DIR = "127.0.0.1"

    # server port
    PORT: int = 8080

    bytes_recv = 1024*1024
    bytes_sent = 1024*1024
