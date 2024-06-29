# import inspect
# import logging
import re
from utils.utils import in_range
from models.rules import Rules


class ClientRules(Rules):
    """
    ### Rules:
        - `spaces_rule:` Esta regla esta definida por tal cosa. La cantida minima y maxima de espacios es variable, solo debe pasar como argumento al decorador `len_spaces_range=(3, 5)` donde 3 es e minimo de espacios y 5 es el maximo
    """

    def __init__(
        self,
        len_spaces_range=(3, 5),
        valid_characters=r"^[a-zA-Z0-9 ]+$",
        len_chain_range=(50, 100),
    ):
        self.len_spaces_range = len_spaces_range
        self.valid_characters = valid_characters
        self.len_chain_range = len_chain_range

        not_rules = ["__call__", "__init__"]
        super().__init__(rules_class=ClientRules, not_rules=not_rules)

    def end_init_spaces_rule(self, chain):
        if chain[:1] == " " or chain[-1:] == " ":
            raise SyntaxError("the chains can not contain spaces in init or end")

    def count_spaces_rule(self, chain):
        if not in_range(
            chain.count(" "), self.len_spaces_range[0], self.len_spaces_range[1]
        ):
            raise SyntaxError(
                f"the chains should have between {self.len_spaces_range[0]} and {self.len_spaces_range[1]} spaces"
            )

    def consecutive_spaces_rule(self, chain):
        for i in range(len(chain) - 1):
            if chain[i] == " " and chain[i + 1] == " ":
                raise SyntaxError("the chains can not contain consecutive spaces.")

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
