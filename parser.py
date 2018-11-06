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
                         | block_multiple EOF
       block_multiple : block_multiple statement
                     | block_multiple function_decl
                     | statement
                     | function_decl'''

def p_compound_statement(p):
    '''compound_statement : LBRACE RBRACE
                          | LBRACE compound_multiple RBRACE
       compound_multiple : compound_multiple statement
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
                       | logical_or_expr or_multiple
       or_multiple : or_multiple OR logical_or_expr
                   | OR logical_or_expr'''

def p_logical_and_expr(p):
    '''logical_and_expr : equality_expr
                        | equality_expr and_multiple
       and_multiple : and_multiple AND equality_expr
                    | AND equality_expr'''

def p_relational_expr(p):
    '''relational_expr : add_expr
                       | add_expr relational_multiple
       relational_multiple : relational_multiple LT add_expr
                           | relational_expr LE add_expr
                           | relational_expr GT add_expr
                           | relational_expr GE add_expr
                           | LT add_expr
                           | LE add_expr
                           | GT add_expr
                           | GE add_expr'''

def p_add_expr(p):
    '''add_expr : mult_expr
                | mult_expr add_multiple
       add_multiple : add_multiple PLUS mult_expr
                    | add_multiple MINUS mult_expr
                    | PLUS mult_expr
                    | MINUS mult_expr'''

def p_mult_expr(p):
    '''mult_expr : seq_expr
                 | seq_expr mult_multiple
       mult_multiple : mult_multiple TIMES seq_expr
                     | mult_multiple DIVIDE seq_expr
                     | mult_multiple MODULO seq_expr
                     | TIMES seq_expr
                     | DIVIDE seq_expr
                     | MODULO seq_expr'''

def p_eof(p):
    '''EOF :'''
    pass





parser = yacc.yacc()
s = input("input here:\n")
parser.parse(s)
