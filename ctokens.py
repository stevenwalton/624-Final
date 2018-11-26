# ----------------------------------------------------------------------
# ctokens.py
#
# Token specifications for symbols in ANSI C and C++.  This file is
# meant to be used as a library in other tokenizers.
# ----------------------------------------------------------------------

# Reserved words

tokens = [
    # Literals (identifier, integer constant, float constant, string constant, char const)
    'ID', 'TYPEID', 'INTEGER', 'FLOAT', 'STRING', 'CHARACTER', 'TRUE', 'FALSE',

    # Operators (+,-,*,/,%,|,&,~,^,<<,>>, ||, &&, !, <, <=, >, >=, ==, !=)
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
    'LOR', 'LAND', 'LNOT',
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

    # Assignment (=, *=, /=, %=, +=, -=, <<=, >>=, &=, ^=, |=)
    'EQUALS', 'TIMESEQUAL', 'DIVEQUAL', 'MODEQUAL', 'PLUSEQUAL', 'MINUSEQUAL',
    'LSHIFTEQUAL','RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL', 'OREQUAL',

    # Increment/decrement (++,--)
    'INCREMENT', 'DECREMENT',

    # Structure dereference (->)
    'ARROW',

    # Ternary operator (?)
    'TERNARY',

    # Delimeters ( ) [ ] { } , . ; :
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',
    'COMMA', 'PERIOD', 'SEMI', 'COLON',

    # Ellipsis (...)
    'ELLIPSIS',

    # Keywords (if, else, for, in, do, while, next, break, return, function,
    # void, NULL, logical, integer, float, string, object, numeric, $)
    'IF', 'ELSE', 'FOR', 'IN', 'DO', 'WHILE', 'NEXT', 'BREAK',
    'RETURN', 'FUNCTION',
    'TYPEVOID', 'TYPENULL', 'TYPELOGICAL', 'TYPEINTEGER', 'TYPEFLOAT', 'TYPESTRING',
    'TYPEOBJECT', 'TYPENUMERIC', 'DOLLAR'
]

# Keywords that are specifically reserved: ones which do special lookups
reserved = {
        "if"    : "IF",
        "then"  : "THEN",
        "else"  : "ELSE",
        "while" : "WHILE",
        "break" : "BREAK"
        }

tokens += list(reserved.values())

# Operators
t_PLUS             = r'\+'
t_MINUS            = r'-'
t_TIMES            = r'\*'
t_DIVIDE           = r'/'
t_MODULO           = r'%'
t_OR               = r'\|'
t_AND              = r'&'
t_NOT              = r'~'
t_XOR              = r'\^'
t_LSHIFT           = r'<<'
t_RSHIFT           = r'>>'
t_LOR              = r'\|\|'
t_LAND             = r'&&'
t_LNOT             = r'!'
t_LT               = r'<'
t_GT               = r'>'
t_LE               = r'<='
t_GE               = r'>='
t_EQ               = r'=='
t_NE               = r'!='

# Assignment operators

t_EQUALS           = r'='
t_TIMESEQUAL       = r'\*='
t_DIVEQUAL         = r'/='
t_MODEQUAL         = r'%='
t_PLUSEQUAL        = r'\+='
t_MINUSEQUAL       = r'-='
t_LSHIFTEQUAL      = r'<<='
t_RSHIFTEQUAL      = r'>>='
t_ANDEQUAL         = r'&='
t_OREQUAL          = r'\|='
t_XOREQUAL         = r'\^='

# Increment/decrement
t_INCREMENT        = r'\+\+'
t_DECREMENT        = r'--'

# ->
t_ARROW            = r'->'

# ?
t_TERNARY          = r'\?'

# Delimeters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_COMMA            = r','
t_PERIOD           = r'\.'
t_SEMI             = r';'
t_COLON            = r':'
t_ELLIPSIS         = r'\.\.\.'

# Keywords
t_IF               = r'if'
t_ELSE             = r'else'
t_FOR              = r'for'
t_IN               = r'in'
t_DO               = r'do'
t_WHILE            = r'while'
t_NEXT             = r'next'
t_BREAK            = r'break'
t_RETURN           = r'return'
t_FUNCTION         = r'function'

t_TYPEVOID         = r'void'
t_TYPENULL         = r'NULL'
t_TYPELOGICAL      = r'logical'
t_TYPEINTEGER      = r'integer'
t_TYPEFLOAT        = r'float'
t_TYPESTRING       = r'string'
t_TYPEOBJECT       = r'object'
t_TYPENUMERIC      = r'numeric'
t_DOLLAR           = r'\$'

# Identifiers
#t_ID = r'[A-Za-z_][A-Za-z0-9_]*'
def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Integer literal
t_INTEGER = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

# Floating literal
t_FLOAT = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

# String literal
t_STRING = r'\"([^\\\n]|(\\.))*?\"'

# Character constant 'c' or L'c'
t_CHARACTER = r'(L)?\'([^\\\n]|(\\.))*?\''

# BOOLS!!! (boo)
t_TRUE  = r'T'
t_FALSE = r'F'

# Comment (C-Style)
def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    return t

# Comment (C++-Style)
def t_CPPCOMMENT(t):
    r'//.*\n'
    t.lexer.lineno += 1
    return t
# t_EMPTY         = r''

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#def t_eof(t):
#    print("\n")
#    more = input('Enter more input (none to quit): ')
#    if more == 'q' or 'Q' or 'exit':
#        return None
#    if more:
#        t.lexer.input(more)
#        return t.lexer.token()
#    return None
