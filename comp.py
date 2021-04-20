
import ply.lex as lex
import ply.yacc as yacc
from collections import deque

from SymbolTable import SymbolTable

# Declare stack to keep track of scopes
s_scopes = deque()

s_var_declaration_ids = deque() # To keep track of type for var declaration

# last type for declared variable 
last_type = ''

# curretn type for declared variable 
current_type = ''

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

# Build scanner (lexer)
lexer = lex.lex()

# Read text file (prueba1.txt / prueba2.txt)
f = open('prueba1.txt','r')
data = f.read()

# Test lex with text file
lexer.input(data)

# Tokenize
for tok in lexer:
    print(tok)

# Start of grammar
start = 'programa'

def p_vacio(p):
     'vacio :'
     pass

def p_programa(p):
    'programa : PROGRAM create_symbol_table ID program_name PUNTO_COMA clases declaracion_variables declaracion_funciones main'

# Create an instance of SymbolTable
def p_create_symbol_table(p):
    'create_symbol_table :'
    global symbol_table
    symbol_table = SymbolTable()

# Add row to SymbolTable for global
def p_program_name(p):
  'program_name :'
  s_scopes.append('Global')
  print("Scope added in STACK: Global")
  symbol_table.add_scope('Global', 'NP')
  print("Scope added in SYMBOL TABLE: Global")

def p_main(p):
    'main : MAIN PARENTESIS_I PARENTESIS_D bloque'
    # 
    s_scopes.pop()
    print("Scope deleted from STACK: Global")
    symbol_table.get_scope('Global').print()

def p_bloque(p):
    '''bloque     : LLAVE_I estatutos LLAVE_D

       estatutos  : estatuto estatutos
                  | vacio'''

def p_clases(p):
    '''clases       : CLASS ID herencia LLAVE_I contenido LLAVE_D PUNTO_COMA nueva_clase   
                    | vacio
                    
       herencia     : MENOR_QUE INHERITS MAYOR_QUE 
                    | vacio

       contenido    : atributos metodos

       atributos    : declaracion_variables 

       metodos      : declaracion_funciones 

       nueva_clase  : clases'''

def p_declaracion_variables(p):
  '''declaracion_variables : variables PUNTO_COMA declaracion_variables
                           | vacio'''

def p_variables(p):
    '''variables : VAR tipo_compuesto ID aux1
                 | VAR tipo_simple ID aux2 aux3
    
        aux1 : COMA ID aux1
             | vacio
        
        aux2 : CORCHETE_I CTEINT CORCHETE_D
             | CORCHETE_I CTEINT COMA CTEINT CORCHETE_D
             | vacio
            
        aux3 : COMA ID aux2 aux3
             | vacio'''
    # Add variable into symbol table
    if (p[1] == 'var'):
        s_var_declaration_ids.append(p[3])
        while len(s_var_declaration_ids) > 0:
            print("Variable added into symbolTable ->",s_var_declaration_ids[-1] )
            symbol_table.add_item(s_scopes[-1] , s_var_declaration_ids.pop(), current_type)

    elif (p[1] == ','):
        s_var_declaration_ids.append(p[2])
        print("APPEND variable to var_declaration stack ->", p[2])

def p_tipo_simple(p):
    '''tipo_simple : INT 
                    | FLOAT 
                    | CHAR'''
    global current_type
    current_type = p[1]

def p_tipo_compuesto(p):
    '''tipo_compuesto : ID 
                    | DATAFRAME
                    | FILE'''
    global current_type
    current_type = p[1]

def p_declaracion_funciones(p):
  '''declaracion_funciones : funciones funciones2
                           | vacio'''

def p_funciones(p):
  '''funciones    : FUNC funciones_tipo ID  

    funciones_tipo : tipo_simple  
                   | VOID'''
    
    # Add function scope into stack
  if (p[1] == "func"):
    s_scopes.append(p[3])
    print("Scope added in stack: ", p[3])

    # Add function into Symbol Table
    symbol_table.add_scope(p[3], p[2])
    print("Scope added in symbol table: ", p[3])


def p_funciones2(p): 
    '''funciones2  : PARENTESIS_I declaracion_parametros PARENTESIS_D LLAVE_I declaracion_variables estatutos LLAVE_D pop_scope funciones_rep
    funciones_rep  : funciones funciones2
                   | vacio'''

# Remove  scope from stack
def p_pop_scope(p):
  'pop_scope :'
  #s_scopes.pop()
  print("Scope deleted from STACK:", s_scopes.pop())

def p_declaracion_parametros(p):
    '''declaracion_parametros : param param2
                              | vacio'''

def p_param(p):
    '''param : tipo_simple ID '''    
    symbol_table.add_item(s_scopes[-1], p[2], current_type)
    print("----- Added parameter", p[2], "with type", current_type)

def p_param2(p):
    '''param2 : COMA param param2
              | vacio'''

def p_estatuto(p):
    '''estatuto : asignacion
                | llamada_void
                | retorno
                | lectura
                | escritura
                | condicion
                | ciclo_while
                | ciclo_for'''

def p_variable(p):
    '''variable : ID h
       h        : CORCHETE_I expresion CORCHETE_D 
                | CORCHETE_I expresion COMA expresion CORCHETE_D
                | vacio '''

def p_asignacion(p):
    'asignacion : variable IGUAL expresion PUNTO_COMA'

def p_llamada_void(p):
    '''llamada_void : ID PARENTESIS_I expresion I PARENTESIS_D

       I            : COMA expresion I 
                    | vacio'''

def p_lectura(p):
    'lectura : READ variable'

def p_retorno(p):
    'retorno : RETURN expresion PUNTO_COMA'

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

def p_ciclo_while(p):
    'ciclo_while : WHILE PARENTESIS_I expresion PARENTESIS_D bloque'

def p_ciclo_for(p):
    'ciclo_for : FOR variable IGUAL expresion UNTIL bloque'

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
        exit()
    # else:
    #     print('Syntax error at EOF')


## Contruir parser
parser = yacc.yacc()

print(data)
parser.parse(data)

## Cerrar archivo
f.close()



