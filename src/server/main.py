from api.server import Server
from config.config import ServerConfig
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, help="Server port")
parser.add_argument("--dir", type=str, help="Server dir")
args = parser.parse_args()

port = args.port if args.port else ServerConfig.PORT
dir = args.dir if args.dir else ServerConfig.DIR

Server(port=port, dir=dir).start()
