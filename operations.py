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

def project(relation: Relation, condition: list[str]) -> Relation:
    relation_copy = deepcopy(relation)
    column_indices = []
    for column in condition:
        column_indices.append(relation.columns.index(column))
    column_indices.sort()

    new_columns = []
    for index in column_indices:
            new_columns.append(relation_copy.columns[index])
    relation_copy.columns = new_columns

    new_rows = []
    for row in relation_copy.rows:
        new_row = []
        for index in column_indices:
            new_row.append(row[index])
        new_rows.append(new_row)
    relation_copy.rows = new_rows

    return relation_copy
        
def cross_product(left_relation: Relation, right_relation: Relation):
    left_relation_copy = deepcopy(left_relation)
    right_relation_copy = deepcopy(right_relation)

    new_relation_name = left_relation_copy.name + right_relation_copy.name
    new_columns = left_relation_copy.columns + right_relation_copy.columns
    new_rows = []
    for left_row in left_relation_copy.rows:
        for right_row in right_relation_copy.rows:
            new_row = deepcopy(left_row) + deepcopy(right_row)
            new_rows.append(new_rows)
    # return Relation(new_relation_name, )

    