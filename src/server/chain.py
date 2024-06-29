from server.rules import ServerRules
import logging


class Chains:
    def __init__(self) -> None:
        self.chains = []

    @ServerRules()
    def metric_chain(self, chain):
        if chain["state"] == "ok":
            return self.calculate_metric(chain["chain"])
        else:
            logging.error(chain["message"])
            return chain["metric"]

    def calculate_metric(self, chain):
        pass

    def get_chains(self, chains):
        for chain in chains:
            self.metric_chain(chain)
