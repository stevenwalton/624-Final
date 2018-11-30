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
        self.visit.register(ast.InterpreterMultipleBlock, self.visit_interpreter_multiple_block)
        self.visit.register(ast.MultipleStmt, self.visit_multiple_statement)
        self.visit.register(ast.BasicOperators, self.visit_basic_operators)

    def visit(self, node: ast.InterpreterBlock):
        for name, child in node.children():
            self.visit(child)

    def visit_if(self, node: ast.If):
        print("visiting if")
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
        print("visiting conditional")
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
                c = self.visit(cond)
            elif self.visit(cond) == True:
                t = self.visit(iftrue)
            elif self.visit(cond) == False:
                f = self.visit(iffalse)
            print("*****************")
            print(c)
            print(t)
            print(f)
            print("*****************")
            return (c, t, f)
        except:
            pass

    def visit_equality(self, node: ast.Equality):
        print("visiting equality")
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
        print("visiting unary")
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
                r = self.visit(expr)
                print("unary result: ", r)
                return r
        except:
            pass

    def visit_constant(self, node: ast.Constant):
        print("visiting constant")
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
        print("visiting id")
        id_name = None
        for name, child in node.children():
            if name == "name":
                id_name = child
        try:
            if id_name:
                if id_name in self.symbolTable:
                    print("value: ", self.symbolTable[id_name])
                    return (id_name, self.symbolTable[id_name])
                else:
                    return (id_name, None)
        except:
            pass

    def visit_assignment(self, node: ast.Assignment):
        print("visiting assignment")
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
        # self.symbolTable[lvalue] = rvalue
        # print("symbol table: ", self.symbolTable)
        try:
            if lvalue is not None:
                left = self.visit(lvalue)
            if rvalue is not None:
                right = self.visit(rvalue)
            self.symbolTable[lvalue] = rvalue
            print("symbol table: ", self.symbolTable)
            return left,right
        except:
            pass

    def visit_interpreter_multiple_block(self, node):
        print("visiting interp mult")
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
        print("visiting mult stmt")
        statement = None
        multi_stmt = None
        for name, child in node.children():
            if name == "statemetn":
                statement = child
            elif name == "multi_stmt":
                multi_stmt = child
        try:
            if statement:
                s = self.visit(statement)
            if multi_stmt:
                m = self.visit(multi_stmt)
            return (s,m)
        except:
            pass

    def visit_basic_operators(self, node):
        print("visiting basic")
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
            print("===========================")
            print("left: ", left)
            leftV = self.visit(left)
            rightV = self.visit(right)
            print("leftV", leftV)
            print("rightV", rightV)
            print("---------------------------")
            if isinstance(left, tuple):
                leftV = left[1]
            if isinstance(right, tuple):
                rightV = right[1]
            print("leftV", leftV)
            print("rightV", rightV)
            if operator == "+":
                print("why???")
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

    # def visit_basic_operators(self, node):
    #     op = None
    #     lexpr = None
    #     rexpr = None
    #     for name, child in node.children():
    #         if name == "operator":
    #             op = child
    #         elif name == "left":
    #             lexpr = child
    #         elif name == "right":
    #             rexpr = child
    #     try:
    #         l = self.visit(lexpr)
    #         r = self.visit(rexpr)
    #         if op == "+":
    #             return l + r
    #         elif op == "-":
    #             return l - r
    #         elif op == "*":
    #             return l * r
    #         elif op == "/":
    #             return l / r
    #         elif op == "%":
    #             return l % r
    #     except:
    #         pass

def main():
    result = parser.tree()
    gen = EidosGenerator()
    r = gen.visit(result)
    print(r)

if __name__ == '__main__':
    main()
