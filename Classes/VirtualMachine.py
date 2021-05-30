# VirtualMachine class ...
import SemanticCube as sc
from Utilities import ranges, GLOBALS_BASE_ADDRESS, LOCALS_BASE_ADDRESS, CONSTANTS_BASE_ADDRESS, OBJECTS_BASE_ADDRESS, error
import Classes.MemoryHandler as mh
from Classes.Memory import Memory
from Classes.FunctionDirectory import FunctionDirectory
from Classes.ClassDirectory import ClassDirectory
from math import floor

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

  def store_constants(self, constant_directory):
    '''Stores all constants from semantic into memory'''
    for key, type_directory in constant_directory.items():  # iterate over constant directory
      for constant, virtual_address in type_directory.items(): # iterate over each specific type directory
        self.__main.push(virtual_address, constant)          # add constant to memory

  def proceed(self):
    '''Updates the quadruple iterator plus one'''
    self.__quadruple_iterator += 1

  def next_process(self):
    if self.__quadruple_iterator+1 < len(self.__quadruple_list):
      return self.__quadruple_list[self.__quadruple_iterator+1]
    else:
      False
  
  def current_process(self):
    '''Retrieves the current quadruple running'''
    return self.__quadruple_list[self.__quadruple_iterator]

  def get_value(self, virtual_address):
    '''Gets the value of an address depending on its scope'''
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
    if len(self.__s_contexts) == 0:
      self.__main.push(assignTo, value)
    else:
      self.__s_contexts[-1].push(assignTo, value)
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

      elif operator == 'PRINT':
        # print("execute PRINT")
        res = ""
        value_type = mh.get_type_from_address(quadruple[3])
        value = self.get_value(quadruple[3])
        res += str(self.cast(value, value_type))

        while True:
          next_process = self.next_process()

          if next_process[0] == 'PRINT':
            next_type = mh.get_type_from_address(next_process[3])
            next_value = self.get_value(next_process[3])
            res = res + str(self.cast(next_value, next_type))
            self.proceed()
          else:
            break
        
        print(res)
        self.proceed()
        

      elif operator in ['+', '-', '*', '/', '&', '|', '<', '>', '<>', '==']:
        # print("execute binary operation")
        # Execute binary operation and send temporal result to memory
        value = self.binary_operation(quadruple)
        assignTo = quadruple[3]
        # if len(self.__s_contexts) == 0:
        #   self.__main.push(assignTo, value)
        # else:
        #   self.__s_contexts[-1].push(assignTo, value)
        self.assign(assignTo, value)
        self.proceed()
      
      elif operator == '=':
        l_type = mh.get_type_from_address(quadruple[1])
        l_value = self.get_value(quadruple[1])

        if l_type == 5: # Check if it is a pointer
          l_value = self.get_value(l_value)

        assignTo_type = mh.get_type_from_address(quadruple[3])
        assignTo = quadruple[3]
        if assignTo_type == 5: # Check if it is a pointer
          assignTo = self.get_value(assignTo)
        
        if l_value == None:
          error("Trying to assign empty address")

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

