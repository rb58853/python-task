from client.models.rules import ClientRules
from client.config.config import ClientConfig
import logging
import random


class ChainGenerate:
    def random_numbers_and_letters_chain():
        chain_len = random.randint(
            ClientConfig.CHAIN_RANGE[0], ClientConfig.CHAIN_RANGE[1] + 1
        )
        return "".join(
            random.choice(ClientConfig.CHOISED_CHARACTERS) for _ in range(chain_len)
        )

    def append_spaces(chain):
        spaces_count = random.randint(
            ClientConfig.SPACES_RANGE[0], ClientConfig.SPACES_RANGE[1] + 1
        )
        exclude = [
            (value + len(chain)) % len(chain)
            for value in ClientConfig.INVALID_SPACES_INDEX
        ]
        includes = list(set(range(0, len(chain))) - set(exclude))

        for _ in range(len(spaces_count)):
            if not len(includes):
                logging.error(f"The chain {chain} can't have more spaces")
                break
            index = random.choice(includes)
            includes.pop(index)
            chain[index] = " "

        return chain if chain.count(" ") > ClientConfig.SPACES_RANGE[0] else None

    def generate():
        chain = ChainGenerate.random_numbers_and_letters_chain()
        chain = ChainGenerate.append_spaces(chain)
        return chain


class Chains:
    def __init__(self) -> None:
        self.chains = []

    @ClientRules()
    def append_chain(self, chain):
        if chain[0]:
            self.append(chain[1])
            logging.info(f"The chain '{chain[1]}' was append")
        else:
            logging.warning(f"The chain '{chain[1]}' was not append")

    def append_autogenerate_chain(self):
        self.append(ChainGenerate.random_numbers_and_letters_chain())

    def generate_n_chains(self, n=ClientConfig.CHAINS_COUNT):
        while n > 0:
            n -= 1
            self.autogenerate_chain()

    def to_file(self):
        return self.chains

    def send(self, chains_count=None):
        pass

    def __str__(self) -> str:
        return "\n".join([chain for chain in self.chains])

    def __len__(self) -> int:
        return len(self.chains)

    def append(self, chain):
        self.chains.append(chain)
