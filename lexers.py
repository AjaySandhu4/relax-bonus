from pyparsing import *
from globals import *

def lexing_query(raw_query: str):
    try:
        ppc = pyparsing_common
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
        join_condition = Group(Word(alphas+'.')+Suppress('=')+Word(alphas+'.'))
        project_condition = Group(OneOrMore(Word(alphas)+Optional(Suppress(','))))
        select_condition = Group(Word(alphas+'.')+oneOf("= > < <= >=")+Word(alphas+'.'))
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
        parsedQuery = expr.parseString(raw_query)
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
        element = Word(alphanums + '\'@.')
        row = Group(delimitedList(element, delim=','))
        relation = relation_name + Literal('=').suppress() + Literal('{').suppress() + Group(OneOrMore(row)) + Literal('}').suppress()
        relations = OneOrMore(Group(relation))
        return relations.parseString(raw_relations)
    except:
        print("Error in relation lexer")
        exit()