import ply.lex as lex
import ply.yacc as yacc
from ctokens import *


lexer = lex.lex()

# def p_expr_statement_semi(t):
#     '''expr_statement : SEMI
#                       | test SEMI
#        test : test SEMI
#             | SEMI'''

def p_interpreter_block(p):
    '''interpreter_block : EOF
                         | block_optional EOF
       block_optional : block_optional statement
                     | block_optional function_decl
                     | statement
                     | function_decl'''

def p_compound_statement(p):
    '''compound_statement : LBRACE RBRACE
                          | LBRACE compound_optional RBRACE
       compound_optional : compound_optional statement
                         | statement'''

def p_statement(p):
    '''statement : compound_statement
                 | expr_statement
                 | selection_statement
                 | for_statement
                 | do_while_statement
                 | while_statement
                 | jump_statement'''

def p_eof(p):
    '''EOF : '''
    pass



def p_function_decl(p):
    '''function_decl : FUNCTION return_type_spec ID param_list compound_statement'''

def p_return_type_spec(p):
    '''return_type_spec : LPAREN type_spec RPAREN'''

def p_type_spec(p):
    '''type_spec : VOID
                 | NULL
                 | '''

parser = yacc.yacc()
s = input("input here:\n")
parser.parse(s)
