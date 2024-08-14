import itertools

_count = itertools.count()
create_id = lambda: next(_count)

class Table:
    _cache = {}
    def __new__(cls, name):
        if name not in Table._cache:
            Table._cache[name] = super().__new__(cls)
        return Table._cache[name]
    
    def __init__(self, name):
        if not hasattr(self, '_db'):
            self._db = {}

    def __getitem__(self, node):
        return self._db[node]
    
    def __setitem__(self, node, value):
        self._db[node] = value

    def get(self, node, default =None):
        return self._db.get(node, default)
    
class Node:
    def __repr__(self):
        data = vars(self)
        args = ','.join(f'{key}={value!r}' for key, value in data.items() if key != 'id')
        return f'{type(self).__name__}({args})'

    def __eq__(self, other):
        return type(self) == type(other) and vars(self) == vars(other)

class Statement(Node):
    pass

class Expression(Node):
    pass

class Type(Node):
    pass

class TypeName(Type):
    def __init__(self, name):
        assert isinstance(name, str), name
        self.id = create_id()
        self.name = name


class UnaryOp(Expression):
    def __init__(self, operand):
        self.id = create_id()
        self.operand = operand

    
class BinOp(Expression):
    def __init__(self, left:Expression, right:Expression):
        self.id = create_id()
        self.left = left
        self.right = right

    
class RelOp(BinOp):
    pass

class Add(BinOp):pass
class Sub(BinOp):pass 
class Mul(BinOp):pass
class Div(BinOp):pass
class Mod(BinOp):pass
class And(BinOp):pass
class Or(BinOp):pass
class Xor(BinOp):pass
class Shl(BinOp):pass
class Shr(BinOp):pass
class Not(BinOp):pass

class Neg(UnaryOp):pass
class Pos(UnaryOp):pass
class LogNot(UnaryOp):pass

class Eq(RelOp):pass
class Ne(RelOp):pass
class Lt(RelOp):pass
class Gt(RelOp):pass
class Le(RelOp):pass
class Ge(RelOp):pass

class LogAnd(BinOp):pass
    
class LogOr(BinOp):pass

class Str(Expression):
    def __init__(self, value):
        assert isinstance(value, str) and value[0] == "'" and value[-1] == "'", value
        self.id = create_id()
        self.value = value
    
class Bytes(Expression):
    def __init__(self, value):
        assert isinstance(value, str) and value[0:2] == "b'" and value[-1] == "'", value
        self.id = create_id()
        self.value = value
    
class Pointer(Expression):
    def __init__(self, value):
        assert isinstance(value, Statements), value
        self.id = create_id()
        self.value = value
    
class Null(Expression):
    def __init__(self):
        self.id = create_id()

class Integer(Expression):
    def __init__(self, value):
        self.id = create_id()
        self.value = value

class Boolean(Expression):
    def __init__(self, value):
        self.value = value
        self.id = create_id()

class Float(Expression):
    def __init__(self, value):
        self.value = value
        self.id = create_id()

class Name(Expression):
    def __init__(self, value):
        self.id = create_id()
        self.value = value

class Indexer(Expression):
    def __init__(self, value:Expression, start:Integer, end:Integer = None, step:Integer = None):
        assert isinstance(value, Name) or isinstance(value, Str) or isinstance(value, Array), value
        assert (isinstance(start, Expression)), start
        assert (isinstance(end, Expression)) or not end, end
        assert (isinstance(step, Expression)) or not step, step

        self.id = create_id()
        self.value = value
        self.start = start
        self.end = end
        self.step = step 

class Array(Expression):
    def __init__(self, elements):
        assert isinstance(elements, list) and all(isinstance(e, Expression) for e in elements), elements
        self.id = create_id()
        self.elements = elements

class Group(Expression):
    def __init__(self, value: Expression):
        assert isinstance(value, Expression), value
        self.id = create_id()
        self.value = value
    
class Statements(Node):
    def __init__(self, statements):
        assert isinstance(statements, list) and all(isinstance(s, Statement) for s in statements), statements
        self.id = create_id()
        self.statements = statements

class IfStatement(Statement):
    def __init__(self, test:Expression, consequence, alternative, elif_block):
        assert isinstance(test, Expression), test
        assert isinstance(consequence, Statements), consequence
        assert isinstance(alternative, Statements) or alternative is None, alternative
        self.id = create_id()
        self.test = test
        self.consequence = consequence
        self.alternative = alternative
        self.elif_block = elif_block
 
class WhileStatement(Statement):
    def __init__(self, test:Expression, body):
        assert isinstance(test, Expression), test
        assert isinstance(body, Statements) or body is None, body
        self.id = create_id()
        self.test = test
        self.body = body
    
class ConstDeclaration(Statement):
    def __init__(self, name, type, value):
        assert isinstance(name, Name), name
        assert isinstance(type, Type) or type is None, type
        assert isinstance(value, Expression), value
        self.id = create_id()
        self.name = name
        self.type = type
        self.value = value

class VarDeclaration(Statement):
    def __init__(self, name, type, value):
        assert isinstance(name, Name), name
        assert isinstance(type, Type) or type is None, type
        assert isinstance(value, Expression) or value is None, value
        self.id = create_id()
        self.name = name
        self.type = type
        self.value = value    

class Assignment(Expression):
    def __init__(self, location, value):
        assert isinstance(location, Name) or isinstance(location, Indexer), location
        assert isinstance(value, Expression), value
        self.id = create_id()
        self.location = location
        self.value = value

class PrintStatement(Statement):
    def __init__(self, value):
        self.value = value
        self.id = create_id()

class ExprAsStatement(Statement):
    def __init__(self, expression):
        assert isinstance(expression, Expression), expression
        self.id = create_id()
        self.expression = expression

class BreakStatement(Statement):
    def __init__(self):
        self.id = create_id()        

class ContinueStatement(Statement):
    def __init__(self):
        self.id = create_id()

class LastStatement(Statement):
    def __init__(self, value):
        assert isinstance(value, Expression), value
        self.id = create_id()
        self.value = value

class Parameter(Node):
    def __init__(self, name, type):
        assert isinstance(name, Name), name
        assert isinstance(type, Type), type
        self.id = create_id()
        self.name = name
        self.type = type

class FunctionDeclaration(Statement):
    def __init__(self, name, arguments, return_type, body):
        assert isinstance(name, Name), name
        assert isinstance(arguments, list) and all(isinstance(a, Parameter) for a in arguments), arguments
        assert isinstance(return_type, Type), return_type
        assert isinstance(body, Statements), body
        self.id = create_id()
        self.name = name
        self.arguments = arguments
        self.return_type = return_type
        self.body = body

class ReturnStatement(Statement):
    def __init__(self, value):
        assert isinstance(value, Expression), value
        self.id = create_id()
        self.value = value

class FunctionCall(Expression):
    def __init__(self, name, arguments):
        assert isinstance(name, Name), name
        assert isinstance(arguments, list) and all(isinstance(a, Expression) for a in arguments), arguments
        self.id = create_id()
        self.name = name
        self.arguments = arguments

