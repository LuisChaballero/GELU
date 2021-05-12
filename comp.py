import ply.lex as lex
import ply.yacc as yacc
from lexer import *

from collections import deque

from SymbolTable import SymbolTable
from SemanticTypeTable import SemanticTypeTable
from ClassDirectory import ClassDirectory

# --------------
# Build lexer (lexer)
lexer = lex.lex()

# Read text file (prueba1.txt / prueba2.txt)
f = open('prueba2.txt','r')
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
s_types = deque() # To keep track of the operands' types
s_print_items = deque() # To keep track of all the strings and expresions used in a PRINT
s_jumps = deque() # To keep track of all the conditional jumps for GOTO

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
    'programa : PROGRAM init_global_env ID program_name PUNTO_COMA declaracion_clases declaracion_variables declaracion_funciones main'

# Create an instance of ...
def p_init_global_env(p):
    'init_global_env :'
    global symbol_table
    global semantic_cube
    global class_directory

    symbol_table = SymbolTable()
    semantic_cube = SemanticTypeTable()
    class_directory = ClassDirectory()

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
    print("---- SymbolTable")
    symbol_table.print()
    print("---- ClassDirectory")
    class_directory.print()
    class_directory.get_scope('mult').print()
    print("---------------- QUADRUPULES LIST -------------------")
    for index in range(len(l_quadrupules)):
        print(index, l_quadrupules[index])
    # print(*l_quadrupules,sep = "\n")

def p_bloque(p):
    '''bloque     : LLAVE_I estatutos LLAVE_D

       estatutos  : estatuto estatutos
                  | vacio'''

def p_declaracion_clases(p):
    '''declaracion_clases : clases clases_02 
                          | vacio '''

def p_clases(p):
    '''clases       : CLASS ID herencia LLAVE_I 
                    
       herencia     : MENOR_QUE INHERITS MAYOR_QUE 
                    | vacio'''
    if(p[1] == 'class'):
        class_directory.add_class(p[2])
        s_scopes.append(p[2])

        # Create attribute Table (similar to Global variables in Symbol Table)
        class_directory.add_attributes_Table(p[2], 'Class_Globals', 'NC')
        s_scopes.append('Class_Globals')

def p_clases_02(p):
    '''clases_02 : atributos metodos LLAVE_D PUNTO_COMA pop_scope nueva_clase   

       atributos : add_scope_attributes declaracion_variables 

       metodos   : add_scope_methods declaracion_funciones pop_scope
       
       nueva_clase : clases clases_02
                   | vacio'''

def p_add_scope_attributes(p):
    'add_scope_attributes :'
    # s_scopes.append('Attributes')

def p_add_scope_methods(p):
    'add_scope_methods :'
    # s_scopes.append('Methods')

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
        # Add the left-most variable (last) into stack   
        s_var_declaration_ids.append(p[3]) 

        # Get the current scope
        current_scope = s_scopes.pop()  
        # Put variables from stack into symbol table or class directory
        while len(s_var_declaration_ids) > 0:
            print(s_scopes)
            # print("Variable added into symbolTable ->",s_var_declaration_ids[-1] )
            # symbol_table.add_item(s_scopes[-1] , s_var_declaration_ids.pop(), current_type)
          
            if(current_scope == 'Global' ): # Global variables in SymbolTable  
                variable_id = s_var_declaration_ids.pop()

                # Add global variable into Symbol Table
                symbol_table.add_item(current_scope , variable_id, current_type)
                print("+Global variable added into symbolTable ->", variable_id )
                
            elif(current_scope == 'Class_Globals'): # Local variables in Class 
                class_name = s_scopes[-1]
                attribute_id = s_var_declaration_ids.pop()

                # Add local variable in class scope 
                class_directory.add_attribute(class_name, current_scope, attribute_id, current_type)
                print("+Global attribute added into ClassDirectory ->", class_name, current_scope, attribute_id, current_type)
            
            elif(s_scopes[-1] == 'Class_Globals'): # Local variables in Methods in Class 
                method_name = current_scope
                s_scopes.pop() # Pop out 'Class_Globals' scope
                class_name = s_scopes[-1]
                variable_id = s_var_declaration_ids.pop()

                # Add local variable in Method scope of a class 
                class_directory.add_variable(class_name, method_name, variable_id, current_type)
                print("+Local variable in a Method added into ClassDirectory ->", class_name, method_name, variable_id, current_type)

                # Put 'Class_Globals' into stack
                s_scopes.append('Class_Globals')

            elif(s_scopes[-1] == 'Global'): # Local variables in functions in SymbolTable
                function_name = current_scope
                variable_id = s_var_declaration_ids.pop()

                # Add local variable in function scope on SymbolTable
                symbol_table.add_item(function_name, variable_id, current_type)
                print("+Local variable in a Function added into symbolTable ->", function_name, variable_id, current_type )

        s_scopes.append(current_scope) 
           
    elif (p[1] == ','):
        # Add variable into stack
        s_var_declaration_ids.append(p[2])
        # print("APPEND variable to var_declaration stack ->", p[2])

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
        function_name = p[3]
        current_scope = s_scopes[-1]
        if(current_scope == 'Global'): # Add function in Symbol Table
            
            # print("Scope added in stack: ", p[3])

            # Add function into Symbol Table
            symbol_table.add_scope(function_name, current_type)
            s_scopes.append(function_name)
            print("FUNCTION added in Symbol Table: ", function_name, current_type)

        else: # Add method in class directory
            
            s_scopes.pop() # Remove 'Class_Globals'
            class_name = s_scopes[-1] # Class scope
            s_scopes.append(current_scope) # Add 'Class_Globals'

            # Add method in class
            class_directory.add_method(class_name, function_name, current_type)
            s_scopes.append(function_name)
            print("METHOD added in Class Directory: ", class_name, function_name, current_type)

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
                | ciclo_for_01'''

def p_variable(p):
    '''variable : ID h
       h        : CORCHETE_I expresion CORCHETE_D 
                | CORCHETE_I expresion COMA expresion CORCHETE_D
                | vacio '''
    if(len(p) == 3):
        s_operands.append(p[1])
        variable_type = symbol_table.get_scope(s_scopes[-1]).search(p[1])
        if(not variable_type == False):
            s_types.append(variable_type)
        else:
            print("Variable", p[1], "is not declared")
            exit()

def p_asignacion(p):
    'asignacion : variable IGUAL expresion PUNTO_COMA'


    expresion_result = s_operands.pop() # Result of the expresion 
    expresion_type = s_types.pop() # Result's type

    variable_operand = s_operands.pop()
    variable_type = s_types.pop()

    # print("&&& Asignacion expresion_result: ", expresion_result) 
    # print("&&& Asignacion expresion_type: ", expresion_type) 
    # print("&&& Asignacion variable_operand: ", variable_operand) 
    # print("&&& Asignacion variable_type: ", variable_type) 

    if(variable_type == expresion_type):
        quadruple = (p[2], expresion_result, None, variable_operand) 
        l_quadrupules.append(quadruple) # add quadrupule to list
        print(quadruple) 
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
    '''escritura : PRINT PARENTESIS_I escritura2 PARENTESIS_D quad_print PUNTO_COMA'''

def p_escritura2(p):
    '''escritura2 : CTESTRING k
                  | expresion k append_expresion_print

       k         : COMA escritura2
                 | vacio '''
    if(len(p) == 3 and not p[1] == ',' and not p[1] == ')'):
        print("\n\nESCRITURA:", p[1])
        s_print_items.append(p[1])
        print("PRINT STRING APPEND:",p[1])

def p_quad_print(p):
    'quad_print :'
    while(len(s_print_items) > 0):
        item = s_print_items.pop()
        quadruple = ('PRINT', None, None, item)
        l_quadrupules.append(quadruple)
        print(quadruple)

def p_append_expresion_print(p):
    'append_expresion_print : '
    res_expresion = s_operands.pop() # Result of the expresion
    s_types.pop() # Take out the expresion's result type

    s_print_items.append(res_expresion)
    # print("PRINT EXPRESION APPEND:", res_expresion)
                
def p_condicion(p):
    '''condicion : IF PARENTESIS_I expresion PARENTESIS_D quad_IF_01 bloque l quad_IF_02

       l         : ELSE quad_IF_03 bloque
                 | vacio'''

# Generate quadrupules of GOTOF 
def p_quad_IF_01(p):
    'quad_IF_01 : '
    res_type = s_types.pop() # Obtain expression's type

    if(not res_type == 'ERROR'):
        res_expresion = s_operands.pop() # Obtain result of the expression

        # Generate "incomplete" qudrupule
        false_quadruple = ('GOTOF', res_expresion, None, None)
        l_quadrupules.append(false_quadruple )

        index_GOTOF = len(l_quadrupules)-1 # Obtain the current/last index of the quadrupule´s list
        s_jumps.append(index_GOTOF) # Put the index of the incomplete qudrupule on stack
    else:
        print("Error: Type mismatch on expression IF")
        exit()

def p_quad_IF_02(p):
    'quad_IF_02 :'
    pending_GOTO_index= s_jumps.pop() # Index of an incompleted quadrupule
    old_GOTO_quadrupule = l_quadrupules[pending_GOTO_index] # Obtain incompleted GOTO quadrupule
    print("OLD QUADRUPULE", old_GOTO_quadrupule)

    next_index = len(l_quadrupules) # index to skip over the else statement

    # Replace GOTO quadrupule with the one that knows where to jump
    new_GOTO_quadrupule = (old_GOTO_quadrupule[0], old_GOTO_quadrupule[1], None, next_index) # Complete quadrupule: (GOTOF, res_expresion, None, index)
    l_quadrupules[pending_GOTO_index] = new_GOTO_quadrupule 
    # print("NEW QUADRUPULE", new_GOTO_quadrupule)

def p_quad_IF_03(p):
    'quad_IF_03 :'
    false_quadrupule = s_jumps.pop()

    quadrupule_GOTO = ('GOTO', None, None, None)
    l_quadrupules.append(quadrupule_GOTO)

    index_GOTO = len(l_quadrupules)-1 # Index of incompleted GOTO quadrupule
    s_jumps.append(index_GOTO)

    # Replace previous GOTOF quadrupule with the one that knows where to jump
    qudrupule_GOTOF = l_quadrupules[false_quadrupule]
    # print("OLD qudrupule_GOTOF",qudrupule_GOTOF)
    qudrupule_GOTOF = (qudrupule_GOTOF[0], qudrupule_GOTOF[1], None, index_GOTO + 1) 
    # print("NEW qudrupule_GOTOF",qudrupule_GOTOF)

    l_quadrupules[false_quadrupule] = qudrupule_GOTOF 

def p_ciclo_while(p):
    'ciclo_while : WHILE PARENTESIS_I quad_while_01 expresion PARENTESIS_D quad_while_02 bloque quad_while_03'
    
def p_quad_while_01(p):
    'quad_while_01 :'
    first_quadruple_expresion_index = len(l_quadrupules)
    s_jumps.append(first_quadruple_expresion_index)

def p_quad_while_02(p):
    'quad_while_02 :'
    res_expresion_type = s_types.pop()

    if(res_expresion_type == 'ERROR'):
        print("Error: Type mismatch in while")
        exit()
    else:
        res_expresion = s_operands.pop()
        quadruple_GOTOF = ('GOTOF', res_expresion, None, None)
        l_quadrupules.append(quadruple_GOTOF)
        # print("quadruple_GOTOF",quadruple_GOTOF)

        index_previous_GOTOF = len(l_quadrupules)-1
        s_jumps.append(index_previous_GOTOF)
        # print("index_previous_GOTOF",index_previous_GOTOF)

def p_quad_while_03(p):
    'quad_while_03 :'
    index_previous_GOTOF = s_jumps.pop() 
    index_expresion = s_jumps.pop()
    # print("index_previous_GOTOF",index_previous_GOTOF)
    # print("index_expresion",index_expresion)

    quadruple_GOTO = ('GOTO', None, None, index_expresion)
    # l_quadrupules
    l_quadrupules.append(quadruple_GOTO)
    # print("quadruple_GOTO",quadruple_GOTO)

    index_skip = len(l_quadrupules) # index to skip while

    quadruple_previous_GOTOF = l_quadrupules[index_previous_GOTOF] 
    new_quadruple = (quadruple_previous_GOTOF[0], quadruple_previous_GOTOF[1], None, index_skip)
    l_quadrupules[index_previous_GOTOF] = new_quadruple

def p_ciclo_for_01(p):
    'ciclo_for_01 : FOR variable IGUAL exp quad_for_01 ciclo_for_02'

def p_ciclo_for_02(p):
    'ciclo_for_02 : UNTIL quad_for_02 expresion quad_for_03 bloque quad_for_04'

def p_quad_for_01(p):
    'quad_for_01 :'
    exp_type = s_types.pop()
    exp_result = s_operands.pop()  
    print("exp_type", exp_type)

    var_type = s_types.pop()
    variable = s_operands.pop()

    if (exp_type != var_type):
        print("Error: ", exp_type, "not assignable to", var_type)
        exit()
    elif(var_type != 'int'):
        print("Error: ", variable, "is not of type INT")
        exit()
    else:
        quadruple_EQUAL = ('EQUAL', exp_result, None, variable)
        l_quadrupules.append(quadruple_EQUAL)

        # s_operands.append(variable)
        # s_types.append(var_type)

def p_quad_for_02(p):
    'quad_for_02 :'
    # Save the index to the first quadrupule of the expression
    index_before_exp = len(l_quadrupules)
    s_jumps.append(index_before_exp)

def p_quad_for_03(p):
    'quad_for_03 :'
    expresion_type = s_types.pop()
    expresion_result = s_operands.pop()  
    print("expresion_type:", expresion_type )

    if(expresion_type != 'bool'):
        print("Error: Expression result from FOR must be boolean ")
        exit()
    else:
        # var_type = s_types.pop()
        # variable = s_operands.pop()

        # Generate incomplete quadrupule to skip Bloque
        quad_GOTOF = ('GOTOF', expresion_result, None, None)
        l_quadrupules.append(quad_GOTOF)

        # Save the index to the incomplete GOTOF
        index_GOTOF = len(l_quadrupules)-1
        s_jumps.append(index_GOTOF)

def p_quad_for_04(p):
    'quad_for_04 :'
    # Obtain saved indexes
    index_pending_GOTF = s_jumps.pop()
    index_to_expresion = s_jumps.pop()

    # Quadrupule to check value of the FOR´s expression
    quadruple_GOTO = ('GOTO', None, None, index_to_expresion)
    l_quadrupules.append(quadruple_GOTO)

    # Add the missing index to the previous GOTOF to skip Bloque when expression is false
    pending_GOTF = l_quadrupules[index_pending_GOTF] 
    pending_GOTF= (pending_GOTF[0], pending_GOTF[1], None, len(l_quadrupules))
    l_quadrupules[index_pending_GOTF] = pending_GOTF

def p_expresion(p):
    '''expresion : exp m quadrupule_creation_relational

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
                result = temporal_variable_base_name + str(temporal_variable_count)
                temporal_variable_count += 1
                print("temporal variable: ", result)

                quadruple = (operator, left_operand, right_operand, result) # 'result' is supposed to be temporal space
                l_quadrupules.append(quadruple) # add quadrupule to list
                print(quadruple) 

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
                result = temporal_variable_base_name + str(temporal_variable_count)
                temporal_variable_count += 1
                print("temporal variable: ", result)

                quadruple = (operator, left_operand, right_operand, result) # 'result' is supposed to be temporal space
                l_quadrupules.append(quadruple) # Add quadrupule to list
                print(quadruple) 

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
                result = temporal_variable_base_name + str(temporal_variable_count)
                temporal_variable_count += 1
                print("temporal variable: ", result)

                quadruple = (operator, left_operand, right_operand, result) # 'result' is supposed to be temporal space
                l_quadrupules.append(quadruple) # add quadrupule to list
                print(quadruple) 

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
        operand_type = symbol_table.get_scope(s_scopes[-1]).search(p[1]) # Get variable´s type

        if(operand_type):
            s_operands.append(p[1])
            print("$$$ Operand ", p[1], "added into s_operands $$$")

            s_types.append(operand_type)
            print("$$$ Operand_type added into stack: ", operand_type)
        else:
            print("Variable", p[1], "is not declared")
            exit()
    # Pendiente considerar las constantes alv. Ponte vergas
    
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



