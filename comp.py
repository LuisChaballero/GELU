
import ply.lex as lex
import ply.yacc as yacc

tokens = [
    'ID',
    'CTEINT',
    'CTEFLOAT',
    'CTESTRING',
    'CTECHAR',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'LBRACK',
    'RBRACK',
    'COMMA',
    'SEMICOL',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUAL',
    'NOTEQUAL',
    'LT',
    'MT',
    'DOT'
]

reserved = {
    'program' : 'PROGRAM',
    'main': 'MAIN',
    'class': 'CLASS',
    'inherits': 'INHERITS',
    'func': 'FUNC',
    'void': 'VOID',
    'int': 'INT',
    'file': 'FILE',
    'dataframe': 'DATAFRAME',
    'float': 'FLOAT', 
    'char': 'CHAR',
    'print': 'PRINT',
    'read': 'READ',
    'return': 'RETURN',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'until': 'UNTIL',
} 

tokens +=  reserved.values()

## Regular expressions for types
t_CTESTRING = r'\"([^\\\n]|(\\.))*?\"' # strings
t_CTEINT = r'[0-9]+' # Non-negative int numbers
t_CTEFLOAT = r'[0-9]+(\.[0-9]+)?' # Non-negative float numbers
t_CTECHAR = r'\'.\'' # char

## Regular ex
def t_ID(t):
    r'[a-zA-Z_][0-9a-z_A-Z]*'
    #if t.value in reserved:
    t.type = reserved.get(t.value,'ID')  # Check for keywords 
    return t

## Regular expression for NOTEQUAL symbol
t_NOTEQUAL = r'<>' # Different symbol

## Regular expressions for literals (one character symbols)
t_LPAREN = r'\(' # Left parenthesis
t_RPAREN = r'\)' # Right parenthesis
t_LBRACE = r'\{' # Left brace
t_RBRACE = r'\}' # Right brace
t_LBRACK = r'\[' # Left bracket
t_RBRACK = r'\]' # Right bracket
t_COMMA = r'\,' # comma
t_SEMICOL = r'\;' # semicolon
t_PLUS = r'\+' # Addition symmbol
t_MINUS = r'\-' # Substraction symbol
t_TIMES = r'\*' # Multiply
t_DIVIDE= r'\/' # Divide
t_EQUAL = r'\=' # Equal symbol
t_LT = r'\<' # less than symbol
t_MT = r'\>' # more than symbol
t_DOT = r'\.' # dot symbol

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

## Build scanner (lexer)
lexer = lex.lex()

## Read text file (prueba1.txt / prueba2.txt)
f = open("prueba1.txt","r")
data = f.read()

## Test lex with text file
lexer.input(data)

## Tokenize
for tok in lexer:
    print(tok)

## Start of grammar
start = 'programa'

def p_empty(p):
     'empty :'
     pass

def p_programa(p):
    'programa : PROGRAM ID SEMICOL clases decVar funciones main'

def p_main(p):
    'main : MAIN LPAREN RPAREN bloque'

def p_bloque(p):
    '''bloque : LBRACE estatutos RBRACE 
       estatutos : estatuto estatutos
                 | empty'''

def p_clases(p):
    '''clases    : CLASS ID heren LBRACE contenido RBRACE SEMICOL nuevacl
       heren     : LT INHERITS MT 
                 | empty
       contenido : attr met
       attr      : decVar 
                 | empty
       met       : funciones 
                 | empty
       nuevacl   : clases
                 | empty'''

def p_decVar(p): 
    '''decVar : tipo SEMICOL e 
                 | empty
       tipo      : tiposimple a b
                 | tipoCompuesto c d 
       a         : ID 
                 | ID LBRACK CTEINT RBRACK
                 | ID LBRACK CTEINT COMMA CTEINT RBRACK
       b         : COMMA a b 
                 | empty
       c         : ID
       d         : COMMA c d 
                 | empty
       e         : decVar
                 | empty'''

def p_tiposimple(p):
    '''tiposimple : INT 
                  | FLOAT 
                  | CHAR'''

def p_tipoCompuesto(p):
    '''tipoCompuesto : ID 
                     | DATAFRAME
                     | FILE'''

def p_funciones(p):
    '''funciones : FUNC f ID LPAREN param RPAREN LBRACK decVar estatutos RBRACK z  
       f : tiposimple 
         | VOID
       z : funciones
         | empty'''

def p_param(p):
    '''param : tiposimple ID g 
             | empty
       g     : COMMA param
             | empty'''

def p_estatuto(p):
    '''estatuto : asignacion
                | llamadaVoid
                | retorno
                | lectura
                | escritura
                | condicion
                | cicloWhile
                | cicloFor'''

def p_variable(p):
    '''variable : ID h
       h        : LBRACK expresion RBRACK 
                | LBRACK expresion COMMA expresion RBRACK
                | empty '''

def p_asignacion(p):
    '''asignacion : variable EQUAL expresion SEMICOL'''

def p_llamadaVoid(p):
    '''llamadaVoid : ID LPAREN expresion I RPAREN
       I           : COMMA expresion I 
                   | empty'''

def p_lectura(p):
    'lectura : READ variable'

def p_retorno(p):
    'retorno : RETURN expresion'

def p_escritura(p):
    '''escritura : PRINT LPAREN j
       j         : CTESTRING k 
                 | expresion k
       k         : COMMA j 
                 | RPAREN SEMICOL '''
                
def p_condicion(p):
    '''condicion : IF LPAREN expresion RPAREN bloque l
       l         : ELSE bloque
                 | empty'''

def p_cicloWhile(p):
    '''cicloWhile : WHILE LPAREN expresion RPAREN bloque'''

def p_cicloFor(p):
    '''cicloFor : FOR variable EQUAL expresion UNTIL bloque'''

def p_expresion(p):
    '''expresion : exp m
       m         : MT exp
                 | LT exp
                 | NOTEQUAL exp
                 | empty''' 

def p_exp(p):
    '''exp : termino n
       n   : PLUS exp 
           | MINUS exp
           | empty'''               


def p_termino(p):
    '''termino : factor o
       o       : TIMES termino 
               | DIVIDE termino
               | empty'''

def p_factor(p):
    '''factor : ID p
              | LPAREN expresion RPAREN
              | varcte
              | PLUS varcte
              | MINUS varcte
       p      : LBRACK expresion RBRACK
              | LBRACK expresion COMMA expresion RBRACK
              | LPAREN expresion q RPAREN
              | DOT ID
              | DOT ID LPAREN r RPAREN
       q      : COMMA expresion q
              | empty 
       r      : varcte s
              | empty
       s      : COMMA varcte  s
              | empty'''

def p_varcte(p):
    '''varcte : CTECHAR
              | CTEINT
              | CTEFLOAT'''

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

## Build parser
parser = yacc.yacc()

print(data)
parser.parse(data)

## Close file
f.close()



