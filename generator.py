import ast
import parser
from functools import singledispatch
import traceback
import sys
import numpy as np

class EidosGenerator():
    '''
    '''
    def __init__(self):
        # the current symbol table: a dictionary of variable names and values
        self.curSymTable = {}
        #
        self.stack = []
        # a dict of function name mapping to a function node
        self.funcTable = {}
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
        self.visit.register(ast.Break, self.visit_break)
        self.visit.register(ast.FunctionDecl, self.visit_function_decl)
        self.visit.register(ast.CompoundStmt, self.visit_compound)
        self.visit.register(ast.FunctionCall, self.visit_function_call)
        self.visit.register(ast.ParamSpec, self.visit_param_spec)
        self.visit.register(ast.Return, self.visit_return)
        self.visit.register(ast.Relational, self.visit_relational)
        self.visit.register(ast.CreateMatrix, self.visit_matrix)

    def getCurSymTable(self):
        return self.curSymTable

    def getFuncTable(self):
        return self.funcTable
    def updateFuncTable(self,f):
        '''
        updates the function table
        Used in the interpreter
        '''
        self.funcTable = f

    def listExtract(self, ls):
        # if len(ls) == 1:
        #     return ls
        # return ls[:1] + self.listExtract(ls[1])
        result = []
        for item in ls:
            if isinstance(item, list):
                result = result + self.listExtract(item)
            else:
                result.append(item)
        return result

    def lookupSymTables(self, s):
        if s in self.curSymTable:
            v = self.curSymTable[s]
            if v == 'T':
                v = True
            elif v == 'F':
                v = False
            return v
        for i in range(1, len(self.stack)+1):
            if s in self.stack[-i]:
                v = self.stack[-i][s]
                if v == 'T':
                    v = True
                elif v == 'F':
                    v = False
        raise Exception("name {} is not defined".format(s))

    def setValueInStack(self, s, v):
        if s in self.curSymTable:
            self.curSymTable[s] = v
            return True
        for i in range(1, len(self.stack)+1):
            if s in self.stack[-i]:
                self.stack[-i][s] = v
                return True
        self.curSymTable[s] = v
        return True

    def visit(self, node: ast.InterpreterBlock):
        # if isinstance(node, str):
        #     print(node)
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
            cond = self.visit(cond)
            if isinstance(cond, ast.ID):
                cond = self.lookupSymTables(cond.getName())
            if cond == True:
                return self.visit(iftrue)
            else:
                if iffalse:
                    return self.visit(iffalse)
        except Exception as e:
            raise Exception(e)

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
        except TypeError as e:
            raise Exception("TypeError: Cannot compare these types\n{}".format(e))
        except Exception as e:
            raise Exception(e)

    def visit_equality(self, node: ast.Equality):
        '''
        Performs == and != actions
        Will type error if the types cannot be compared
        '''
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
            if isinstance(nodel, ast.ID):
                nodel = self.lookupSymTables(nodel.getName())
            if isinstance(noder, ast.ID):
                noder = self.lookupSymTables(noder.getName())
            if op == "==":
                return (nodel == noder)
            elif op == "!=":
                return (nodel != noder)
            else:
                print("error in visiting equality node")
        except TypeError as e:
            raise Exception("TypeError: Cannot compare types {} and {}".format(type(left),type(right)))
        except Exception as e:
            raise Exception(e)

    def visit_relational(self, node):
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
            if isinstance(nodel, ast.ID):
                nodel = self.lookupSymTables(nodel.getName())
            if isinstance(noder, ast.ID):
                noder = self.lookupSymTables(noder.getName())
            if op == "<":
                return (nodel < noder)
            elif op == "<=":
                return (nodel <= noder)
            elif op == ">":
                return (nodel > noder)
            elif op == ">=":
                return (nodel >= noder)
            else:
                print("error in visiting relational node")
        except TypeError as e:
            raise Exception("TypeError: Cannot compare types {} and {}".format(type(left),type(right)))
        except Exception as e:
            raise Exception(e)

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
            e = self.visit(expr)
            if op is not None:
                if isinstance(e, ast.ID):
                    e = self.lookupSymTables(e.getName())
                if e == 'F':
                    e = False
                elif e == 'T':
                    e = True
                if op == '!':
                    return (not e)
                elif op == '+':
                    return e
                elif op == '-':
                    return -e
            return e
        except Exception as e:
            raise Exception(e)

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
            elif ctype == 'bool':
                return value
        except Exception as e:
            raise Exception(e)

    def visit_id(self, node: ast.ID):
        #print("Visit id")
        return node

    def visit_assignment(self, node: ast.Assignment):
        '''
        Sets rvalue to lvale
        Will return type if error in rvalue
        '''
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
            if isinstance(right, ast.Return):
                right = right.getExpr()
            if isinstance(right, ast.ID):
                right = self.lookupSymTables(right.getName())
            if isinstance(right, bool) and right == True:
                right = 'T'
            elif isinstance(right, bool) and right == False:
                right = 'F'
            self.setValueInStack(left.getName(), right)
            return left,right
        except TypeError as e:
            raise Exception("TypeError: Cannot set rvalue of type {}".type(rvalue))
        except Exception as e:
            raise Exception(e)

    def visit_interpreter_multiple_block(self, node):
        #print("visiting interp mult")
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
            s = None;
            f = None;
            b = None;
            if statement:
                s = self.visit(statement)
                #return s
            if function_decl:
                f = self.visit(function_decl)
            if block:
                b = self.visit(block)
                #return(b)
            return(s,f,b)
        except Exception as e:
            raise Exception(e)

    def visit_multiple_statement(self, node):
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
                # print(s)
                if isinstance(s, ast.Break) or isinstance(s, ast.Return):
                    return s
            if multi_stmt:
                m = self.visit(multi_stmt)
                if isinstance(m, ast.Break) or isinstance(m, ast.Return):
                    return m
            return m
        except Exception as e:
            raise Exception(e)

    def visit_basic_operators(self, node):
        '''
        Performs basic arithmetic operations
        Performs error checking for type errors and
        division or modulo by zero
        '''
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
            if isinstance(leftV, ast.ID):
                leftV = self.lookupSymTables(leftV.getName())
            if isinstance(rightV, ast.ID):
                rightV = self.lookupSymTables(rightV.getName())
            if operator == "+":
                return leftV + rightV
            elif operator == "-":
                return leftV - rightV
            elif operator == "*":
                return leftV * rightV
            elif operator == "/":
                return leftV / rightV
            elif operator == "%":
                return leftV % rightV

        except ZeroDivisionError as e: # For /0 or %0
            if operator == "/":
                raise Exception("ZeroDivisionError: rvalue has a value of 0!")
            elif operator == "%":
                raise Exception("ZeroModuleError: rvalue has a value of 0!")

        except TypeError as e: # If lvalue and rvalue have incompatible types
            raise Exception("TypeError: Cannot perform {} between lvalue {} and rvalue {}".format(operator,type(leftV),type(rightV)))

        except Exception as e:
            raise Exception(e)

    def visit_while(self, node):
        cond = None
        stmt = None
        for name, child in node.children():
            if name == "cond":
                cond = child
            elif name == "stmt":
                stmt = child
        try:
            compound = False
            # if it's compound statement
            if isinstance(stmt, ast.CompoundStmt):
                compound = True
                statement = None
                for name, child in stmt.children():
                    if name == 'statement':
                        stmt = child
                self.stack.append(self.curSymTable)
                self.curSymTable = {}

            while(self.visit(cond)):
                r = self.visit(stmt)
                if isinstance(r, ast.Break) or isinstance(r, ast.Return):
                    break
            if compound:
                try:
                    self.curSymTable = self.stack.pop()
                except IndexError:
                    pass
                except Exception as e:
                    raise Exception(e)

        except Exception as e:
            raise Exception(e)

    def visit_do(self, node):
        self.visit_while(node)

    def visit_sequence(self, node):
        '''
        Generates a range of values: beginning:end
        if beginning or end can safely be converted to an int we will try to
        do that. If they cannot then we will raise an error telling the user
        both types.
        Error will try to tell user if it is the beginning or end value with error
        Will display warnings if autocasting from float to int, but will continue
        '''
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

            # Check if b or e is a float and if so downcast to int
            if type(b) is not int and type(b) is not float and type(e) is not int and type(e) is not float:
                raise TypeError("TypeError: Cannot convert EITHER values to int. Sequence contains types",type(b),type(e))
            elif type(b) is int and type(e) is int:
                pass
            elif type(b) is float and type(e) is float and b == round(b) and e == round(e):
                print("WARNING: Downcasting",b,"and",e,"to integers")
                b = round(b)
                e = round(e)

            elif type(b) is float and type(e) is int and b == round(b):
                print("WARNING: Downcasting", b, "to integer")
                b = round(b)

            elif type(b) is int and type(e) is float and e == round(e):
                print("WARNING: Downcasting",e,"to integer")
                e = round(e)

            elif type(b) is float and type(e) is float and b != round(b) and e != round(e):
                raise TypeError("Cannot safely convert EITHER value from float to int without loss of precision. Values {}:{}".format(b,e))
            elif type(b) is float and b != round(b):
                raise TypeError("Cannot safely convert BEGINNING value of {} to int without loss of precision".format(b))
            elif type(e) is float and e != round(e):
                raise TypeError("Cannot safely convert END value of {} to int without loss of precision".format(e))

            if isinstance(b, ast.ID):
                b = self.lookupSymTables(b.getName())
            if isinstance(e, ast.ID):
                e = self.lookupSymTables(e.getName())
            # returns python range, not eidos range
            return range(b,e+1)

        except TypeError as e: # beginning or end cannot safely be converted to ints
            raise Exception("TypeError: {}".format(e))
        except Exception as e:
            raise Exception(e)

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
                x = self.visit(ID).getName()
                self.curSymTable[x] = i
                r = self.visit(stmt)
                if isinstance(r, ast.Break) or isinstance(r, ast.Return):
                    break
        except Exception as e:
            raise Exception(e)

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
            raise Exception(e)

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
            raise Exception(e)

    def visit_compound(self, node):
        statement = None
        for name, child in node.children():
            if name == 'statement':
                statement = child
        self.stack.append(self.curSymTable)
        self.curSymTable = {}
        try:
            r = self.visit(statement)
            self.curSymTable = self.stack.pop()
            return r
        except Exception as e:
            raise Exception(e)

    def visit_function_decl(self, node):
        fId = ""
        for name, child in node.children():
            if name == "fId":
                fId = child
        #print("Function node: {}".format(node))
        #print(type(node))
        self.funcTable[fId.getName()] = node

    def visit_sqrt(self, node):
        # print("visiting sqrt")
        for name, child in node.children():
            if name == 'arguments':
                arguments = child
        arguments = self.listExtract(arguments)
        if len(arguments) > 1:
            raise Exception("sqrt function takes exactly one argument")
        n = self.visit(arguments[0])
        if isinstance(n, ast.ID):
            n = self.lookupSymTables(n.getName())
        return np.sqrt(n)

    def visit_abs(self, node):
        # print("visiting abs")
        for name, child in node.children():
            if name == 'arguments':
                arguments = child
        arguments = self.listExtract(arguments)
        if len(arguments) > 1:
            raise Exception("sqrt function takes exactly one argument")
        n = self.visit(arguments[0])
        if isinstance(n, ast.ID):
            n = self.lookupSymTables(n.getName())
        return abs(n)

    def visit_function_call(self, node):
        name_expr = None
        arguments = None
        for name, child in node.children():
            if name == 'name_expr':
                name_expr = child
            elif name == 'arguments':
                arguments = child
        try:
            if name_expr == "sqrt":
                return self.visit_sqrt(node)
            elif name_expr == "abs":
                return self.visit_abs(node)

            func = self.funcTable[name_expr.getName()]
            returnType = None;
            paramLst = None;
            stmt = None;
            for name, child in func.children():
                if name == 'returnType':
                    returnType = child;
                elif name == 'paramLst':
                    paramLst = child;
                elif name == 'stmt':
                    stmt = child;
            paramLst = self.listExtract(paramLst)
            arguments = self.listExtract(arguments)

            # setting up symbol table
            # not doing parameter list type and size checking
            self.stack.append(self.curSymTable)
            self.curSymTable = {}
            for i in range(len(paramLst)):
                tspec, paramID, valueOption = self.visit(paramLst[i])
                value = self.visit(arguments[i])
                self.curSymTable[paramID.getName()] = value

            for name, child in stmt.children():
                if name == 'statement':
                    stmt = child
            result = self.visit(stmt)
            if isinstance(result, ast.Return):
                result = result.getExpr()
            if isinstance(result, ast.ID):
                result = self.lookupSymTables(result.getName())
            self.curSymTable = self.stack.pop()
            return result
        except Exception as e:
            raise Exception(e)


    def visit_param_spec(self, node):
        tspec = None;
        paramID = None;
        valueOption = None;
        for name, child in node.children():
            if name == "tspec":
                tspec = child
            elif name == "paramID":
                paramID = child;
            elif name == "valueOption":
                valueOption = child;
        return (tspec, paramID, valueOption)

    def visit_return(self, node):
        # Error handling. I think the return is fine. It is function that needs work
        #print("Visit return")
        #print("CurSymTable: {}".format(self.curSymTable))
        #print("Stack: {}".format(self.stack))
        #print("Node: {}".format(node))
        expr = None
        for name, child in node.children():
            if name == "expr":
                expr = child
        try:
            r =  self.visit(expr)
            #print("Will return: {}".format(r))
            return ast.Return(r)
        except Exception as e:
            raise Exception(e)

    def visit_break(self, node):
        return node

    def visit_matrix(self, node):
        arguments = None
        for name, child in node.children():
            if name == 'arguments':
                arguments = child
        try:
            arguments = self.listExtract(arguments)
            entries = self.visit(arguments[0])
            if type(entries) is range:
                start = entries.start
                end = entries.stop
            else:
                raise Exception("The first argument must be a sequence.")

            nrows = 1
            ncols = 1
            if len(arguments) == 1:
                initmatrix = np.zeros(len(entries))
                j=0
                for i in entries:
                    initmatrix[j] = i
                    j += 1
                return initmatrix

            elif len(arguments) == 2:
                name, value = arguments[1]

                nID = self.visit(name)
                var = None
                for name, child in nID.children():
                    var = child

                nVal = self.visit(value)
                if var == "nrow":
                    nrows = nVal
                elif var == "ncol":
                    ncols = nVal

                if nrows != 1:
                    ncols = int(len(entries)/nrows)
                    initmatrix = np.zeros((nrows, ncols))

                if ncols != 1:
                    nrows = int(len(entries)/ncols)
                    initmatrix = np.zeros((nrows, ncols))

                i = entries.start
                for c in range(ncols):
                    for r in range(nrows):
                        initmatrix[r][c] = i
                        i += 1
                return initmatrix

        except Exception as e:
            raise Exception(e)

def runReturn(prog,oldFunctionTable,dbg=False):
        '''
        Runs an Eidos program that is passed in as a string
        Calls yacc from parser.py
        dbg will call the debug option in yacc
        Returns the full symbol table. The interpreter will use
        this to update.
        '''
        result = parser.runProgram(prog,dbg=False)
        gen = EidosGenerator()
        try:
            gen.updateFuncTable(oldFunctionTable)
            r = gen.visit(result)
            return(r,gen.getCurSymTable(),gen.getFuncTable())
        except:
            print("ERROR when parsing input")
            pass

def run(prog,dbg=False):
    '''
    Runs an Eidos program that is passed in as a string
    Calls yacc from parser.py
    dbg will call the debug option in yacc
    '''
    result = parser.runProgram(prog,dbg=False)
    gen = EidosGenerator()
    r = gen.visit(result)
    #print(r)
    print(gen.getCurSymTable())

def main():
    result = parser.tree()
    gen = EidosGenerator()
    r = gen.visit(result)
    print(r)
    print("Current Symbol table: {}".format(gen.getCurSymTable()))
    #print("Function Sym Table: {}".format(gen.getFuncTable()))

if __name__ == '__main__':
    main()
