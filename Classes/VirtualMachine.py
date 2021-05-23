# VirtualMachine class ...

import Classes.MemoryHandler as mh
from Classes.FunctionDirectory import FunctionDirectory
from Classes.ClassDirectory import ClassDirectory

from collections import deque

class VirtualMachine:
  # Class constructor that saves the quadruple list and runs its execution
  def __init__(self, quadruple_list, memory_handler, functionDirectory, classDirectory):
    self.memory_handler = memory_handler
    self.quadruple_list = quadruple_list
    self.s_contexts = deque()
    self.s_jumps = deque()
    self.run()

  # Method to execute the list of quadruples
  def run(self):
    execute_quadruples = True
    iterator = 0
    
    print("Start while loop")
    # Execute quadruples
    while execute_quadruples:
      quadruple = self.quadruple_list[iterator]
      operator = quadruple[0]
      print("Iter:", iterator, "   Quadruple:", quadruple)

      if operator == 'GOTO':
        print("execute GOTO: ", quadruple[3])
        iterator = quadruple[3] - 1
      
      elif operator == 'GOTOV':
        print("execute GOTOV: ", quadruple[3])
        if quadruple[1]:
          iterator = quadruple[3]
      
      elif operator == 'GOTOF':
        print("execute GOTOF: ", quadruple[3])
        if quadruple[1]:
          iterator = quadruple[3]
      
      # elif operator == 'ERA':
      #   print("execute ERA: ", quadruple[1])
      #   # s_jumps.append(iterator)
      #   # iterator = 
      #   if quadruple[2] == 0: # In functionDirectory
      #     memory_handler = mh.MemoryHandler()
      #     self.s_contexts.append(memory_handler)
      #   else:
          

      elif operator == 'PRINT':
        print("execute PRINT")
        value = self.memory_handler.value(quadruple[3])
        print(value)

      elif operator == '=':
        print("execute EQUAL")
        value = self.memory_handler.value(quadruple[1])
        virtual_address = quadruple[3]
        self.memory_handler.push(virtual_address, value)

      elif operator == '+':
        print("execute MAS")
        left_value = self.memory_handler.value(quadruple[1])
        right_value = self.memory_handler.value(quadruple[2])
        res = left_value + right_value
        print("Executing suma > ", res)
        self.memory_handler.push(quadruple[3], res)

      elif operator == '-':
        print("execute MENOS")
        left_value = self.memory_handler.value(quadruple[1])
        right_value = self.memory_handler.value(quadruple[2])
        res = left_value - right_value
        self.memory_handler.push(quadruple[3], res)
        
      elif operator == '*':
        print("execute POR")
        left_value = self.memory_handler.value(quadruple[1])
        right_value = self.memory_handler.value(quadruple[2])
        res = left_value * right_value
        self.memory_handler.push(quadruple[3], res)
      
      elif operator == '/':
        print("execute ENTRE")
        left_value = self.memory_handler.value(quadruple[1])
        right_value = self.memory_handler.value(quadruple[2])
        res = left_value / right_value

        # Res must be of type int
        if (
              quadruple[3] in range(mh.GLOBAL_VARIABLE_INT_ADDRESS, mh.GLOBAL_VARIABLE_INT_ADDRESS+3000) or 
              quadruple[3] in range(mh.GLOBAL_TEMPORAL_INT_ADDRESS, mh.GLOBAL_TEMPORAL_INT_ADDRESS+1000) or 
              quadruple[3] in range(mh.LOCAL_VARIABLE_INT_ADDRESS, mh.LOCAL_VARIABLE_INT_ADDRESS+3000) or 
              quadruple[3] in range(mh.LOCAL_TEMPORAL_INT_ADDRESS, mh.LOCAL_TEMPORAL_INT_ADDRESS+1000) or 
              quadruple[3] in range(mh.CLASS_GLOBAL_VARIABLE_INT_ADDRESS, mh.CLASS_GLOBAL_VARIABLE_INT_ADDRESS+1000) or 
              quadruple[3] in range(mh.CLASS_LOCAL_VARIABLE_INT_ADDRESS, mh.CLASS_LOCAL_VARIABLE_INT_ADDRESS+1000) or 
              quadruple[3] in range(mh.CLASS_LOCAL_TEMPORAL_INT_ADDRESS, mh.CLASS_LOCAL_TEMPORAL_INT_ADDRESS+1000) or 
              quadruple[3] in range(mh.CONSTANT_INT_ADDRESS, mh.CONSTANT_INT_ADDRESS+1000)
            ):
          self.memory_handler.push(quadruple[3], int(res))
        else:
          self.memory_handler.push(quadruple[3], res)

      elif operator == '<>':
        print("execute DIFERENTE")
        left_value = self.memory_handler.value(quadruple[1])
        right_value = self.memory_handler.value(quadruple[2])
        res = left_value != right_value
        self.memory_handler.push(quadruple[3], res)
        
      elif operator == '<':
        print("execute MENOR_QUE")
        left_value = self.memory_handler.value(quadruple[1])
        right_value = self.memory_handler.value(quadruple[2])
        res = left_value < right_value
        self.memory_handler.push(quadruple[3], res)

      elif operator == '>':
        print("execute MAYOR_QUE")
        left_value = self.memory_handler.value(quadruple[1])
        right_value = self.memory_handler.value(quadruple[2])
        res = left_value > right_value
        self.memory_handler.push(quadruple[3], res)

      elif operator == '&':
        print("execute AND")

      elif operator == '|':
        print("execute OR")

      elif operator == 'END':
        execute_quadruples = False
        print("execute END")

      iterator += 1
