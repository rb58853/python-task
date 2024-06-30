import inspect
import re
from utils.utils import in_range
from config.config import ChainsConfig, logging


class ClientRules:
    """
    ### Rules:
        - `spaces_rule:` Esta regla esta definida por tal cosa. La cantida minima y maxima de espacios es variable, solo debe pasar como argumento al decorador `len_spaces_range=(3, 5)` donde 3 es e minimo de espacios y 5 es el maximo
    """

    def __init__(
        self,
        len_spaces_range=ChainsConfig.SPACES_RANGE,
        valid_characters=ChainsConfig.VALID_CHARACTERS,
        len_chain_range=ChainsConfig.CHAIN_RANGE,
    ):
        self.len_spaces_range = len_spaces_range
        self.valid_characters = valid_characters
        self.len_chain_range = len_chain_range
        self.not_rules = ["__call__", "__init__"]

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            chains_self = args[0]
            chain = args[1]
            is_valid = True

            rules = inspect.getmembers(ClientRules, predicate=inspect.isfunction)
            for rule_name, rule in rules:
                if rule_name not in self.not_rules:
                    try:
                        rule(self, chain)
                    except Exception as e:
                        logging.error(f"{type(e).__name__}: {e} Chain: '{chain}'.")
                        is_valid = False

            if not is_valid:
                logging.warning(f"The chain '{chain}' was not append")
                chain = None

            return func(self=chains_self, chain=chain)

        return wrapper

    def invalid_pos_spaces_rule(self, chain):
        for index in ChainsConfig.INVALID_SPACES_INDEX:
            if chain[index] == " ":
                raise SyntaxError("the chains can not contain spaces in init or end")

    def count_spaces_rule(self, chain):
        if not in_range(
            chain.count(" "), self.len_spaces_range[0], self.len_spaces_range[1]
        ):
            raise SyntaxError(
                f"the chains should have between {self.len_spaces_range[0]} and {self.len_spaces_range[1]} spaces"
            )

    def min_spaces_distance_rule(self, chain):
        for i in range(len(chain) - 1):
            if chain[i] == " ":
                for character in chain[
                    i + 1 : i + ChainsConfig.SPACES_MIN_DISTANCE + 1
                ]:
                    if character == " ":
                        raise SyntaxError(
                            "the chains can not contain consecutive spaces."
                        )

    def characters_rule(self, chain):
        if not bool(re.match(self.valid_characters, chain)):
            raise SyntaxError(
                f"the chains only can has caracters '{self.valid_characters}'."
            )

    def len_chain_rule(self, chain):
        if not in_range(len(chain), self.len_chain_range[0], self.len_chain_range[1]):
            raise SyntaxError(
                f"the chains should have between {self.len_chain_range[0]} and {self.len_chain_range[1]} characters."
            )
