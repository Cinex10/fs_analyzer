class RuleEngine:
    def __init__(self, rules_file='data/rules.txt'):
        self.rules_file = rules_file
        self.rules = self._parse_rules()

    def _parse_rules(self):
        rules = []
        rule = []
        try:
            with open(self.rules_file, 'r') as file:
                for line in file:
                    if line.startswith('#'):
                        rules.append(' '.join(rule))
                        rule = []
                        continue
                    rule.append(line.strip())
        except FileNotFoundError:
            print(f"Error: The file {self.rules_file} was not found.")
        return rules

    def get_rules(self):
        return self.rules