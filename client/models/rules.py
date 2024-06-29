import functools
import inspect


class ClientRules:
    def __init__(self, len_spaces_range=(3, 5), valid_characters=r"^[a-zA-Z0-9 ]+$"):
        self.not_rules = ["__call__", "__init__"]
        self.len_spaces_range = len_spaces_range
        self.valid_characters = valid_characters

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            chains_self = args[0]
            chain = args[1]
            result_chain = ("ok", chain)

            rules = inspect.getmembers(ClientRules, predicate=inspect.isfunction)
            for rule_name, rule in rules:
                if rule_name not in self.not_rules:
                    rule(self, chain)

            return func(self=chains_self, chain=result_chain)

        return wrapper

    def spaces_rule(self, chain):
        # if chain[:1] == " " or chain[-1:] == " ":
        #     return ("error", "the chains can not contain spaces in init or end")

        count_spaces = chain.count(" ")
        min_spaces = self.len_spaces_range[0]
        max_spaces = self.len_spaces_range[1]

        if count_spaces > max_spaces or count_spaces < min_spaces:
            return SyntaxError(
                f"the chains should have between {min_spaces} and {max_spaces} spaces"
            )

        for i in range(len(chain) - 1):
            if chain[i] == " " and chain[i + 1] == " ":
                return SyntaxError("the chains can not contain consecutive spaces")

        return False

    def caracters_rule(self, chain):

        return False
