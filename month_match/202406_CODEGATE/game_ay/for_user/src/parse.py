import pathlib
from lexer import tokenize, Token
from model import Statements, BreakStatement, ContinueStatement, PrintStatement, Assignment, LogOr, LogAnd, Eq, Ne, Lt, Gt, Le, Ge, Add, Sub, Mul, Div, Integer, Boolean, Float, Str, Name, Neg, Pos, LogNot, Group, TypeName, ConstDeclaration, VarDeclaration, IfStatement, WhileStatement, ExprAsStatement, FunctionDeclaration, Parameter, ReturnStatement, FunctionCall, Array, Indexer, Null, Xor, Or, And, Mod, LastStatement, Shl, Shr, Bytes, Pointer
class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokens.append(Token('EOF', 'EOF', 0, 0))
        self.n = 0

    def __repr__(self) -> str:
        cur_tok = self.current()
        return f"TokenStream({self.n}, ={cur_tok})"
    
    def current(self):
        return self.tokens[self.n]
    
    def advance(self):
        self.n += 1
    
    def peek(self, toktype):
        if self.current().type == toktype:
            return self.current()
        
    def accept(self, toktype) -> Token:
        tok = self.peek(toktype)
        if tok:
            self.advance()
        return tok
    
    def expect(self, toktype) -> Token:
        tok = self.accept(toktype)

        if not tok:
            raise SyntaxError(f'Line {tok.lineno}: Expected {toktype}. Got {tok.value}.')
        return tok
    
    def synchronize(self, tokentypes):
        while(tok:=self.current()):
            if tok.type == "EOF":
                return
            if tok.type in tokentypes:
                break
            self.advance()
        self.advance()
    
def parse_file(filename: str) -> Statements:
    if not pathlib.Path(filename).exists():
        print("[!] File not found.")
        return None
    
    code = pathlib.Path(filename).read_text()
    return parse_source(code)

def parse_source(text:str) -> Statements:
    tokens = tokenize(text)
    token_stream = TokenStream(tokens)
    return parse_program(token_stream)

def parse_program(token_stream: TokenStream) -> Statements:
    return parse_statements(token_stream)
    
def parse_statements(stream) -> Statements:
    statements = []
    while not (stream.peek('EOF') or stream.peek('}')): 
        try:
            statement = parse_statement(stream)
            statements.append(statement)
        except SystemError as err:
            print(err)
            stream.synchronize([';'])

    return Statements(statements)

def parse_statement(stream: TokenStream):
    if stream.peek('BREAK'):
        return parse_break_statement(stream)
    elif stream.peek('CONTINUE'):
        return parse_continue_statement(stream)
    elif stream.peek("PRINT"):
        return parse_print_statement(stream)
    elif stream.peek("CONST"):
        return parse_const_declaration(stream)
    elif stream.peek("VAR"):
        return parse_var_declaration(stream)
    elif stream.peek("IF"):
        return parse_if_statement(stream)
    elif stream.peek("WHILE"):
        return parse_while_statement(stream)
    elif stream.peek("FUNC"):
        return parse_func_declaration(stream)
    elif stream.peek("RETURN"):
        return parse_return_statement(stream)
    elif stream.peek("LAST"):
        return parse_last_statement(stream)
    else:
        return parse_expr_statement(stream)

def parse_last_statement(stream: TokenStream):
    start = stream.expect('LAST')
    value = parse_expression(stream)
    stream.expect(';')
    return start.mark(LastStatement(value))

def parse_return_statement(stream: TokenStream):
    start = stream.expect('RETURN')
    value = parse_expression(stream)
    stream.expect(';')
    return start.mark(ReturnStatement(value))

def parse_func_declaration(stream: TokenStream):
    start = stream.expect('FUNC')
    fname = stream.expect('NAME')
    stream.expect('(')
    params = []
    while not stream.peek(')'):
        if stream.peek('NAME'):
            aname = stream.expect('NAME')
            type = stream.expect('NAME')
            params.append(Parameter(Name(aname.value), TypeName(type.value)))
        else:
            stream.expect(',')
    
    stream.expect(')')
    if stream.peek('NAME'):
        tok = stream.expect('NAME')
        return_type = TypeName(tok.value)
    else:
        return_type = None
    stream.expect('{')
    statements = parse_statements(stream)
    stream.expect('}')
    return start.mark(FunctionDeclaration(Name(fname.value), params, return_type, statements))

def parse_expr_statement(stream: TokenStream):
    start = stream.current()
    expr = parse_expression(stream)
    stream.expect(';')
    return start.mark(ExprAsStatement(expr))

def parse_while_statement(stream: TokenStream):
    start = stream.expect('WHILE')
    test = parse_expression(stream)
    stream.expect('{')
    body = parse_statements(stream)
    stream.expect('}')
    return start.mark(WhileStatement(test, body))

def parse_if_statement(stream: TokenStream):
    start = stream.expect('IF')
    test = parse_expression(stream)
    stream.expect('{')
    consequence = parse_statements(stream)
    stream.expect('}')

    elif_block = []
    while(stream.accept('ELIF')):
        elif_test = parse_expression(stream)
        stream.expect('{')
        elif_consequence = parse_statements(stream)
        elif_block.append((elif_test, elif_consequence))
        stream.expect('}')

    if(stream.accept('ELSE')):
        stream.expect('{')
        alternative = parse_statements(stream)
        stream.expect('}')
    else:
        alternative = None
    return start.mark(IfStatement(test, consequence, alternative, elif_block))

def parse_var_declaration(stream: TokenStream):
    start = stream.expect('VAR')
    ntok = stream.expect('NAME')
    if(tok:=stream.accept('NAME')):
        typename = TypeName(tok.value)
    else:
        typename = None
    
    if(tok:=stream.accept('=')):
        value = parse_expression(stream)
    else:
        value = None
    stream.expect(';') 
    return start.mark(VarDeclaration(Name(ntok.value), typename, value))

def parse_const_declaration(stream: TokenStream):
    start = stream.expect('CONST')
    ntok = stream.expect('NAME')
    if(tok:=stream.accept('NAME')):
        typename = TypeName(tok.value)
    else:
        typename = None
    
    stream.expect('=')
    value = parse_expression(stream)
    stream.expect(';') 
    return start.mark(ConstDeclaration(Name(ntok.value), typename, value))

def parse_break_statement(stream: TokenStream):
    start:Token = stream.expect('BREAK')
    stream.expect(';')
    return start.mark(BreakStatement())

def parse_continue_statement(stream: TokenStream):
    start:Token = stream.expect('CONTINUE')
    stream.expect(';')
    return start.mark(ContinueStatement())

def parse_print_statement(stream:TokenStream):
    start = stream.expect('PRINT')
    value = parse_expression(stream)
    stream.expect(';')
    return start.mark(PrintStatement(value))

def parse_expression(stream:TokenStream):
    return parse_assignment(stream)

def parse_assignment(stream:TokenStream):
    left = parse_orterm(stream)
    if(op:=stream.accept('=')):
        right = parse_expression(stream)
        left = op.mark(Assignment(left, right))
    return left

def parse_orterm(stream:TokenStream):
    left = parse_andterm(stream)
    while (tok:=(stream.accept('||'))):
        right = parse_andterm(stream)
        left = tok.mark(LogOr(left, right))
    return left

def parse_andterm(stream):
    left = parse_shiftterm(stream)
    while (tok:=(stream.accept('&&'))):
        right = parse_shiftterm(stream)
        left = tok.mark(LogAnd(left, right))
    return left

def parse_shiftterm(stream:TokenStream):
    left = parse_relterm(stream)
    while (tok:=(stream.accept('<<') or stream.accept('>>'))):
        right = parse_relterm(stream)
        if tok.type == '<<': left = tok.mark(Shl(left, right))
        else: left = tok.mark(Shr(left, right))
    return left

def parse_relterm(stream:TokenStream):
    left = parse_addterm(stream)
    while (tok:=(stream.accept('<') or stream.accept('<=') or
                 stream.accept('>') or stream.accept('>=') or
                 stream.accept('==') or stream.accept('!='))):
        right = parse_addterm(stream)
        if tok.type == '<': left = tok.mark(Lt(left, right))
        elif tok.type == '<=': left = tok.mark(Le(left, right))
        elif tok.type == '>': left = tok.mark(Gt(left, right))
        elif tok.type == '>=': left = tok.mark(Ge(left, right))
        elif tok.type == '==': left = tok.mark(Eq(left, right))
        elif tok.type == '!=': left = tok.mark(Ne(left, right))

    return left
        
def parse_addterm(stream:TokenStream):
    left = parse_logicterm(stream)
    while (op:=(stream.accept('+') or stream.accept('-'))):
        right = parse_logicterm(stream)
        if op.type == '+': left = op.mark(Add(left, right))
        else: left = op.mark(Sub(left, right))
    return left

def parse_logicterm(stream:TokenStream):
    left = parse_multerm(stream)
    while (op:=(stream.accept('^') or stream.accept('|') or stream.accept('&'))):
        right = parse_multerm(stream)
        if op.type == '^': left = op.mark(Xor(left, right))
        elif op.type == '|': left = op.mark(Or(left, right))
        else: left = op.mark(And(left, right))
    return left

def parse_multerm(stream:TokenStream):
    left = parse_factor(stream)
    while (op:=(stream.accept('*') or stream.accept('/') or stream.accept('%'))):
        right = parse_factor(stream)
        if op.type == '*': 
            left = op.mark(Mul(left, right))
        elif op.type == '%':
            left = op.mark(Mod(left, right))
        else: 
            left = op.mark(Div(left, right))
    return left

def parse_factor(stream:TokenStream):
    if (tok:=stream.accept('INTEGER')):
        return tok.mark(Integer(tok.value))
    
    elif (tok:=stream.accept('FLOAT')):
        return tok.mark(Float(tok.value))
    
    elif (tok:=stream.accept('POINTER')):
        return tok.mark(Pointer(tok.value))
    
    elif (tok:=stream.accept('TRUE')):
        return tok.mark(Boolean(tok.value))

    elif (tok:=stream.accept('FALSE')):
        return tok.mark(Boolean(tok.value))
    
    elif (tok:=stream.accept('NULL')):
        return tok.mark(Null())

    elif (tok:=stream.accept("STR")):
        if stream.accept("["):
            start = Null()
            end = Null()
            step = Null()
            if not stream.peek(':'):
                start = parse_expression(stream)

            if not stream.peek(':'):
                if stream.accept(']'):
                    return tok.mark(Indexer(Str(tok.value), start))
                else:
                    raise SyntaxError(f"Line {stream.current().lineno}: Syntax error at {stream.current().value}")

            if stream.accept(':'):
                if stream.accept(']'):
                    return tok.mark(Indexer(Str(tok.value), start, end))
                
                if not stream.peek(':'):
                    end = parse_expression(stream)
                if stream.accept(']'):
                    return tok.mark(Indexer(Str(tok.value), start, end))
                
                stream.expect(':')
                if stream.accept(']'):
                    return tok.mark(Indexer(Str(tok.value), start, end, step))
                step = parse_expression(stream)

            stream.expect(']')
            return tok.mark(Indexer(Str(tok.value), start, end, step))
        return tok.mark(Str(tok.value))

    elif (tok:=stream.accept("BYTES")):
        if stream.accept("["):
            start = Null()
            end = Null()
            step = Null()
            if not stream.peek(':'):
                start = parse_expression(stream)

            if not stream.peek(':'):
                if stream.accept(']'):
                    return tok.mark(Indexer(Str(tok.value), start))
                else:
                    raise SyntaxError(f"Line {stream.current().lineno}: Syntax error at {stream.current().value}")

            if stream.accept(':'):
                if stream.accept(']'):
                    return tok.mark(Indexer(Str(tok.value), start, end))
                
                if not stream.peek(':'):
                    end = parse_expression(stream)
                if stream.accept(']'):
                    return tok.mark(Indexer(Str(tok.value), start, end))
                
                stream.expect(':')
                if stream.accept(']'):
                    return tok.mark(Indexer(Str(tok.value), start, end, step))
                step = parse_expression(stream)

            stream.expect(']')
            return tok.mark(Indexer(Str(tok.value), start, end, step))
        return tok.mark(Bytes(tok.value))


    elif (tok:=stream.accept("NAME")):
        if stream.accept('('):
            args = []
            while not stream.peek(')'):
                args.append(parse_expression(stream))
                if not stream.accept(','):
                    break
            stream.expect(')')
            return tok.mark(FunctionCall(Name(tok.value), args))

        elif stream.accept('['):
            start = Null()
            end = Null()
            step = Null()
            if not stream.peek(':'):
                start = parse_expression(stream)

            if not stream.peek(':'):
                if stream.accept(']'):
                    return tok.mark(Indexer(Name(tok.value), start))
                else:
                    raise SyntaxError(f"Line {stream.current().lineno}: Syntax error at {stream.current().value}")

            if stream.accept(':'):
                if stream.accept(']'):
                    return tok.mark(Indexer(Name(tok.value), start, end))
                
                if not stream.peek(':'):
                    end = parse_expression(stream)
                if stream.accept(']'):
                    return tok.mark(Indexer(Name(tok.value), start, end))
                
                stream.expect(':')
                if stream.accept(']'):
                    return tok.mark(Indexer(Name(tok.value), start, end, step))
                step = parse_expression(stream)

            stream.expect(']')
            return tok.mark(Indexer(Name(tok.value), start, end, step))
                
        return tok.mark(Name(tok.value))

    elif (tok:=stream.accept("-")):
        operand = parse_factor(stream)
        return tok.mark(Neg(operand))

    elif (tok:=stream.accept("+")):
        operand = parse_factor(stream)
        return tok.mark(Pos(operand)) 

    elif (tok:=stream.accept("!")):
        operand = parse_factor(stream)
        return tok.mark(LogNot(operand))

    elif (tok:=stream.accept("(")): 
        value = parse_expression(stream)
        stream.expect(')')
        return tok.mark(Group(value))

    elif (tok:=stream.accept("[")): 
        values = []
        while not stream.peek(']'):
            values.append(parse_expression(stream))
            if not stream.accept(','):
                break
        stream.expect(']')

        if stream.accept("["):
            start = Null()
            end = Null()
            step = Null()
            if not stream.peek(':'):
                start = parse_expression(stream)

            if not stream.peek(':'):
                if stream.accept(']'):
                    return tok.mark(Indexer(Array(values), start))
                else:
                    raise SyntaxError(f"Line {stream.current().lineno}: Syntax error at {stream.current().value}")

            if stream.accept(':'):
                if stream.accept(']'):
                    return tok.mark(Indexer(Array(values), start, end))
                
                if not stream.peek(':'):
                    end = parse_expression(stream)
                if stream.accept(']'):
                    return tok.mark(Indexer(Array(values), start, end))
                
                stream.expect(':')
                if stream.accept(']'):
                    return tok.mark(Indexer(Array(values), start, end, step))
                step = parse_expression(stream)

            stream.expect(']')
            return tok.mark(Indexer(Array(values), start, end, step))

        return tok.mark(Array(values))
  
    else:
        raise SyntaxError(f"Line {stream.current().lineno}: Syntax error at {stream.current().value}")
