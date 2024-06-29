import functools


class ClientRules:
    def __init__(self, len_spaces_range=(3, 5)):
        self.len_spaces_range = len_spaces_range

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            chains_self = args[0]
            chain = args[1]
            result_chain = ("ok", chain)

            spaces_rules = self.spaces_rule(chain)
            if spaces_rules:
                return self.func(spaces_rules)

            return func(self=chains_self, chain=result_chain)

        return wrapper

    def spaces_rule(self, chain):
        # if chain[:1] == " " or chain[-1:] == " ":
        #     return ("error", "the chains can not contain spaces in init or end")

        count_spaces = chain.count(" ")
        min_spaces = self.len_spaces_range[0]
        max_spaces = self.len_spaces_range[1]

        if count_spaces > max_spaces or count_spaces < min_spaces:
            return (
                "error",
                f"the chains should have between {min_spaces} and {max_spaces} spaces",
            )

        for i in range(len(chain) - 1):
            if chain[i] == " " and chain[i + 1] == " ":
                return ("error", "the chains can not contain consecutive spaces")

        return False

    def caracters_rule(self, chain):
        if chain[:1] == " " or chain[-1:] == " ":
            return ("error", "the chains can not contain spaces in init or end")

        count_spaces = chain.count(" ")
        if count_spaces > 5 or count_spaces < 3:
            return ("error", "the chains should have between 3 and 5 spaces")

        return False
