from globals import *
import lexers
import sys
from collections import namedtuple

sys.setrecursionlimit(3000)
Node = namedtuple("Node", ["value", "children"])


def main():
    with open('relations.txt') as relation_file:
        raw_relations = relation_file.read()
        print(lexers.lexing_relations(raw_relations))
        # print(raw_relations)

    tests = [
        '(Courses) × (takes)',
        'π name, title, mark (Student)',
        '(Student) ⨝ id=sid (takes)',
        '(π name, title, mark ((Student) ⨝ Student.id=Takes.sid (takes))) ⨝ cid=Course.id (Course)',
        '((Courses) × (((takes) × (Student)) × (Student))) ⨝ cid=Course.id (Course)',
        'Courses',
        '(Courses)',
        '((Courses) × (takes))'
    ]
    print()
    # for test in tests:
    #     print(test, '->', lexers.lexing_query(test))



def buildSyntaxTree():
    print("YESSIR")

    

if __name__ == "__main__":
    main()