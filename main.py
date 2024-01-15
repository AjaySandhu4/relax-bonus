from globals import *
from parsers import *
import sys
from pprint import pprint

sys.setrecursionlimit(3000)

def main():
    with open('relations.txt') as relation_file:
        raw_relations = relation_file.read()
        relation_tokens = lexing_relations(raw_relations)
        # pprint(relation_tokens)
        relations_dict = parse_relations(relation_tokens)
        # pprint(relations_dict['Student'].name)
    
    tests = [
        '(Courses) × (takes)',
        'π name, title, mark (Student)',
        '(Student) ⨝ id=sid (takes)',
        '(π name, title, mark ((Student) ⨝ Student.id=Takes.sid (takes))) ⨝ cid=Course.id (Course)',
        '((Courses) × (((takes) × (Student)) × (Student))) ⨝ cid=Course.id (Course)',
        'Courses',
        '(Courses)',
        '((Courses) × (takes))',
        'σ Student.mark>4 (Student)'
    ]
    
    query = parse_query(tests[8])
    print(query)

    # perform()
    # for test in tests:
    #     print(test, '->', parse_query(test))
    

def perform(operator = None, left_arg = None, right_arg = None, condition = None):
    print(5)

    

if __name__ == "__main__":
    main()