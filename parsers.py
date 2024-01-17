from pyparsing import *
from globals import *
from classes import *
from pprint import pprint

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
        # cross_product_op = Literal(OPERATORS['cross_product'])
        inner_join_op = Literal(OPERATORS['inner_join'])
        # intersection_op = Literal(OPERATORS['intersection'])
        # union_op = Literal(OPERATORS['union'])
        # minus_op = Literal(OPERATORS['minus'])
        LPAR = Literal("(").suppress()
        RPAR = Literal(")").suppress()
        join_op = (inner_join_op) # add rest

        expr = Forward()
        relation_column = Group(Word(alphas) + Literal('.').suppress() + Word(alphas))
        join_condition = Group(relation_column+Suppress('=')+relation_column)
        project_condition = Group(OneOrMore(Word(alphas)+Optional(Suppress(','))))
        select_condition_rhs = pyparsing_common.real | Literal('\'').suppress() + Word(alphanums) + Literal('\'').suppress()
        select_condition_rhs.setParseAction(parse_numbers)
        select_condition = Group(Optional(Word(alphas)+Literal('.')).suppress()+Word(alphas)+oneOf("= > < <= >=")+select_condition_rhs)
        # bin_op = (cross_product_op | inner_join_op | intersection_op | union_op | minus_op)
        # expr <<= (
        #     (LPAR+relationName+RPAR)
        #     | (LPAR+expr+RPAR + bin_op + LPAR+expr+RPAR) 
        #     | (project_op + project_condition + LPAR+expr+RPAR)
        # )
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
        # print(type(parsedQuery) == str)
        # return parsedQuery if type(parsedQuery) == str else parsedQuery[0]
        return parsedQuery
    except:
        print("Error in query lexer")
        return None



# Altering parsed array to be in format: [<operator>, <optional: condition>, <expression>, <if second expression required: expression>]
def putOperatorFirst(tokens):
    if((type(tokens[0]) != str) and ((type(tokens[0][0]) != str) or (tokens[0][0] not in UNARY_OPERATORS))):
        tokens[0][0], tokens[0][1] = tokens[0][1], tokens[0][0]
        if(len(tokens[0]) == 4):
            tokens[0][1], tokens[0][2] = tokens[0][2], tokens[0][1]

def lexing_relations(raw_relations: str):
    try:
        relation_name = Word(alphas)
        column_name = Word(alphanums)
        number_element = pyparsing_common.real
        string_element = Optional(Literal('\'')).suppress() + Word(alphanums + '@.') + Optional(Literal('\'')).suppress()
        element = number_element| column_name | string_element
        element.setParseAction(parse_numbers)
        # element.setParseAction(parse_numbers)
        # element = QuotedString(quoteChar='\'').addParseAction(removeQuotes) | Word(alphanums)
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
        # pprint(relation_dict[relation_name])
    return relation_dict
        
def parse_numbers(tokens):
    try:
        tokens[0] = float(tokens[0])
    except:
        return

