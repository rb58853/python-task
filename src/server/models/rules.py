import inspect
from config.config import ChainsConfig


class ServerRules:
    """
    When using this class as a decorator for a function, it will analyze the passed string to determine if it is valid or not. In case it is not valid according to a given rule, the `state` will be `"error"` and will has a specific metric for this rule.
    Each of the functions in this class constitutes a rule for the generation of strings by the client. The functions whose names are contained in `self.not_rules` do not constitute a rule.

    ### Rules:
    - `invalid_subchain`: Rule that defines all invalid substrings within a string. These substrings can appear in any form, each character being either lowercase or uppercase.
        - `ChainsConfig.INVALIDS_SUBCHAIN`: Invalid strings that should not be substrings of the main string
    """

    def __init__(self):
        self.not_rules = ["__call__", "__init__"]

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            chains_self = args[0]
            chain = args[1]

            rules = inspect.getmembers(ServerRules, predicate=inspect.isfunction)
            for rule_name, rule in rules:
                if rule_name not in self.not_rules:
                    eval_rule = rule(self, chain)
                    if eval_rule["state"] == "error":
                        return func(self=chains_self, chain=eval_rule)

            return func(self=chains_self, chain={"chain": chain, "state": "ok"})

        return wrapper

    def invalid_subchain(self, chain):
        for subchain in ChainsConfig.INVALIDS_SUBCHAIN:
            if subchain.lower() in chain.lower():
                return {
                    "chain": chain,
                    "state": "error",
                    "message": f"Invalid substring {subchain.lower()} detected in chain '{chain}'",
                    "metric": 1000,
                }
            else:
                return {
                    "chain": chain,
                    "state": "ok",
                }
