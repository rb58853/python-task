import inspect
import logging


class ServerRules:
    """
    ### Rules:
        - `spaces_rule:` Esta regla esta definida por tal cosa. La cantida minima y maxima de espacios es variable, solo debe pasar como argumento al decorador `len_spaces_range=(3, 5)` donde 3 es e minimo de espacios y 5 es el maximo
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

    def double_a_rule(self, chain):
        if "aa" in chain.lower():
            return {
                "chain": chain,
                "state": "error",
                "message": f"Double 'a' rule detected in chain '{chain}'",
                "metric": 1000,
            }
