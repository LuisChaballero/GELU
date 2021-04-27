import ply.lex as lex
import ply.yacc as yacc
from lexer import *

from collections import deque

from SymbolTable import SymbolTable
from SemanticTypeTable import SemanticTypeTable

# --------------
# Build lexer (lexer)
lexer = lex.lex()

# Read text file (prueba1.txt / prueba2.txt)
f = open('prueba1.txt','r')
data = f.read()

# Test lex with text file
lexer.input(data)

# Tokenize
for tok in lexer:
    print(tok)

#--------------

# Declared stacks
s_scopes = deque() # To keep track of scopes
s_var_declaration_ids = deque() # To keep track of type for var declaration
s_operators = deque() # To keep track of operators in expresions
s_operands = deque() # To keep track of operands in expresions
s_types = deque() # ???

# Declared lists
l_quadrupules = [] # To save the code optimization in form of quadrupules. (op, op_izq, op_der, res)

# current type for declared variable 
current_type = ''

# Simulates the implementation of temporal variables 
temporal_variable_base_name = "temp"
temporal_variable_count = 0

# Precedence
precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'ENTRE'),
)

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
    global semantic_cube
    symbol_table = SymbolTable()
    semantic_cube = SemanticTypeTable()

# Add row to SymbolTable for global
def p_program_name(p):
  'program_name :'
  s_scopes.append('Global')
#   print("Scope added in STACK: Global")
  symbol_table.add_scope('Global', 'NP')
#   print("Scope added in SYMBOL TABLE: Global")

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
    # Add variables into symbol table
    if (p[1] == 'var'):
        s_var_declaration_ids.append(p[3])
        # Put variables from stack into symbol table
        while len(s_var_declaration_ids) > 0:
            print("Variable added into symbolTable ->",s_var_declaration_ids[-1] )
            symbol_table.add_item(s_scopes[-1] , s_var_declaration_ids.pop(), current_type)

    elif (p[1] == ','):
        # Add variable into stack
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
  print("Scope deleted from STACK:", s_scopes.pop())

def p_declaracion_parametros(p):
    '''declaracion_parametros : param param2
                              | vacio'''

def p_param(p):
    '''param : tipo_simple ID '''    
    # Add parameter (local variable) into function scope
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
    if(len(p) == 3):
        s_operands.append(p[1])
        variable_type = symbol_table.get_scope(s_scopes[-1]).search(p[1])
        s_types.append(variable_type)

        

def p_asignacion(p):
    'asignacion : variable IGUAL expresion PUNTO_COMA'


    expresion_result = s_operands.pop() # Result of the expresion 
    expresion_type = s_types.pop() # Result's type

    variable_operand = s_operands.pop()
    variable_type = s_types.pop()

    print("&&& Asignacion expresion_result: ", expresion_result) 
    print("&&& Asignacion expresion_type: ", expresion_type) 
    print("&&& Asignacion variable_operand: ", variable_operand) 
    print("&&& Asignacion variable_type: ", variable_type) 

    if(variable_type == expresion_type):
        print("&&& Asignacion p[2](=): ", p[2])
        quadrupule = (p[2], expresion_result, None, variable_operand) 
        l_quadrupules.append(quadrupule) # add quadrupule to list
        print(quadrupule) 
    else:
        print("Type mismatch in Asignacion:", expresion_type, "not assignable to", variable_type)
        exit()

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
    '''expresion : exp  m quadrupule_creation_relational

       m         : MAYOR_QUE greater_than_append exp
                 | MENOR_QUE less_than_append exp
                 | NO_IGUAL different_append exp
                 | vacio''' 

def p_quadrupule_creation_relational(p):
    'quadrupule_creation_relational :'
    print("#################Quadrupul_creation_relation")
    if(len(s_operators) != 0):
        if(s_operators[-1] == 'MAYOR_QUE' or s_operators[-1] == 'MENOR_QUE' or s_operators[-1] == 'NO_IGUAL' ):
            right_operand = s_operands.pop() # Get right operand from stack
            right_type = s_types.pop() # Get right operand's type from stack

            left_operand = s_operands.pop() # Get left operand from stack
            left_type = s_types.pop() # Get left operand's type from stack

            operator = s_operators.pop() # Get operand from stack

            res_type = semantic_cube.result_type(left_type, right_type, operator)

            if(not res_type == 'ERROR'):
                # Temporable variable simulation
                global temporal_variable_count
                temporal_variable_count += 1
                result = temporal_variable_base_name + str(temporal_variable_count)
                print("temporal variable: ", result)

                quadrupule = (operator, left_operand, right_operand, result) # 'result' is supposed to be temporal space
                l_quadrupules.append(quadrupule) # add quadrupule to list
                print(quadrupule) 

                s_operands.append(result) # Add the result into the operands stack
                s_types.append(res_type) # Add result's type into the types stack
            else:
                print("Error: Type mismatch")
                exit()


def p_greater_than_append(p):
    'greater_than_append :'
    s_operators.append('MAYOR_QUE')
    print("$$$ Addition operator MAYOR_QUE appended in stack $$$")

def p_less_than_append(p):
    'less_than_append :'
    s_operators.append('MENOR_QUE')
    print("$$$ Addition operator MENOR_QUE appended in stack $$$")

def p_different_append(p):
    'different_append :'
    s_operators.append('NO_IGUAL')
    print("$$$ Different operator NO_IGUAL appended in stack $$$")

def p_exp(p):
    '''exp : termino quadrupule_creation_01 n

       n   : MAS addition_append exp 
           | MENOS substraction_append exp
           | vacio'''               

def p_addition_append(p):
    'addition_append :'
    # Push addition operator into operator stack
    s_operators.append('MAS')
    print("$$$ Addition operator MAS appended in stack $$$")

def p_substraction_append(p):
    'substraction_append :'
    # Push substraction operator into operator stack
    s_operators.append('MENOS')
    print("$$$ Substraction operator MENOS appended in stack $$$")

def p_quadrupule_creation_01(p):
    'quadrupule_creation_01 :'
    print("quadrupule_creation_01 start")
    if(len(s_operators) != 0): 
        if(s_operators[-1] == 'MAS' or s_operators[-1] == 'MENOS'):
            right_operand = s_operands.pop() # Get right operand from stack
            right_type = s_types.pop() # Get right operand's type from stack
            
            left_operand = s_operands.pop() # Get left operand from stack
            left_type = s_types.pop() # Get left operand's type from stack

            operator = s_operators.pop() # Get operand from stack

            res_type = semantic_cube.result_type(left_type, right_type, operator)
            print("res_type : ", res_type)

            if(not res_type == 'ERROR'):
                # Temporable variable simulation
                global temporal_variable_count
                temporal_variable_count += 1
                result = temporal_variable_base_name + str(temporal_variable_count)
                print("temporal variable: ", result)

                quadrupule = (operator, left_operand, right_operand, result) # 'result' is supposed to be temporal space
                l_quadrupules.append(quadrupule) # Add quadrupule to list
                print(quadrupule) 

                s_operands.append(result) # Add the result into the operands stack
                s_types.append(res_type) # Add result's type into the types stack
            else:
                print("Error: Type mismatch")
                exit()

def p_termino(p):
    '''termino : factor quadrupule_creation_02 o

       o       : POR multiplication_append termino 
               | ENTRE divition_append termino
               | vacio'''

def p_multiplication_append(p):
    'multiplication_append :'
    s_operators.append('POR')
    print("$$$ Multiplication POR appended in stack$$$")

def p_divition_append(p):
    'divition_append :'
    s_operators.append('ENTRE')
    print("$$$ Divition operator ENTRE in stack $$$")

def p_quadrupule_creation_02(p): 
    'quadrupule_creation_02 :'
    print("quadrupule_creation_02 start")
    if(len(s_operators) != 0):
        if(s_operators[-1] == 'POR' or s_operators[-1] == 'ENTRE'):
            right_operand = s_operands.pop() # Get right operand from stack
            right_type = s_types.pop() # Get right operand's type from stack

            left_operand = s_operands.pop() # Get left operand from stack
            left_type = s_types.pop() # Get left operand's type from stack

            operator = s_operators.pop() # Get operand from stack

            res_type = semantic_cube.result_type(left_type, right_type, operator)

            if(not res_type == 'ERROR'):
                # Temporable variable simulation
                global temporal_variable_count
                temporal_variable_count += 1
                result = temporal_variable_base_name + str(temporal_variable_count)
                print("temporal variable: ", result)

                quadrupule = (operator, left_operand, right_operand, result) # 'result' is supposed to be temporal space
                l_quadrupules.append(quadrupule) # add quadrupule to list
                print(quadrupule) 

                s_operands.append(result) # Add the result into the operands stack
                s_types.append(res_type) # Add result's type into the types stack
            else:
                print("Error: Type mismatch")
                exit()

# def p_factor(p):
#     '''factor : varcte 
#               | ID factor2
#               | PARENTESIS_I expresion PARENTESIS_D
#               | MAS varcte
#               | MENOS varcte'''

def p_factor(p):
    '''factor : varcte 
              | ID factor2
              | PARENTESIS_I parenthesis_left_append expresion PARENTESIS_D parenthesis_left_pop'''

    # Add ID into operands stack. 
    if(len(p) == 3):
        s_operands.append(p[1])
        print("$$$ Operand ", p[1], "added into s_operands $$$")

        operand_type = symbol_table.get_scope(s_scopes[-1]).search(p[1]) # Get variable´s type
        s_types.append(operand_type)
        print("$$$ Operand_type added into stack: ", operand_type)
def p_parenthesis_left_append(p):
    'parenthesis_left_append :'
    s_operators.append('PARENTESIS_I')
    print("$$$ Parenteis Izquierdo en stack")

def p_parenthesis_left_pop(p):
    'parenthesis_left_pop :'
    s_operators.pop()
    print("$$$ Parenteis izquierdo sacado del stack $$$")

def p_factor2(p):
    '''factor2 : CORCHETE_I expresion CORCHETE_D
               | CORCHETE_I expresion COMA expresion CORCHETE_D
               | PARENTESIS_I expresion multiple_expresion PARENTESIS_D
               | PUNTO ID
               | PUNTO ID PARENTESIS_I r PARENTESIS_D
               | vacio

       r      : varcte s
              | vacio
              
       s      : COMA varcte  s
              | vacio '''

def p_multiple_expresion(p):
    '''multiple_expresion : COMA expresion multiple_expresion
                          | vacio '''

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



