import inspect
import logging


class Rules:
    def __init__(self, rules_class, not_rules) -> None:
        self.rules_class = rules_class
        self.not_rules = not_rules

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            chains_self = args[0]
            chain = args[1]
            is_valid = True

            rules = inspect.getmembers(self.rules_class, predicate=inspect.isfunction)
            for rule_name, rule in rules:
                if rule_name not in self.not_rules:
                    try:
                        rule(self, chain)
                    except Exception as e:
                        logging.error(f"{type(e).__name__}: {e} Chain: '{chain}'.")
                        is_valid = False

            return func(self=chains_self, chain=(is_valid, chain))

        return wrapper
