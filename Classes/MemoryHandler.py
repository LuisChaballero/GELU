# What does this class do

# Global Variable Address
GLOBAL_VARIABLE_INT_ADDRESS = 1000              # Int global address (1,000 - 3,999)
GLOBAL_TEMPORAL_INT_ADDRESS = 4000              # Temporal global INT (4,000 - 4,999)

GLOBAL_VARIABLE_FLOAT_ADDRESS = 5000            # Float global address (5,000 - 7,999)
GLOBAL_TEMPORAL_FLOAT_ADDRESS = 8000            # Temporal global Float (8,000 - 8,999)

GLOBAL_VARIABLE_CHAR_ADDRESS = 9000             # Char global address (9,000 - 11,999)
GLOBAL_TEMPORAL_CHAR_ADDRESS = 12000            # Temporal global Float (12,000 - 12,999)

GLOBAL_TEMPORAL_BOOL_ADDRESS = 13000            # Temporal global Bool (13,000 - 13,999)

# Local Variable Address        
LOCAL_VARIABLE_INT_ADDRESS = 14000              # Int global address (14,000 - 16,999)
LOCAL_TEMPORAL_INT_ADDRESS = 17000              # Temporal global INT (17,000 - 17,999)

LOCAL_VARIABLE_FLOAT_ADDRESS = 18000            # Float global address (18,000 - 20,999)
LOCAL_TEMPORAL_FLOAT_ADDRESS = 21000            # Temporal global Float (21,000 - 21,999)

LOCAL_VARIABLE_CHAR_ADDRESS = 22000             # Char global address (22,000 - 24,999)
LOCAL_TEMPORAL_CHAR_ADDRESS = 25000             # Temporal global Float (25,000 - 25,999)

LOCAL_TEMPORAL_BOOL_ADDRESS = 26000             # Temporal global Bool (26,000 - 26,999)

# Class Global Variable Address
CONSTANT_INT_ADDRESS = 27000       # Int global address (27,000 - 28,999)
CONSTANT_FLOAT_ADDRESS = 28000     # Float global address (28,000 - 28,999)
CONSTANT_CHAR_ADDRESS = 29000      # Char global address (29,000 - 29,999)

# Class Instance
CLASS_INSTANCE_ADDRESS = 30000                   # Class instances (30,000 - 30,999)

# Class definition for memoryHandler to...
class MemoryHandler:
  
  # memoryDirectory constructor
  def __init__(self):
    self.memory = {}
    self.global_variable_counters = {
      'int': GLOBAL_VARIABLE_INT_ADDRESS, 
      'float': GLOBAL_VARIABLE_FLOAT_ADDRESS, 
      'char': GLOBAL_VARIABLE_CHAR_ADDRESS
    }

    self.global_temporal_counters = {
      'int': GLOBAL_TEMPORAL_INT_ADDRESS, 
      'float': GLOBAL_TEMPORAL_FLOAT_ADDRESS, 
      'char': GLOBAL_TEMPORAL_CHAR_ADDRESS,
      'bool': GLOBAL_TEMPORAL_BOOL_ADDRESS
    }
    
    self.local_variable_counters = {
      'int': LOCAL_VARIABLE_INT_ADDRESS, 
      'float': LOCAL_VARIABLE_FLOAT_ADDRESS, 
      'char': LOCAL_VARIABLE_CHAR_ADDRESS
    }
    
    self.local_temporal_counters = {
      'int': LOCAL_TEMPORAL_INT_ADDRESS, 
      'float': LOCAL_TEMPORAL_FLOAT_ADDRESS, 
      'char': LOCAL_TEMPORAL_CHAR_ADDRESS,
      'bool': LOCAL_TEMPORAL_BOOL_ADDRESS
    }

    self.constant_int_counters = CONSTANT_INT_ADDRESS
    self.constant_int_directory = {}

    self.constant_float_counters = CONSTANT_FLOAT_ADDRESS
    self.constant_float_directory = {}

    self.constant_char_counters = CONSTANT_CHAR_ADDRESS
    self.constant_char_directory = {}


# -------- VIRTUAL ADDRESS HANDLING ---------

  # Function to update NON-CLASS counters 
  # scope = 'global' or 'local'
  # item_type = 'variable' or 'temporal'
  def add_item(self, data_type, scope, item_type):
    if data_type == "int" or data_type == "float" or data_type == "char":
      if scope == "global":
        if item_type == "variable":
          self.global_variable_counters[data_type] += 1
        else: # temporal
          self.global_temporal_counters[data_type] += 1
      else: # local
        if item_type == "variable":
          self.local_variable_counters[data_type] += 1
        else: # temporal
          self.local_temporal_counters[data_type] += 1
    elif data_type == "bool":
      if scope == "global":
        self.global_temporal_counters[data_type] += 1
      else: # local
        self.local_temporal_counters[data_type] += 1

  def get_address(self, data_type, scope, item_type):
    if data_type == "int" or data_type == "float" or data_type == "char":
      if scope == "global":
        if item_type == "variable":
          return self.global_variable_counters[data_type]
        else: # temporal
          return self.global_temporal_counters[data_type]
      else: # local
        if item_type == "variable":
          return self.local_variable_counters[data_type]
        else: # temporal
          return self.local_temporal_counters[data_type]
    elif data_type == "bool":
      if scope == "global":
        return self.global_temporal_counters[data_type]
      else: # local
        return self.local_temporal_counters[data_type]

  # Function to update CLASS counters 
  # scope = 'global' or 'local'
  # item_type = 'variable' or 'temporal'
  def add_class_item(self, data_type, scope, item_type):
    if data_type == "int" or data_type == "float" or data_type == "char":
      if scope == "global":
        self.class_global_variable_counters[data_type] += 1
      else: # local
        if item_type == "variable":
          self.class_local_variable_counters[data_type] += 1
        else: # temporal
          self.class_local_temporal_counters[data_type] += 1
    elif data_type == "bool":
      self.class_local_temporal_counters[data_type] += 1

  def get_class_address(self, data_type, scope, item_type):
    if data_type == "int" or data_type == "float" or data_type == "char":
      if scope == "global":
        if item_type == "variable":
          return self.class_global_variable_counters[data_type]
        else: # temporal
          return self.class_global_temporal_counters[data_type]
      else: # local
        if item_type == "variable":
          return self.class_local_variable_counters[data_type]
        else: # temporal
          return self.class_local_temporal_counters[data_type]
    elif data_type == "bool":
      if scope == "global":
        return self.class_global_temporal_counters[data_type]
      else: # local
        return self.class_local_temporal_counters[data_type]
 

  def add_constant_item(self, data_type, data_value):
    if data_type == "int":
      self.constant_int_directory[data_value] = self.constant_int_counters
      self.push(self.constant_int_counters, data_value) # Add constant to real memory 
      self.constant_int_counters += 1
      return self.constant_int_directory[data_value]

    elif data_type == "float":
      self.constant_float_directory[data_value] = self.constant_float_counters
      self.push(self.constant_float_counters, data_value) # Add constant to real memory 
      self.constant_float_counters += 1
      return self.constant_float_directory[data_value]

    elif data_type == "char":
      self.constant_char_directory[data_value] = self.constant_char_counters
      self.push(self.constant_char_counters, data_value) # Add constant to real memory 
      self.constant_char_counters += 1     
      return self.constant_char_directory[data_value]

  def get_constant_address(self, data_type, constant_value):

    if data_type == "int": 
      # return self.constant_int_directory.get(data_value, False)
      constant_int_address = self.constant_int_directory.get(constant_value, False)
      if constant_int_address: # Constant is in directory
        return constant_int_address
      else: # Put constant in directory
        return self.add_constant_item(data_type, constant_value)
      
    elif data_type == "float":
      # return self.constant_float_directory.get(data_value, False)
      constant_float_address = self.constant_float_directory.get(constant_value, False)
      if constant_float_address:  # Constant is in directory
        return constant_float_address
      else: # Put constant in directory
        return self.add_constant_item(data_type, constant_value)

    elif data_type == "char":
      # return self.constant_char_directory.get(data_value, False)
      constant_char_address = self.constant_char_directory.get(constant_value, False)
      if constant_char_address: # Constant is in directory
        return constant_char_address
      else: # Put constant in directory
        return self.add_constant_item(data_type, constant_value)

# -------- MEMORY HANDLING ---------

  # Method to add element into memory
  def push(self, virtual_address, value):
    self.memory[virtual_address] = value

  # Method to get retreive element from memory
  def value(self, virtual_address):
    if self.memory.get(virtual_address, False):
      return self.memory[virtual_address]
    else:
      return False
