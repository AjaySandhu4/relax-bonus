from tabulate import tabulate

class Relation:
    def __init__(self, relation_name, columns, rows):
        self.name: str = relation_name
        self.columns: list = columns
        self.rows: list = rows

    def print(self):
        print(tabulate(self.rows, headers=self.columns, tablefmt='fancy_grid'))
