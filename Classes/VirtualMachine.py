# VirtualMachine class ...

import Classes.MemoryHandler as mh

class VirtualMachine:
  # Class constructor that saves the quadruple list and runs its execution
  def __init__(self, quadruple_list):
    self.quadruple_list = quadruple_list
    self.run()

  # Method to execute the list of quadruples
  def run(self):
    memory_handler = mh.MemoryHandler()
    iterator = 0
    
    print("Start while loop")
    # Execute quadruples
    while iterator < len(self.quadruple_list):
      quadruple = self.quadruple_list[iterator]
      operator = quadruple[0]
      print("Iter:", iterator, "   Quadruple:", quadruple)

      if operator == 'GOTO':
        print("execute GOTO: ", quadruple[3])
        iterator = quadruple[3]

      elif operator == '+':
        print("execute MAS")
        left_value = memory_handler.value(quadruple[1])
        right_value = memory_handler.value(quadruple[2])
        res = left_value + right_value
        memory_handler.push(quadruple[3], res)

      elif operator == '-':
        print("execute MENOS")
        left_value = memory_handler.value(quadruple[1])
        right_value = memory_handler.value(quadruple[2])
        res = left_value - right_value
        memory_handler.push(quadruple[3], res)
        
      elif operator == '*':
        print("execute POR")
        left_value = memory_handler.value(quadruple[1])
        right_value = memory_handler.value(quadruple[2])
        res = left_value * right_value
        memory_handler.push(quadruple[3], res)
      
      elif operator == '/':
        print("execute ENTRE")
        left_value = memory_handler.value(quadruple[1])
        right_value = memory_handler.value(quadruple[2])
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
          memory_handler.push(quadruple[3], int(res))
        else:
          memory_handler.push(quadruple[3], res)

      elif operator == '<>':
        print("execute DIFERENTE")
        left_value = memory_handler.value(quadruple[1])
        right_value = memory_handler.value(quadruple[2])
        res = left_value != right_value
        memory_handler.push(quadruple[3], res)
        
      elif operator == '<':
        print("execute MENOR_QUE")
        left_value = memory_handler.value(quadruple[1])
        right_value = memory_handler.value(quadruple[2])
        res = left_value < right_value
        memory_handler.push(quadruple[3], res)

      elif operator == '>':
        print("execute MAYOR_QUE")
        left_value = memory_handler.value(quadruple[1])
        right_value = memory_handler.value(quadruple[2])
        res = left_value > right_value
        memory_handler.push(quadruple[3], res)

      elif operator == '&':
        print("execute AND")

      elif operator == '|':
        print("execute OR")
        
        


      iterator += 1
