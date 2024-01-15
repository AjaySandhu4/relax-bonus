from pyparsing import *

# Define basic tokens
identifier = Word(alphas, alphanums + "_")
select_op = "σ"
project_op = "π"
cross_product_op = "×"
natural_join_op = "⨝"
union_op = "∪"
difference_op = "−"

# Define the grammar
expr = Forward()

atom = identifier.setResultsName("relation") | Group("(" + expr + ")")

operation = (
    (select_op + "(" + expr + "," + identifier + "=" + identifier + ")")
    | (project_op + "(" + expr + "," + identifier + "," + identifier + ")")
)

expr << infixNotation(atom, [(cross_product_op, 2, opAssoc.LEFT)])
expr << infixNotation(expr, [(natural_join_op, 2, opAssoc.LEFT)])
expr << infixNotation(expr, [(union_op, 2, opAssoc.LEFT)])
expr << infixNotation(expr, [(difference_op, 2, opAssoc.LEFT)])
expr <<= operation | atom

# Test the parser
def parse_relational_algebra(expression):
    return expr.parseString(expression, parseAll=True)

if __name__ == "__main__":
    expression = "(Student) ⨝ id=sid (takes)"
    result = parse_relational_algebra(expression)
    print("Parsed Result:")
    print(result)