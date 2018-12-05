import ply.lex as lex
import ply.yacc as yacc
import ast
from ctokens import *

# Print out tree and contents of p at each step
#DEBUG=True
DEBUG=False
OPTIMIZE=1

lexer = lex.lex(optimize=OPTIMIZE)


def p_interpreter_block(p):
    '''
    interpreter_block : EOF
                      | interpreter_multiple_block EOF
    '''
    if DEBUG:
        print("\ninterp_block: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        p[0] = p[1]

def p_interpreter_multiple_block1(p):
    '''
    interpreter_multiple_block : statement
                               | statement interpreter_multiple_block
    '''
    if DEBUG:
        print("\ninterp_mult_block1: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        p[0] = ast.InterpreterMultipleBlock(p[1], None, p[2])
    else:
        p[0] = p[1]

def p_interpreter_multiple_block2(p):
    '''
    interpreter_multiple_block : function_decl
                               | function_decl interpreter_multiple_block
    '''
    if DEBUG:
        print("\ninterp_mult_block2: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        p[0] = ast.InterpreterMultipleBlock(None, p[1], p[2])
    else:
        # p[0] = ast.InterpreterMultipleBlock(None, p[1], None)
        p[0] = p[1]


def p_compound_statement(p):
    '''
    compound_statement : LBRACE RBRACE
                       | LBRACE multiple_statement RBRACE
    '''
    if DEBUG:
        print("\ncompound stmt: ",end="")
        # Note: Nests the statements
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = ast.CompoundStmt(p[2])

def p_multiple_statement(p):
    '''
    multiple_statement : statement
                       | statement multiple_statement
    '''
    if DEBUG:
        print("\nmultiple statement: ",end="")
        # Note: Nests the statements
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        p[0] = ast.MultipleStmt(p[1], p[2])
    else:
        p[0] = p[1]

def p_statement(p):
    '''
    statement : compound_statement
              | expr_statement
              | selection_statement
              | for_statement
              | do_while_statement
              | while_statement
              | jump_statement
    '''
    if DEBUG:
        print("\nstatement: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    # p[0] = ast.Statement(p[1])
    p[0] = p[1]


def p_expr_statement(p):
    '''
    expr_statement : SEMI
                   | assignment_expr SEMI
    '''
    if DEBUG:
        print("\nexpr stmt: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if p[1] != ';':
        p[0] = p[1]


def p_selection_statement(p):
    '''
    selection_statement : IF LPAREN expr RPAREN statement
                        | IF LPAREN expr RPAREN statement ELSE statement
    '''
    if DEBUG:
        print("\nselection statement: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 6:
        p[0] = ast.If(p[3],p[5],None)
    else:
        p[0] = ast.If(p[3],p[5],p[7])



def p_for_statement(p):
    '''
    for_statement : FOR LPAREN ID IN expr RPAREN statement
    '''
    if DEBUG:
        print("\nfor stmt: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = ast.For(ast.ID(p[3]), p[5], p[7])


def p_do_while_statement(p):
    '''
    do_while_statement : DO statement WHILE LPAREN expr RPAREN SEMI
    '''
    if DEBUG:
        print("\ndo while stmt: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = ast.Do(p[5],p[2])

def p_while_statement(p):
    '''
    while_statement : WHILE LPAREN expr RPAREN statement
    '''
    if DEBUG:
        print("\nwhile stmt: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = ast.While(p[3],p[5])

def p_jump_statement_0(p):
    '''
    jump_statement : NEXT SEMI
    '''
    if DEBUG:
        print("\njmp stmt: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = ast.Next()


def p_jump_statement_1(p):
    '''
    jump_statement : BREAK SEMI
    '''
    if DEBUG:
        print("\njmp stmt: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = ast.Break()

def p_jump_statement_2(p):
    '''
    jump_statement : RETURN SEMI
    '''
    if DEBUG:
        print("\njmp stmt: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = ast.Return(None)

def p_jump_statement_3(p):
    '''
    jump_statement : RETURN expr SEMI
    '''
    if DEBUG:
        print("\njmp stmt: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = ast.Return(p[2])


def p_expr(p):
    '''
    expr : conditional_expr
    '''
    if DEBUG:
        print("\nexpr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = p[1]

def p_assignment_expr(p):
    '''
    assignment_expr : conditional_expr
                    | conditional_expr EQUALS conditional_expr
    '''
    if DEBUG:
        print("\nassignment expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    # only w/ constant
    if len(p) == 4:
        p[0] = ast.Assignment(p[2],p[1],p[3])
    else:
        p[0] = p[1]

def p_conditional_expr(p):
    '''
    conditional_expr : logical_or_expr
                     | conditional_else_expr
    '''
    if DEBUG:
        print("\ncond expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = ast.Conditional(p[1],None, None)

def p_conditional_else_expr(p):
    '''
    conditional_else_expr : logical_or_expr TERNARY conditional_expr ELSE conditional_expr
    '''
    if DEBUG:
        print("\nConditional Else: ",end="")
        # Note: doesn't have "ELSE"
        #p[0] = ("?", p[1], p[3],p[5])
        #### NEED TO FIX
        p[0] = ast.Conditional(p[1],p[3],p[5])

def p_logical_or_expr(p):
    '''
    logical_or_expr : logical_and_expr
                    | logical_and_expr OR or_multiple
    '''
    if DEBUG:
        print("\nor expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    # only w/ constant
    l = len(p)
    if l == 4:
        p[0] = ast.LogicalOR(p[1],p[3])
    else:
        p[0] = p[1]


def p_or_multiple(p):
    '''
    or_multiple : logical_and_expr
                | logical_and_expr OR or_multiple
    '''
    if DEBUG:
        print("\nor mult expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    l = len(p)
    if l == 4:
        p[0] = ast.LogicalOR(p[1],p[3])
    else:
        p[0] = p[1]


def p_logical_and_expr(p):
    '''
    logical_and_expr : equality_expr
                     | equality_expr AND and_multiple
    '''

    if DEBUG:
        print("\nand expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    l = len(p)
    if l == 4:
        p[0] = ast.LogicalAND(p[1],p[3])
    else:
        p[0] = p[1]

def p_and_multiple(p):
    '''
       and_multiple : equality_expr
                    | equality_expr AND and_multiple
    '''
    if DEBUG:
        print("\nand mult expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    l = len(p)
    if l == 4:
        #p[0] = (p[2],p[1],p[3])
        p[0] = ast.LogicalAND(p[1],p[3])
    else:
        p[0] = p[1]
        #p[0] = ast.LogicalAND(p[1],None)


def p_equality_expr(p):
    '''
    equality_expr : relational_expr
                  | relational_expr NE equality_multiple
                  | relational_expr EQ equality_multiple
    '''
    if DEBUG:
        print("\nequality expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = ast.Equality(p[2],p[1],p[3])
    else:
        p[0] = p[1]

def p_equality_multiple(p):
    '''
    equality_multiple : relational_expr
                      | relational_expr NE equality_multiple
                      | relational_expr EQ equality_multiple
    '''
    if DEBUG:
        print("\nequality multiple expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = ast.Equality(p[2],p[1],p[3])
    else:
        p[0] = p[1]


def p_relational_expr(p):
    '''
    relational_expr : add_expr
                    | add_expr LT relational_multiple
                    | add_expr LE relational_multiple
                    | add_expr GT relational_multiple
                    | add_expr GE relational_multiple
    '''
    if DEBUG:
        print("\nrelational expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = ast.Relational(p[2],p[1],p[3])
    else:
        p[0] = p[1]

def p_relational_multiple(p):
    '''
    relational_multiple : add_expr
                        | add_expr LT relational_multiple
                        | add_expr LE relational_multiple
                        | add_expr GT relational_multiple
                        | add_expr GE relational_multiple
    '''
    if DEBUG:
        print("\nrelational multiple expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = ast.Relational(p[2],p[1],p[3])
    else:
        p[0] = p[1]


def p_add_expr(p):
    '''
    add_expr : mult_expr
             | add_expr PLUS mult_expr
             | add_expr MINUS mult_expr
    '''
    if DEBUG:
        print("\nadd expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = ast.BasicOperators(p[2],p[1],p[3])
    else:
        p[0] = p[1]


def p_mult_expr(p):
    '''
    mult_expr : seq_expr
              | seq_expr TIMES mult_expr
              | seq_expr DIVIDE mult_expr
              | seq_expr MODULO mult_expr
    '''
    if DEBUG:
        print("\nmult expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
      p[0] = ast.BasicOperators(p[2],p[1],p[3])
    else:
      p[0] = p[1]

def p_seq_expr(p):
    '''
    seq_expr : exp_expr
             | exp_expr COLON exp_expr
    '''
    if DEBUG:
        print("\nseq expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = ast.Sequence(p[1],p[3])
    else:
        p[0] = p[1]

def p_exp_expr(p):
    '''
    exp_expr : unary_expr
             | unary_expr XOR exp_expr
    '''
    if DEBUG:
        print("\nexp expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = ast.Exp(p[1],p[3], None)
    else:
        p[0] = p[1]

def p_unary_expr(p):
    '''
    unary_expr : postfix_expr
               | NOT unary_expr
               | PLUS unary_expr
               | MINUS unary_expr
    '''
    if DEBUG:
        print("\nunary expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        p[0] = ast.UnaryOp(p[1],p[2])
    else:
        p[0] = ast.UnaryOp(None,p[1])

# Split this into 3!!!
def p_postfix_expr(p):
    '''
    postfix_expr : primary_expr
                 | primary_expr expr_array
                 | primary_expr object_call
    '''
    if DEBUG:
        print("\npostfix expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        # need modification for array and object call
        # p[0] = ast.Postfix(p[1], p[2])
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]

def p_postfix_expr2(p):
    '''
    postfix_expr : primary_expr argument_array
    '''
    if DEBUG:
        print("\npostfix expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = ast.FunctionCall(p[1], p[2])

# We left out leading comma case (,exp,exp) and (,) because they are dumb
#   and should result in errors
def p_expr_array(p):
    '''
    expr_array : LBRACKET RBRACKET
               | LBRACKET expr RBRACKET
               | LBRACKET expr COMMA RBRACKET
               | LBRACKET expr COMMA expr RBRACKET
               | LBRACKET multi_expr RBRACKET
               | LBRACKET COMMA multi_expr RBRACKET
    '''
    if DEBUG:
        print("\nexpr_array: ",end="")
    if len(p) == 6: # LBRACKET expr COMMA expr RBRACKET
        p[0] = ast.Array(p[2],p[4])
    elif len(p) == 5 and p[2] == ',': # LBRACKET COMMA multi_expr RBRACKET
        p[0] = ast.Array(p[3],None) # Do we want to force this ordering?
    elif len(p) == 5 and p[3] == ',': # LBRACKET expr COMMA RBRACKET
        p[0] = ast.Array(p[3],None)
    elif len(p) == 4: # LBRACKET expr RBRACKET
        p[0] = ast.Array(p[3],None)
    else:
        pass

def p_multi_expr(p):
    '''
    multi_expr : expr COMMA multi_expr
               | expr COMMA
               | expr
    '''
    if DEBUG:
        print("\nmulti_expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    l = len(p)
    if l == 4:
        p[0] = ast.Array(p[1],p[3])
    elif l == 3:
        p[0] = ast.Array(p[1],None)
    else:
        p[0] = ast.Array(p[1],None)

def p_argument_array(p):
    '''
    argument_array : LPAREN RPAREN
                   | LPAREN argument_expr_list RPAREN
    '''
    if DEBUG:
        print("\nargument array: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = p[2]
    else:
        pass

def p_object_call(p):
    '''
    object_call : PERIOD ID
    '''
    if DEBUG:
        print("\nobject call: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = ast.ObjectCall(ast.ID(p[2]))

def p_primary_expr(p):
    '''
    primary_expr : constant
                 | LPAREN expr RPAREN
    '''
    if DEBUG:
        print("\nprimary expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_primary_expr_ID(p):
    '''
    primary_expr : ID
    '''
    if DEBUG:
        print("\nprimary expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = ast.ID(p[1])


def p_argument_expr_list(p):
    '''
    argument_expr_list : argument_expr
                       | argument_expr COMMA argument_expr_list
    '''
    if DEBUG:
        print("\nargument expr lst: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = [p[1],p[3]]
    else:
        p[0] = [p[1]]

def p_argument_expr(p):
    '''
    argument_expr : conditional_expr
                  | ID EQUALS conditional_expr
    '''
    if DEBUG:
        print("\nargument expr: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = (p[2], ast.ID(p[1]), p[3])
    else:
        p[0] = p[1]

def p_constant_0(p):
    '''
    constant : INTEGER
    '''
    if DEBUG:
        print("\nconst: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    t = "int"
    p[0] = ast.Constant(t,p[1])

def p_constant_1(p):
    '''
    constant : FLOAT
    '''
    if DEBUG:
        print("\nconst: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    t = "float"
    p[0] = ast.Constant(t,p[1])

def p_constant_2(p):
    '''
    constant : STRING
    '''
    if DEBUG:
        print("\nconst: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    t = "string"
    p[0] = ast.Constant(t,p[1])

def p_constant_3(p):
    '''
    constant : CHARACTER
    '''
    if DEBUG:
        print("\nconst: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    t = "char"
    p[0] = ast.Constant(t,p[1])

def p_constant_4(p):
    '''
    constant : TRUE
             | FALSE
    '''
    if DEBUG:
        print("\nconst: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    t = "bool"
    p[0] = ast.Constant(t,p[1])



def p_function_decl(p):
    '''
    function_decl : FUNCTION return_type_spec ID param_list compound_statement
    '''
    if DEBUG:
        print("\nfun decl: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = ast.FunctionDecl(p[2], ast.ID(p[3]), p[4], p[5])

def p_return_type_spec(p):
    '''
    return_type_spec : LPAREN type_spec RPAREN
    '''
    if DEBUG:
        print("\nreturn type spec: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = p[2]

# Split into two
def p_type_spec(p):
    '''
    type_spec : type_spec_options
              | type_spec_options DOLLAR
    '''
    if DEBUG:
        print("\ntype spec: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = p[1] # Do I need $? No


#Do we want to include the singleton types?
def p_type_spec_option(p):
    '''
    type_spec_options : TYPEVOID
                      | TYPENULL
                      | TYPELOGICAL
                      | TYPEINTEGER
                      | TYPEFLOAT
                      | TYPESTRING
                      | TYPEOBJECT
                      | TYPEOBJECT object_class_spec
                      | TYPENUMERIC
                      | PLUS
                      | TIMES
    '''
    if DEBUG:
        print("\ntype spec option: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        p[0] = (p[1],p[2]) #???
    else:
        p[0] = p[1]

def p_object_class_spec(p):
    '''
    object_class_spec : GT ID LT
    '''
    if DEBUG:
        print("\nobject class spec: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    #p[0] = p[2]
    p[0] = ast.ObjectClassSpec(ast.ID(p[2]))


# Split into 3
def p_param_list(p):
    '''
    param_list : LPAREN param_option RPAREN
    '''
    if DEBUG:
        print("\nparam list: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = p[2]


def p_param_option(p):
    '''
    param_option : TYPEVOID
                 | param_spec
                 | param_spec param_spec_multiple
    '''
    if DEBUG:
        print("\nparam option: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 3:
        # p[0] = ast.ParamOption(p[1],p[2])
        p[0] = [p[1], p[2]]
    else:
        # p[0] = ast.ParamOption(p[1],None)
        p[0] = [p[1]]

def p_param_spec_multiple(p):
    '''
    param_spec_multiple : COMMA param_spec
                        | param_spec_multiple COMMA param_spec
    '''
    if DEBUG:
        print("\nparam spec mult: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 4:
        p[0] = [p[1], p[3]]
        # p[0] = ast.ParamOption(p[1],p[3])
    else:
        # p[0] = ast.ParamOption(p[2],None) # Should reverse?
        p[0] = [p[2]]


#####################
## Checked up to here
#####################
# FIX
# Needs type checking eventually
def p_param_spec(p):
    '''
    param_spec : type_spec ID
               | LBRACKET type_spec ID EQUALS value_option RBRACKET
    '''
    if DEBUG:
        print("\nparam spec: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    if len(p) == 7:
        p[0] = ast.ParamSpec(p[2],ast.ID(p[3]),p[5])
    else:
        p[0] = ast.ParamSpec(p[1],ast.ID(p[2]),None)

def p_value_option(p):
    '''
    value_option : constant
    '''
    if DEBUG:
        print("\nvalue option: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = p[1]

def p_value_option(p):
    '''
    value_option : ID
    '''
    if DEBUG:
        print("\nvalue option: ",end="")
        for i in range(len(p)):
            print(i," ",p[i], " ",end="")
    p[0] = ast.ID(p[1])

def p_eof(p):
    '''
    EOF :
    '''
    pass
    #return p[0]

def tree():
    # prog = input("input here:\n",end="")

    #prog = 'c(1,2,3);'
    #prog = 'if (if(F)); break;'
    # This works, but not else if
    #prog = 'if (if(F));something; else; break;'
    #prog = 'if (F) x=12;'
    #prog = 'if (F) x=12; else x=5;'
    #prog = 'cmColors(0);'
    #prog = 'integerDiv(6, y=3);'
    #prog = 'T==F;'
    #prog = 'T | F;'
    #prog = 'T & F;'
    #prog = "for (myvar in 1:10) x=5;"
    #prog = "x=5+1.0;"


    #prog = 'while(x<5) break;'
    #prog = 'do x=x+2; while (x<5);'
    #prog = 'for (i in 1:20) return;'
    #prog = 'a = ( x==y ? f1() else f2());' # Treats lvalue
    #prog = 'if (F){ if(F) break; }else x=42;'
    # prog = 'x = 5; if (x == 5) y = 6;'
    # prog = 'x = 1; while (x != 5) x = x + 1;'
    # prog = 'x = 1; do x = x + 1; while (x != 5);'
    # prog = 'x = 0; z = 0; for (i in 1 : 5) {y = x; if (i == 3) x = 0; else x = x + 1; z = z + 1;}'
    # prog = 'x = 3; if (x%2 != 0) x = x + 1;'
    #prog = '3==4 | 4==4;'
    #prog = 'x = 0; y = 0; function (int) foo (int x, int y, int z) { return x + y + z;} function (int) bar (int x, int y) { if (x != y) return x * y; else return x;} x = bar(5, 5); y = bar(2,3);'
    #prog = 'function(int) foo(int x) {return x+1;}'
    #prog = 'function(int) foo(int x) {return x+1;} foo(1);'
    prog = 'function(int) foo(int x, int y) {x=x+1;y=x+1;z=x+y; return z;} foo(1,2);'

    # prog = 'x = 0; y = 0; if (x != y) x = x + 1; else y = y + 1; x = 5;'
    # prog = 'x = 0; for (i in 1 : 5) {y = x + i; x = x + 1;}'
    # prog = 'x = 0; y = 0; while (x != 5) {x = x + 1; i = x;}'
    # prog = 'x = 0; y = 0; do {x = x + 1; i = x;} while (x != 5);'
    # prog = 'x = 5; y = 0; if (x != y) {x = x + 1; y = x * 2; i = x;}'
    # prog = 'z = 10; function (int) bar (int x, int y) { if (x != y) return x * y; z = 100; return 1000;} w = bar(4, 5);'
    # prog = 'x = 1; while (x != 10) {x = x + 1; if (x == 3) {x = 100; break;}}'
    # prog = 'x = 1; while (x != 10) break;'
    # prog = 'x = 5; for (i in 1 : 20) {x = x + 1; if (i == 10) break;}'
    # prog = 'x = 0; z = 0; for (i in 1 : 5) {y = x; if (i == 3) x = 0; else x = x + 1; z = z + 1;}'
    # prog = 'function (int) factorial (int x) { if (x == 0) return 1; y = x-1; return y;} x = factorial(1);'


    parser = yacc.yacc()
    result = parser.parse(prog, debug=False)
    # if DEBUG:
    #     print("\n=====\nDONE\n=====")
    #     print("Parsed: ", end="")
    #     print(prog)
    #     print("Result: ",result)
    # else:
    #     print(result)
    return result

def runProgram(prog,dbg=False):
    '''
    Runs an Eidos program that is passed in as a string.
    Dbg option calls yacc's debugger
    '''
    parser = yacc.yacc()
    result = parser.parse(prog, debug=dbg)
    return result

if __name__ == '__main__':
    tree()
