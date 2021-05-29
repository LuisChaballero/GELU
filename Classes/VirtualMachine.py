# VirtualMachine class ...
import SemanticCube as sc
from Utilities import ranges, GLOBALS_BASE_ADDRESS, LOCALS_BASE_ADDRESS, CONSTANTS_BASE_ADDRESS, OBJECTS_BASE_ADDRESS, error
import Classes.MemoryHandler as mh
from Classes.Memory import Memory
from Classes.FunctionDirectory import FunctionDirectory
from Classes.ClassDirectory import ClassDirectory

from collections import deque

class VirtualMachine:
  # Class constructor that saves the quadruple list and runs its execution
  def __init__(self, quadruple_list, function_directory, class_directory, constant_directory):
    self.__main = Memory()
    self.__quadruple_list = quadruple_list
    self.__s_contexts = deque()
    self.__s_jumps = deque()
    self.__quadruple_iterator = 0
    self.store_constants(constant_directory)

  # Method to store all constants into memory
  def store_constants(self, constant_directory):
    for key, type_directory in constant_directory.items():  # iterate over constant directory
      for value, virtual_address in type_directory.items(): # iterate over each specific type directory
        self.__main.push(virtual_address, value)          # add constant to memory

  # Method to update the quadruple iterator
  def next_process(self):
    self.__quadruple_iterator += 1
  
  # Method to retrieve the current process running
  def current_process(self):
    return self.__quadruple_list[self.__quadruple_iterator]

  # Method to get the value of an address depending on its scope
  def get_value(self, virtual_address):
    # Infer scope from address
    scope = mh.get_scope_from_address(virtual_address)

    # Address is in main memory
    if scope in ['global', 'constant']:
      return self.__main.value(virtual_address)
    # Address could be in main memory or in a stack of memory
    elif scope == 'local': 
      current_context = self.__s_contexts[-1] # Get the current memory context
      # Validate if address is in current context
      if not current_context.address_exists(virtual_address): # Not in current context
        # Validate if address is in main memory
        if not self.__main.address_exists(virtual_address):  # Not in memory
          error("This address does not exist in main")
        else:
         return self.__main.value(virtual_address)
      # Return value from current context
      else:
        return current_context.value(virtual_address)

  # Method to execute a binary operation
  def binary_operation(self, quadruple):
    operator, l_address, r_operand, res_address = quadruple
    # Check for operands data types infered from address
    # l_type = mh.get_type_from_address(l_address)
    # r_type = mh.get_type_from_address(l_address)

    # Get operand_address values
    l_value = self.get_value(l_address)
    r_value = self.get_value(r_operand)

    ################### FALTA VALIDAR SI ES TIPO POINTER
    # res_type = sc.result_type(l_type, r_type)

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
        return l_value / r_value
    elif operator == '&':
      return l_value and r_value
    elif operator == '|':
      return l_value or value
    elif operator == '<':
      return l_value < r_value
    elif operator == '>':
      return l_value > r_value
    elif operator == '<>':
      return l_value != r_value
    elif operator == '==':
      return l_value == r_value   

  # Method to execute the list of quadruples
  def run(self):
    execute_quadruples = True
    
    print("Start processor")
    # Execute quadruples
    while execute_quadruples:
      quadruple = self.current_process()
      operator = quadruple[0]

      if operator == 'GOTO':
        print("execute GOTO: ", quadruple[3])
        self.__quadruple_iterator = quadruple[3]
      
      elif operator == 'GOTOV':
        print("execute GOTOV: ", quadruple[3])
        if quadruple[1]:
          iterator = quadruple[3]
      
      elif operator == 'GOTOF':
        print("execute GOTOF: ", quadruple[3])
        if quadruple[1]:
          iterator = quadruple[3]

      elif operator == 'PRINT':
        print("execute PRINT")
        value = self.__main.value(quadruple[3])
        if value == 0:
          print(int(value))
        else:
          print(value)

      elif operator in ['+', '-', '*', '/', '&', '|', '<', '>', '<>', '==']:
        print("execute EQUAL")
        # Execute binary operation and send temporal result to memory
        res = self.binary_operation(quadruple)
        if len(self.__s_contexts) == 0:
          self.__main.push(quadruple[3], res)
        else:
          self.__s_contexts[-1].push(quadruple[3], res)
          
      
      elif operator == '&':
        print("execute AND")
        left_operand = self.__main.value(quadruple[1])
        right_operand = self.__main.value(quadruple[2])
        virtual_address = quadruple[3]
        res = left_operand and right_operand
        self.__main.push(virtual_address, res)
      
      elif operator == '|':
        print("execute OR")
        left_operand = self.__main.value(quadruple[1])
        right_operand = self.__main.value(quadruple[2])
        virtual_address = quadruple[3]
        res = left_operand or right_operand
        self.__main.push(virtual_address, res)

      elif operator == '+':
        print("execute MAS")
        left_value = self.__main.value(quadruple[1])
        right_value = self.__main.value(quadruple[2])
        res = left_value + right_value
        print("Executing suma > ", res)
        self.__main.push(quadruple[3], res)

      elif operator == '-':
        print("execute MENOS")
        left_value = self.__main.value(quadruple[1])
        right_value = self.__main.value(quadruple[2])
        res = left_value - right_value
        self.__main.push(quadruple[3], res)
        
      elif operator == '*':
        print("execute POR")
        left_value = self.__main.value(quadruple[1])
        right_value = self.__main.value(quadruple[2])
        res = left_value * right_value
        self.__main.push(quadruple[3], res)
      
      elif operator == '/':
        print("execute ENTRE")
        left_value = self.__main.value(quadruple[1])
        right_value = self.__main.value(quadruple[2])
        res = left_value / right_value

        # Res must be of type int
        if (
              quadruple[3] in range(mh.GLOBAL_VARIABLE_INT_ADDRESS, mh.GLOBAL_VARIABLE_INT_ADDRESS+mh.ranges['variable']) or 
              quadruple[3] in range(mh.GLOBAL_TEMPORAL_INT_ADDRESS, mh.GLOBAL_TEMPORAL_INT_ADDRESS+mh.ranges['temporal']) or 
              quadruple[3] in range(mh.LOCAL_VARIABLE_INT_ADDRESS, mh.LOCAL_VARIABLE_INT_ADDRESS+mh.ranges['variable']) or 
              quadruple[3] in range(mh.LOCAL_TEMPORAL_INT_ADDRESS, mh.LOCAL_TEMPORAL_INT_ADDRESS+mh.ranges['temporal']) or 
              quadruple[3] in range(mh.CONSTANTS_BASE_ADDRESS[0], mh.CONSTANTS_BASE_ADDRESS[0]+mh.ranges['constant'])
            ):
          self.__main.push(quadruple[3], int(res))
        else:
          self.__main.push(quadruple[3], res)

      elif operator == '<>':
        print("execute DIFERENTE")
        left_value = self.__main.value(quadruple[1])
        right_value = self.__main.value(quadruple[2])
        res = left_value != right_value
        self.__main.push(quadruple[3], res)
        
      elif operator == '<':
        print("execute MENOR_QUE")
        left_value = self.__main.value(quadruple[1])
        right_value = self.__main.value(quadruple[2])
        res = left_value < right_value
        self.__main.push(quadruple[3], res)

      elif operator == '>':
        print("execute MAYOR_QUE")
        left_value = self.__main.value(quadruple[1])
        right_value = self.__main.value(quadruple[2])
        res = left_value > right_value
        self.__main.push(quadruple[3], res)

      elif operator == '&':
        print("execute AND")

      elif operator == '|':
        print("execute OR")

      elif operator == 'END':
        execute_quadruples = False
        print("execute END")

