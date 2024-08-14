from model import *

def opstr(node):
    return {
        Add: '+',
        Sub: '-',
        Mul: '*',
        Div: '/',
        Neg: '-',
        Eq: '==',
        Ne: '!=',
        Gt: '>',
        Ge: '>=',
        Lt: '<',
        Le: '<=',
        And: '&',
        Or: '|',
        Xor: '^',
        LogAnd: '&&',
        LogOr: '||',
        LogNot: '!',
        Shl: '<<',
        Shr: '>>',
        }[type(node)]