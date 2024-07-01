from models.rules import ServerRules
from config.config import ChainsConfig
import logging


class Chains:
    def __init__(self, name: str, count, chains) -> None:
        self.name = name
        self.count = count
        self.chains = chains
        self.metrics = []
        self.errors = []

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
        numbers_count = 0
        spaces_count = chain.count(" ")
        for number in ChainsConfig.NUMBERS:
            numbers_count += chain.count(number)
        letters_count = len(chain) - spaces_count - numbers_count
        return (letters_count * 1.5 + numbers_count * 2) / spaces_count

    def evaluate_all_chains(self):
        for index, chain in enumerate(self.chains):
            temp_eval = self.metric_chain(chain)
            self.errors[index] = temp_eval["error"]
            self.metrics[index] = temp_eval["metric"]

    def __str__(self) -> str:
        result_str = ""
        for chain, metric, error in zip(self.chains, self.metrics, self.errors):
            result_str += f"'{chain}': {metric}"
            if error:
                result_str += f" | Error: {error}"
            result_str += "\n"

        return result_str