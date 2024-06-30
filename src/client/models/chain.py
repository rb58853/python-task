from client.models.rules import ClientRules
from client.config.config import ClientConfig
import logging
import random
import time
from tqdm import tqdm

class ChainGenerate:
    def random_numbers_and_letters_chain():
        chain_len = random.randint(
            ClientConfig.CHAIN_RANGE[0], ClientConfig.CHAIN_RANGE[1]
        )
        return "".join(
            random.choice(ClientConfig.CHOISED_CHARACTERS) for _ in range(chain_len)
        )

    def append_spaces(chain):
        # Rule count spaces
        spaces_count = random.randint(
            ClientConfig.SPACES_RANGE[0], ClientConfig.SPACES_RANGE[1]
        )

        # Rule invalid index spaces (beging and end)
        exclude = [
            (value + len(chain)) % len(chain)
            for value in ClientConfig.INVALID_SPACES_INDEX
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
                max(index - ClientConfig.SPACES_MIN_DISTANCE, 0),
                min(index + ClientConfig.SPACES_MIN_DISTANCE + 1, len(chain)),
            ):
                if invalid_index in includes:
                    includes.remove(invalid_index)
            ##########################

        return chain if chain.count(" ") > ClientConfig.SPACES_RANGE[0] else None

    def generate():
        chain = ChainGenerate.random_numbers_and_letters_chain()
        chain = ChainGenerate.append_spaces(chain)
        return chain


class Chains:
    def __init__(self) -> None:
        self.chains = []

    @ClientRules()
    def append_with_rules(self, chain):
        if chain[0]:
            self.append(chain[1])
            logging.info(f"The chain '{chain[1]}' was append")
        else:
            logging.warning(f"The chain '{chain[1]}' was not append")

    def append_autogenerate_chain(self):
        chain = ChainGenerate.generate()
        if chain:
            self.append(chain)

    def generate_n_chains(self, n=ClientConfig.CHAINS_COUNT):
        init_time = time.time()
        for _ in tqdm(range(n), desc="Generating chains", ncols=100):
            self.append_autogenerate_chain()

        duration = time.time() - init_time
        logging.warning(f"append {n} chains in {duration}s")

    def to_file(self):
        return self.chains

    def send(self, chains_count=None):
        pass

    def __str__(self) -> str:
        return "\n".join([chain for chain in self])

    def __len__(self) -> int:
        return len(self.chains)

    def __iter__(self):
        return iter(self.chains)

    def append(self, chain):
        self.chains.append(chain)
