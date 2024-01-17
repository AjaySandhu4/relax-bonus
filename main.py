from copy import deepcopy
from globals import *
from parsers import *
import sys
from pprint import pprint

sys.setrecursionlimit(3000)

relations_dict = {}

def main():
    with open('relations.txt') as relation_file:
        raw_relations = relation_file.read()
        relation_tokens = lexing_relations(raw_relations)
        # pprint(relation_tokens)
        global relations_dict 
        relations_dict = parse_relations(relation_tokens)
        # pprint(relations_dict['Student'].name)
    # pprint(relations_dict)
    
    tests = [
        '(Courses) × (takes)',
        'π name, title, mark (Student)',
        '(Student) ⨝ id=sid (takes)',
        '(π name, title, mark ((Student) ⨝ Student.id=Takes.sid (takes))) ⨝ cid=Course.id (Course)',
        '((Courses) × (((takes) × (Student)) × (Student))) ⨝ cid=Course.id (Course)',
        'Courses',
        '(Courses)',
        '((Courses) × (takes))',
        'σ Student.name=\'John\' (Student)',
        'σ Student.id=2 (Student)',
        'π id, email (Student)',
        'π email (Student)',
        'π name, id, email (Student)',
    ]
    
    query = parse_query(tests[12])
    result = perform(query)
    if(isinstance(result, Relation)):
        result.print()
    # pprint(query)

    # perform()
    # for test in tests:
    #     print(test, '->', parse_query(test))
    

# def perform(operator = None, left_arg = None, right_arg = None, condition = None):
#     print(5)
def perform(query):
    # try:
        if(type(query) == str):
            return deepcopy(relations_dict[query]) if query in relations_dict else None
        elif(len(query) == 1):
            return perform(query[0])
        elif(len(query) == 3):
            op = query[0]
            if op in UNARY_OPERATORS:
                condition = query[1]
                relation = perform(query[2])
                return RELATION_OPS_FUNCTIONS[op](relation, condition)
            else:
                left_relation = perform(query[1]) #check query[1] or query[2] can possibly be relation?
                right_relation = perform(query[2])
                return RELATION_OPS_FUNCTIONS[op](left_relation, right_relation)
        elif(len(query) == 4):
            op = query[0]
            condition = query[1]
            left_relation = perform(query[3]) #check query[1] or query[2] can possibly be relation?
            right_relation = perform(query[4])
            return RELATION_OPS_FUNCTIONS[op](left_relation, right_relation, condition)
        else:
            return None
    # except:
    #     print('Failed to perform query')
    #     return None




    

if __name__ == "__main__":
    main()