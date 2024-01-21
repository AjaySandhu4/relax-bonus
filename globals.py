from operations import *

OPERATORS = {
    'select': 'σ',
    'project': 'π',
    'inner_join': '⨝',
    'left_outer_join': '⟕',
    'right_outer_join': '⟖',
    'full_outer_join': '⟗',
    'cross_product': '×',
    'intersection': '∩',
    'union': '∪',
    'minus': '-'
}
UNARY_OPERATORS = OPERATORS['select']+OPERATORS['project']

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