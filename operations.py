from classes import *
from copy import deepcopy
import operator

COMPARISON_OPS = {
    '!=': operator.ne,
    '=': operator.eq,
    '>=': operator.ge,
    '<=': operator.le,
    '<': operator.lt,
    '>': operator.gt,
}

NULL = 'NULL'

def select(relation: Relation, condition: [str, str, str or int]) -> Relation:
    try:
        relation_copy = deepcopy(relation)
        filter_by = condition[0]
        comparator = COMPARISON_OPS[condition[1]]
        rhs_operand = condition[2]
        compare_columns = (rhs_operand in relation_copy.columns)
        column_index = relation_copy.columns.index(filter_by)
        if compare_columns:
            # Check if there are at least 2 columns with same name if comparing columns of same name
            if (filter_by == rhs_operand):
                if relation_copy.columns.count(filter_by) >= 2:
                    comparison_column_index = relation_copy.columns.index(rhs_operand, column_index+1)
                else:
                    return relation_copy
            else:
                comparison_column_index = relation_copy.columns.index(rhs_operand)
        new_rows = []
        for row in relation_copy.rows:
            if compare_columns and comparator(row[column_index], row[comparison_column_index]):
                new_rows.append(row)
            elif((not compare_columns) and comparator(row[column_index], rhs_operand)):
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

def inner_join(left_relation: Relation, right_relation: Relation, condition: list = None) -> Relation:
    if(condition == None):
        return natural_join(left_relation, right_relation)
    else:
        relation_cross_product = cross_product(left_relation, right_relation)
        # print('relation after cross product:')
        # relation_cross_product.print()
        selected_cross_product = select(relation_cross_product, condition)
        # print('relation after select with condition', condition)
        # selected_cross_product.print()
        return selected_cross_product

def natural_join(left_relation: Relation, right_relation: Relation) -> Relation:
    print("In natural join")
    try:
        common_column = None
        for left_column in left_relation.columns:
            if left_column in right_relation.columns:
                common_column = left_column
        if common_column == None:
            return cross_product(left_relation, right_relation) # Return cross product if no common column between relations
        print(common_column)
        joined_relations = inner_join(left_relation, right_relation, [common_column, '=', common_column])
        right_relation_columns = deepcopy(right_relation.columns)
        left_relation_columns = deepcopy(left_relation.columns)
        right_relation_columns.remove(common_column)
        joined_relations_with_no_duplicate_columns = project(joined_relations, left_relation_columns+right_relation_columns)
        return joined_relations_with_no_duplicate_columns
    except:
        print('Failed to do the natural join operation')
        exit()

def left_outer_join(left_relation: Relation, right_relation: Relation, condition: list) -> Relation:
    print('in left outer join')
    inner_joined_relation = inner_join(left_relation, right_relation, condition)
    inner_joined_relation.rows += unmatching_left_relation_rows(left_relation,right_relation,condition)
    return inner_joined_relation
    
def right_outer_join(left_relation: Relation, right_relation: Relation, condition: list) -> Relation:
    print('in right outer join')
    inner_joined_relation = inner_join(left_relation, right_relation, condition)
    inner_joined_relation.rows += unmatching_right_relation_rows(left_relation,right_relation,condition)
    return inner_joined_relation

def full_outer_join(left_relation: Relation, right_relation: Relation, condition: list) -> Relation:
    print('in full outer join')
    inner_joined_relation = inner_join(left_relation, right_relation, condition)
    inner_joined_relation.rows += unmatching_left_relation_rows(left_relation,right_relation,condition)
    inner_joined_relation.rows += unmatching_right_relation_rows(left_relation,right_relation,condition)
    return inner_joined_relation

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

def compare(left, right, comparator):
    if left == NULL or right == NULL: # Always return false if either operand is NULL
        return False
    return comparator(left,right)

def unmatching_left_relation_rows(left_relation: Relation, right_relation: Relation, condition: list) -> list:
    lhs_operand = condition[0]
    comparator = COMPARISON_OPS[condition[1]]
    rhs_operand = condition[2]
    left_relation_copy_rows = deepcopy(left_relation.rows)
    left_column_condition_index = left_relation.columns.index(lhs_operand)
    right_column_condition_index = right_relation.columns.index(rhs_operand)
    new_left_rows = []
    for left_row in left_relation_copy_rows:
        found_match = False
        for right_row in right_relation.rows:
            if compare(left_row[left_column_condition_index] , right_row[right_column_condition_index], comparator):
                found_match = True
        if found_match == False:
            left_row += [NULL]*(len(right_relation.columns)) # Fill rest of row with None
            new_left_rows.append(left_row)
    return new_left_rows

def unmatching_right_relation_rows(left_relation: Relation, right_relation: Relation, condition: list) -> list:
    lhs_operand = condition[0]
    comparator = COMPARISON_OPS[condition[1]]
    rhs_operand = condition[2]
    right_relation_copy_rows = deepcopy(right_relation.rows)
    left_column_condition_index = left_relation.columns.index(lhs_operand)
    right_column_condition_index = right_relation.columns.index(rhs_operand)
    new_right_rows = []
    for right_row in right_relation_copy_rows:
        found_match = False
        for left_row in left_relation.rows:
            if compare(left_row[left_column_condition_index] , right_row[right_column_condition_index], comparator):
                found_match = True
        if found_match == False:
            right_row = [NULL]*(len(left_relation.columns)) + right_row # Fill rest of row with None
            new_right_rows.append(right_row)
    return new_right_rows

RELATION_OPS_FUNCTIONS = {
    'σ': select,
    'π': project,
    '⨝': inner_join,
    '⟕': left_outer_join,
    '⟖': right_outer_join,
    '⟗': full_outer_join,
    '×': cross_product,
    '∩': intersection,
    '∪': union,
    '-': minus
}



    