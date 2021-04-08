
import ply.lex as lex
import ply.yacc as yacc

tokens = [
    'ID',
    'CTEINT',
    'CTEFLOAT',
    'CTESTRING',
    'CTECHAR',
    'PARENTESIS_I',
    'PARENTESIS_D',
    'LLAVE_I',
    'LLAVE_D',
    'CORCHETE_I',
    'CORCHETE_D',
    'COMA',
    'PUNTO_COMA',
    'MAS',
    'MENOS',
    'POR',
    'ENTRE',
    'IGUAL',
    'NO_IGUAL',
    'MENOR_QUE',
    'MAYOR_QUE',
    'PUNTO'
]

reserved = {
    'program' : 'PROGRAM',
    'main': 'MAIN',
    'class': 'CLASS',
    'inherits': 'INHERITS',
    'func': 'FUNC',
    'void': 'VOID',
    'var':'VAR',
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

## Expresiones regulares para tipos de dato
t_CTESTRING = r'\"([^\\\n]|(\\.))*?\"' # strings
t_CTEINT = r'[0-9]+' # Numeros entersos no negativos
t_CTEFLOAT = r'[0-9]+(\.[0-9]+)?' # Numeros flotantes no negativos
t_CTECHAR = r'\'.\'' # char

## Regular ex
def t_ID(t):
    r'[a-zA-Z_][0-9a-z_A-Z]*'
    t.type = reserved.get(t.value,'ID')  # Check for keywords 
    return t

t_NO_IGUAL = r'<>' # Simbolo de desigualdad

## Expresiones regulares par los literales (simbolos de un solo caracter)
t_PARENTESIS_I = r'\(' # Parentesis izquierdo
t_PARENTESIS_D = r'\)' # Parentesis derecho
t_LLAVE_I = r'\{' # Llave izquierda
t_LLAVE_D = r'\}' # Llave derecha
t_CORCHETE_I = r'\[' # Corchete izquierdo
t_CORCHETE_D = r'\]' # Corchete derecho
t_COMA = r'\,' # coma
t_PUNTO_COMA = r'\;' # Punto y coma
t_MAS = r'\+' # Simbolo de suma
t_MENOS = r'\-' # Simbolo de resta
t_POR = r'\*' # Simbolo de multiplicación
t_ENTRE = r'\/' # Simbolo de división
t_IGUAL = r'\=' # Simbolo de iguak
t_MENOR_QUE = r'\<' # Simbolo de menor que
t_MAYOR_QUE = r'\>' # Simbolo de mayor que
t_PUNTO = r'\.' # Punto

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

def p_vacio(p):
     'vacio :'
     pass

def p_programa(p):
    'programa : PROGRAM ID PUNTO_COMA clases decVar funciones main'

def p_main(p):
    'main : MAIN PARENTESIS_I PARENTESIS_D bloque'

def p_bloque(p):
    '''bloque : LLAVE_I estatutos LLAVE_D 
       estatutos : estatuto estatutos
                 | vacio'''

def p_clases(p):
    '''clases    : CLASS ID heren LLAVE_I contenido LLAVE_D PUNTO_COMA nuevacl
                 | vacio
       heren     : MENOR_QUE INHERITS MAYOR_QUE 
                 | vacio
       contenido : attr met
       attr      : decVar 
                 | vacio
       met       : funciones 
                 | vacio
       nuevacl   : clases
                 | vacio'''

def p_decVar(p): 
    '''decVar : VAR tipo PUNTO_COMA e 
                 | vacio
       tipo      : tiposimple a b
                 | tipoCompuesto c d 
       a         : ID 
                 | ID CORCHETE_I CTEINT CORCHETE_D
                 | ID CORCHETE_I CTEINT COMA CTEINT CORCHETE_D
       b         : COMA a b 
                 | vacio
       c         : ID
       d         : COMA c d 
                 | vacio
       e         : decVar
                 | vacio'''

def p_tiposimple(p):
    '''tiposimple : INT 
                  | FLOAT 
                  | CHAR'''

def p_tipoCompuesto(p):
    '''tipoCompuesto : ID 
                     | DATAFRAME
                     | FILE'''

def p_funciones(p):
    '''funciones : FUNC f ID PARENTESIS_I param PARENTESIS_D LLAVE_I decVar estatutos LLAVE_D z  
                 | vacio
       f         : tiposimple 
                 | VOID
       z         : funciones
                 | vacio'''

def p_param(p):
    '''param : tiposimple ID g 
             | vacio
       g     : COMA param
             | vacio'''

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
       h        : CORCHETE_I expresion CORCHETE_D 
                | CORCHETE_I expresion COMA expresion CORCHETE_D
                | vacio '''

def p_asignacion(p):
    '''asignacion : variable IGUAL expresion PUNTO_COMA'''

def p_llamadaVoid(p):
    '''llamadaVoid : ID PARENTESIS_I expresion I PARENTESIS_D
       I           : COMA expresion I 
                   | vacio'''

def p_lectura(p):
    'lectura : READ variable'

def p_retorno(p):
    'retorno : RETURN expresion'

def p_escritura(p):
    '''escritura : PRINT PARENTESIS_I j
       j         : CTESTRING k 
                 | expresion k
       k         : COMA j 
                 | PARENTESIS_D PUNTO_COMA '''
                
def p_condicion(p):
    '''condicion : IF PARENTESIS_I expresion PARENTESIS_D bloque l
       l         : ELSE bloque
                 | vacio'''

def p_cicloWhile(p):
    '''cicloWhile : WHILE PARENTESIS_I expresion PARENTESIS_D bloque'''

def p_cicloFor(p):
    '''cicloFor : FOR variable IGUAL expresion UNTIL bloque'''

def p_expresion(p):
    '''expresion : exp m
       m         : MAYOR_QUE exp
                 | MENOR_QUE exp
                 | NO_IGUAL exp
                 | vacio''' 

def p_exp(p):
    '''exp : termino n
       n   : MAS exp 
           | MENOS exp
           | vacio'''               


def p_termino(p):
    '''termino : factor o
       o       : POR termino 
               | ENTRE termino
               | vacio'''

def p_factor(p):
    '''factor : varcte 
              | ID p
              | PARENTESIS_I expresion PARENTESIS_D
              | MAS varcte
              | MENOS varcte
       p      : CORCHETE_I expresion CORCHETE_D
              | CORCHETE_I expresion COMA expresion CORCHETE_D
              | PARENTESIS_I expresion q PARENTESIS_D
              | PUNTO ID
              | PUNTO ID PARENTESIS_I r PARENTESIS_D
              | vacio
       q      : COMA expresion q
              | vacio 
       r      : varcte s
              | vacio
       s      : COMA varcte  s
              | vacio'''

def p_varcte(p):
    '''varcte : CTECHAR
              | CTEINT
              | CTEFLOAT'''

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

## Contruir parser
parser = yacc.yacc()

print(data)
parser.parse(data)

## Cerrar archivo
f.close()



