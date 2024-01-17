from classes import *
from copy import deepcopy
from globals import *
import operator

COMPARISON_OPS = {
    '!=': operator.ne,
    '=': operator.eq,
    '>=': operator.ge,
    '<=': operator.le,
    '<': operator.lt,
    '>': operator.gt,
}

def select(relation: Relation, condition: [str, str, str or int]) -> Relation:
    try:
        relation_copy = deepcopy(relation)
        filter_by = condition[0]
        comparator = COMPARISON_OPS[condition[1]]
        rhs_operand = condition[2]
        column_index = relation_copy.columns.index(filter_by)
        new_rows = []
        for row in relation_copy.rows:
            if(comparator(row[column_index], rhs_operand)):
                new_rows.append(row)
        relation_copy.rows = new_rows
        return relation_copy
    except:
        print('Failed to do selection operation')
        exit()

# def project(relation: Relation, condition: list[str]) -> Relation:
#     relation_copy = deepcopy(relation)
    