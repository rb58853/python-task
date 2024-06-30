from models.chain import Chains
from config.config import ClientConfig

chains = Chains()
chains.generate_n_chains(10000)
file = chains.to_file()
