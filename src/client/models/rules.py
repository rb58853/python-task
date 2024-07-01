import inspect
import re
from utils.utils import in_range
from config.config import ChainsConfig, logging


class ClientRules:
    """
    ## `ClientRules`
    When using this class as a decorator for a function, it will analyze the passed string to determine if it is valid or not. In case it is not valid according to a given rule, an exception will be thrown from the function that applies the rule.
    Each of the functions in this class constitutes a rule for the generation of strings by the client. The functions whose names are contained in `self.not_rules` do not constitute a rule.

    ### Rules:
    - `invalid_pos_spaces_rule`: This rule is equivalent to not being able to have spaces at the end or beginning of a string. It is an extended mode where all positions where a space cannot be allowed can be passed.
        - `ChainsConfig.INVALID_SPACES_INDEX`: Invalid positions for a space.
    - `count_spaces_rule`: This rule defines that the number of spaces in a string must be within a given range.
        - `ChainsConfig.SPACES_RANGE`: Range of the number of spaces that a string can have.
    - `min_spaces_distance_rule`: Minimum distance between two spaces. It is an extended version of the "Two consecutive spaces" rule. Two consecutive spaces are equivalent to the minimum distance between spaces needing to be 1.
        - `ChainsConfig.SPACES_MIN_DISTANCE`: Minimum distance that must exist between two spaces.
    - `characters_rule`: Rule that defines the valid characters for a string.
        - `ChainsConfig.VALID_CHARACTERS`: Valid characters that a string can have in the form of a regular expression, for example `r"^[a-zA-Z0-9 ]+$"`.
    - `len_chain_rule`: A string must have a size within a given range.
        - `ChainsConfig.CHAIN_RANGE`: Size range that the string must have."""

    def __init__(self):
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
                logging.warning(f"The chain '{chain}' was not added.")
                chain = None

            return func(self=chains_self, chain=chain)

        return wrapper

    def invalid_pos_spaces_rule(self, chain):
        for index in ChainsConfig.INVALID_SPACES_INDEX:
            if chain[index] == " ":
                raise SyntaxError(
                    f"The chains cannot contain spaces in the positions {ChainsConfig.INVALID_SPACES_INDEX}."
                )

    def count_spaces_rule(self, chain):
        min_count = ChainsConfig.SPACES_RANGE[0]
        max_count = ChainsConfig.SPACES_RANGE[1]
        if not in_range(chain.count(" "), min_count, max_count):
            raise SyntaxError(
                f"The chains must have a count of spaces between {min_count} and {max_count}."
            )

    def min_spaces_distance_rule(self, chain):
        for i in range(len(chain) - 1):
            if chain[i] == " ":
                for character in chain[
                    i + 1 : i + ChainsConfig.SPACES_MIN_DISTANCE + 1
                ]:
                    if character == " ":
                        raise SyntaxError(
                            f"There must be a distance of at least {ChainsConfig.SPACES_MIN_DISTANCE} between spaces."
                        )

    def characters_rule(self, chain):
        valid_characters = ChainsConfig.VALID_CHARACTERS
        if not bool(re.match(valid_characters, chain)):
            raise SyntaxError(
                f"Chains can only contain characters included in the regular expression: '{valid_characters}'."
            )

    def len_chain_rule(self, chain):
        len_chain_range = ChainsConfig.CHAIN_RANGE
        if not in_range(len(chain), len_chain_range[0], len_chain_range[1]):
            raise SyntaxError(
                f"The chains must have a length between {len_chain_range[0]} and {len_chain_range[1]} characters."
            )
