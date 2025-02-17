from models.rules import ServerRules
from config.config import ChainsConfig
import logging
from tqdm import tqdm

class Chains:
    """
    ## `Chains`
    Receive the file name and its content; process the latter.

    ### Inputs:
    - `name`: The name of the file received.
    - `chains`: The content of the file received.
    """

    def __init__(self, name: str, chains) -> None:
        self.name = name
        self.chains = chains
        self.metrics = []
        self.errors = []

    @ServerRules()
    def eval_chain(self, chain, log=False):
        if chain["state"] == "ok":
            return {
                "error": None,
                "metric": self.calculate_metric(chain["chain"]),
            }
        else:
            if log:
                logging.error(chain["message"])
            return {"error": chain["message"], "metric": chain["metric"]}

    def calculate_metric(self, chain):
        numbers_count = 0
        spaces_count = chain.count(" ")
        if spaces_count == 0:
            raise Exception("Spaces count must be > 0")

        for number in ChainsConfig.NUMBERS:
            numbers_count += chain.count(number)
        letters_count = len(chain) - spaces_count - numbers_count
        return (letters_count * 1.5 + numbers_count * 2) / spaces_count

    def evaluate_all_chains(self):
        self.errors = []
        self.metrics = []
        for chain in tqdm(self.chains, desc="Evaluating chains", ncols=100):
            temp_eval = self.eval_chain(chain)
            self.errors.append(temp_eval["error"])
            self.metrics.append(temp_eval["metric"])

    def __str__(self) -> str:
        result_str = ""
        for chain, metric, error in zip(self.chains, self.metrics, self.errors):
            result_str += f"'{chain}': {metric}"
            if error:
                result_str += f" | Error: {error}"
            result_str += "\n"

        return result_str
