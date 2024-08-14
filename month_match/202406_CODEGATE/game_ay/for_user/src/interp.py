from model import *
from format import opstr
import time
import random
import os
import struct
import queue

lineno = Table('lineno')

class WValue:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f"WValue({self.type}, {self.value})"

class WEnvironment:
    def __init__(self, parent = None):
        self.env = {}
        self.define("ord", WValue("builtins_function",([Parameter(Name("x"), TypeName("STR"))], TypeName("INT"), Statements([]))))
        self.define("chr", WValue("builtins_function",([Parameter(Name("x"), TypeName("INT"))], TypeName("STR"), Statements([]))))
        self.define("int", WValue("builtins_function",([Parameter(Name("x"), TypeName("STR"))], TypeName("INT"), Statements([]))))
        self.define("str", WValue("builtins_function",([Parameter(Name("x"), TypeName("INT"))], TypeName("STR"), Statements([]))))
        self.define("pack", WValue("builtins_function",([Parameter(Name("x"), TypeName("INT")), Parameter(Name("y"), TypeName("INT"))], TypeName("BYTES"), Statements([]))))
        self.define("unpack", WValue("builtins_function",([Parameter(Name("x"), TypeName("BYTES")), Parameter(Name("y"), TypeName("INT"))], TypeName("INT"), Statements([]))))
        self.define("bytes", WValue("builtins_function",([Parameter(Name("x"), TypeName("ARRAY"))], TypeName("BYTES"), Statements([]))))
        self.define("append", WValue("builtins_function",([Parameter(Name("x"), TypeName("ARRAY")), Parameter(Name("y"), TypeName("ANY"))], TypeName("ARRAY"), Statements([]))))
        self.define("pop", WValue("builtins_function",([Parameter(Name("x"), TypeName("ARRAY"))], TypeName("ANY"), Statements([]))))
        self.define("list", WValue("builtins_function",([Parameter(Name("x"), TypeName("ANY"))], TypeName("ANY"), Statements([]))))
        self.define("pread", WValue("builtins_function",([Parameter(Name("x"), TypeName("INT"))], TypeName("BYTES"), Statements([]))))
        self.define("pwrite", WValue("builtins_function",([Parameter(Name("x"), TypeName("INT")), Parameter(Name("y"), TypeName("BYTES"))], TypeName("BOOL"), Statements([]))))
        self.define("len", WValue("builtins_function",([Parameter(Name("x"), TypeName("ANY"))], TypeName("INT"), Statements([]))))
        self.define("sleep", WValue("builtins_function",([Parameter(Name("x"), TypeName("FLOAT"))], TypeName("BOOL"), Statements([]))))
        self.define("rand", WValue("builtins_function",([Parameter(Name("x"), TypeName("INT"))], TypeName("INT"), Statements([]))))
        self.define("time", WValue("builtins_function",([], TypeName("FLOAT"), Statements([]))))
        self.define("flag", WValue("builtins_function",([], TypeName("BYTES"), Statements([]))))
        self.define("input", WValue("builtins_function",([Parameter(Name("x"), TypeName("STR"))], TypeName("BYTES"), Statements([]))))
        self.parent = parent

        self.last = None

    def __repr__(self):
        return f"WEnvironment<{self.parent}, ={self.env}>"
    
    def define(self, name, value):
        self.env[name] = value

    def lookup(self, name):
        parent = self.parent
        if name in self.env:
            return self.env[name]
        
        elif parent:
            return self.parent.lookup(name)
        else:
            raise NameError(f"NameError: name '{name}' is not defined")
        
    def assign(self, name, value):
        if name in self.env:
            self.env[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise NameError(f"NameError: name '{name}' is not defined")

class WBreak(Exception): pass

class WContinue(Exception): pass

class WReturn(Exception):
    def __init__(self, value):
        self.value = value

class Machines:
    def __init__(self, machine_count = 2):
        self.program = [None] * machine_count
        self.P = {}
        for i in range(machine_count):
            self.P[i] = queue.Queue()
    
        self.machine_count= machine_count
        self.last = None

    def set_program(self, machine_id, program):
        if machine_id < 0 or machine_id >= self.machine_count:
            raise IndexError(f"IndexError: list index out of range")
        self.program[machine_id] = program
    
    def get_program(self, machine_id):
        if machine_id < 0 or machine_id >= self.machine_count:
            raise IndexError(f"IndexError: list index out of range")
        return self.program[machine_id]

    def run_program(self, machine_id):
        if machine_id < 0 or machine_id >= self.machine_count:
            raise IndexError(f"IndexError: list index out of range")
        self.interpret_code(self.get_program(machine_id), machine_id = machine_id)

    def rP(self, idx):
        if idx < 0 or idx >= self.machine_count:
            raise IndexError(f"IndexError: list index out of range")
        return self.P[idx].get()
            

    def wP(self, idx, value):
        if idx < 0 or idx >= self.machine_count:
            raise IndexError(f"IndexError: list index out of range")
        
        self.P[idx].put(value)

    def interpret_code(self, nodes, machine_id = 0):
        self.interpret_node(nodes, WEnvironment(), machine_id=machine_id)

    def interpret_node(self, node, environ: WEnvironment, machine_id = 0):
        if isinstance(node, Statements):
            result = None
            for stmt in node.statements:
                result = self.interpret_node(stmt, environ, machine_id=machine_id)
            return result
        
        elif isinstance(node, Pointer):
            return WValue('pointer', node.value)
        
        elif isinstance(node, Integer):
            return WValue('int', int(node.value))
        
        elif isinstance(node, Boolean):
            return WValue('bool', bool(node.value))
        
        elif isinstance(node, Null):
            return WValue('null', None)
        
        elif isinstance(node, Float):
            return WValue('float', float(node.value))
        
        elif isinstance(node, Str):
            return WValue('str', eval(node.value))

        elif isinstance(node, Bytes):
            return WValue('bytes', eval(node.value))
        
        elif isinstance(node, Array):
            return WValue('list', [self.interpret_node(item, environ, machine_id=machine_id).value for item in node.elements])
        
        elif isinstance(node, BinOp):
            left = self.interpret_node(node.left, environ, machine_id=machine_id)
            right = self.interpret_node(node.right, environ, machine_id=machine_id)
            if left.type != right.type:
                raise TypeError(f"TypeError: unsupported operand type(s) for {opstr(node)}: '{left.type}' and '{right.type}'")
            
            if isinstance(node, Add): return WValue(left.type, left.value + right.value)
            elif isinstance(node, Sub): return WValue(left.type, left.value - right.value)
            elif isinstance(node, Mul): return WValue(left.type, left.value * right.value)
            elif isinstance(node, Div): return WValue(left.type, left.value / right.value)
            elif isinstance(node, Mod): return WValue(left.type, left.value % right.value)
            elif isinstance(node, Eq):
                return WValue('bool', left.value == right.value)
            elif isinstance(node, Ne): return WValue('bool', left.value != right.value)
            elif isinstance(node, Gt): return WValue('bool', left.value > right.value)
            elif isinstance(node, Ge): return WValue('bool', left.value >= right.value)
            elif isinstance(node, Lt): return WValue('bool', left.value < right.value)
            elif isinstance(node, Le): return WValue('bool', left.value <= right.value)
            elif isinstance(node, And): return WValue('int', left.value & right.value)
            elif isinstance(node, Or): return WValue('int', left.value | right.value)
            elif isinstance(node, Xor): return WValue('int', left.value ^ right.value)
            elif isinstance(node, LogAnd): return WValue('bool', left.value and right.value)
            elif isinstance(node, LogOr): return WValue('bool', left.value or right.value)
            elif isinstance(node, Shl): return WValue('int', left.value << right.value)
            elif isinstance(node, Shr): return WValue('int', left.value >> right.value)
            else:
                raise NotImplementedError(f"Operation {opstr(node)} not implemented")
        
        elif isinstance(node, UnaryOp):
            operand = self.interpret_node(node.operand, environ, machine_id=machine_id)
            if isinstance(node, Neg): return WValue(operand.type, -operand.value)
            elif isinstance(node, LogNot): return WValue('bool', not operand.value)
            elif isinstance(node, Pos): return operand
            else:
                raise NotImplementedError(f"Operation {opstr(node)} not implemented")
            
        elif isinstance(node, Group):
            return self.interpret_node(node.value, environ, machine_id=machine_id)
        
        elif isinstance(node, Indexer):
            target = self.interpret_node(node.value, environ, machine_id=machine_id)
            start = self.interpret_node(node.start, environ, machine_id=machine_id)
            end = None
            step = None
            if node.end:
                end = self.interpret_node(node.end, environ, machine_id=machine_id)
            else:
                target_type = type(target.value[start.value])
                _type = None
                if target_type == str:
                    _type = 'str'
                elif target_type == list:
                    _type = 'list'
                elif target_type == int:
                    _type = 'int'
                elif target_type == float:
                    _type = 'float'
                elif target_type == bytes:
                    _type = 'bytes'
                else:
                    _type = target.type 

                return WValue(_type, target.value[start.value])

            if node.step:
                step = self.interpret_node(node.step, environ, machine_id=machine_id)
            else:
                return WValue(target.type, target.value[start.value:end.value])

            return WValue(target.type, target.value[start.value:end.value:step.value])

        elif isinstance(node, PrintStatement):
            value = self.interpret_node(node.value, environ, machine_id=machine_id)
            if not value:
                print(None)
                return
            if value.type == 'str':
                print(value.value, end='')
            else:
                print(value.value)

        elif isinstance(node, Name):
            return environ.lookup(node.value)
        
        elif isinstance(node, ConstDeclaration):
            value = self.interpret_node(node.value, environ, machine_id=machine_id)
            environ.define(node.name.value, value)

        elif isinstance(node, VarDeclaration):
            if node.value:
                value = self.interpret_node(node.value, environ, machine_id=machine_id)
            else:
                value = None

            environ.define(node.name.value, value)

        elif isinstance(node, Assignment):
            value = self.interpret_node(node.value, environ, machine_id=machine_id)
            if isinstance(node.location, Name):
                environ.assign(node.location.value, value)
            elif isinstance(node.location, Indexer):
                target = self.interpret_node(node.location.value, environ, machine_id=machine_id)
                start = self.interpret_node(node.location.start, environ, machine_id=machine_id).value
                end = None
                step = None
                if node.location.end:
                    end = self.interpret_node(node.location.end, environ, machine_id=machine_id).value
                
                if node.location.step:
                    step = self.interpret_node(node.location.step, environ, machine_id=machine_id).value

                if not end and not step:
                    target.value[start] = value.value
                else:
                    target.value[start:end:step] = value.value

            else:
                raise RuntimeError(f"Can't assign to {node.location}")
            
        elif isinstance(node, ExprAsStatement):
            return self.interpret_node(node.expression, environ, machine_id=machine_id)
        
        elif isinstance(node, IfStatement):
            test = self.interpret_node(node.test, environ, machine_id=machine_id)
            if test.value:
                return self.interpret_node(node.consequence, environ, machine_id=machine_id)
            else:
                for i in range(len(node.elif_block)):
                    elif_test = self.interpret_node(node.elif_block[i][0], environ, machine_id=machine_id)
                    if elif_test.value:
                        return self.interpret_node(node.elif_block[i][1], environ, machine_id=machine_id)

                if node.alternative:
                    return self.interpret_node(node.alternative, environ, machine_id=machine_id)
        
        elif isinstance(node, WhileStatement):
            while (test := self.interpret_node(node.test, environ, machine_id=machine_id)).value:
                try:
                    self.interpret_node(node.body, environ, machine_id=machine_id)
                except WBreak:
                    break
                except WContinue:
                    continue

        elif isinstance(node, FunctionDeclaration):
            value = WValue('function', (node.arguments, node.return_type, node.body))
            environ.define(node.name.value, value)

        elif isinstance(node, FunctionCall):
            func = self.interpret_node(node.name, environ, machine_id=machine_id)  
            args = [self.interpret_node(arg, environ, machine_id=machine_id) for arg in node.arguments]
            parameters, return_type, body = func.value
            newenv = WEnvironment()
            
            newenv.parent = environ
            
            if node.name.value == "ord":
                return WValue('int', ord(args[0].value))
            
            elif node.name.value == "chr":
                return WValue('str', chr(args[0].value))
            
            elif node.name.value == "int":
                return WValue('int', int(args[0].value))
            elif node.name.value == 'str':
                return WValue('str', str(args[0].value))
            elif node.name.value == "bytes":
                return WValue('bytes', bytes(args[0].value))

            elif node.name.value == 'list':
                return WValue('list', list(args[0].value))
            
            elif node.name.value == "append":
                args[0].value.append(args[1].value)
                return WValue('list', args[0].value)
          
            elif node.name.value == "pread":
                n = args[0].value
                if n < 0 or n >= self.machine_count:
                    return WValue('bytes', b"")
                
                if node.arguments[0].value == str(0) and machine_id != 0:
                    return WValue('bool', False)

                buffer = self.rP(n)
                return WValue(type(buffer), buffer)
                            
            elif node.name.value == "pwrite":
                n = args[0].value
                if n < 0 or n >= self.machine_count:
                    return WValue('bool', False)
                
                if node.arguments[0].value == str(0) and machine_id != 0:
                    return WValue('bool', False)

                self.wP(n, args[1].value)

                return WValue('bool', True)

            elif node.name.value == "len":
                return WValue('int', len(args[0].value))     
            
            elif node.name.value == "unpack":
                if args[1].value == 1:
                    return WValue('int', struct.unpack("<B", args[0].value)[0])
                elif args[1].value == 2:
                    return WValue('int', struct.unpack("<H", args[0].value)[0])
                elif args[1].value == 4:
                    return WValue('int', struct.unpack("<I", args[0].value)[0])
                elif args[1].value == 8:
                    return WValue('int', struct.unpack("<Q", args[0].value)[0])
                else:
                    raise ValueError(f"ValueError: unpack requires a size of 1, 2, 4, or 8")
            
            elif node.name.value == "pack":
                if args[1].value == 1:
                    return WValue('bytes', struct.pack("<B", args[0].value))
                elif args[1].value == 2:
                    return WValue('bytes', struct.pack("<H", args[0].value))
                elif args[1].value == 4:
                    return WValue('bytes', struct.pack("<I", args[0].value))
                elif args[1].value == 8:
                    return WValue('bytes', struct.pack("<Q", args[0].value))
                else:
                    raise ValueError(f"ValueError: pack requires a size of 1, 2, 4, or 8")
                
            elif node.name.value == "sleep":
                time.sleep(args[0].value)
                return WValue('bool', True)
            
            elif node.name.value == "rand":
                return WValue('int', random.randint(0, args[0].value))
            
            elif node.name.value == "time":
                return WValue('float', time.time())

            elif node.name.value == "flag":
                import pathlib
                if machine_id != 0:
                    return WValue('bytes', b"Permission denied!")
                
                return WValue('bytes',pathlib.Path("./flag").read_bytes())
            
            elif node.name.value == "pop":
                return WValue(args[0].type, args[0].value.pop())
            
            elif node.name.value == "input":
                return WValue('bytes', input(args[0].value).encode())
            
            for parm, arg in zip(parameters, args):
                newenv.define(parm.name.value, arg)
            try:
                self.interpret_node(body, newenv, machine_id=machine_id)
                return None 
            except WReturn as ret:
                return ret.value
            
        elif isinstance(node, ReturnStatement):
            raise WReturn(self.interpret_node(node.value, environ, machine_id=machine_id))
        
        elif isinstance(node, BreakStatement):
            raise WBreak()

        elif isinstance(node, ContinueStatement):
            raise WContinue()
        
        elif isinstance(node, LastStatement):
            self.last = self.interpret_node(node.value, environ, machine_id=machine_id)
            return self.last
        
        else:
            raise RuntimeError(f"Can't interpret {node}")
