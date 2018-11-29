import ast
import parser

class EidosGenerator():
    '''
    '''
    def __init__(self):
        pass;

    def visit(self, node: ast.InterpreterBlock):
        for name, child in node.children():
            print("!!!")
            print(child.__type__)
            self.visit(child)

    def visit(self, node: ast.If):
        # cond, iftrue, iffalse = None
        cond = None
        iftrue = None
        iffalse = None
        for name, child in node.children():
            if name is "cond":
                cond = child
            elif name is "iftrue":
                iftrue = child
            elif name is "iffalse":
                iffalse = child
        try:
            if self.visit(cond) is True:
                self.visit(iftrue)
            else:
                self.visit(iffalse)
        except:
            pass

    def visit(self, node: ast.Conditional):
        cond = None
        iftrue = None
        iffalse = None
        print("!!!")
        for name, child in node.children():
            if name is "cond":
                cond = child
            elif name is "iftrue":
                iftrue = child
            elif name is "iffalse":
                iffalse = child
        try:
            if self.visit(cond) is True:
                self.visit(iftrue)
            else:
                self.visit(iffalse)
        except:
            pass

    def visit(self, node: ast.Equality):
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
            if name is "operator":
                op = child
            elif name is "left":
                left = child
            elif name is "right":
                right = child
        try:
            # print(op)
            if op is "==":
                return self.visit(left) == self.visit(right)
            elif op is "!=":
                return self.visit(left) != self.visit(right)
            else:
                # print(op)
                print("error in visiting equality node")
        except:
            print("caught an exception")
            pass

def main():
    result = parser.tree()
    print(isinstance(result, ast.Conditional))
    gen = EidosGenerator()
    r = gen.visit(result)
    # print(r)

if __name__ == '__main__':
    main()
