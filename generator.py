import ast
import parser
from functools import singledispatch

class EidosGenerator():
    '''
    '''
    def __init__(self):
        # no scoping version, only one symbolTable
        self.symbolTable = {}
        # self.ifBreak = False
        self.visit = singledispatch(self.visit)
        self.visit.register(ast.If, self.visit_if)
        self.visit.register(ast.Conditional, self.visit_conditional)
        self.visit.register(ast.Equality, self.visit_equality)
        self.visit.register(ast.UnaryOp, self.visit_unary)
        self.visit.register(ast.Constant, self.visit_constant)
        self.visit.register(ast.ID, self.visit_id)
        self.visit.register(ast.Assignment, self.visit_assignment)
        self.visit.register(ast.InterpreterMultipleBlock, self.visit_interpreter_multiple_block)
        self.visit.register(ast.MultipleStmt, self.visit_multiple_statement)
        self.visit.register(ast.BasicOperators, self.visit_basic_operators)
        self.visit.register(ast.While, self.visit_while)
        self.visit.register(ast.Do, self.visit_do)
        self.visit.register(ast.Sequence, self.visit_sequence)
        self.visit.register(ast.For, self.visit_for)
        self.visit.register(ast.LogicalOR, self.visit_logical_or)
        self.visit.register(ast.LogicalAND, self.visit_logical_and)
        # self.visit.register(ast.Break, self.visit_break)

    def getSymbolTable(self):
        return self.symbolTable

    def visit(self, node: ast.InterpreterBlock):
        for name, child in node.children():
            self.visit(child)

    def visit_if(self, node: ast.If):
        # print("visiting if")
        cond = None
        iftrue = None
        iffalse = None
        for name, child in node.children():
            if name == "cond":
                cond = child
            elif name == "iftrue":
                iftrue = child
            elif name == "iffalse":
                iffalse = child
        try:
            if self.visit(cond) == True:
                return self.visit(iftrue)
            else:
                return self.visit(iffalse)
        except:
            pass

    def visit_conditional(self, node: ast.Conditional):
        # print("visiting conditional")
        cond = None
        iftrue = None
        iffalse = None
        for name, child in node.children():
            if name == "cond":
                cond = child
            elif name == "iftrue":
                iftrue = child
            elif name == "iffalse":
                iffalse = child
        try:

            # Where it is "breaking". Returns None, because there are no iftrue/iffalse nodes
            c = None
            if iftrue == None and iffalse == None:
                c = self.visit(cond)
            elif c == True:
                return self.visit(iftrue)
            elif c == False:
                return self.visit(iffalse)
            return c
        except:
            pass

    def visit_equality(self, node: ast.Equality):
        # print("visiting equality")
        op = None
        left = None
        right = None
        for name, child in node.children():
            if name == "operator":
                op = child
            elif name == "left":
                left = child
            elif name == "right":
                right = child
        try:
            nodel = self.visit(left)
            noder = self.visit(right)
            if nodel in self.symbolTable:
                nodel = self.symbolTable[nodel]
            if noder in self.symbolTable:
                noder = self.symbolTable[noder]
            if op == "==":
                return (nodel == noder)
            elif op == "!=":
                return (nodel != noder)
            else:
                print("error in visiting equality node")
        except:
            print("caught an exception")
            pass

    def visit_unary(self, node: ast.UnaryOp):
        # print("visiting unary")
        op = None
        expr = None
        for name, child in node.children():
            if name == "op":
                op = child
            elif name == "expr":
                expr = child
        try:
            if op is not None:
                pass
            else:
                # return print(self.visit(expr))
                return self.visit(expr)
        except:
            pass

    def visit_constant(self, node: ast.Constant):
        # print("visiting constant")
        ctype = None
        value = None
        for name, child in node.children():
            if name == "type":
                ctype = child
            elif name == "value":
                value = child
        try:
            if ctype == "int":
                return int(value)
            elif ctype == "float":
                return float(value)
            elif ctype == "string":
                return value
            elif ctype == "character":
                return value
        except:
            pass

    def visit_id(self, node: ast.ID):
        # print("visiting id")
        id_name = None
        for name, child in node.children():
            if name == "name":
                id_name = child
        try:
            if id_name:
                return id_name
        except:
            pass

    def visit_assignment(self, node: ast.Assignment):
        # print("visiting assignment")
        op = None
        lvalue = None
        rvalue = None
        for name, child in node.children():
            if name == "op":
                op = child
            elif name == "lvalue":
                lvalue = child
            elif name == "rvalue":
                rvalue = child
        try:
            left = self.visit(lvalue)
            right = self.visit(rvalue)
            # no connecting
            if right in self.symbolTable:
                right = self.symbolTable[right]
            self.symbolTable[left] = right
            return left,right
        except:
            pass

    def visit_interpreter_multiple_block(self, node):
        # print("visiting interp mult")
        statement = None
        function_decl = None
        block = None
        for name, child in node.children():
            if name == "statement":
                statement = child
            elif name == "function_decl":
                function_decl = child
            elif name == "block":
                block = child
        try:
            if statement:
                n = self.visit(statement)
            if function_decl:
                s = self.visit(function_decl)
            if block:
                b = self.visit(block)
            return (n, s, b)
        except:
            pass

    def visit_multiple_statement(self, node):
        # if self.ifBreak:
        #     print("!")
        #     self.ifBreak = False
        #     return
        statement = None
        multi_stmt = None
        for name, child in node.children():
            if name == "statement":
                statement = child
            elif name == "multi_stmt":
                multi_stmt = child
        try:
            if statement:
                s = self.visit(statement)
            if multi_stmt:
                m = self.visit(multi_stmt)
            # if not isinstance(s, tuple):
            #     s = (s,)
            # if not isinstance(m, tuple):
            #     m = (m,)
            # return s+m
            return s,m
        except:
            pass

    def visit_basic_operators(self, node):
        # print("visiting basic")
        operator = None
        left = None
        right = None
        for name, child in node.children():
            if name == "operator":
                operator = child
            elif name == "left":
                left = child
            elif name == "right":
                right = child
        try:
            # values of left and right
            leftV = self.visit(left)
            rightV = self.visit(right)
            if leftV in self.symbolTable:
                leftV = self.symbolTable[leftV]
            if rightV in self.symbolTable:
                rightV = self.symbolTable[rightV]
            if operator == "+":
                return leftV + rightV
            elif operator == "-":
                return leftV + rightV
            elif operator == "*":
                return leftV * rightV
            elif operator == "/":
                return leftV / rightV
            elif operator == "%":
                return leftV % rightV
        except:
            print("error in basic operator")

    def visit_while(self, node):
        cond = None
        stmt = None
        for name, child in node.children():
            if name == "cond":
                cond = child
            elif name == "stmt":
                stmt = child
        try:
            while(self.visit(cond)):
                self.visit(stmt)
        except:
            print("error in while")

    def visit_do(self, node):
        self.visit_while(node)

    def visit_sequence(self, node):
        beginning = None
        end = None
        for name, child in node.children():
            if name == "beginning":
                beginning = child
            elif name == "end":
                end = child
        try:
            b = self.visit(beginning)
            e = self.visit(end)
            if b in self.symbolTable:
                b = self.symbolTable[b]
            if e in self.symbolTable:
                e = self.symbolTable[e]
            # returns python range, not eidos range
            return range(b,e+1)
        except:
            print("error in visiting seq")

    def visit_for(self, node):
        ID = None;
        cond = None;
        stmt = None;
        for name, child in node.children():
            if name == "id":
                ID = child
            elif name == "cond":
                cond = child;
            elif name == "stmt":
                stmt = child;
        try:
            ran = self.visit(cond)
            for i in ran:
                x = self.visit(ID)
                self.symbolTable[x] = i
                r = self.visit(stmt)
                # print(r)
                # if "break" in r:
                #     self.ifBreak = false
                #     break;
                # print(isinstance(r, ast.Break))
        except Exception as e:
            raise

    def visit_logical_or(self, node):
        first = None
        second = None
        for name, child in node.children():
            if name == "first":
                first = child
            elif name == "second":
                second = child
        try:
            fst = self.visit(first)
            snd = self.visit(second)
            if fst or snd:
                return True
            else:
                return False
        except Exception as e:
            raise

    def visit_logical_and(self, node):
        first = None
        second = None
        for name, child in node.children():
            if name == "first":
                first = child
            elif name == "second":
                second = child
        try:
            fst = self.visit(first)
            snd = self.visit(second)
            if fst and snd:
                return True
            else:
                return False
        except Exception as e:
            raise

def run(prog,dbg=False):
    '''
    Runs an Eidos program that is passed in as a string
    Calls yacc from parser.py
    dbg will call the debug option in yacc
    '''
    result = parser.runProgram(prog,dbg=False)
    gen = EidosGenerator()
    r = gen.visit(result)
    print(r)
    print(gen.getSymbolTable())

def main():
    result = parser.tree()
    gen = EidosGenerator()
    r = gen.visit(result)
    print(r)
    print(gen.getSymbolTable())

if __name__ == '__main__':
    main()
