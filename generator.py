import ast
import parser
from functools import singledispatch

class EidosGenerator():
    '''
    '''
    def __init__(self):
        self.visit = singledispatch(self.visit)
        self.visit.register(ast.Conditional, self.visit_conditional)
        self.visit.register(ast.Equality, self.visit_equality)
        self.visit.register(ast.UnaryOp, self.visit_unary)
        self.visit.register(ast.Constant, self.visit_constant)

    def visit(self, node: ast.InterpreterBlock):
        for name, child in node.children():
            print(child.__type__)
            self.visit(child)

    def visit(self, node: ast.If):
        # cond, iftrue, iffalse = None
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
        # print("I'm in Conditional!")
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
        # print("I'm in Equality!")
        # print("--------------------------------------")
        # print(node)
        # print("======================================")
        op = None
        left = None
        right = None
        # print(node.children())
        for name, child in node.children():
            # print("--------------------------------------")
            # print("info: ",name, child)
            # print(name)
            # print("======================================")
            # print(child)
            # print("--------------------------------------")
            if name == "operator":
                op = child
            elif name == "left":
                left = child
            elif name == "right":
                right = child
            # print("======================================")
            # print(op)
            # print("--------------------------------------")
            # print(left)
            # print("--------------------------------------")
            # print(right)
            # print("======================================")
        try:
            if op == "==":
                nodel = self.visit(left)
                # print(nodel)
                noder = self.visit(right)
                # print(noder)
                tf = (nodel == noder)
                # print(tf)
                return tf
            elif op == "!=":
                return self.visit(left) != self.visit(right)
            else:
                # print(op)
                print("error in visiting equality node")
        except:
            print("caught an exception")
            pass

    def visit_unary(self, node: ast.UnaryOp):
        # print("I'm in Unary!")
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
        # print("I'm in Constant!")
        ctype = None
        value = None
        # print(node)
        # print(node.children())
        for name, child in node.children():
            if name == "type":
                ctype = child
            elif name == "value":
                value = child

            # print("======================================")
            # print(ctype)
            # print("--------------------------------------")
            # print(value)
            # print("======================================")
        try:
            if ctype == "int":
                return int(value)
            elif ctype == "float":
                return float(value)
            elif ctype == "string":
                return value
            elif ctype == "character":
                return value
            elif ctype == "ID":
                return value
        except:
            pass
       


def main():
    result = parser.tree()
    #print(isinstance(result, ast.Conditional))
    gen = EidosGenerator()
    r = gen.visit(result)
    print(r)

if __name__ == '__main__':
    main()
