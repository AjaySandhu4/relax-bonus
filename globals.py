from operations import *

OPERATORS = {
    'select': 'σ',
    'project': 'π',
    'inner_join': '⨝',
    'cross_product': '×',
    'intersection': '∩',
    'union': '∪',
    'minus': '-'
}
UNARY_OPERATORS = OPERATORS['select']+OPERATORS['project']

RELATION_OPS_FUNCTIONS = {
    'σ': select,
    'π': project,
    # '⨝': ,
    '×': cross_product,
    '∩': intersection,
    '∪': union,
    '-': minus
}