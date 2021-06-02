from Helpers.Utilities import ranges, types, error, GLOBALS_BASE_ADDRESS, LOCALS_BASE_ADDRESS, CONSTANTS_BASE_ADDRESS, OBJECTS_BASE_ADDRESS

class MemoryHandler():
  def __init__(self):
    self.__global_variable_counters = {
                                        0: GLOBALS_BASE_ADDRESS['variable'][0], 
                                        1: GLOBALS_BASE_ADDRESS['variable'][1], 
                                        2: GLOBALS_BASE_ADDRESS['variable'][2]
                                      }

    self.__global_temporal_counters = {
                                        0: GLOBALS_BASE_ADDRESS['temporal'][0], 
                                        1: GLOBALS_BASE_ADDRESS['temporal'][1], 
                                        2: GLOBALS_BASE_ADDRESS['temporal'][2],
                                        3: GLOBALS_BASE_ADDRESS['temporal'][3],
                                        5: GLOBALS_BASE_ADDRESS['temporal'][5]
                                      }
    
    self.__local_variable_counters =  {
                                        0: LOCALS_BASE_ADDRESS['variable'][0], 
                                        1: LOCALS_BASE_ADDRESS['variable'][1], 
                                        2: LOCALS_BASE_ADDRESS['variable'][2]
                                      }
    
    self.__local_temporal_counters =  {
                                        0: LOCALS_BASE_ADDRESS['temporal'][0], 
                                        1: LOCALS_BASE_ADDRESS['temporal'][1], 
                                        2: LOCALS_BASE_ADDRESS['temporal'][2],
                                        3: LOCALS_BASE_ADDRESS['temporal'][3],
                                        5: LOCALS_BASE_ADDRESS['temporal'][5]
                                      }

    self.__constants_directory =  {
                                    0:{}, 
                                    1:{}, 
                                    2:{}, 
                                    4:{}
                                  }

    self.__constants_counters =  {
                                  0: CONSTANTS_BASE_ADDRESS[0], # Int
                                  1: CONSTANTS_BASE_ADDRESS[1],  # Float
                                  2: CONSTANTS_BASE_ADDRESS[2],  # Char
                                  4: CONSTANTS_BASE_ADDRESS[4]   # String
                                }

  # Method to validate an address considering the data_type, scope, item_type, and is_constant
  def is_address_valid(self, virtual_address, data_type, scope, item_type, is_constant=False):
    # Check if address is for a constant
    if is_constant:
      if not CONSTANTS_BASE_ADDRESS[data_type] <= virtual_address < (CONSTANTS_BASE_ADDRESS[data_type] + ranges["constant"]): # Count exceeded
        error("Too many %s constants" % types[data_type])

    else: # is variable or temporal
      # Is an int, float, char
      if data_type in [0,1,2]:
        if scope == "global":
          if item_type in ["variable", "temporal"]:
            if not GLOBALS_BASE_ADDRESS[item_type][data_type] <= virtual_address < (GLOBALS_BASE_ADDRESS[item_type][data_type] + ranges[item_type]):
              error("Too many %s %s %ss" % (types[data_type], scope, item_type))

        if scope == "local":
          if item_type in ["variable", "temporal"]:
            if not LOCALS_BASE_ADDRESS[item_type][data_type] <= virtual_address < (LOCALS_BASE_ADDRESS[item_type][data_type] + ranges[item_type]):
              error("Too many %s %s %ss" % (types[data_type], scope, item_type))
        
      elif data_type in [3,5]: # bool or pointer
        if scope == "global":
          if not GLOBALS_BASE_ADDRESS[item_type][data_type] <= virtual_address < (GLOBALS_BASE_ADDRESS[item_type][data_type] + ranges[item_type]):
              error("Too many '%s' global temporal variables" % types[data_type])
        elif scope == "local": # local
          if not LOCALS_BASE_ADDRESS[item_type][data_type] <= virtual_address < (LOCALS_BASE_ADDRESS[item_type][data_type] + ranges[item_type]):
              error("Too many '%s' local temporal variables" % types[data_type])

    return virtual_address

  # Function to update counters
  # scope = 'global' or 'local'
  # item_type = 'variable' or 'temporal'
  def add_to_counter(self, data_type, scope, item_type, size_allocation=1, is_constant=False):
    if is_constant:
      self.__constants_counters[data_type] += size_allocation
    else:
      if data_type in [0,1,2]:
        if scope == "global":
          if item_type == "variable":
            self.__global_variable_counters[data_type] += size_allocation
          else: # temporal
            self.__global_temporal_counters[data_type] += size_allocation
        elif scope == "local": # local
          if item_type == "variable":
            self.__local_variable_counters[data_type] += size_allocation
          else: # temporal
            self.__local_temporal_counters[data_type] += size_allocation
      elif data_type in [3,5]:
        if scope == "global":
          self.__global_temporal_counters[data_type] += size_allocation
        elif scope == "local": # local
          self.__local_temporal_counters[data_type] += size_allocation

  # Function to get the next available address depending on the data_type, scope, and item_type
  def next_address(self, data_type, scope, item_type):
    if data_type in [0,1,2]: # int, float, char
      if scope == "global":
        if item_type == "variable":
          available_address = self.__global_variable_counters[data_type] 
        else: # temporal
          available_address = self.__global_temporal_counters[data_type] 
      elif scope == "local": # local
        if item_type == "variable":
          available_address = self.__local_variable_counters[data_type]
        else: # temporal
          available_address = self.__local_temporal_counters[data_type]
    elif data_type in [3, 5]: # bool or pointer
      if scope == "global":
        available_address = self.__global_temporal_counters[data_type] 
      elif scope == "local": # local
        available_address = self.__local_temporal_counters[data_type]

    # Return available address when valid
    return self.is_address_valid(available_address, data_type, scope, item_type)

  # Method to get the next available constant by data type
  def next_constant_address(self, data_type):
    # Get next available address
    available_address = self.__constants_counters[data_type]
    # Returns address when valid
    return self.is_address_valid(available_address, data_type, None, None, True)
    
  def new_variable(self, data_type, scope, item_type, size_allocation=1):
    '''Handles variable declaration for 'variable' and 'temporal\''''
    # Get next address if available
    available_address = self.next_address(data_type, scope, item_type)
    # Update corresponding counter
    self.add_to_counter(data_type, scope, item_type, size_allocation)
    # Return assigned virtual address
    return available_address

  # Method to add constant to constant directory depending on its data type
  def new_constant(self, data_type, data_value):
    # Get next address if available
    available_address = self.next_constant_address(data_type)
    # Add constant to directory of constants of respective data type
    self.__constants_directory[data_type][data_value] = available_address
    # Update corresponding counter
    self.add_to_counter(data_type, None, None, True, 1)
    # Return assigned virtual address
    return self.__constants_directory[data_type][data_value]

  # Method that returns the virtual address of an existing constant in constants directory
  def constant_exists(self, data_type, constant_value):
    return self.__constants_directory[data_type].get(constant_value, False)

  # Method to reset local addresses counters
  def reset_locals_counters(self):
    self.__local_variable_counters = {
      0: LOCALS_BASE_ADDRESS['variable'][0],
      1: LOCALS_BASE_ADDRESS['variable'][1],
      2: LOCALS_BASE_ADDRESS['variable'][2]
    }
    
    self.__local_temporal_counters = {
      0: LOCALS_BASE_ADDRESS['temporal'][0],
      1: LOCALS_BASE_ADDRESS['temporal'][1],
      2: LOCALS_BASE_ADDRESS['temporal'][2],
      3: LOCALS_BASE_ADDRESS['temporal'][3],
      5: LOCALS_BASE_ADDRESS['temporal'][5]
    }

  # Method to get the constants directory
  def get_constants_directory(self):
    return self.__constants_directory

# Function to get scope of range for an address
def get_scope_from_address(virtual_address):
  if virtual_address in range(GLOBALS_BASE_ADDRESS['variable'][0], LOCALS_BASE_ADDRESS['variable'][0]):
    return 'global'
  elif virtual_address in range(LOCALS_BASE_ADDRESS['variable'][0], CONSTANTS_BASE_ADDRESS[0]):
    return 'local'
  elif virtual_address in range(CONSTANTS_BASE_ADDRESS[0], OBJECTS_BASE_ADDRESS):
    return 'constant'
  elif virtual_address in range(OBJECTS_BASE_ADDRESS, OBJECTS_BASE_ADDRESS+ranges['instance']):
    return 'instance'
  else:
    error("Invalid address")

# Function to get data type from address
def get_type_from_address(virtual_address):
  if (virtual_address in range(GLOBALS_BASE_ADDRESS['variable'][0], GLOBALS_BASE_ADDRESS['variable'][1]) or
      virtual_address in range(GLOBALS_BASE_ADDRESS['temporal'][0], GLOBALS_BASE_ADDRESS['temporal'][1]) or
      virtual_address in range(LOCALS_BASE_ADDRESS['variable'][0], LOCALS_BASE_ADDRESS['variable'][1]) or
      virtual_address in range(LOCALS_BASE_ADDRESS['temporal'][0], LOCALS_BASE_ADDRESS['temporal'][1]) or
      virtual_address in range(CONSTANTS_BASE_ADDRESS[0], CONSTANTS_BASE_ADDRESS[1])):
    return 0
  elif (virtual_address in range(GLOBALS_BASE_ADDRESS['variable'][1], GLOBALS_BASE_ADDRESS['variable'][2]) or
        virtual_address in range(GLOBALS_BASE_ADDRESS['temporal'][1], GLOBALS_BASE_ADDRESS['temporal'][2]) or
        virtual_address in range(LOCALS_BASE_ADDRESS['variable'][1], LOCALS_BASE_ADDRESS['variable'][2]) or
        virtual_address in range(LOCALS_BASE_ADDRESS['temporal'][1], LOCALS_BASE_ADDRESS['temporal'][2]) or
        virtual_address in range(CONSTANTS_BASE_ADDRESS[1], CONSTANTS_BASE_ADDRESS[2])):
    return 1
  elif (virtual_address in range(GLOBALS_BASE_ADDRESS['variable'][2], GLOBALS_BASE_ADDRESS['temporal'][0]) or
        virtual_address in range(GLOBALS_BASE_ADDRESS['temporal'][2], GLOBALS_BASE_ADDRESS['temporal'][3]) or
        virtual_address in range(LOCALS_BASE_ADDRESS['variable'][2], LOCALS_BASE_ADDRESS['temporal'][0]) or
        virtual_address in range(LOCALS_BASE_ADDRESS['temporal'][2], LOCALS_BASE_ADDRESS['temporal'][3]) or
        virtual_address in range(CONSTANTS_BASE_ADDRESS[2], CONSTANTS_BASE_ADDRESS[4])):
    return 2
  elif (virtual_address in range(GLOBALS_BASE_ADDRESS['temporal'][3], GLOBALS_BASE_ADDRESS['temporal'][5]) or 
        virtual_address in range(LOCALS_BASE_ADDRESS['temporal'][3], LOCALS_BASE_ADDRESS['temporal'][5])):
    return 3
  elif virtual_address in range(CONSTANTS_BASE_ADDRESS[4], OBJECTS_BASE_ADDRESS):
    return 4
  elif (virtual_address in range(GLOBALS_BASE_ADDRESS['temporal'][5], LOCALS_BASE_ADDRESS['variable'][0]) or
        virtual_address in range(LOCALS_BASE_ADDRESS['temporal'][5], CONSTANTS_BASE_ADDRESS[0])):
    return 5