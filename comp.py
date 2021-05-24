import ply.lex as lex
import ply.yacc as yacc
from lexer import *

from collections import deque

from Classes.FunctionDirectory import FunctionDirectory
from Classes.SemanticTypeTable import SemanticTypeTable
from Classes.ClassDirectory import ClassDirectory
import Classes.MemoryHandler as mh
from Classes.VirtualMachine import VirtualMachine



# --------------
# Build lexer (lexer)
lexer = lex.lex()

# Read text file (prueba1.txt / prueba2.txt)
f = open('prueba3.txt','r')
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
s_function_call_arguments = deque() # To verify the arguments in a function call with parameters table
s_function_call_argument_types = deque() # Arguments' type in a function call

# Declared lists
l_quadrupules = [] # To save the code optimization in form of quadrupules. (op, op_izq, op_der, res)


# current type for declared variable 
current_type = ''

# Catches the constant
current_constant = None
current_constant_type = ''

# Simulates the implementation of temporal variables 
temporal_variable_base_name = "temp"
temporal_variable_count = 0

# Counter to verify the arguments in a function call with the parameters table
argument_counter = 0

# Helper functions

# Function to add variables to memory_directory depending on their scope
def variable_declaration(class_directory, function_directory, memory_directory, current_scope, variable_dimension, variable_id, m1):
  # Check variable scope
  if(current_scope == 'Global' ): # Global variables in FunctionDirectory  

    virtual_address = memory_directory.get_address(current_type, "global", "variable")
    print()
    memory_directory.add_item(current_type, "global", "variable")

    # There's an error adding global variable into Function Directory
    if variable_dimension == "simple" and function_directory.add_item(current_scope, variable_id, current_type, virtual_address, False, m1) == False:
      print("ERROR: Failed at declaring global variable", variable_id)
      exit()
   
    # There's an error adding global array or matrix into Function Directory
    elif (variable_dimension == "array" or variable_dimension == "matrix") and function_directory.add_item(current_scope, variable_id, current_type, virtual_address, True, m1) == False:
      print("ERROR: Failed at declaring global variable array", variable_id)
      exit()
    
    print("+++++Global variable added into functionDirectory ->", variable_id, current_type, virtual_address, variable_dimension, m1)
      
  elif(current_scope == 'Class_Globals'): # Global variables (attributes) in Class 
    class_name = s_scopes[-1]
    attribute_id = s_var_declaration_ids.pop()

    virtual_address = memory_directory.get_class_address(current_type, "global", "variable")
    memory_directory.add_class_item(current_type, "global", "variable", virtual_address)

    # There's an error adding global variable into Function Directory
    if variable_dimension == "simple" and class_directory.add_attribute(current_scope, variable_id, current_type, virtual_address, False, m1) == False:
      print("ERROR: Failed at declaring attribute", variable_id  ,"in class", class_name)
      exit()
   
    # There's an error adding global array or matrix into Function Directory
    elif (variable_dimension == "array" or variable_dimension == "matrix") and class_directory.add_attribute(current_scope, variable_id, current_type, virtual_address, True, m1) == False:
      print("ERROR: Failed at declaring array or matrix attribute", variable_id  ,"in class", class_name)
      exit()
    

    # # Add attribute into Class Directory
    # if variable_dimension == "simple" and class_directory.add_attribute(current_scope , variable_id, current_type, virtual_address, False, m1) == False:
    #     print("ERROR: Failed at declaring attribute", variable_id, "in class", class_name)
    #     exit()
   
    # # Add attribute (array or matrix) into Class Directory
    # else:
    #   if class_directory.add_attribute(current_scope , variable_id, current_type, virtual_address, True, m1) == False:
    #     print("ERROR: Failed at declaring attribute", variable_id, "in class", class_name)
    #     exit()

    # # Add attributes in class scope 
    # if not class_directory.add_attribute(class_name, current_scope, attribute_id, current_type):
    #   print("ERROR: Failed at declaring attributes in class", class_name)
    #   exit()
    print("+Global attribute added into ClassDirectory ->", class_name, current_scope, attribute_id, current_type)
  
  elif(s_scopes[-1] == 'Class_Globals'): # Local variables in Methods in Class 
    method_name = current_scope
    s_scopes.pop() # Pop out 'Class_Globals' scope
    class_name = s_scopes[-1]

    virtual_address = memory_directory.get_class_address(current_type, "local", "variable")
    memory_directory.add_class_item(current_type, "local", "variable", virtual_address)

    # There's an error adding global variable into Function Directory
    if variable_dimension == "simple" and class_directory.add_variable(current_scope, variable_id, current_type, virtual_address, False, m1) == False:
      print("ERROR: Failed at declaring local vairbale", variable_id, "on method", method_name, "on class", class_name)
      exit()
   
    # There's an error adding global array or matrix into Function Directory
    elif (variable_dimension == "array" or variable_dimension == "matrix") and class_directory.add_variable(current_scope, variable_id, current_type, virtual_address, True, m1) == False:
      print("ERROR: Failed at declaring local vairbale", variable_id, "on method", method_name, "on class", class_name)
      exit()

      
    print("+Local variable in a Method added into ClassDirectory ->", class_name, method_name, variable_id, current_type)

    # Put 'Class_Globals' into stack
    s_scopes.append('Class_Globals')

  elif(s_scopes[-1] == 'Global'): # Local variables in functions in functionDirectory
      function_name = current_scope

      virtual_address = memory_directory.get_address(current_type, "local", "variable")
      memory_directory.add_item(current_type, "local", "variable")

      # There's an error adding global variable into Function Directory
      if variable_dimension == "simple" and function_directory.add_item(current_scope, variable_id, current_type, virtual_address, False, m1) == False:
        print("ERROR: Failed at declaring local variable", variable_id,"in", function_name)
        exit()
    
      # There's an error adding global array or matrix into Function Directory
      elif (variable_dimension == "array" or variable_dimension == "matrix") and function_directory.add_item(current_scope, variable_id, current_type, virtual_address, True, m1) == False:
        print("ERROR: Failed at declaring local variable", variable_id,"in", function_name)
        exit()

      # if variable_dimension == "simple" and function_directory.add_item(current_scope , variable_id, current_type, virtual_address, False, m1) == False:
      #   print("ERROR: Failed at declaring local variable", variable_id,"in", function_name)
      #   exit()
   
      # # Add global array or matrix into Function Directory
      # else:
      #   if function_directory.add_item(current_scope , variable_id, current_type, virtual_address, True, m1) == False:
      #     print("ERROR: Failed at declaring local variable", variable_id,"in", function_name)
      #     exit()

      # # Add local variable in function scope on FunctionDirectory
      # if not function_directory.add_item(function_name, variable_id, current_type, virtual_address):
      #   print("ERROR: Failed at declaring local variable", variable_id,"in", function_name)
      #   exit()

      print("++Local variable in a Function added into functionDirectory ->", function_name, variable_id, current_type ,virtual_address)

# Start of grammar
start = 'programa'

def p_vacio(p):
     'vacio :'
     pass

def p_programa(p):
    'programa : PROGRAM init_global_env ID program_name PUNTO_COMA quad_GOTO_Main declaracion_clases declaracion_variables declaracion_funciones main'

# Create an instance of ...
def p_init_global_env(p):
    'init_global_env :'
    global function_directory
    global semantic_cube
    global class_directory
    global memory_directory
    
    function_directory = FunctionDirectory()
    semantic_cube = SemanticTypeTable()
    class_directory = ClassDirectory()
    memory_directory = mh.MemoryHandler()

# Add row to FunctionDirectory for global
def p_program_name(p):
  'program_name :'
  s_scopes.append('Global')
#   print("Scope added in STACK: Global")
  function_directory.add_scope('Global', 'NP')
#   print("Scope added in FUNCTION DIRECTORY: Global")

def p_quad_GOTO_Main(p):
    'quad_GOTO_Main :'
    pending_GOTO_Main = ('GOTO', None, None, None) #  
    l_quadrupules.append(pending_GOTO_Main)

    pending_GOTO_Main_index = len(l_quadrupules)-1
    s_jumps.append(pending_GOTO_Main_index)

def p_main(p):
    'main : MAIN PARENTESIS_I PARENTESIS_D fill_pending_GOTO_Main bloque append_END_quad'
    #   
    s_scopes.pop()
    print("Scope deleted from STACK: Global")
    print("---- FunctionDirectory")
    function_directory.print()

    print("---------------- QUADRUPULES LIST -------------------")
    for index in range(len(l_quadrupules)):
        print(index, l_quadrupules[index])
    print("")
    virtual_machine = VirtualMachine(l_quadrupules, memory_directory, class_directory, function_directory)

    

def p_fill_pending_GOTO_Main(p):
    'fill_pending_GOTO_Main :'
    pending_GOTO_Main_index = s_jumps.pop()
    pending_GOTO_Main = l_quadrupules[pending_GOTO_Main_index]

    first_quadruple_of_Main = len(l_quadrupules)
    new_GOTO_Main = (pending_GOTO_Main[0], None, None, first_quadruple_of_Main)

    l_quadrupules[pending_GOTO_Main_index] = new_GOTO_Main
def p_append_END_quad(p):
    'append_END_quad :'
    quadruple_END = ('END', None, None, None)
    l_quadrupules.append(quadruple_END)
    print(quadruple_END)

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
        if class_directory.add_class(p[2]) == False:
            print("Error: Class",p[2],"already exists")
            exit()
        else:
            s_scopes.append(p[2])

            # Create attribute Table (similar to Global variables in Function Directory)
            class_directory.add_attributes_Table(p[2], 'Class_Globals', 'NC')
            s_scopes.append('Class_Globals')

def p_clases_02(p):
    '''clases_02 : atributos metodos LLAVE_D PUNTO_COMA pop_scope nueva_clase   

       atributos : declaracion_variables 

       metodos   : declaracion_funciones pop_scope
       
       nueva_clase : clases clases_02
                   | vacio'''
    # The 'pop_scope' in metodos is to take out 'Class_Globales'

def p_declaracion_variables(p):
  '''declaracion_variables : variables PUNTO_COMA declaracion_variables
                           | vacio'''

# def p_variables(p):
#     '''variables : VAR ID ID aux1
#                  | VAR tipo_simple ID aux2 aux3
#                  | VAR tipo_simple ID CORCHETE_I CTEINT CORCHETE_D
#                  | VAR tipo_simple ID CORCHETE_I CTEINT COMA CTEINT CORCHETE_D
    
#         aux1 : COMA ID aux1
#              | vacio
        
#         aux2 : CORCHETE_I CTEINT CORCHETE_D
#              | CORCHETE_I CTEINT COMA CTEINT CORCHETE_D
#              | vacio
            
#         aux3 : COMA ID aux2 aux3
#              | vacio'''


def p_variables(p):
    '''variables : VAR ID ID aux1
                 | VAR tipo_simple variables_02
    
        aux1 : COMA ID aux1
             | vacio'''
    
def p_variables_02(p):
    '''variables_02 : ID aux3
                    | ID CORCHETE_I CTEINT CORCHETE_D aux3
                    | ID CORCHETE_I CTEINT COMA CTEINT CORCHETE_D aux3
            
       aux3 : COMA ID aux3
            | COMA ID CORCHETE_I CTEINT CORCHETE_D aux3
            | COMA ID CORCHETE_I CTEINT COMA CTEINT CORCHETE_D aux3
            | vacio '''
    
    # Get the ID's current scope
    current_scope = s_scopes.pop() 
    # var_id = None
    # var_m1 = None
    # variable_dimension = None
    if p[1] == ',' : # First token is a comma
      variable_dimension = None
      var_m1 = None
      # var_id = p[2]
      if len(p) == 4: # ID is a simple variable
        variable_dimension = "simple"

      elif len(p) == 7: # ID is an array
        variable_dimension = "array"

      elif len(p) == 9: # ID is a matrix
        variable_dimension = "matrix"
        var_m1 = p[6]

      print("----------------------p[2]",p[2])
      print("variable_dimension:", variable_dimension)
      print("current_scope",current_scope)

      # Add variable to memory_directory
      variable_declaration(class_directory, function_directory, memory_directory, current_scope, variable_dimension, p[2], var_m1)
     

    elif len(p) != 2: # First token is an ID
      variable_dimension = None
      var_m1 = None
      # var_id = p[1]
      if len(p) == 3: # ID is a simple variable
        variable_dimension = "simple"

      elif len(p) == 6: # ID is an array
        variable_dimension = "array"

      elif len(p) == 8:# ID iis a matix
        variable_dimension = "matrix"
        var_m1 = p[5]

      print("----------------------p[1]",p[1])
      variable_declaration(class_directory, function_directory, memory_directory, current_scope, variable_dimension, p[1], var_m1)
      
    # variable_declaration(class_directory, function_directory, memory_directory, current_scope, variable_dimension, var_id, var_m1)

    # Return current scope to the stack of scopes
    s_scopes.append(current_scope) 
           
    


def p_tipo_simple(p):
    '''tipo_simple : INT 
                   | FLOAT 
                   | CHAR'''
    global current_type
    current_type = p[1]

# def p_tipo_compuesto(p):
#     '''tipo_compuesto : ID 
#                     | DATAFRAME
#                     | FILE'''
#     global current_type
#     current_type = p[1]

def p_declaracion_funciones(p):
    '''declaracion_funciones : funciones funciones2
                           | vacio'''

def p_current_type_void_function(p):
    'current_type_void_function :'
    global current_type
    current_type = 'VOID'

def p_funciones(p):
    '''funciones    : FUNC funciones_tipo ID  

     funciones_tipo : tipo_simple  
                    | VOID current_type_void_function'''
    
    # Add function scope into stack
    if p[1] == "func":
        function_name = p[3]
        current_scope = s_scopes[-1]
        if(current_scope == 'Global'): # Add function in Function Directory
            # print("Scope added in stack: ", p[3])

            # Add function into Function Directory
            if function_directory.add_scope(function_name, current_type) == False:
                print('ERROR: Function',function_name,'already declared in function directory')
                exit()
            else:
                # Insert number of temporals before quadruples from Estatuos
                function_directory.get_scope(function_name).set_number_of_temporals(temporal_variable_count)

                # Insert reference of where to jump to execute the function's quadruples when called
                inital_address = len(l_quadrupules)
                function_directory.get_scope(function_name).set_initial_address(inital_address)

                s_scopes.append(function_name)
                print("FUNCTION added in Function Directory: ", function_name, current_type)

        else: # Add method in class directory
            
            
            s_scopes.pop() # Remove 'Class_Globals'
            class_name = s_scopes[-1] # Class scope
            s_scopes.append(current_scope) # Add 'Class_Globals'

            # Add method in class
            if class_directory.add_method(class_name, function_name, current_type) == False:
                print('ERROR: Method',function_name,' in class', class_name, 'already declared')
                exit()
            else:
                # Insert number of temporals before quadruples from Estatuos
                class_directory.get_class(class_name).get_scope(function_name).set_number_of_temporals(temporal_variable_count)

                # Insert reference of where to jump to execute the function's quadruples when called
                inital_address = len(l_quadrupules)
                class_directory.get_class(class_name).get_scope(function_name).set_initial_address(inital_address)

                s_scopes.append(function_name)
                print("METHOD added in Class Directory: ", class_name, function_name, current_type)

def p_funciones2(p):
    '''funciones2  : PARENTESIS_I declaracion_parametros PARENTESIS_D LLAVE_I declaracion_variables estatutos LLAVE_D func_closure funciones_rep
    funciones_rep  : funciones funciones2
                   | vacio'''

def p_func_closure(p):
    'func_closure :'
    func_name = s_scopes.pop()

    if(s_scopes[-1] == 'Global'):
        # Delete vars table from function
        # function_directory.get_scope(func_name).remove_vars_table()

        # 
        quadruple = ('ENDPROC', None, None, None)
        l_quadrupules.append(quadruple)

        # Set number of temporals in function
        function_scope = function_directory.get_scope(func_name)
        intial_number_of_temporals = function_scope.get_number_of_temporals()
        function_scope.set_number_of_temporals(temporal_variable_count - intial_number_of_temporals)
        
        # Set number of local variables in function
        number_of_local_variables = function_scope.get_number_of_local_variables()
        function_scope.set_number_of_local_variables(number_of_local_variables)
    else:
        class_globals = s_scopes.pop() # Remove 'Class_Globals'
        class_name = s_scopes[-1]

        quadruple = ('ENDPROC', None, None, None)
        l_quadrupules.append(quadruple)

        # Set number of temporals in method
        class_scope = class_directory.get_class(class_name)
        function_scope = class_scope.get_scope(func_name)
        intial_number_of_temporals = function_scope.get_number_of_temporals()
        function_scope.set_number_of_temporals(temporal_variable_count - intial_number_of_temporals)
        
        # Set number of local variables in method
        number_of_local_variables = function_scope.get_number_of_local_variables()
        function_scope.set_number_of_local_variables(number_of_local_variables)

        s_scopes.append(class_globals)

# Remove  scope from stack
def p_pop_scope(p):
  'pop_scope :'
  print("Scope deleted from STACK:", s_scopes.pop())

def p_declaracion_parametros(p):
    '''declaracion_parametros : param param2
                              | vacio'''

def p_param(p):
    '''param : tipo_simple ID '''    
    function_name = s_scopes.pop()
    # Is function parameter
    if(s_scopes[-1] == 'Global'):
      
      # Add parameter to memory
      virtual_address = memory_directory.get_address(current_type, "local", "variable")
      memory_directory.add_item(current_type, "local", "variable")
      
      # Add parameter into variables table
      function_directory.add_parameter(function_name, p[2], current_type, virtual_address)
      print("PARAMETER(SymTable):", function_name, p[2], current_type, virtual_address)

      s_scopes.append(function_name) # Put back function scope in stack

    else: # Add parameter from a method scope from a class into Class Directory
        class_globals = s_scopes.pop() # Remove 'Class_Globals' from stack
        class_name = s_scopes[-1] # Get class scope from stack

        virtual_address = memory_directory.get_class_address(current_type, "local", "variable")
        memory_directory.add_class_item(current_type, "local", "variable")

        class_directory.add_parameter(class_name, function_name, p[2], current_type, virtual_address)
        print("PARAMETER(ClassDir):", class_name, function_name, p[2], current_type, virtual_address)

        s_scopes.append(class_globals)
        s_scopes.append(function_name)

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
       h        : CORCHETE_I exp CORCHETE_D 
                | CORCHETE_I exp COMA exp CORCHETE_D
                | vacio '''
    if(len(p) == 3):
        # s_operands.append(p[1])
        current_scope = s_scopes.pop() # Check current scope

        # ID is inside Main
        if len(s_scopes) == 0:
          
            # Check if ID is a global variable in Main
            # print("######## Variable var_exists", function_directory.var_exists(current_scope, p[1]))
            variable = function_directory.var_exists(current_scope, p[1])   
            
            if variable:
              variable_type = variable.get_data_type()
              variable_address = variable.get_address()    

        # ID is inside a function
        elif len(s_scopes) == 1:
            function_name = current_scope

            # Check if ID is a local variable in function
            # print("######## Variable var_exists", function_directory.var_exists(function_name, p[1]))
            variable = function_directory.var_exists(function_name, p[1])

            if variable:
              variable_type = variable.get_data_type()
              variable_address = variable.get_address()
            
            else: # ID is not local variable in function
              
              # Check if ID is a global variable
              variable = function_directory.var_exists(s_scopes[-1], p[1])

              if variable:
                variable_type = variable.get_data_type()
                variable_address = variable.get_address()

        # ID is inside a method
        elif len(s_scopes) == 3:
            method_name = current_scope
            class_globals = s_scopes.pop() # Remove 'Class_Globals'
            class_name = s_scopes[-1]

            # Check if ID is a local variable in method
            class_object = class_directory.get_class(class_name)
            variable = class_object.var_exists(method_name, p[1])
        
            if variable:
              variable_type = variable.get_data_type()
              variable_address = variable.get_address()

            else: # ID is not a local variable in method

              # Check if ID is an attribute in class
              class_object = class_directory.get_class(class_name)
              variable = class_object.var_exists(class_globals, p[1])
              
              if variable:
                  variable_type = variable.get_data_type()
                  variable_address = variable.get_address()

            s_scopes.append(class_globals) # Put back name of class n scope

        s_scopes.append(current_scope) # Put back current scope in stack

        if variable:
            s_operands.append(variable_address) 
            s_types.append(variable_type) # Put variable type in stack
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
    '''llamada_void : ID PARENTESIS_I reset_argument_counter posible_exp PARENTESIS_D PUNTO_COMA
                    | ID PUNTO ID PARENTESIS_I reset_argument_counter posible_exp PARENTESIS_D PUNTO_COMA'''

    if len(p) == 7: # Void function calls
        global argument_counter
        func_name = p[1]
        if not function_directory.scope_exists(func_name):
            print("ERROR: Function",func_name,"not declared")
            exit()
        # Verify number of arguments in function call
        elif function_directory.get_scope(func_name).get_number_of_parameters() != argument_counter:
            print("ERROR: Incoherence in number of arguments in function call", func_name)
            exit()
                
        else:
            # ('ERA', func_name, scope, None) = 
              # scope '0' = FunctionDirectory
              # scope '1' = ClassDirectory
            quadruple_ERA = ('ERA', func_name, 0, None)
            l_quadrupules.append(quadruple_ERA)

            argument_counter = 0
            # Create PARAMETER quadruple for each argument
            while(len(s_function_call_arguments) > 0):
                # Remove the argument in order
                argument = s_function_call_arguments.popleft()
                argument_type = s_function_call_argument_types.popleft()

                # Verify argument type
                if argument_type != function_directory.get_scope(func_name).params_table[argument_counter]:
                    print("ERROR: Argument type is incorrect in function call", func_name)
                    exit()
                else:
                    quadruple_PARAMETER = ('PARAMETER', argument, None, argument_counter)
                    l_quadrupules.append(quadruple_PARAMETER)
                    argument_counter +=1

            quadruple_GOSUB = ('GOSUB', func_name, None, None)
            l_quadrupules.append(quadruple_GOSUB)

    elif len(p) == 8: # void methods from a class
        class_name = p[1]
        method_name = p[3]
        if not class_directory.scope_exists(class_name):
            print("ERROR: Class",class_name,"not declared")
            exit()
        elif not class_directory.get_class(class_name).get_scope(method_name):
            print("ERROR: Method",method_name,"not declared in class", class_name)
            exit()
        elif class_directory.get_class(class_name).get_scope(method_name).get_number_of_parameters() != argument_counter:
            print("ERROR: Incoherence in number of arguments in method call", method_name)
            exit()
        else:
            # ('ERA', func_name, scope, None) = 
              # scope '0' = FunctionDirectory
              # scope '1' = ClassDirectory
            quadruple_ERA = ('ERA', method_name, 1, None)
            l_quadrupules.append(quadruple_ERA)

            argument_counter = 0

            # Create PARAMETER quadruple for each argument
            while(len(s_function_call_arguments) > 0):
                # Remove the argument in order
                argument = s_function_call_arguments.popleft()
                argument_type = s_function_call_argument_types.popleft()

                # Verify argument type
                if argument_type != class_directory.get_class(class_name).get_scope(method_name).params_table[argument_counter]:
                    print("ERROR: Argument type is incorrect in function call", method_name)
                    exit()

                quadruple_PARAMETER = ('PARAMETER', argument, None, argument_counter)
                l_quadrupules.append(quadruple_PARAMETER)
                argument_counter +=1

            quadruple_GOSUB = ('GOSUB', method_name, None, None)
            l_quadrupules.append(quadruple_GOSUB)

def p_posible_exp(p):
    '''posible_exp : exp append_argument I
                   | vacio

      I            : COMA exp append_argument I 
                   | vacio'''

       
def p_reset_argument_counter(p):
    'reset_argument_counter :'
    global argument_counter
    argument_counter = 0

def p_append_argument(p):
    'append_argument :'
    argument = s_operands.pop()
    argument_type = s_types.pop()

    s_function_call_arguments.append(argument)
    s_function_call_argument_types.append(argument_type)

    global argument_counter
    argument_counter+=1

def p_lectura(p):
    'lectura : READ variable'

def p_retorno(p):
    'retorno : RETURN exp PUNTO_COMA'
    expresion_result = s_operands.pop()
    expresion_type = s_types.pop()

    quadruple_RETURN = ('RETURN', None, None, expresion_result)
    l_quadrupules.append(quadruple_RETURN)
    print(quadruple_RETURN)

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
    # print("exp_type", exp_type)

    var_type = s_types.pop()
    variable = s_operands.pop()

    if exp_type != var_type:
        print("Error: ", exp_type, "not assignable to", var_type)
        exit()
    elif(var_type != 'int'):
        print("Error: ", variable, "is not of type INT")
        exit()
    else:
        quadruple_EQUAL = ('EQUAL', exp_result, None, variable)
        l_quadrupules.append(quadruple_EQUAL)


def p_quad_for_02(p):
    'quad_for_02 :'
    # Save the index to the first quadrupule of the expression
    index_before_exp = len(l_quadrupules)
    s_jumps.append(index_before_exp)

def p_quad_for_03(p):
    'quad_for_03 :'
    expresion_type = s_types.pop()
    expresion_result = s_operands.pop()  
    # print("expresion_type:", expresion_type )

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
    if(len(s_operators) != 0):
        if(s_operators[-1] == '>' or s_operators[-1] == '<' or s_operators[-1] == '<>' ):
            # Get right operand
            right_operand = s_operands.pop()
            right_type = s_types.pop()

            # Get left operand
            left_operand = s_operands.pop() 
            left_type = s_types.pop()

            # Get operator
            operator = s_operators.pop()

            # Validate result data type with semantic cube
            res_type = semantic_cube.result_type(left_type, right_type, operator)

            print("RES_TYPE BEFORE VIRTUAL_ADDRESS:",res_type)

            # Check if result data type is valid
            if not res_type == 'ERROR':
              
              # Expresion is inside main
              if s_scopes[-1] == 'Global':
                temporal_virtual_address = memory_directory.get_address(res_type, "global", "temporal")
                memory_directory.add_item(res_type, "global", "temporal")
                print("TEMPORAL GLOBAL VIRTUAL_ADDRESS:", temporal_virtual_address, res_type, left_operand, right_operand, operator)

              # Expresion is inside a function
              elif len(s_scopes) == 2:
                temporal_virtual_address = memory_directory.get_address(res_type, "local", "temporal")
                memory_directory.add_item(res_type, "local","temporal")
                print("TEMPORAL LOCAL VIRTUAL_ADDRESS:", temporal_virtual_address, res_type, left_operand, right_operand, operator)

              # Expresion is inside a method
              elif len(s_scopes) == 4:
                temporal_virtual_address = memory_directory.get_class_address(res_type, "local", "temporal")
                memory_directory.add_class_item(res_type,"local","temporal")
                print("TEMPORAL CLASS LOCAL VIRTUAL_ADDRESS:", temporal_virtual_address, res_type, left_operand, right_operand, operator)

              quadruple = (operator, left_operand, right_operand, temporal_virtual_address)
              l_quadrupules.append(quadruple) # add quadrupule to list
              print(quadruple) 

              s_operands.append(temporal_virtual_address) # Add the result into the operands stack
              s_types.append(res_type) # Add result's type into the types stack
            
            else: # Invalid result type
              print("Error: Type mismatch")
              exit()


def p_greater_than_append(p):
    'greater_than_append :'
    s_operators.append('>')
    # print("$$$ Addition operator MAYOR_QUE appended in stack $$$")

def p_less_than_append(p):
    'less_than_append :'
    s_operators.append('<')
    # print("$$$ Addition operator MENOR_QUE appended in stack $$$")

def p_different_append(p):
    'different_append :'
    s_operators.append('<>')
    # print("$$$ Different operator NO_IGUAL appended in stack $$$")

def p_exp(p):
    '''exp : termino quadrupule_creation_01 n

       n   : MAS addition_append exp 
           | MENOS substraction_append exp
           | vacio'''               

def p_addition_append(p):
    'addition_append :'
    # Push addition operator into operator stack
    s_operators.append('+')
    # print("$$$ Addition operator MAS appended in stack $$$")

def p_substraction_append(p):
    'substraction_append :'
    # Push substraction operator into operator stack
    s_operators.append('-')
    # print("$$$ Substraction operator MENOS appended in stack $$$")

def p_quadrupule_creation_01(p):
    'quadrupule_creation_01 :'
    if(len(s_operators) != 0): 
        if(s_operators[-1] == '+' or s_operators[-1] == '-'):
            right_operand = s_operands.pop() # Get right operand from stack
            right_type = s_types.pop() # Get right operand's type from stack
            
            left_operand = s_operands.pop() # Get left operand from stack
            left_type = s_types.pop() # Get left operand's type from stack

            operator = s_operators.pop() # Get operand from stack

            res_type = semantic_cube.result_type(left_type, right_type, operator)
            # print("res_type : ", res_type)

            if(not res_type == 'ERROR'):

              if s_scopes[-1] == 'Global': # Global temporal
                temporal_virtual_address = memory_directory.get_address(res_type, "global", "temporal")
                memory_directory.add_item(res_type, "global", "temporal")
                print("TEMPORAL GLOBAL VIRTUAL_ADDRESS:", temporal_virtual_address, res_type, left_operand, right_operand, operator)

              elif len(s_scopes) == 2: # Local temporal in a function
                temporal_virtual_address = memory_directory.get_address(res_type, "local", "temporal")
                memory_directory.add_item(res_type, "local","temporal")
                print("TEMPORAL LOCAL VIRTUAL_ADDRESS:", temporal_virtual_address, res_type, left_operand, right_operand, operator)

              elif len(s_scopes) == 4: # Class local temporal_variable_base_name
                temporal_virtual_address = memory_directory.get_class_address(res_type, "local", "temporal")
                memory_directory.add_class_item(res_type,"local","temporal")
                print("TEMPORAL CLASS LOCAL VIRTUAL_ADDRESS:", temporal_virtual_address, res_type, left_operand, right_operand, operator)

              # # Temporable variable simulation
              # global temporal_variable_count
              # result = temporal_variable_base_name + str(temporal_variable_count)
              # temporal_variable_count += 1

              quadruple = (operator, left_operand, right_operand, temporal_virtual_address) 
              l_quadrupules.append(quadruple) # Add quadrupule to list
              print(quadruple) 

              s_operands.append(temporal_virtual_address) # Add the result into the operands stack
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
    s_operators.append('*')
    # print("$$$ Multiplication POR appended in stack$$$")

def p_divition_append(p):
    'divition_append :'
    s_operators.append('/')
    # print("$$$ Divition operator ENTRE in stack $$$")

def p_quadrupule_creation_02(p): 
    'quadrupule_creation_02 :'
    if(len(s_operators) != 0):
        if(s_operators[-1] == '*' or s_operators[-1] == '/'):
            right_operand = s_operands.pop() # Get right operand from stack
            right_type = s_types.pop() # Get right operand's type from stack

            left_operand = s_operands.pop() # Get left operand from stack
            left_type = s_types.pop() # Get left operand's type from stack

            operator = s_operators.pop() # Get operand from stack

            res_type = semantic_cube.result_type(left_type, right_type, operator)

            if(not res_type == 'ERROR'):

              if s_scopes[-1] == 'Global': # Global temporal
                temporal_virtual_address = memory_directory.get_address(res_type, "global", "temporal")
                memory_directory.add_item(res_type, "global", "temporal")
                print("TEMPORAL GLOBAL VIRTUAL_ADDRESS:", temporal_virtual_address, res_type, left_operand, right_operand, operator)

              elif len(s_scopes) == 2: # Local temporal in a function
                temporal_virtual_address = memory_directory.get_address(res_type, "local", "temporal")
                memory_directory.add_item(res_type, "local","temporal")
                print("TEMPORAL LOCAL VIRTUAL_ADDRESS:", temporal_virtual_address, res_type, left_operand, right_operand, operator)

              elif len(s_scopes) == 4: # Class local temporal_variable_base_name
                temporal_virtual_address = memory_directory.get_class_address(res_type, "local", "temporal")
                memory_directory.add_class_item(res_type,"local","temporal")
                print("TEMPORAL CLASS LOCAL VIRTUAL_ADDRESS:", temporal_virtual_address, res_type, left_operand, right_operand, operator)

              # # Temporable variable simulation
              # global temporal_variable_count
              # result = temporal_variable_base_name + str(temporal_variable_count)
              # temporal_variable_count += 1

              quadruple = (operator, left_operand, right_operand, temporal_virtual_address) # 'result' is supposed to be temporal space
              l_quadrupules.append(quadruple) # add quadrupule to list
              print(quadruple) 

              s_operands.append(temporal_virtual_address) # Add the result into the operands stack
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
              | ID 
              | ID CORCHETE_I exp CORCHETE_D 
              | ID CORCHETE_I exp COMA exp CORCHETE_D 
              | ID PARENTESIS_I reset_argument_counter posible_exp PARENTESIS_D
              | ID PUNTO ID 
              | ID PUNTO ID PARENTESIS_I reset_argument_counter posible_exp PARENTESIS_D
              | PARENTESIS_I parenthesis_left_append expresion PARENTESIS_D parenthesis_left_pop '''

    # factor : ID  or  factor : varcte
    if(len(p) == 2):
        global current_constant
        global current_constant_type
        # factor : ID
        # ID is not a constant
        print("p[1]:",p[1])
        print("current_constant",current_constant)
        print("current_constant_type", current_constant_type)
        if( p[1] != 'CTEINT' and p[1] != 'CTEFLOAT' and p[1] != 'CTECHAR' and current_constant == None):
            # operand_type = function_directory.get_scope(s_scopes[-1]).search(p[1]) # Get variable´s type
            current_scope = s_scopes.pop()

            # ID is inside Main
            if len(s_scopes) == 0:

                # Check if ID is a global variable in Main
                # print("######## Variable var_exists", function_directory.var_exists(current_scope, p[1]))       
                variable = function_directory.var_exists(current_scope, p[1])   
            
                if variable:
                  
                  variable_type = variable.get_data_type()
                  
                  variable_address = variable.get_address() 
                  # print("-------------GLOBAL", p[1], variable_address)   

            # ID is inside a function
            elif len(s_scopes) == 1:
                function_name = current_scope

                # Check if ID is a local variable in function
                # print("######## Variable var_exists", function_directory.var_exists(function_name, p[1]))
                variable = function_directory.var_exists(function_name, p[1])

                if variable:
                  variable_type = variable.get_data_type()
                  variable_address = variable.get_address()
                
                else: # ID is not local variable in function
                  
                  # Check if ID is a global variable
                  variable = function_directory.var_exists(s_scopes[-1], p[1])

                  if variable:
                    variable_type = variable.get_data_type()
                    variable_address = variable.get_address()

            # ID is inside a method
            elif len(s_scopes) == 3:
                method_name = current_scope
                class_globals = s_scopes.pop() # Remove 'Class_Globals'
                class_name = s_scopes[-1]
                
                # Check if ID is a local variable in method
                class_object = class_directory.get_class(class_name)
                variable = class_object.var_exists(method_name, p[1])
            
                if variable:
                  variable_type = variable.get_data_type()
                  variable_address = variable.get_address()

                else: # ID is not a local variable in method

                  # Check if ID is an attribute in class
                  variable = class_object.var_exists(class_globals, p[1])
                  
                  if variable:
                      variable_type = variable.get_data_type()
                      variable_address = variable.get_address()

                s_scopes.append(class_globals) # Put back the name of class in stack scopes


            s_scopes.append(current_scope) # Put back current scope

            if(variable):
                s_operands.append(variable_address)
                # print("$$$ Operand ", variable_address, "added into s_operands $$$")

                s_types.append(variable_type)
                # print("$$$ Operand_type added into stack: ", variable_type)
            else:
                print("Variable", p[1], "is not declared")
                exit()
        else:
          

          # factor : varcte
          print("Implementacion de constantes")

          if current_constant_type == 'int' or current_constant_type == 'float' or current_constant_type == 'char':
            print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            print(type(current_constant))
            virtual_address = memory_directory.get_constant_address(current_constant_type, current_constant)
          
          current_constant = None
          s_operands.append(virtual_address)
          s_types.append(current_constant_type)
    
    # factor : ID PUNTO ID 
    elif len(p) == 4:
        print("Atributo de clase")

    # factor : ID PARENTESIS_I reset_argument_counter posible_exp PARENTESIS_D
    elif(len(p) == 6 and p[1] != '('): # LLamada a funcion non-void
        func_name = p[1]

        if not function_directory.scope_exists(func_name):
            print("ERROR: Function",func_name,"not declared")
            exit()

        # Verify number of arguments in function call
        elif function_directory.get_scope(func_name).get_number_of_parameters() != argument_counter:
            print("ERROR: Incoherence in number of arguments in function call", func_name)
            exit()
                
        else:
            # ('ERA', func_name, scope, None) = 
              # scope '0' = FunctionDirectory
              # scope '1' = ClassDirectory
            quadruple_ERA = ('ERA', func_name, 0, None)
            l_quadrupules.append(quadruple_ERA)

            argument_index = 0
            # Create PARAMETER quadruple for each argument
            while(len(s_function_call_arguments) > 0):
                # Remove the argument in order
                argument = s_function_call_arguments.popleft()
                argument_type = s_function_call_argument_types.popleft()

                # Verify argument type
                if argument_type != function_directory.get_scope(func_name).params_table[argument_index]:
                    print("ERROR: Argument type is incorrect in function call", func_name)
                    exit()
                else:
                    quadruple_PARAMETER = ('PARAMETER', argument, None, argument_index)
                    l_quadrupules.append(quadruple_PARAMETER)
                    argument_index +=1

            quadruple_GOSUB = ('GOSUB', func_name, None, None)
            l_quadrupules.append(quadruple_GOSUB)

        print("Llamada función")

    elif len(p) == 5:
        print("Arreglo")

    elif len(p) == 7:
        print("Matriz")

    # ID PUNTO ID PARENTESIS_I reset_argument_counter posible_exp PARENTESIS_D
    # non-void method call
    elif len(p) == 8:
        

        class_name = p[1]
        method_name = p[3]

        if not class_directory.scope_exists(class_name):
            print("ERROR: Class",class_name,"not declared")
            exit()
        
        elif not class_directory.get_class(class_name).get_scope(method_name):
            print("ERROR: Method",method_name,"not declared")
            exit()

        # Verify number of arguments in function call
        elif class_directory.get_class(class_name).get_scope(method_name).get_number_of_parameters() != argument_counter:
            print("ERROR: Incoherence in number of arguments in method call", method_name)
            exit()            
                
        else:
            # ('ERA', func_name, scope, None) = 
              # scope '0' = FunctionDirectory
              # scope '1' = ClassDirectory
            quadruple_ERA = ('ERA', method_name, 1, None)
            l_quadrupules.append(quadruple_ERA)

            argument_index = 0
            # Create PARAMETER quadruple for each argument
            while(len(s_function_call_arguments) > 0):
                # Remove the argument in order
                argument = s_function_call_arguments.popleft()
                argument_type = s_function_call_argument_types.popleft()

                # Verify argument type
                if argument_type != class_directory.get_class(class_name).get_scope(method_name).params_table[argument_index]:
                    print("ERROR: Argument type is incorrect in function call", method_name)
                    exit()
                else:
                    quadruple_PARAMETER = ('PARAMETER', argument, None, argument_index)
                    l_quadrupules.append(quadruple_PARAMETER)
                    argument_index +=1

            quadruple_GOSUB = ('GOSUB', method_name, None, None)
            l_quadrupules.append(quadruple_GOSUB)
         

def p_multiple_exp(p):
    '''multiple_exp : COMA exp multiple_exp
                    | vacio '''

def p_parenthesis_left_append(p):
    'parenthesis_left_append :'
    s_operators.append('(')

def p_parenthesis_left_pop(p):
    'parenthesis_left_pop :'
    s_operators.pop()

def p_varcte(p):
  '''varcte : CTEINT constant_int_assginment 
            | CTEFLOAT constant_float_assginment
            | CTECHAR constant_char_assginment'''

  global current_constant
  current_constant = p[1]

def p_constant_int_assginment(p):
  'constant_int_assginment :'
  global current_constant_type
  current_constant_type = 'int'

def p_constant_float_assginment(p):
  'constant_float_assginment :'
  global current_constant_type
  current_constant_type = 'float'

def p_constant_char_assginment(p):
  'constant_char_assginment :'
  global current_constant_type
  current_constant_type = 'char'


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
