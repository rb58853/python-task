from rules import ClientRules


class Chains:
    def __init__(self) -> None:
        self.chains = []

    @ClientRules()
    def append_chain(self, chain):
        if chain[0] == "ok":
            self.chains.append(chain[1])
            return True
        else:
            print(f"{chain[0]}:{chain[1]}")
            return False

    def to_file(self):
        return self.chains

    def send(self):
        pass

chains = Chains()
chains.append_chain("asd sd q wqqqqwe qqq")