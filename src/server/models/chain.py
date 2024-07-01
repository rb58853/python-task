from models.rules import ServerRules
from config.config import ChainsConfig
import logging


class Chains:
    def __init__(self, name: str, count, chains) -> None:
        self.name = name
        self.count = count
        self.chains = chains
        self.metrics = []
        self.errors: list[str] = []

    @ServerRules()
    def eval_chain(self, chain):
        if chain["state"] == "ok":
            return {
                "error": None,
                "metric": self.calculate_metric(chain["chain"]),
            }
        else:
            logging.error(chain["message"])
            return {"error": chain["message"], "metric": chain["metric"]}

    def calculate_metric(self, chain):
        return 1

    def get_chains(self):
        for index, chain in zip(range(len(self.chains)), self.chains):
            temp_eval = self.metric_chain(chain)
            self.errors[index] = temp_eval["error"]
            self.metrics[index] = temp_eval["metric"]
