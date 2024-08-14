from model import Table

class Token:
    _line = Table('lineno')
    def __init__(self, type, value, lineno, index):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.index = index
    
    def __repr__(self):
        return f"Token({self.type!r}, {self.value!r}, {self.lineno}, {self.index})"
    
    def mark(self, node):
        Token._line[node.id] = [self.lineno, node]
        return node

def match_comment(text, start=0):
    if text[start:start+2] == '/*':
        end = text.find("*/", start)
        if end > 0:
            return text[start:end+2]
        return ''
    
def match_whitespace(text, start=0):
    n = start
    while n < len(text) and text[n].isspace():
        n += 1
    return text[start:n]

def match_line_comment(text, start=0):
    if text[start:start+2] == '//':
        end = text.find('\n', start)
        if end > 0:
            return text[start:end+1]
        return text[start:]
    return ''

def match_digits(text, start=0):
    n = start
    while n < len(text) and text[n].isdigit():
        n += 1
    return text[start:n]

def match_float(text, start = 0):
    if (digits := match_digits(text, start)):
        n = start + len(digits)
        if n < len(text) and text[n] == '.':
            more_digits = match_digits(text, n+1)
            n += len(more_digits) + 1
            return text[start:n]
    elif text[start] == '.':
        if (digits := match_digits(text, start+1)):
            return text[start:start+len(digits)+1]
    return ''

def match_name(text, start = 0):
    n = start
    if text[n].isalpha() or text[n] == '_':
        while n < len(text) and (text[n].isalnum() or text[n] == '_'):
            n += 1
    return text[start:n]

def match_bytes(text, start=0):
        if text[start:start+2] != "b'":
            return ''
        n = start + 2
        while n < len(text) and text[n] != "'":
            n += 1
        return text[start:n+1]   
     
def match_string(text, start=0):
    if text[start] != "'":
        return ''
    n = start + 1
    while n < len(text) and text[n] != "'":
        n += 1
    return text[start:n+1]

def match_symbol(text, start=0):
    if text[start:start+2] in { '<=', '==', '>=', '!=', '&&', '||' ,'<<', '>>'}:
        return text[start:start+2]
    if text[start:start+1] in { '+', '-', '*', '/', '^','<', '>', '=', '(', ')', '{', '}', ',', ';', ":",'!' , "[", "]", "%", "|", "&"}:
        return text[start:start+1]
    return ''

def tokenize(text:str):
    result = []
    lineno = 1
    n = 0 
    while n < len(text):
        if(m := match_comment(text, n)):
            pass
        elif (m := match_line_comment(text, n)):
            pass
        elif (m := match_whitespace(text, n)):
            pass
        elif (m := match_float(text, n)):
            result.append(Token('FLOAT', m, lineno, n))
        elif (m := match_digits(text, n)):
            result.append(Token('INTEGER', m, lineno, n))
        elif (m := match_bytes(text, n)):
            result.append(Token('BYTES', m, lineno, n))
        elif (m := match_string(text, n)):
            result.append(Token('STR', m, lineno, n))
        elif (m := match_name(text, n)):
            if m in { 'var', 'const', 'print', 'else', 'if', 'elif', 'while', 'break', 'continue', 'last',
                      'return', 'func', 'true', 'false', "null"}:
                result.append(Token(m.upper(), m, lineno, n))
            else:
                result.append(Token('NAME', m, lineno, n)) 
        elif (m := match_symbol(text, n)):
            result.append(Token(m, m, lineno, n))
        else:
            print(f"Invalid character {text[n]!r}")  
            n += 1
        n += len(m)
        lineno += m.count('\n')
    return result