from pyparsing import *
from classes import *

OPERATORS = {
    'select': 'σ',
    'project': 'π',
    'inner_join': '⨝',
    'left_outer_join': '⟕',
    'right_outer_join': '⟖',
    'full_outer_join': '⟗',
    'cross_product': '×',
    'intersection': '∩',
    'union': '∪',
    'minus': '-'
}
UNARY_OPERATORS = OPERATORS['select']+OPERATORS['project']

def parse_query(raw_query: str):
    try:
        bin_op = (
            Literal(OPERATORS['select']) 
            | Literal(OPERATORS['cross_product']) 
            | Literal(OPERATORS['inner_join'])
            | Literal(OPERATORS['intersection'])
            | Literal(OPERATORS['union'])
            | Literal(OPERATORS['minus'])
        )
        relationName = Word(alphas)
        select_op = Literal(OPERATORS['select'])
        project_op = Literal(OPERATORS['project'])
        LPAR = Literal("(").suppress()
        RPAR = Literal(")").suppress()
        join_op = (
            Literal(OPERATORS['inner_join'])
            | Literal(OPERATORS['left_outer_join'])
            | Literal(OPERATORS['right_outer_join'])
            | Literal(OPERATORS['full_outer_join'])
        )
        expr = Forward()
        relation_column = Word(alphas)
        join_condition = Group(relation_column+oneOf("= > < <= >=")+relation_column)
        project_condition = Group(OneOrMore(Word(alphas)+Optional(Suppress(','))))
        select_condition_rhs = Word(nums) | Combine(Word(nums) + '.' + Word(nums)) | Literal('\'').suppress() + Word(alphas) + Literal('\'').suppress()
        select_condition_rhs.setParseAction(parse_numbers)
        select_condition = Group(Word(alphas)+oneOf("= > < <= >=")+select_condition_rhs)

        expr <<= (
            Group(project_op + project_condition + LPAR+expr+RPAR)
            | Group(select_op + select_condition + LPAR+expr+RPAR)
            | Group(LPAR+expr+RPAR + bin_op + LPAR+expr+RPAR) 
            | Group(LPAR+expr+RPAR + join_op + join_condition + LPAR+expr+RPAR)
            | (relationName)
            | (LPAR+relationName+RPAR)
            | (LPAR+expr+RPAR)
        )

        expr.setParseAction(putOperatorFirst)
        parsedQuery = expr.parseString(raw_query).asList()
        return parsedQuery
    except:
        print("Error in query parser")
        return None



# Altering parsed array to be in format: [<operator>, <optional: condition>, <expression>, <if second expression required: expression>]
def putOperatorFirst(tokens):
    if((type(tokens[0]) != str) and ((type(tokens[0][0]) != str) or (tokens[0][0] not in UNARY_OPERATORS))):
        tokens[0][0], tokens[0][1] = tokens[0][1], tokens[0][0]
        if(len(tokens[0]) == 4):
            tokens[0][1], tokens[0][2] = tokens[0][2], tokens[0][1]
    return tokens

def lexing_relations(raw_relations: str):
    try:
        relation_name = Word(alphas)
        column_name = Word(alphanums)
        number_element = pyparsing_common.real
        string_element = Optional(Literal('\'')).suppress() + Word(alphanums + '@.') + Optional(Literal('\'')).suppress()
        element = number_element| column_name | string_element
        element.setParseAction(parse_numbers)
        row = Group(delimitedList(element, delim=','))
        relation = relation_name + Literal('=').suppress() + Literal('{').suppress() + Group(OneOrMore(row)) + Literal('}').suppress()
        relations = OneOrMore(Group(relation))
        return relations.parseString(raw_relations).asList()
    except:
        print("Error in relation lexer")
        exit()

def parse_relations(relation_tokens):
    relation_dict = {}
    for relation_token in relation_tokens:
        relation_name = relation_token[0]
        relation_columns = relation_token[1][0]
        relation_rows = relation_token[1][1:]
        relation_dict[relation_name] = Relation(relation_name, relation_columns, relation_rows)
    return relation_dict
        
def parse_numbers(tokens):
    try:
        tokens[0] = float(tokens[0])
    except:
        return
