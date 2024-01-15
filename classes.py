class Relation:
    def __init__(self, relation_name, tokens):
        self.name = relation_name
        self.columns = tokens[0]
        self.rows = tokens[1:]
