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

    def visit_equality(self, node: ast.Equality):
        op = None
        left = None
        right = None
        # print(node.children())
        for name, child in node.children():
            # print("info: ",name, child)
            # print("--------------------------------------")
            # print(name)
            # print("======================================")
            # print(child)
            if name == "operator":
                op = child
            elif name == "left":
                left = child
            elif name == "right":
                right = child
        try:
            if op == "==":
                return self.visit(left) == self.visit(right)
            elif op == "!=":
                return self.visit(left) != self.visit(right)
            else:
                # print(op)
                print("error in visiting equality node")
        except:
            print("caught an exception")
            pass
            
def main():
    result = parser.tree()
    # print(isinstance(result, ast.Conditional))
    gen = EidosGenerator()
    r = gen.visit(result)
    print(r)

if __name__ == '__main__':
    main()
