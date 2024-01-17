from tabulate import tabulate

class Relation:
    def __init__(self, relation_name, tokens):
        self.name: str = relation_name
        self.columns: list = tokens[0]
        self.rows: list = tokens[1:]

    def print(self):
        print(tabulate(self.rows, headers=self.columns, tablefmt='fancy_grid'))
