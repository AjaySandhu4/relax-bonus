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