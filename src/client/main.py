from api.client import Client
from config.config import ClientConfig
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, help="Server to connect port")
parser.add_argument("--dir", type=str, help="Server to connect dir")
parser.add_argument("--filespath", type=str, help="path of generated files")
parser.add_argument("--responsespath", type=str, help="path of response files")
args = parser.parse_args()

port = args.port if args.port else ClientConfig.PORT
dir = args.dir if args.dir else ClientConfig.DIR
filespath = args.filespath if args.filespath else ClientConfig.BASE_DATA_PATH
responsespath = (
    args.responsespath if args.responsespath else ClientConfig.BASE_RESPONSE_DATA_PATH
)

Client(
    server_port=port, server_dir=dir, files_path=filespath, responses_path=responsespath
).start()
