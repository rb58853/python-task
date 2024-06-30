from models.rules import ClientRules
from config.config import ChainsConfig, ClientConfig, logging
import random
import time
import os
from tqdm import tqdm


class ChainGenerate:
    def random_numbers_and_letters_chain():
        chain_len = random.randint(
            ChainsConfig.CHAIN_RANGE[0], ChainsConfig.CHAIN_RANGE[1]
        )
        return "".join(
            random.choice(ChainsConfig.CHOISED_CHARACTERS) for _ in range(chain_len)
        )

    def append_spaces(chain):
        # Rule count spaces
        spaces_count = random.randint(
            ChainsConfig.SPACES_RANGE[0], ChainsConfig.SPACES_RANGE[1]
        )

        # Rule invalid index spaces (beging and end)
        exclude = [
            (value + len(chain)) % len(chain)
            for value in ChainsConfig.INVALID_SPACES_INDEX
        ]
        includes = list(set(range(0, len(chain))) - set(exclude))

        for _ in range(spaces_count):
            if not len(includes):
                logging.error(f"The chain {chain} can't have more spaces")
                break
            index = random.choice(includes)
            chain = chain[:index] + " " + chain[index + 1 :]

            includes.remove(index)

            # Rule consecutive spaces (min spaces distance)
            for invalid_index in range(
                max(index - ChainsConfig.SPACES_MIN_DISTANCE, 0),
                min(index + ChainsConfig.SPACES_MIN_DISTANCE + 1, len(chain)),
            ):
                if invalid_index in includes:
                    includes.remove(invalid_index)
            ##########################

        return chain if chain.count(" ") >= ChainsConfig.SPACES_RANGE[0] else None

    def generate():
        chain = ChainGenerate.random_numbers_and_letters_chain()
        chain = ChainGenerate.append_spaces(chain)
        return chain


class Chains:
    def __init__(
        self,
        name: str = ChainsConfig.DEFAULT_NAME,
        path: str = ClientConfig.BASE_DATA_PATH,
    ) -> None:
        self.chains = []
        self.basepath = path
        self.name = name
        self.fullpath = os.path.sep.join([path, name + ChainsConfig.EXT])

    @ClientRules()
    def append(self, chain, log=True):
        if chain:
            self.fast_append(chain)
            if log:
                logging.info(f"The chain '{chain}' was append")

    def append_autogenerate_chain(self):
        chain = ChainGenerate.generate()
        if chain:
            self.fast_append(chain)
        else:
            logging.warning(f"The chain '{chain}' was not append")

    def generate_n_chains(self, n=ChainsConfig.CHAINS_COUNT):
        init_time = time.time()
        for _ in tqdm(range(n), desc="Generating chains", ncols=100):
            self.append_autogenerate_chain()

        duration = time.time() - init_time
        logging.info(f"append {n} chains in {duration}s")

    def to_file(self):
        if not os.path.exists(self.basepath):
            os.makedirs(self.basepath)

        with open(self.fullpath, "w") as file:
            file.write(str(self))
            file.close()
        return self.fullpath

    def send(self, chains_count=None):
        pass

    def __str__(self) -> str:
        return "\n".join([chain for chain in self])

    def __len__(self) -> int:
        return len(self.chains)

    def __iter__(self):
        return iter(self.chains)

    def fast_append(self, chain):
        self.chains.append(chain)
