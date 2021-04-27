import ply.lex as lex

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
    'global': 'GLOBAL'
} 

tokens +=  reserved.values()

## Expresiones regulares para tipos de dato
t_CTESTRING = r'\"([^\\\n]|(\\.))*?\"' # strings
t_CTEINT = r'[0-9]+' # Numeros entersos no negativos
t_CTEFLOAT = r'[0-9]+\.[0-9]+' # Numeros flotantes no negativos
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
    print('Illegal character %s' % t.value[0])
    t.lexer.skip(1)
