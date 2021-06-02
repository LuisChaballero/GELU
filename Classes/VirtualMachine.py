# VirtualMachine class ...
import Helpers.SemanticCube as sc
from Helpers.Utilities import ranges, GLOBALS_BASE_ADDRESS, LOCALS_BASE_ADDRESS, CONSTANTS_BASE_ADDRESS, OBJECTS_BASE_ADDRESS, error, types
import Classes.MemoryHandler as mh
from Classes.Memory import Memory
from Classes.FunctionDirectory import FunctionDirectory
from Classes.ClassDirectory import ClassDirectory
from math import floor

from collections import deque

class VirtualMachine:
  """Class constructor that saves the quadruple list and runs its execution"""
  def __init__(self, quadruple_list, function_directory, class_directory, constant_directory):
    self.__main = Memory()
    self.__quadruple_list = quadruple_list
    self.__s_execution = deque()
    self.__s_jumps = deque()
    self.__quadruple_iterator = 0
    self.class_directory = class_directory
    self.function_directory = function_directory
    self.store_constants(constant_directory)
    self.class_context = None

  def store_constants(self, constant_directory):
    '''Stores all constants from semantic into memory'''
    for key, type_directory in constant_directory.items():  # iterate over constant directory
      for constant, virtual_address in type_directory.items(): # iterate over each specific type directory
        self.__main.push(virtual_address, constant)          # add constant to memory

  def proceed(self):
    '''Updates the quadruple iterator plus one'''
    self.__quadruple_iterator += 1

  def next_process(self):
    """Returns the next process"""
    if self.__quadruple_iterator+1 < len(self.__quadruple_list):
      return self.__quadruple_list[self.__quadruple_iterator+1]
    else:
      False
  
  def current_process(self):
    '''Retrieves the current quadruple running'''
    # print(self.__quadruple_iterator, self.__quadruple_list[self.__quadruple_iterator])
    return self.__quadruple_list[self.__quadruple_iterator]

  def get_value(self, virtual_address):
    '''Gets the value of an address depending on its scope range'''
    # Infer scope from address
    scope_range = mh.get_scope_from_address(virtual_address)

    # Address is in main memory
    if scope_range in ['global', 'constant']:
      return self.__main.value(virtual_address)
    # Address could be in main memory or in a stack of memory
    elif scope_range == 'local': 
      if len(self.__s_execution) > 0:
        current_context = self.__s_execution[-1] # Get the current memory context
        # Validate if address is in currenresst context
        if current_context.address_exists(virtual_address) == None: # Not in current context
          # Validate if address is in main memory
          if self.__main.address_exists(virtual_address) == None:  # Not in memory
            error("This address does not exist in main %s" % virtual_address)
          else:
            return self.__main.value(virtual_address)
        # Return value from current context
        else:
          return current_context.value(virtual_address)

  def binary_operation(self, quadruple):
    """Executes a binary operation"""
    operator, l_address, r_operand, res_address = quadruple
    
    l_type = mh.get_type_from_address(l_address) # Check for operands data types infered from address
    
    # Get operand_address values
    l_value = self.get_value(l_address)

    if type(r_operand) == tuple: # We want the literal
      r_value = r_operand[0]
      r_type = 0
    else: # We want the value
      r_value = self.get_value(r_operand)
      r_type = mh.get_type_from_address(r_operand)
    
    if l_type == 5:
      l_value = self.get_value(l_value)
    
    if r_type == 5:
      r_value = self.get_value(r_value)
    
    if l_value == None:
      error("Uninitialized left variable")
    
    if r_value == None:
      error("Uninitialized right variable")

    if operator == '+':
      return l_value + r_value
    elif operator == '-':
      return l_value - r_value
    elif operator == '*':
      return l_value * r_value
    elif operator == '/':
      if r_value == 0:
        error("Division by zero")
      else:
        if l_type == 0 and r_type == l_type:
          return floor(l_value / r_value)
        else:
          return l_value / r_value
    elif operator == '&':
      return l_value and r_value
    elif operator == '|':
      return l_value or r_value
    elif operator == '<':
      return l_value < r_value
    elif operator == '>':
      return l_value > r_value
    elif operator == '<>':
      return l_value != r_value
    elif operator == '==':
      return l_value == r_value   

  def assign(self, assignTo, value):
    '''Assigns vale to the specified address depending on the memory context'''
    scope = mh.get_scope_from_address(assignTo)
    if scope == 'global':
      self.__main.push(assignTo, value)
    else:
      self.__s_execution[-1].push(assignTo, value)
    # print("Execute: %s = %s" % (assignTo, value))

  def cast(self, value, v_type):
    '''Casts a value to a specific data type'''
    if v_type in [0,5]:
      return int(value)
    elif v_type == 1:
      return float(value)
    elif v_type in [2,4]:
      return str(value[1:-1]) 
    elif v_type == 3:
      return bool(value)
    else:
      error("Invalid casting to %s" % v_type)

  # Method to execute the list of quadruples
  def run(self):
    '''Simulates a virtual machine executing all quadruples'''
    print("-----Start program execution-----")
    # Execute quadruples
    while True:
      quadruple = self.current_process()
      operator = quadruple[0]

      if operator == 'GOTO':
        # print("execute GOTO: ", quadruple[3])
        self.__quadruple_iterator = quadruple[3]
      
      elif operator == 'GOTOV':
        # print("execute GOTOV: ", quadruple[1], quadruple[3])
        condition = self.get_value(quadruple[1])
        if condition:
          self.__quadruple_iterator = quadruple[3]
        else:
          self.proceed()
      
      elif operator == 'GOTOF':
        # print("execute GOTOF: ", quadruple[1], quadruple[3])
        condition = self.get_value(quadruple[1])
        # print("condition",condition)
        if not condition:
          self.__quadruple_iterator = quadruple[3]
        else:
          self.proceed()

      elif operator == 'ERA':
        self.__s_execution.append(Memory())
        
        self.proceed()
        # print("\nExecute ERA")

      elif operator == 'PARAMETER':
        # print('START PARAMETER')
        argument_address = quadruple[1]
        argument_index = quadruple[3]
        argument_type = quadruple[2]

        # Function/method call was made inside another function/method
        if len(self.__s_execution) > 1:
          # Take out current execution so you can get argument value from previous execution
          current_context = self.__s_execution.pop()
          argument_value = self.get_value(argument_address)

          # Put back current execution 
          self.__s_execution.append(current_context)
        else:
          # Function call was made on main
          current_context = self.__s_execution[-1]
          argument_value = self.get_value(argument_address)
        
        # Create variable on new memory to save the argument value from call
        local_address = current_context.get_handler().new_variable(argument_type, 'local', 'variable')

        current_context.push(local_address, argument_value)
        # print("Execute PARAMETER: address: %s value: %s" % (argument_address, argument_value))
        self.proceed()

      elif operator == 'GOSUB':
        function_name = quadruple[1]
        
        if quadruple[2] == None: # GOSUB to a function
          scope = self.function_directory.get_scope(function_name)
        else: # GOSUB to a method
          class_name = quadruple[2]
          scope = self.class_directory.get_class(class_name).get_scope(function_name)
          
        function_instruction_pointer = scope.get_initial_address()
        self.__s_jumps.append(self.__quadruple_iterator+1)
        
        self.__quadruple_iterator = function_instruction_pointer
        # print("Execute GOSUB")

      elif operator == 'RETURN':
        # print("Execute RETURN")
        function_return_address = quadruple[1]
        function_var_address = quadruple[3]

        function_return = self.get_value(function_return_address)
        
        if self.class_context == None:
          self.__main.push(function_var_address, function_return)
        else:
          self.class_context.push(function_var_address, function_return)
        
        self.proceed()
                  
      elif operator == 'ENDPROC':
        # Delete last activation record
        endproc = self.__s_execution.pop()
        del endproc

        # Continue with next process
        self.__quadruple_iterator = self.__s_jumps.pop()

        # print("Execute ENDPROC")

      elif operator == 'PRINT':
        # print("execute PRINT")
        res = ""
        value_type = mh.get_type_from_address(quadruple[3])

        value = self.get_value(quadruple[3])

        if value_type == 5:
          value = self.get_value(value)

        res += str(self.cast(value, value_type))

        while True:
          next_process = self.next_process()

          if next_process[0] == 'PRINT2':
            next_type = mh.get_type_from_address(next_process[3])
            next_value = self.get_value(next_process[3])

            if next_type == 5:
              next_value = self.get_value(next_value)
            
            if next_type == 2:
              res = res + next_value
            else:
              res = res + str(self.cast(next_value, next_type))

            self.proceed()
          else:
            break
        
        print(res)
        self.proceed()
        
      elif operator == 'READ':
        # Get information from quadruple
        assignTo = quadruple[3]
        data_type = mh.get_type_from_address(assignTo)

        # Ask for user input
        read_input = input()

        # Save user input in the address of the value of the pointer (array or matrix)
        if data_type == 5:
          assignTo = self.get_value(assignTo)
          data_type = mh.get_type_from_address(assignTo)

        size = len(read_input)
        # Catch possible errors of different value type
        try:
          # Cast char to string
          if data_type == 2 and size == 1:
            read_input = str(read_input)
          # Cast to other types
          elif data_type != 2:
            read_input = self.cast(read_input, data_type)
          else:
            error("Expected a %s type value on read" % types[data_type])
        except (ValueError):
          error("Expected a %s type value on read." % types[data_type])

        # Put value in memory
        self.assign(assignTo, read_input)
        self.proceed()

      elif operator in ['+', '-', '*', '/', '&', '|', '<', '>', '<>', '==']:
        # Execute binary operation and send temporal result to memory
        value = self.binary_operation(quadruple)
        assignTo = quadruple[3]
        self.assign(assignTo, value)
        self.proceed()
      
      elif operator == '=':
        l_type = mh.get_type_from_address(quadruple[1])
        l_value = self.get_value(quadruple[1])
        # print(l_value)

        if l_type == 5: # Check if it is a pointer
          l_value = self.get_value(l_value)

        assignTo_type = mh.get_type_from_address(quadruple[3])
        assignTo = quadruple[3]
        if assignTo_type == 5: # Check if it is a pointer
          assignTo = self.get_value(assignTo)
        
        if l_value == None:
          error("Trying to assign empty address %s" % l_value)

        self.assign(assignTo, l_value)
        self.proceed()

      elif operator == 'VER':
        # Verify correct indexation for array and matrix
        index_address = quadruple[1]
        index_value = self.get_value(index_address)

        upper_limit_address = quadruple[3]
        upper_limit = self.get_value(upper_limit_address)

        if not index_value >= 0 and index_value < upper_limit:
          error("Invalid indexation of %s" % quadruple[2])
        self.proceed()
        

      elif operator == 'END':
        print("")
        break

