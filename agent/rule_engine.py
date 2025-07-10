class RuleEngine:
    def __init__(self, rules):
        self.rules = rules

    def match(self, smell_list):
        """Devuelve un patrón si encuentra una regla que coincida con los smells, ignorando el orden."""
        print('paso por aca final1')
        smell_set = set(smell_list)
        print(f"Smells detectados (como set): {smell_set}")
        for rule in self.rules:
            print(f"Regla en comparación: {rule['smells']}")
            if smell_set == set(rule['smells']):
                print('paso por aca final semifinal')
                return rule['pattern']
        print('paso por aca final')
        return None
