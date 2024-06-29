from client.models.rules import ClientRules
import logging

class Chains:
    def __init__(self) -> None:
        self.chains = []

    @ClientRules()
    def append_chain(self, chain):
        if chain[0]:
            self.chains.append(chain[1])
        else:
            logging.warning(f"The chain '{chain[1]}' was not append")

    def to_file(self):
        return self.chains

    def send(self):
        pass

