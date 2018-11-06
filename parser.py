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

def p_expr_statement(p):
    '''expr_statement : SEMI
                      | assignment_expr SEMI'''

def p_selection_statement(p):
    '''selection_statement : IF LPAREN expr RPAREN statement
                           | IF LPAREN expr RPAREN statement ELSE statement'''

def p_for_statement(p):
    '''for_statement : FOR LPAREN ID IN expr RPAREN statement'''

def p_do_while_statement(p):
    '''do_while_statement : DO statement WHILE LPAREN expr RPAREN SEMI'''

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expr RPAREN statement'''

def p_jump_statement(p):
    '''while_statement : NEXT SEMI
                       | BREAK SEMI
                       | RETURN SEMI
                       | RETURN expr SEMI'''
def p_expr(p):
    '''expr : conditional_expr'''

def p_assignment_expr(p):
    '''assignment_expr : conditional_expr
                       | conditional_expr EQUALS conditional_expr'''

def p_logical_or_expr(p):
    '''logical_or_expr : logical_or_expr
                       | logical_or_expr or_optional
       or_optional : or_optional OR logical_or_expr
                   | OR logical_or_expr'''

def p_eof(p):
    '''EOF :'''
    pass





parser = yacc.yacc()
s = input("input here:\n")
parser.parse(s)
