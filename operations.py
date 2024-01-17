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
    try:
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
    except:
        print('Failed to do projects operation')
        exit()
        
def cross_product(left_relation: Relation, right_relation: Relation) -> Relation:
    try:
        left_relation_copy = deepcopy(left_relation)
        right_relation_copy = deepcopy(right_relation)

        new_relation_name = left_relation_copy.name + right_relation_copy.name
        new_columns = left_relation_copy.columns + right_relation_copy.columns
        new_rows = []
        for left_row in left_relation_copy.rows:
            for right_row in right_relation_copy.rows:
                new_row = deepcopy(left_row) + deepcopy(right_row)
                new_rows.append(new_row)
        return Relation(new_relation_name, new_columns, new_rows)
    except:
        print('Failed to do the cross product operation')
        exit()

def intersection(left_relation: Relation, right_relation: Relation) -> Relation:
    try:
        if(not relations_unifiable(left_relation, right_relation)):
            print('Relations not unifiable')
            raise Exception('Relations not unifiable')
        left_relation_copy = deepcopy(left_relation)
        relation_name = left_relation_copy.name + right_relation.name
        new_columns = left_relation_copy.columns
        new_rows = []
        for row in left_relation_copy.rows:
            if(row_in_relation(row, right_relation)):
                new_rows.append(row)
        return Relation(relation_name, new_columns, new_rows)
    except:
        print('Failed to do intersection operation')
        exit()

def union(left_relation: Relation, right_relation: Relation) -> Relation:
    try:
        if(not relations_unifiable(left_relation, right_relation)):
            print('Relations not unifiable')
            raise Exception('Relations not unifiable')
        left_relation_copy = deepcopy(left_relation)
        right_relation_copy = deepcopy(right_relation)
        relation_name = left_relation_copy.name + right_relation_copy.name
        new_columns = left_relation_copy.columns
        new_rows = left_relation_copy.rows
        for row in right_relation_copy.rows:
            if(not row_in_relation(row, left_relation_copy)):
                new_rows.append(row)
        return Relation(relation_name, new_columns, new_rows)
    except:
        print('Failed to do union operation')
        exit()

def minus(left_relation: Relation, right_relation: Relation) -> Relation:
    try:
        if(not relations_unifiable(left_relation, right_relation)):
            print('Relations not unifiable')
            raise Exception('Relations not unifiable')
        left_relation_copy = deepcopy(left_relation)
        relation_name = left_relation_copy.name + right_relation.name
        new_columns = left_relation_copy.columns
        new_rows = []
        for row in left_relation_copy.rows:
            if(not row_in_relation(row, right_relation)):
                new_rows.append(row)
        return Relation(relation_name, new_columns, new_rows)
    except:
        print('Failed to do minus operation')
        exit()

def relations_unifiable(left_relation: Relation, right_relation: Relation) -> bool:
    if(len(left_relation.columns) != len(left_relation.columns)):
        return False
    if(len(left_relation.rows) == 0 or len(right_relation.rows) == 0):
        return True
    first_left_row = left_relation.rows[0]
    first_right_row = right_relation.rows[0]
    for i in range(0, len(first_left_row)):
        if type(first_left_row[i]) != type(first_right_row[i]):
            return False
    return True


def rows_match(r1, r2) -> bool:
    for i in range(0, len(r1)):
        if(r1[i] != r2[i]):
            return False
    return True

def row_in_relation(row: list, relation: Relation):
    for relation_row in relation.rows:
        if rows_match(row,relation_row):
            return True
    return False




    