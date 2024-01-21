from copy import deepcopy
from operations import RELATION_OPS_FUNCTIONS
from parsers import *
import sys

sys.setrecursionlimit(3000)

relations_dict = {}

RELATION_FILE = 'relations.txt'

def main():
    with open(RELATION_FILE) as relation_file:
        try:
            raw_relations = relation_file.read()
            relation_tokens = lexing_relations(raw_relations)
            global relations_dict 
            relations_dict = parse_relation_tokens(relation_tokens)
        except:
            print('Failed to parse relations')
            exit()
    
    while(True):
        print('Enter a relational algebra query (or enter \'q\' to quit):')
        raw_query = input()
        if(raw_query == 'q'):
            print('Bye!')
            return
        try:
            query = parse_query(raw_query)
            result = perform(query)
            if(isinstance(result, Relation)):
                print('\nHere is the result:')
                result.print()
            print()
        except:
            print('Query failed')
            
# Recursively performs query
def perform(query):
    try:
        if(type(query) == str):
            if query in relations_dict:
                return deepcopy(relations_dict[query])
            raise Exception('Failed to find relation', query)
        elif(len(query) == 1):
            return perform(query[0])
        elif(len(query) == 3):
            op = query[0]
            if op in UNARY_OPERATORS:
                condition = query[1]
                relation = perform(query[2])
                return RELATION_OPS_FUNCTIONS[op](relation, condition)
            else:
                left_relation = perform(query[1])
                right_relation = perform(query[2])
                return RELATION_OPS_FUNCTIONS[op](left_relation, right_relation)
        elif(len(query) == 4):
            op = query[0]
            condition = query[1]
            left_relation = perform(query[2])
            right_relation = perform(query[3])
            return RELATION_OPS_FUNCTIONS[op](left_relation, right_relation, condition)
        else:
            raise Exception('Too many arguments')
    except Exception as e:
        print(e)
        print('Failed to perform query')
    
if __name__ == '__main__':
    main()