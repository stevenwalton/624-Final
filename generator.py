import ast
import parser
from functools import singledispatch

class EidosGenerator():
    '''
    '''
    def __init__(self):
        # no scoping version, only one symbolTable
        self.symbolTable = {}
        self.visit = singledispatch(self.visit)
        self.visit.register(ast.If, self.visit_if)
        self.visit.register(ast.Conditional, self.visit_conditional)
        self.visit.register(ast.Equality, self.visit_equality)
        self.visit.register(ast.UnaryOp, self.visit_unary)
        self.visit.register(ast.Constant, self.visit_constant)
        self.visit.register(ast.ID, self.visit_id)
        self.visit.register(ast.Assignment, self.visit_assignment)

    def visit(self, node: ast.InterpreterBlock):
        for name, child in node.children():
            print(child.__type__)
            self.visit(child)

    def visit_if(self, node: ast.If):
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
                self.visit(iftrue)
            else:
                self.visit(iffalse)
        except:
            pass

    def visit_conditional(self, node: ast.Conditional):
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
            if iftrue == None and iffalse == None:
                return self.visit(cond)

            elif self.visit(cond) == True:
                return self.visit(iftrue)
            elif self.visit(cond) == False:
                return self.visit(iffalse)
        except:
            pass

    def visit_equality(self, node: ast.Equality):
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
            if op == "==":
                nodel = self.visit(left)
                noder = self.visit(right)
                tf = (nodel == noder)
                return tf
            elif op == "!=":
                return self.visit(left) != self.visit(right)
            else:
                print("error in visiting equality node")
        except:
            print("caught an exception")
            pass

    def visit_unary(self, node: ast.UnaryOp):
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
                return self.visit(expr)
        except:
            pass

    def visit_constant(self, node: ast.Constant):
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
        op = None
        lvalue = None
        rvalue = None
        for name, child in node.children():
            if name == "op":
                op = child
            elif name == "lvalue":
                lvalue = child
            if name == "rvalue":
                rvalue = child
        self.symbolTable[lvalue] = rvalue
        try:
            if lvalue is not None:
                left = self.visit(lvalue)
            if rvalue is not None:
                right = self.visit(rvalue)
            return left,right
        except:
            pass

def main():
    result = parser.tree()
    gen = EidosGenerator()
    r = gen.visit(result)
    print(r)

if __name__ == '__main__':
    main()
