import os
from re import L
import types
import ply.lex as lex
import ply.yacc as yacc
import Classes.MemoryHandler as mh
import Helpers.SemanticCube as sc
from lexer import *
from collections import deque
from Classes.FunctionDirectory import FunctionDirectory
from Classes.ClassDirectory import ClassDirectory
from Classes.VirtualMachine import VirtualMachine
from Helpers.Utilities import error, types

# --------------
# Build lexer

lexer = lex.lex()

# Read text file
f = open(os.path.join(os.path.dirname(__file__), './TestCases/', 'Arreglo.txt'), 'r')
data = f.read()

# Test lex with text file
lexer.input(data)

# Tokenize
for tok in lexer:
    print(tok)

#--------------

# Declare empty instances
function_directory = None
class_directory = None
memory_handler = None

# Declared stacks
s_scopes = deque()                        # To keep track of scopes
s_operators = deque()                     # To keep track of operators in expressions
s_operands = deque()                      # To keep track of operands in expressions
s_assignment = deque()
s_types = deque()                         # To keep track of the operands' types
s_print_items = deque()                   # To keep track of all the strings and expressions used in a PRINT
s_jumps = deque()                         # To keep track of all the conditional jumps for GOTO
s_function_call_arguments = deque()       # To verify the arguments in a function call with parameters table
s_function_call_argument_types = deque()  # Arguments' type in a function call
s_dimensions = deque()                    # To keep track of the context when evaluating nested arrays or matrices
s_variables = deque()                     # To keep track of IDs in declaration

# Declared lists
l_quadruples = [] # To save the code optimization in form of quadruples. (op, op_izq, op_der, res)

# current type for declared variable 
current_type = None

# Catches the constant
current_constant = None
current_constant_type = None

# Catches the second dimension
second_dimension = None

# Simulates the implementation of temporal variables 
temporal_variable_base_name = "temp"
temporal_variable_count = 0

# Counter to verify the arguments in a function call with the parameters table
argument_counter = 0

# --------------------------- HELPER FUNCTIONS ----------------------------


def variable_allocation(variable_dimensions, scope, item_type):
  """Allocates the virtual memory for any type of variable

    Parameters
    ----------
    variable_dimensions : str
        Pending
    scope : bool, optional
        Pending...
    item_type : 
        Pending...
    Returns
    -------
    int
        the base virtual address for the variable
  """

  if variable_dimensions[0] == 0: # Normal variable
      virtual_address = memory_handler.new_variable(current_type, scope, item_type)
    
  elif variable_dimensions[0] == 1: # Variable is an array
    # Get the size of array 
    array_size = variable_dimensions[1]
    virtual_address = memory_handler.new_variable(current_type, scope, item_type, array_size)
  else: # Variable is a matrix
    # Get the size of matrix
    matrix_size = variable_dimensions[1] * variable_dimensions[2]
    virtual_address = memory_handler.new_variable(current_type, scope, item_type, matrix_size)

  return virtual_address 

# Function to add variables to memory_handler depending on their scope
def variable_declaration(variable):

  current_scope, variable_dimensions, variable_id = variable

  # Check variable scope
  if(current_scope == 'global' ): # Global variables in FunctionDirectory  

    virtual_address = variable_allocation(variable_dimensions, "global", "variable")

    # There's an error adding global variable into Function Directory
    if not function_directory.add_item(current_scope, variable_id, current_type, virtual_address, variable_dimensions):
       error("Failed at declaring global variable %s" % variable_id)
    
    # print("+++++Global variable added into functionDirectory ->", variable_id, current_type, virtual_address, variable_dimensions)
      
  elif(current_scope == 'class_globals'): # Global variables (attributes) in Class 
    class_name = s_scopes[-1]

    virtual_address = variable_allocation(variable_dimensions, "global", "variable")

    # There's an error adding global variable into Function Directory
    if not class_directory.add_attribute(class_name, current_scope, variable_id, current_type, virtual_address, variable_dimensions):
      error("Failed at declaring attribute %s in class %s" % (variable_id, class_name))
    
    # print("+Global attribute added into ClassDirectory ->", class_name, current_scope, variable_id, current_type)
  
  elif(s_scopes[-1] == 'class_globals'): # Local variables in Methods in Class 
    method_name = current_scope
    s_scopes.pop() # Pop out 'class_globals' scope
    class_name = s_scopes[-1]

    virtual_address = variable_allocation(variable_dimensions, "local", "variable")

    # There's an error adding local variable into Function Directory
    if not class_directory.add_variable(class_name, method_name, variable_id, current_type, virtual_address, variable_dimensions):
      error("Failed at declaring local variable %s in method %s on class %s" % (variable_id, method_name, class_name))

    # Update the number of local variables used in method 
    class_directory.get_class(class_name).get_scope(method_name).add_to_count(current_type, "variable")

    # print("+Local variable in a Method added into ClassDirectory ->", class_name, method_name, variable_id, current_type)

    # Put 'class_globals' into stack
    s_scopes.append('class_globals')

  elif(s_scopes[-1] == 'global'): # Local variables in functions in functionDirectory
      function_name = current_scope

      virtual_address = variable_allocation(variable_dimensions, "local", "variable")

      # There's an error adding global variable into Function Directory
      if not function_directory.add_item(function_name, variable_id, current_type, virtual_address, variable_dimensions):
        error("Failed at declaring local variable %s in %s" %(variable_id, function_name))

      # Update the number of local variables used in method 
      variable_scope = function_directory.get_scope(function_name)
      variable_scope.add_to_count(current_type, "variable")

      # print("++Local variable in a Function added into functionDirectory ->", function_name, variable_id, current_type ,virtual_address)

# Function to generate quadruples from all expressions
def generate_expression_quadruple():
  
  # Get right operand
  right_operand = s_operands.pop()
  right_type = s_types.pop()

  # Get left operand
  left_operand = s_operands.pop() 
  left_type = s_types.pop()

  # Get operator
  operator = s_operators.pop()

  # Validate result data type with semantic cube
  res_type = sc.result_type(left_type, right_type, operator)

  global current_type
  current_type = res_type

  # Check if result data type is invalid
  if res_type == -1:
      error("Type mismatch")
  
  else: # Valid result type
      # expression is inside main
      if s_scopes[-1] == 'global':
        variable_dimensions = (0,0,0) # Normal variable
        temporal_virtual_address = variable_allocation(variable_dimensions, "global", "temporal")
        
        # print("TEMPORAL GLOBAL VIRTUAL_ADDRESS:", temporal_virtual_address, res_type, left_operand, right_operand, operator)

      # expression is inside a function
      elif len(s_scopes) == 2:
        function_name = s_scopes[-1]

        variable_dimensions = (0,0,0) # Normal variable
        temporal_virtual_address = variable_allocation(variable_dimensions, "local", "temporal")

        # print("TEMPORAL LOCAL VIRTUAL_ADDRESS:", temporal_virtual_address, res_type, left_operand, right_operand, operator)

        function_directory.get_scope(function_name).add_to_count(current_type, "temporal")

      # expression is inside a method
      elif len(s_scopes) == 4:
        variable_dimensions = (0,0,0) # Normal variable
        temporal_virtual_address = variable_allocation(variable_dimensions, "local", "temporal")
        # temporal_virtual_address = memory_handler.new_variable(current_type, "local", "temporal")

        # print("TEMPORAL CLASS LOCAL VIRTUAL_ADDRESS:", temporal_virtual_address, res_type, left_operand, right_operand, operator)

        method_name = s_scopes.pop()
        class_globals = s_scopes.pop()
        class_name = s_scopes[-1]
        
        # Update the number of local temporals of current_type used in method 
        class_directory.get_class(class_name).get_scope(method_name).add_to_count(current_type, "temporal")

        s_scopes.append(class_globals)
        s_scopes.append(method_name)

      quadruple = (operator, left_operand, right_operand, temporal_virtual_address)
      l_quadruples.append(quadruple) # add quadruple to list
      print(quadruple) 

      s_operands.append(temporal_virtual_address) # Add the result into the operands stack
      s_types.append(res_type) # Add result's type into the types stack

# Function to validate that a specific-dimension variable exists in any of the three possible scopes: global, function, method
def variable_validation(variable_id, dimension_type):
  current_scope = s_scopes.pop()
  variable = None
  # ID is inside Main
  if len(s_scopes) == 0:
    # Check if ID is a global variable in Main
    variable = function_directory.var_exists(current_scope, variable_id)   

  # ID is inside a function
  elif len(s_scopes) == 1:
      function_name = current_scope

      # Check if ID is a local variable in function
      variable = function_directory.var_exists(function_name, variable_id)

      if not variable: # Not in local
        # Check if ID is a global variable
        variable = function_directory.var_exists(s_scopes[-1], variable_id)

  # ID is inside a method
  elif len(s_scopes) == 3:
      method_name = current_scope
      class_globals = s_scopes.pop() # Remove 'class_globals'
      class_name = s_scopes[-1]
      
      # Check if ID is a local variable in method
      class_object = class_directory.get_class(class_name)
      variable = class_object.var_exists(method_name, variable_id)
  
      if not variable: # Not in local
        # Check if ID is an attribute in class
        variable = class_object.var_exists(class_globals, variable_id)

      s_scopes.append(class_globals) # Put back the name of class in stack scopes

  s_scopes.append(current_scope) # Put back current scope
  
  if not variable or dimension_type != variable.get_dimensions()[0]:
    return False
  else:
    return variable

def store_constant(data_type, constant_value):
  """Returns address if constant literal exists"""
  virtual_address = memory_handler.constant_exists(data_type, constant_value)

  if not virtual_address: # Not saved constant, add it to constant directory
    virtual_address = memory_handler.new_constant(data_type, constant_value)
  
  return virtual_address

def guadalupan_patch(variable):
  """Sends the result of a non-void function or method to a temporal"""
  variable_type = variable.get_data_type()
  variable_address = variable.get_address()
  
  # Global or local temporal
  scope = 'local' if len(s_scopes) in [2,4] else 'global'
    
  # Obtain a new temporal variable to store the return of the function
  temporal_virtual_address = memory_handler.new_variable(variable_type, scope, 'temporal')

  # Assign the return of the function into a temporal variable
  quadruple_parche = ('=', variable_address, None, temporal_virtual_address)
  l_quadruples.append(quadruple_parche)

  # Put temporal variable in stack
  s_operands.append(temporal_virtual_address)
  s_types.append(variable_type)
  
  
#  ------------------------------------------------------------------------

# --------------------------- GRAMMAR -----------------------------
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
  global class_directory
  global memory_handler
  
  function_directory = FunctionDirectory()
  class_directory = ClassDirectory()
  memory_handler = mh.MemoryHandler()

# Add row to FunctionDirectory for global
def p_program_name(p):
  'program_name :'
  s_scopes.append('global')
  function_directory.add_scope('global', 'NP')

def p_quad_GOTO_Main(p):
  'quad_GOTO_Main :'
  pending_GOTO_Main = ('GOTO', None, None, None) #  
  l_quadruples.append(pending_GOTO_Main)

  pending_GOTO_Main_index = len(l_quadruples)-1
  s_jumps.append(pending_GOTO_Main_index)

def p_main(p):
  'main : MAIN PARENTESIS_I PARENTESIS_D fill_pending_GOTO_Main bloque append_END_quad'
  #   
  s_scopes.pop()
  print("Scope deleted from STACK: Global")

  print("---------------- quadrupleS LIST -------------------")
  for index in range(len(l_quadruples)):
      print(index, "\t", l_quadruples[index])
  print("")
  
  virtual_machine = VirtualMachine(l_quadruples, function_directory, class_directory, memory_handler.get_constants_directory())
  virtual_machine.run()
    

def p_fill_pending_GOTO_Main(p):
  'fill_pending_GOTO_Main :'
  pending_GOTO_Main_index = s_jumps.pop()
  pending_GOTO_Main = l_quadruples[pending_GOTO_Main_index]

  first_quadruple_of_Main = len(l_quadruples)
  new_GOTO_Main = (pending_GOTO_Main[0], None, None, first_quadruple_of_Main)

  l_quadruples[pending_GOTO_Main_index] = new_GOTO_Main

def p_append_END_quad(p):
  'append_END_quad :'
  quadruple_END = ('END', None, None, None)
  l_quadruples.append(quadruple_END)
  print(quadruple_END)

def p_bloque(p):
  '''bloque : LLAVE_I estatutos LLAVE_D

  estatutos : estatuto estatutos
            | vacio'''

def p_declaracion_clases(p):
  '''declaracion_clases : clases clases_02 
                        | vacio '''

def p_clases(p):
  '''clases    : CLASS ID herencia LLAVE_I 
                  
      herencia    : MENOR_QUE INHERITS MAYOR_QUE 
                  | vacio'''
  if(p[1] == 'class'):
    if not class_directory.add_class(p[2]):
      error("Class %s already exists" %  p[2])
        
    else:
      s_scopes.append(p[2])

      # Create attribute Table (similar to Global variables in Function Directory)
      class_directory.add_attributes_Table(p[2], 'class_globals', 'NC')
      s_scopes.append('class_globals')

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


def p_variables(p):
    '''variables : VAR ID ID aux1
                 | VAR tipo_simple variables_02
    
        aux1 : COMA ID aux1
             | vacio'''
    
def p_variables_02(p):
    '''variables_02 : ID aux3
                    | ID CORCHETE_I CTEINT CORCHETE_D aux3
                    | ID CORCHETE_I CTEINT COMA CTEINT CORCHETE_D aux3
            
              aux3  : COMA ID aux3
                    | COMA ID CORCHETE_I CTEINT CORCHETE_D aux3
                    | COMA ID CORCHETE_I CTEINT COMA CTEINT CORCHETE_D aux3
                    | vacio '''
    
    current_scope = s_scopes.pop()

    if p[1] == ',' : # Not first declared variable
      variable_dimensions = None
  
      # ID is a simple variable
      if len(p) == 4:
        variable_dimensions = (0, 0, 0)

      # ID is an array
      elif len(p) == 7: 
        variable_dimensions = (1, p[4], 0)

      # ID is a matrix
      elif len(p) == 9: 
        variable_dimensions = (2, p[4], p[6])
        # Add ctein into constant directotry

      # Add variable to memory_handler
      variable = (current_scope, variable_dimensions, p[2])
      s_variables.append(variable)

    elif len(p) != 2: # First declared variable 
      variable_dimensions = None

      if len(p) == 3: # ID is a simple variable
        variable_dimensions = (0, 0, 0)

      elif len(p) == 6: # ID is an array
        variable_dimensions = (1, p[3], 0)
        # Add int dimension in constant directotry

      elif len(p) == 8:# ID iis a matix
        variable_dimensions = (2, p[3], p[5])
        # Add int dimensions in constant directotry

      # print("----------------------p[1]",p[1])

      variable = (current_scope, variable_dimensions, p[1])
      s_variables.append(variable)

      # Store 0 as a constant
      store_constant(0, 0)
      
      while len(s_variables) > 0:
        variable = s_variables.pop()
        dimensions = variable[1]
        
        # Store limits as constants for array and matrix
        if dimensions[0] == 1: # is an array
          store_constant(0, dimensions[1])

        elif dimensions[0] == 2: # is a matrix
          store_constant(0, dimensions[1])  
          store_constant(0, dimensions[2])        

        print(variable)
        variable_declaration(variable)

    # Return current scope to the stack of scopes
    s_scopes.append(current_scope) 

def p_tipo_simple(p):
  '''tipo_simple : INT
                 | FLOAT 
                 | CHAR'''
  global current_type
  current_type = p[1]
  if current_type == 'int':
    current_type = 0
  elif current_type == 'float':
    current_type = 1
  elif current_type == 'char':
    current_type = 2


def p_declaracion_funciones(p):
  '''declaracion_funciones : funciones funciones2
                           | vacio'''

def p_current_type_void_function(p):
  'current_type_void_function :'
  global current_type
  current_type = 'VOID'

def p_funciones(p):
  '''funciones     : FUNC funciones_tipo ID  

    funciones_tipo : tipo_simple  
                   | VOID current_type_void_function'''
  
  # Add function scope into stack
  if p[1] == "func":
      function_name = p[3]
      current_scope = s_scopes[-1]
      if(current_scope == 'global'): # Add function in Function Directory
          # Function already exists
          if not function_directory.add_scope(function_name, current_type):
            error("Function %s already declared in function directory" % function_name)

          else:
            # Create global variable for function return
            if current_type != 'VOID':
              var_function_name = (current_scope, (0,0,0), function_name)
              variable_declaration(var_function_name)

            # Insert reference of where to jump to execute the function's quadruples when called
            inital_address = len(l_quadruples)
            function_directory.get_scope(function_name).set_initial_address(inital_address)

            s_scopes.append(function_name)
            # print("FUNCTION added in Function Directory: ", function_name, current_type)

      else: # Add method in class directory

        # Create global variable (attribute) for method return
        if current_type != 'VOID':
          var_function_name = (current_scope, (0,0,0), function_name)
          variable_declaration(var_function_name)

        s_scopes.pop() # Remove 'class_globals'
        class_name = s_scopes[-1] # Class scope
        s_scopes.append(current_scope) # Add 'class_globals'

        # Add method in class
        if not class_directory.add_method(class_name, function_name, current_type):
          error("Method %s in class %s already declared" % (function_name, class_name))

        else:
          # Insert reference of where to jump to execute the function's quadruples when called
          inital_address = len(l_quadruples)
          class_directory.get_class(class_name).get_scope(function_name).set_initial_address(inital_address)

          s_scopes.append(function_name)
          # print("METHOD added in Class Directory: ", class_name, function_name, current_type)

def p_funciones2(p):
  '''funciones2  : PARENTESIS_I declaracion_parametros PARENTESIS_D LLAVE_I declaracion_variables estatutos LLAVE_D func_closure funciones_rep
  funciones_rep  : funciones funciones2
                  | vacio'''

def p_func_closure(p):
  'func_closure :'
  func_name = s_scopes.pop()

  if(s_scopes[-1] == 'global'):
    # Delete vars table from function
    function_directory.get_scope(func_name).remove_vars_table()

    # Resets local variables and local temporal counters to the base address
    memory_handler.reset_locals_counters()

    quadruple = ('ENDPROC', None, None, None)
    l_quadruples.append(quadruple)

      
  else:
    class_globals = s_scopes.pop() # Remove 'class_globals'
    class_name = s_scopes[-1]

    # Delete vars table from method
    class_scope = class_directory.get_class(class_name)
    class_scope.get_scope(func_name).remove_vars_table()

    # Resets local variables and local temporal counters to the base address
    memory_handler.reset_locals_counters()

    quadruple = ('ENDPROC', None, None, None)
    l_quadruples.append(quadruple)

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
  
  if(s_scopes[-1] == 'global'): # Is function parameter
    # Add parameter to memory
    virtual_address = memory_handler.next_address(current_type, "local", "variable")
    memory_handler.add_to_counter(current_type, "local", "variable")
    
    # Add parameter into variables table
    parameter_dimensions = (0, None, None)
    function_directory.add_parameter(function_name, p[2], current_type, virtual_address, parameter_dimensions)
    # print("PARAMETER(SymTable):", function_name, p[2], current_type, virtual_address)

    s_scopes.append(function_name) # Put back function scope in stack

  else: # Add parameter from a method scope from a class into Class Directory
    class_globals = s_scopes.pop() # Remove 'class_globals' from stack
    class_name = s_scopes[-1] # Get class scope from stack

    virtual_address = memory_handler.next_address(current_type, "local", "variable")
    memory_handler.add_to_counter(current_type, "local", "variable") # += 1

    parameter_dimensions = (0, None, None)
    class_directory.add_parameter(class_name, function_name, p[2], current_type, virtual_address, parameter_dimensions)
    # print("PARAMETER(ClassDir):", class_name, function_name, p[2], current_type, virtual_address)

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
  '''variable : aux_ID variable_02'''

def p_variable_02(p):
  '''variable_02 : CORCHETE_I parenthesis_left_append exp array_helper
                 | vacio '''
  # It is a single ID 
  if len(p) == 2:
    if s_dimensions[-1][0] == 'id':
      var_id = s_dimensions.pop()[1]

    # print("s_dimensions.pop(single_ID):", var_id)
    variable = variable_validation(var_id, 0)

    if not variable:
      error("Variable %s is not declared" % var_id)
        
    s_assignment.append((variable.get_address(), variable.get_data_type()))
    # s_operands.append(variable.get_address())
    # s_types.append(variable.get_data_type())

  # Can be array or matrix
  elif len(p) == 5:
    # Array/Matrix first dimension
    dimension_1 = s_operands.pop()
    dimension_1_type = s_types.pop()

    # Validate that first dimension type is int
    if not dimension_1_type == 0:
      error("Indexing with non int type on array")
      
    # Get tuple from stack of dimensions
    elem1, elem2 = s_dimensions.pop()
    # print("s_dimensions.pop(Array or Matrix):", elem1, elem2)

    if elem1 == 'id': # we are having an array

      # Validate if variable exists
      variable = variable_validation(elem2, 1)

      if not variable:
        error("Array %s not declared" % elem2)

      array_name = elem2

      # Get array information from varsTable
      upper_limit = variable.get_dimensions()[1]
      base_address = variable.get_address()
      array_type = variable.get_data_type()
      upper_limit_address = memory_handler.constant_exists(0, upper_limit)

      # Generate quadruple (VER dim1)
      quadruple_VER = ('VER', dimension_1, array_name, upper_limit_address)
      l_quadruples.append(quadruple_VER)
      
      # Generate quadruple (S1 + BaseAddress)
      scope = 'global' if s_scopes[-1] == 'global' else 'local'
      array_virtual_address = memory_handler.new_variable(5, scope, 'temporal')
      quadruple_PLUS_BaseAddress = ('+', dimension_1, (base_address,), array_virtual_address)
      l_quadruples.append(quadruple_PLUS_BaseAddress)

      # Push to stacks
      s_assignment.append((array_virtual_address, array_type))
      # s_operands.append(array_virtual_address)
      # s_types.append(array_type)

    else: # we are having a matrix
      dimension_2 = elem1
      dimension_2_type = elem2
      message, matrix_id = s_dimensions.pop()
      # print("s_dimensions.pop(Matrix):", message, matrix_id)

      # Validate that second dimension type is int
      if not dimension_2_type == 0:
        error("Indexing with non int type on matrix")

      # Validate if variable exists
      variable = variable_validation(matrix_id, 2)

      if not variable:
        error("Matrix %s not declared" % matrix_id)

      # Get matrix information from varsTable
      matrix_dimension = variable.get_dimensions()
      first_upper_limit = matrix_dimension[1]
      second_upper_limit = matrix_dimension[2]
      base_address = variable.get_address()
      matrix_type = variable.get_data_type()

      # Get dimensions' limits as address
      first_upper_limit_address = memory_handler.constant_exists(0, first_upper_limit)
      second_upper_limit_address = memory_handler.constant_exists(0, second_upper_limit)

      # Generate quadruple (VER dim1)
      quadruple_VER = ('VER', dimension_1, matrix_id, first_upper_limit_address)
      l_quadruples.append(quadruple_VER)

      # Gnerate quadruple (s1 * m1)
      scope = 'global' if s_scopes[-1] == 'global' else 'local'
      m1_virtual_address = memory_handler.new_variable(dimension_1_type, scope, "temporal")
      quadruple_s1_times_m1 = ('*', dimension_1, second_upper_limit_address, m1_virtual_address) # s1 * m1
      l_quadruples.append(quadruple_s1_times_m1)
      print(quadruple_s1_times_m1)

      # Generate quadruple (VER dim2) 
      quadruple_VER = ('VER', dimension_2, matrix_id, second_upper_limit_address)
      l_quadruples.append(quadruple_VER)

      # Generate quadruple (S1 * m1 + S2)
      s2_virtual_address = memory_handler.new_variable(dimension_2_type, scope, 'temporal')
      quadruple_sum_s2 = ('+',m1_virtual_address, dimension_2, s2_virtual_address )
      l_quadruples.append(quadruple_sum_s2)
      
      # Generate quadruple (S1 * m1 + S2 + BaseAddress)
      matrix_virtual_address = memory_handler.new_variable(5, scope, 'temporal')
      quadruple_PLUS_BaseAddress = ('+', s2_virtual_address, (base_address,), matrix_virtual_address)
      l_quadruples.append(quadruple_PLUS_BaseAddress)

      # Push to stacks
      s_assignment.append((matrix_virtual_address, matrix_type))
      # s_operands.append(matrix_virtual_address)
      # s_types.append(matrix_type)

def p_asignacion(p):
  'asignacion : variable ASIGNA exp PUNTO_COMA'
  
  expression_result = s_operands.pop() # Result of the expression 
  expression_type = s_types.pop() # Result's type

  # variable_operand = s_operands.pop()
  # variable_type = s_types.pop()
  variable_operand, variable_type = s_assignment.pop()

  if(variable_type == expression_type):
    quadruple = ('=', expression_result, None, variable_operand) 
    l_quadruples.append(quadruple) # add quadruple to list
    # print(quadruple) 
  else:
    error("Type mismatch: %s not assignable to %s" % (types[expression_type], types[variable_type]))

def p_llamada_void(p):
  '''llamada_void : ID PARENTESIS_I reset_argument_counter posible_exp PARENTESIS_D PUNTO_COMA
                  | ID PUNTO ID PARENTESIS_I reset_argument_counter posible_exp PARENTESIS_D PUNTO_COMA'''

  if len(p) == 7: # Void function calls
    global argument_counter
    func_name = p[1]
    if not function_directory.scope_exists(func_name):
      error("Function %s not declared" % func_name)

    # Verify number of arguments in function call
    elif function_directory.get_scope(func_name).get_number_of_parameters() != argument_counter:
      error("Incoherence in number of arguments in function call %s" % func_name)
            
    else:
      quadruple_ERA = ('ERA', func_name, None, None)
      l_quadruples.append(quadruple_ERA)

      argument_counter = 0
      # Create PARAMETER quadruple for each argument
      while(len(s_function_call_arguments) > 0):
        # Remove the argument in order
        argument = s_function_call_arguments.popleft()
        argument_type = s_function_call_argument_types.popleft()

        function_scope = function_directory.get_scope(func_name)
        
        # Verify argument type
        if argument_type != function_scope.get_params_table()[argument_counter]:
          error("Argument type is incorrect in function call %s" % func_name)
          
        else:
          # local_variable_dimensions = (0,0,0)
          # local_variable_address = variable_allocation(local_variable_dimensions, 'local', 'variable')
          
          quadruple_PARAMETER = ('PARAMETER', argument, argument_type, argument_counter)
          l_quadruples.append(quadruple_PARAMETER)
          argument_counter +=1

      quadruple_GOSUB = ('GOSUB', func_name, None, None)
      l_quadruples.append(quadruple_GOSUB)
        

  elif len(p) == 8: # void methods from a class
    class_name = p[1]
    method_name = p[3]
    if not class_directory.scope_exists(class_name):
      print("Class %s not declared" % class_name)

    elif not class_directory.get_class(class_name).get_scope(method_name):
      print("Method %s not declared in class %s" % (method_name,class_name))

    elif class_directory.get_class(class_name).get_scope(method_name).get_number_of_parameters() != argument_counter:
      error("Incoherence in number of arguments in method call %s" % method_name)

    else:
      quadruple_ERA = ('ERA', method_name, None, None)
      l_quadruples.append(quadruple_ERA)

      argument_counter = 0

      # Create PARAMETER quadruple for each argument
      while(len(s_function_call_arguments) > 0):
        # Remove the argument in order
        argument = s_function_call_arguments.popleft()
        argument_type = s_function_call_argument_types.popleft()

        # Verify argument type
        if argument_type != class_directory.get_class(class_name).get_scope(method_name).params_table[argument_counter]:
          error("Argument type is incorrect in function call %s" % method_name)

        quadruple_PARAMETER = ('PARAMETER', argument, argument_type, argument_counter)
        l_quadruples.append(quadruple_PARAMETER)
        argument_counter +=1

      quadruple_GOSUB = ('GOSUB', method_name, class_name, None)
      l_quadruples.append(quadruple_GOSUB)


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
  'lectura : READ variable PUNTO_COMA'
  variable_address, variable_type = s_assignment.pop()
  quadruple_READ = ('READ', None, None, variable_address)
  l_quadruples.append(quadruple_READ)


def p_retorno(p):
  'retorno : RETURN exp PUNTO_COMA'
  expression_result = s_operands.pop()
  expression_type = s_types.pop()

  if len(s_scopes) not in [2, 4]:
    error("Return statement used outside a function or method scope")
    
  func_name = s_scopes.pop()
  func_variable = None

  if s_scopes[-1] == 'global': # Return of a function
    if function_directory.get_scope(func_name).get_data_type() == 'VOID':
      error("Return statement used on void function %s" % func_name)

    func = function_directory.get_scope('global')
    func_variable = func.search(func_name)
    func_type = func_variable.get_data_type()

    # Check expression type with return type
    if func_type != expression_type:
      error("Invalid return type in function %s, func_type: %s, exp_type: %s" % (func_name, func_type, expression_type))
  else: # Return of a method
    class_globals = s_scopes.pop()
    class_name = s_scopes[-1]

    class_dir = class_directory.get_class(class_name)

    if class_dir.get_scope(func_name).get_data_type() == 'VOID':
      error("Return statement used on void method %s of class %s" % (func_name, class_name))

    class_global_scope = class_dir.get_scope('class_globals')
    func_variable = class_global_scope.search(func_name)
    method_type =  func_variable.get_data_type()

    # Check expression type with return type
    if method_type != expression_type:
      error("Invalid return type in method %s" % func_name)
    
    s_scopes.append(class_globals)
  
  s_scopes.append(func_name)

  func_variable_address = func_variable.get_address()
  
  quadruple_RETURN = ('RETURN', expression_result, None, func_variable_address)
  l_quadruples.append(quadruple_RETURN)

  quadruple_ENDPROC = ('ENDPROC', None, None, None)
  l_quadruples.append(quadruple_ENDPROC)
    
  print(quadruple_RETURN)

def p_escritura(p):
  '''escritura : PRINT PARENTESIS_I escritura2 PARENTESIS_D quad_print PUNTO_COMA'''

def p_escritura2(p):
  '''escritura2 : CTESTRING k
                | hiper_expression k append_expression_print

              k : COMA escritura2
                | vacio '''
  
  if len(p) == 3 and p[1] != ',': 
    # Save ctestring to constants directory 
    virtual_address = store_constant(4, p[1])

    # print("ESCRITURA:", p[1], "address:", virtual_address)
    s_print_items.append(virtual_address)

def p_quad_print(p):
  'quad_print :'

  if len(s_print_items) > 0:
    item_address = s_print_items.pop()
    quadruple_PRINT = ('PRINT', None, None, item_address)
    l_quadruples.append(quadruple_PRINT)
    print(quadruple_PRINT)

  while(len(s_print_items) > 0):
    item_address = s_print_items.pop()
    quadruple_PRINT = ('PRINT2', None, None, item_address)
    l_quadruples.append(quadruple_PRINT)
    print(quadruple_PRINT)

def p_append_expression_print(p):
  'append_expression_print : '
  print(s_operands)
  res_expression_address = s_operands.pop() # Result of the expression
  s_types.pop() # Take out the expression's result type

  s_print_items.append(res_expression_address)
  # print("PRINT expression APPEND:", res_expression)
                
def p_condicion(p):
  '''condicion : IF PARENTESIS_I hiper_expression PARENTESIS_D quad_IF_01 bloque l quad_IF_02

     l         : ELSE quad_IF_03 bloque
               | vacio'''

# Generate quadruples of GOTOF 
def p_quad_IF_01(p):
  'quad_IF_01 : '
  res_type = s_types.pop() # Obtain expression's type

  if(not res_type == -1):
    res_expression = s_operands.pop() # Obtain result of the expression

    # Generate "incomplete" qudrupule
    false_quadruple = ('GOTOF', res_expression, None, None)
    l_quadruples.append(false_quadruple )

    index_GOTOF = len(l_quadruples)-1 # Obtain the current/last index of the quadruple??s list
    s_jumps.append(index_GOTOF) # Put the index of the incomplete qudrupule on stack
  else:
    error("Type mismatch on 'if' expression")

def p_quad_IF_02(p):
  'quad_IF_02 :'
  pending_GOTO_index= s_jumps.pop() # Index of an incompleted quadruple
  old_GOTO_quadruple = l_quadruples[pending_GOTO_index] # Obtain incompleted GOTO quadruple
  # print("OLD quadruple", old_GOTO_quadruple)

  next_index = len(l_quadruples) # index to skip over the else statement

  # Replace GOTO quadruple with the one that knows where to jump
  new_GOTO_quadruple = (old_GOTO_quadruple[0], old_GOTO_quadruple[1], None, next_index) # Complete quadruple: (GOTOF, res_expression, None, index)
  l_quadruples[pending_GOTO_index] = new_GOTO_quadruple 

def p_quad_IF_03(p):
  'quad_IF_03 :'
  false_quadruple = s_jumps.pop()

  quadruple_GOTO = ('GOTO', None, None, None)
  l_quadruples.append(quadruple_GOTO)

  index_GOTO = len(l_quadruples)-1 # Index of incompleted GOTO quadruple
  s_jumps.append(index_GOTO)

  # Replace previous GOTOF quadruple with the one that knows where to jump
  qudrupule_GOTOF = l_quadruples[false_quadruple]
  qudrupule_GOTOF = (qudrupule_GOTOF[0], qudrupule_GOTOF[1], None, index_GOTO + 1) 

  l_quadruples[false_quadruple] = qudrupule_GOTOF 

def p_ciclo_while(p):
  'ciclo_while : WHILE PARENTESIS_I quad_while_01 hiper_expression PARENTESIS_D quad_while_02 bloque quad_while_03'
    
def p_quad_while_01(p):
  'quad_while_01 :'
  first_quadruple_expression_index = len(l_quadruples)
  s_jumps.append(first_quadruple_expression_index)

def p_quad_while_02(p):
  'quad_while_02 :'
  res_expression_type = s_types.pop()

  if(res_expression_type == -1):
    error("Type mismatch in while")

  else:
    res_expression = s_operands.pop()
    quadruple_GOTOF = ('GOTOF', res_expression, None, None)
    l_quadruples.append(quadruple_GOTOF)

    index_previous_GOTOF = len(l_quadruples)-1
    s_jumps.append(index_previous_GOTOF)

def p_quad_while_03(p):
  'quad_while_03 :'
  index_previous_GOTOF = s_jumps.pop() 
  index_expression = s_jumps.pop()


  quadruple_GOTO = ('GOTO', None, None, index_expression)
  l_quadruples.append(quadruple_GOTO)

  index_skip = len(l_quadruples) # index to skip while

  quadruple_previous_GOTOF = l_quadruples[index_previous_GOTOF] 
  new_quadruple = (quadruple_previous_GOTOF[0], quadruple_previous_GOTOF[1], None, index_skip)
  l_quadruples[index_previous_GOTOF] = new_quadruple

def p_ciclo_for_01(p):
  'ciclo_for_01 : FOR aux_ID ASIGNA exp quad_for_01 ciclo_for_02'

def p_ciclo_for_02(p):
  'ciclo_for_02 : UNTIL quad_for_02 hiper_expression quad_for_03 bloque quad_for_04'

def p_quad_for_01(p):
  'quad_for_01 :'
  exp_type = s_types.pop()
  exp_result = s_operands.pop()  

  # var_id = variable_tuple[1]
  var_id = s_dimensions[-1][1]
  variable = variable_validation(var_id, 0)

  if not variable:
    error("Variable %s not declared" % var_id)

  var_type = variable.get_data_type()
  variable_address = variable.get_address()

  # var_type = s_types.pop()
  # variable = s_operands.pop()

  if exp_type != var_type:
    error("Type %s not assignable to %s" % (exp_type, var_type))

  elif(var_type != 0): # Not int
    error("Variable %s is not of type int" % variable)

  else:
    quadruple_EQUAL = ('=', exp_result, None, variable_address)
    l_quadruples.append(quadruple_EQUAL)


def p_quad_for_02(p):
  'quad_for_02 :'
  # Save the index to the first quadruple of the expression
  index_before_exp = len(l_quadruples)
  s_jumps.append(index_before_exp)

def p_quad_for_03(p):
  'quad_for_03 :'
  expression_type = s_types.pop()
  expression_result = s_operands.pop()  
  # print("expression_type:", expression_type )

  if(expression_type != 3):
      error("Expression result from FOR must be boolean")

  else:
      # Generate incomplete quadruple to skip Bloque
      quad_GOTOV = ('GOTOV', expression_result, None, None)
      l_quadruples.append(quad_GOTOV)

      # Save the index to the incomplete GOTOF
      index_GOTOV = len(l_quadruples)-1
      s_jumps.append(index_GOTOV)

def p_quad_for_04(p):
  'quad_for_04 :'

  variable_tuple = s_dimensions.pop()
  var_id = variable_tuple[1]

  constant_1_address = store_constant(0, 1)
  variable = variable_validation(var_id, 0)
  variable_address = variable.get_address()

  scope = 'global' if s_scopes[-1] == 'global' else 'local'
  id_virtual_address = memory_handler.new_variable(0, scope, 'temporal')
  
  quad_variable_plus_1 = ('+', variable_address, constant_1_address, id_virtual_address)
  l_quadruples.append(quad_variable_plus_1)

  quad_assign_to_for_id = ('=', id_virtual_address, None, variable_address)
  l_quadruples.append(quad_assign_to_for_id)

  # Obtain saved indexes
  index_pending_GOTF = s_jumps.pop()
  index_to_expression = s_jumps.pop()

  # quadruple to check value of the FOR??s expression
  quadruple_GOTO = ('GOTO', None, None, index_to_expression)
  l_quadruples.append(quadruple_GOTO)

  # Add the missing index to the previous GOTOF to skip Bloque when expression is false
  pending_GOTF = l_quadruples[index_pending_GOTF] 
  pending_GOTF= (pending_GOTF[0], pending_GOTF[1], None, len(l_quadruples))
  l_quadruples[index_pending_GOTF] = pending_GOTF

def p_hiper_expression(p):
  '''hiper_expression : super_expression   quadruple_creation_AND

  hiper_expression_02 : AND and_append super_expression
                      | vacio'''

def p_quadruple_creation_AND(p):
  'quadruple_creation_AND :'
  if(len(s_operators) != 0):
      if(s_operators[-1] == '&'):
        generate_expression_quadruple()

def p_and_append(p):
  'and_append :'
  s_operators.append('&')

def p_super_expression(p):
  '''super_expression : expression super_expression_02 quadruple_creation_OR

  super_expression_02 : OR or_append expression
                      | vacio'''

def p_quadruple_creation_OR(p):
  'quadruple_creation_OR :'
  if(len(s_operators) != 0):
    if(s_operators[-1] == '|'):
      generate_expression_quadruple()
    
def p_or_append(p):
  'or_append :'
  s_operators.append('|')

def p_expression(p):
  '''expression : exp m quadruple_creation_relational

      m         : MAYOR_QUE greater_than_append exp
                | MENOR_QUE less_than_append exp
                | NO_IGUAL different_append exp
                | IGUAL equal_append exp
                | vacio''' 

def p_quadruple_creation_relational(p):
  'quadruple_creation_relational :'
  if len(s_operators) != 0:
    if s_operators[-1]  in ['>' , '<', '<>', '==']:
      generate_expression_quadruple()

def p_greater_than_append(p):
  'greater_than_append :'
  s_operators.append('>')

def p_less_than_append(p):
  'less_than_append :'
  s_operators.append('<')

def p_different_append(p):
  'different_append :'
  s_operators.append('<>')

def p_equal_append(p):
  'equal_append :'
  s_operators.append('==')

def p_exp(p):
  '''exp : termino quadruple_creation_01 n

      n   : MAS addition_append exp 
          | MENOS substraction_append exp
          | vacio'''               

def p_addition_append(p):
  'addition_append :'
  # Push addition operator into operator stack
  s_operators.append('+')

def p_substraction_append(p):
  'substraction_append :'
  # Push substraction operator into operator stack
  s_operators.append('-')

def p_quadruple_creation_01(p):
  'quadruple_creation_01 :'
  if(len(s_operators) != 0): 
    if(s_operators[-1] == '+' or s_operators[-1] == '-'):
      generate_expression_quadruple()

def p_termino(p):
  '''termino : factor quadruple_creation_02 o

      o       : POR multiplication_append termino 
              | ENTRE divition_append termino
              | vacio'''

def p_multiplication_append(p):
  'multiplication_append :'
  s_operators.append('*')

def p_divition_append(p):
  'divition_append :'
  s_operators.append('/')

def p_quadruple_creation_02(p): 
  'quadruple_creation_02 :'
  if len(s_operators) != 0:
    if(s_operators[-1] == '*' or s_operators[-1] == '/'):
      generate_expression_quadruple()


def p_factor(p):
  '''factor : varcte 
            | MENOS varcte
            | aux_ID factor_02
            | PARENTESIS_I parenthesis_left_append hiper_expression PARENTESIS_D parenthesis_left_pop'''

  if len(p) == 2:
    # factor : varcte
    global current_constant
    global current_constant_type

    if current_constant_type in [0, 1, 2]:
      virtual_address = store_constant(current_constant_type, current_constant)

      s_operands.append(virtual_address)
      s_types.append(current_constant_type)
    current_constant = None

  elif p[1] == '-':
    # factor : MENOS varcte
    if current_constant_type in [0, 1, 2]:
      current_constant *= -1
      # Get constant address
      virtual_address = store_constant(current_constant_type, current_constant)
    
      s_operands.append(virtual_address)
      s_types.append(current_constant_type)
      
    current_constant = None
         
def p_aux_ID(p):
  'aux_ID : ID'
  s_dimensions.append(('id', p[1]))

def p_factor_02(p):
  '''factor_02 : CORCHETE_I parenthesis_left_append exp array_helper
               | PARENTESIS_I parenthesis_left_append reset_argument_counter posible_exp PARENTESIS_D parenthesis_left_pop
               | PUNTO ID 
               | PUNTO ID PARENTESIS_I reset_argument_counter posible_exp PARENTESIS_D
               | vacio'''
  # It is a single ID 
  if len(p) == 2:
    if s_dimensions[-1][0] == 'id':
      var_id = s_dimensions.pop()[1]

    # Check if variable is declared
    variable = variable_validation(var_id, 0)

    if not variable:
      error("Variable %s is not declared" % var_id)
        
    else:
      s_operands.append(variable.get_address())
      s_types.append(variable.get_data_type())

  # It is an attribute
  elif len(p) == 3:
      print("Atributo de clase")

 # Can be array or matrix
  elif len(p) == 5 and p[1] != '(':
    # First dimension of array or matrix
    dimension_1 = s_operands.pop()
    dimension_1_type = s_types.pop()

    # Validate that first dimension type is int
    if not dimension_1_type == 0:
      error("Indexing with non int type on array")
      
    # Get tuple from stack of dimensions can be ('id', ID) or (dim2, tim_type)
    elem1, elem2 = s_dimensions.pop()

    if elem1 == 'id': # we are having an array

      # Validate if variable exists
      variable = variable_validation(elem2, 1)

      if not variable:
        error("Array %s not declared" % elem2)
      
      array_name = elem2

      # Get array information from varsTable
      upper_limit = variable.get_dimensions()[1]
      base_address = variable.get_address()
      array_type = variable.get_data_type()

      upper_limit_address = memory_handler.constant_exists(0, upper_limit)

      # Generate quadruple (VER dim1)
      quadruple_VER = ('VER', dimension_1, array_name, upper_limit_address)
      l_quadruples.append(quadruple_VER)
      
      # Generate quadruple (S1 + BaseAddress)
      scope = 'global' if s_scopes[-1] == 'global' else 'local'
      array_virtual_address = memory_handler.new_variable(5, scope, 'temporal')
      quadruple_PLUS_BaseAddress = ('+', dimension_1, (base_address,), array_virtual_address)
      l_quadruples.append(quadruple_PLUS_BaseAddress)

      # Push to stacks
      s_operands.append(array_virtual_address)
      s_types.append(array_type)

    else: # we are having a matrix
      dimension_2 = elem1
      dimension_2_type = elem2
      message, matrix_id = s_dimensions.pop()

      # Validate that second dimension type is int
      if not dimension_2_type == 0:
        error("Indexing with non int type on matrix %s" % matrix_id)

      # Validate if variable exists
      variable = variable_validation(matrix_id, 2)

      if not variable:
        error("Matrix %s not declared" % matrix_id)

      # Get matrix information from varsTable
      matrix_dimension = variable.get_dimensions()
      matrix_type = variable.get_data_type()
      first_upper_limit = matrix_dimension[1]
      second_upper_limit = matrix_dimension[2]
      base_address = variable.get_address()

      # Get dimensions' limits as address
      first_upper_limit_address = memory_handler.constant_exists(0, first_upper_limit)
      second_upper_limit_address = memory_handler.constant_exists(0, second_upper_limit)

      # Generate quadruple (VER dim1)
      quadruple_VER = ('VER', dimension_1, matrix_id, first_upper_limit_address)
      l_quadruples.append(quadruple_VER)

      # Gnerate quadruple (s1 * m1)
      scope = 'global' if s_scopes[-1] == 'global' else 'local'
      m1_virtual_address = memory_handler.new_variable(dimension_1_type, scope,"temporal")
      quadruple_s1_times_m1 = ('*', dimension_1, second_upper_limit_address, m1_virtual_address) # s1 * m1
      l_quadruples.append(quadruple_s1_times_m1)
      print(quadruple_s1_times_m1)

      # Generate quadruple (VER dim2) 
      quadruple_VER = ('VER', dimension_2, matrix_id, second_upper_limit_address)
      l_quadruples.append(quadruple_VER)

      # Generate quadruple (S1 * m1 + S2)
      s2_virtual_address = memory_handler.new_variable(dimension_2_type, scope, 'temporal')
      quadruple_sum_s2 = ('+', m1_virtual_address, dimension_2, s2_virtual_address )
      l_quadruples.append(quadruple_sum_s2)
      
      # Generate quadruple (S1 * m1 + S2 + BaseAddress)
      matrix_virtual_address = memory_handler.new_variable(5, scope, 'temporal')
      quadruple_PLUS_BaseAddress = ('+', s2_virtual_address, (base_address,), matrix_virtual_address)
      l_quadruples.append(quadruple_PLUS_BaseAddress)

      # Push to stacks
      s_operands.append(matrix_virtual_address)
      s_types.append(matrix_type)

  # It is a function
  elif(len(p) == 7 and p[1] != '['): # LLamada a funcion non-void
    func_name = s_dimensions[-1][1]

    if not function_directory.scope_exists(func_name):
      error("Function %s not declared" % func_name)

    # Verify number of arguments in function call
    elif function_directory.get_scope(func_name).get_number_of_parameters() != argument_counter:
      error("Incoherence in number of arguments in function call  %s" % func_name) 
            
    else:
      quadruple_ERA = ('ERA', func_name, None, None)
      l_quadruples.append(quadruple_ERA)

      argument_index = 0
      # Create PARAMETER quadruple for each argument
      while(len(s_function_call_arguments) > 0):
        # Remove the argument in order
        argument = s_function_call_arguments.popleft()
        argument_type = s_function_call_argument_types.popleft()

        # Verify argument type
        if argument_type != function_directory.get_scope(func_name).get_params_table()[argument_index]:
          error("Argument type is incorrect in function call %s" % func_name) 

        else:
          quadruple_PARAMETER = ('PARAMETER', argument, argument_type, argument_index)
          l_quadruples.append(quadruple_PARAMETER)
          argument_index +=1

      quadruple_GOSUB = ('GOSUB', func_name, None, None)
      l_quadruples.append(quadruple_GOSUB)

      # Obtain variable information of the function??s global variable
      variable = variable_validation(func_name, 0)

      if not variable:
        error("Invalid call of void function %s" % func_name)
      
      # Assign the return value of the function into a temporal
      guadalupan_patch(variable)

  # PUNTO ID PARENTESIS_I reset_argument_counter posible_exp PARENTESIS_D
  elif len(p) == 7: # non-void method call
    # class_name = s_dimensions.pop()[0]
    class_name = s_dimensions[-1][0]
    method_name = p[3]

    if not class_directory.scope_exists(class_name):
      error("Class %s not declared" % class_name)   
    
    elif not class_directory.get_class(class_name).get_scope(method_name):
      error("Method %s not declared" % method_name)    

    # Verify number of arguments in function call
    elif class_directory.get_class(class_name).get_scope(method_name).get_number_of_parameters() != argument_counter:
      error("Incoherence in number of arguments in method call %s" % method_name)    
            
    else:
      quadruple_ERA = ('ERA', method_name, None, None)
      l_quadruples.append(quadruple_ERA)

      argument_index = 0
      # Create PARAMETER quadruple for each argument
      while(len(s_function_call_arguments) > 0):
        # Remove the argument in order
        argument = s_function_call_arguments.popleft()
        argument_type = s_function_call_argument_types.popleft()

        # Verify argument type
        if argument_type != class_directory.get_class(class_name).get_scope(method_name).params_table[argument_index]:
          error("Argument type is incorrect in method call %s" % method_name)

        else:
          quadruple_PARAMETER = ('PARAMETER', argument, argument_type, argument_index)
          l_quadruples.append(quadruple_PARAMETER)
          argument_index +=1

      quadruple_GOSUB = ('GOSUB', method_name, class_name, None)
      l_quadruples.append(quadruple_GOSUB)

      #Obtain variable information of the method's global variable
      variable = variable_validation(method_name, 0)

      if not variable:
        error("Invalid call of void method %s" % method_name)
      
      # Assign the return value of the method into a temporal
      guadalupan_patch(variable)

def p_array_helper(p):
  '''array_helper : CORCHETE_D parenthesis_left_pop
                  | COMA exp CORCHETE_D parenthesis_left_pop''' 
  print("\n\n(2)", s_operands)
  if len(p) == 5:
    dimension_2 = s_operands.pop()
    dimension_2_type = s_types.pop()

    # Add second dimension to stack
    s_dimensions.append((dimension_2, dimension_2_type))   

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
  current_constant_type = 0

def p_constant_float_assginment(p):
  'constant_float_assginment :'
  global current_constant_type
  current_constant_type = 1

def p_constant_char_assginment(p):
  'constant_char_assginment :'
  global current_constant_type
  current_constant_type = 2

def p_error(p):
  if p:
      error("Syntax error at '%s'" % p.value)

## Contruir parser
parser = yacc.yacc()

print(data)
parser.parse(data)

## Cerrar archivo
f.close()
