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
        '(Course) × (takes)',
        'π name (Student)',
        '(takes) ⨝ cname=name (Course)',
        '(Student) ⨝ id=sid (takes)',
        '(π name, title, mark ((Student) ⨝ id=sid (takes))) ⨝ sid=id (Course)',
        '((Course) × (((takes) × (Student)) × (Student))) ⨝ sid=id (Course)',
        'Courses',
        '(Courses)',
        '((Courses) × (takes))',
        'σ name=\'John\' (Student)',
        'σ id=2 (Student)',
        'π id, email (Student)',
        'π email (Student)',
        'π name, id, email (Student)',
        '(Course) ∩ (takes)',
        '(takes) ∩ (takesTwo)',
        '(takes) ∪ (takesTwo)',
        '(takes) - (takesTwo)',
        '(Student) ⨝ (CourseTwo)'
    ]
    test = tests[len(tests)-1]
    pprint(len(tests[len(tests)-1]))
    pprint(test)
    query = parse_query(test)
    print(relations_dict)
    result = perform(query)
    if(isinstance(result, Relation)):
        result.print()

    # pprint(query)

    # perform()
    # for test in tests:
    #     print(test, '->', parse_query(test))
    

def perform(query):
    # try:
        if(type(query) == str):
            if query in relations_dict:
                return deepcopy(relations_dict[query])
            print('Failed to find relation', query)
            exit()
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
            left_relation = perform(query[2]) #check query[1] or query[2] can possibly be relation?
            right_relation = perform(query[3])
            return RELATION_OPS_FUNCTIONS[op](left_relation, right_relation, condition)
        else:
            return None
    # except:
    #     print('Failed to perform query')
    #     return None




    

if __name__ == "__main__":
    main()