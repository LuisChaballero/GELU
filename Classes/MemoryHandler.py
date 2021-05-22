# What does this class do

# Global Variable Address
GLOBAL_VARIABLE_INT_ADDRESS = 1000      # Int global address (1,000 - 3,999)
GLOBAL_TEMPORAL_INT_ADDRESS = 4000      # Temporal global INT (4,000 - 4,999)

GLOBAL_VARIABLE_FLOAT_ADDRESS = 5000    # Float global address (5,000 - 7,999)
GLOBAL_TEMPORAL_FLOAT_ADDRESS = 8000    # Temporal global Float (8,000 - 8,999)

GLOBAL_VARIABLE_CHAR_ADDRESS = 9000     # Char global address (9,000 - 11,999)
GLOBAL_TEMPORAL_CHAR_ADDRESS = 12000    # Temporal global Float (12,000 - 12,999)

GLOBAL_TEMPORAL_BOOL_ADDRESS = 13000    # Temporal global Bool (13,000 - 13,999)

# Local Variable Address
LOCAL_VARIABLE_INT_ADDRESS = 14000      # Int global address (14,000 - 16,999)
LOCAL_TEMPORAL_INT_ADDRESS = 17000      # Temporal global INT (17,000 - 17,999)

LOCAL_VARIABLE_FLOAT_ADDRESS = 18000    # Float global address (18,000 - 20,999)
LOCAL_TEMPORAL_FLOAT_ADDRESS = 21000   # Temporal global Float (21,000 - 21,999)

LOCAL_VARIABLE_CHAR_ADDRESS = 22000     # Char global address (22,000 - 24,999)
LOCAL_TEMPORAL_CHAR_ADDRESS = 25000     # Temporal global Float (25,000 - 25,999)

LOCAL_TEMPORAL_BOOL_ADDRESS = 26000     # Temporal global Bool (26,000 - 26,999)
CONSTANT_INT_ADDRESS = 27000            # Constant INT (27,000 - 27,999)
CONSTANT_FLOAT_ADDRESS = 28000          # Constant FLOAT (28,000 - 28,999)
CONSTANT_CHAR_ADDRESS = 29000           # Constant CHAR (29,000 - 29,999)

# Class memory space
CLASS_GLOBAL_VARIABLE_INT_ADDRESS = 30000      # Int global address (30,000 - 30,999)
CLASS_GLOBAL_VARIABLE_FLOAT_ADDRESS = 31000    # Float global address (31,000 - 31,999)
CLASS_GLOBAL_VARIABLE_CHAR_ADDRESS = 32000     # Char global address (32,000 - 32,999)


# Local Variable Address
CLASS_LOCAL_VARIABLE_INT_ADDRESS = 33000      # Int global address (33,000 - 33,999)
CLASS_LOCAL_TEMPORAL_INT_ADDRESS = 34000      # Temporal global INT (34,000 - 34,999)

CLASS_LOCAL_VARIABLE_FLOAT_ADDRESS = 35000    # Float global address (35,000 - 35,999)
CLASS_LOCAL_TEMPORAL_FLOAT_ADDRESS = 36000   # Temporal global Float (36,000 - 36,999)

CLASS_LOCAL_VARIABLE_CHAR_ADDRESS = 37000     # Char global address (37,000 - 37,999)
CLASS_LOCAL_TEMPORAL_CHAR_ADDRESS = 38000     # Temporal global Float (38,000 - 38,999)

CLASS_LOCAL_TEMPORAL_BOOL_ADDRESS = 39000     # Temporal global Bool (39,000 - 39,999)
CLASS_CONSTANT_INT_ADDRESS = 40000            # Constant INT (40,000 - 40,999)
CLASS_CONSTANT_FLOAT_ADDRESS = 41000          # Constant FLOAT (41,000 - 41,999)
CLASS_CONSTANT_CHAR_ADDRESS = 42000           # Constant CHAR (42,000 - 42,999)

# Class definition for memoryHandler to...
class memoryHandler:
  
  # memoryDirectory constructor
  def __init__(self):
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
    self.class_global_variable_counters = {
      'int': CLASS_GLOBAL_VARIABLE_INT_ADDRESS, 
      'float': CLASS_GLOBAL_VARIABLE_FLOAT_ADDRESS, 
      'char': CLASS_GLOBAL_VARIABLE_CHAR_ADDRESS
    }
    # self.class_global_temporal_counters = {
    #   'int': CLASS_GLOBAL_TEMPORAL_INT_ADDRESS, 
    #   'float': CLASS_GLOBAL_TEMPORAL_FLOAT_ADDRESS, 
    #   'char': CLASS_GLOBAL_TEMPORAL_CHAR_ADDRESS,
    #   'bool': CLASS_GLOBAL_TEMPORAL_BOOL_ADDRESS,
    # }
    self.class_local_variable_counters = {
      'int': CLASS_LOCAL_VARIABLE_INT_ADDRESS, 
      'float': CLASS_LOCAL_VARIABLE_FLOAT_ADDRESS, 
      'char': CLASS_LOCAL_VARIABLE_CHAR_ADDRESS
    }
    self.class_local_temporals = {
      'int': CLASS_LOCAL_TEMPORAL_INT_ADDRESS, 
      'float': CLASS_LOCAL_TEMPORAL_FLOAT_ADDRESS, 
      'char': CLASS_LOCAL_TEMPORAL_CHAR_ADDRESS,
      'bool': CLASS_LOCAL_TEMPORAL_BOOL_ADDRESS,
    }

    # self.locals = {}
    # self.constants = {}
    # self.global_variable_int_counter = GLOBAL_VARIABLE_INT_ADDRESS
    # self.global_temporal_int_counter = GLOBAL_TEMPORAL_INT_ADDRESS
    # self.global_variable_float_counter = GLOBAL_VARIABLE_FLOAT_ADDRESS
    # self.global_temporal_float_counter = GLOBAL_TEMPORAL_FLOAT_ADDRESS
    # self.global_variable_char_counter = GLOBAL_VARIABLE_CHAR_ADDRESS
    # self.global_temporal_char_counter = GLOBAL_TEMPORAL_CHAR_ADDRESS
    # self.global_temporal_bool_counter = GLOBAL_TEMPORAL_BOOL_ADDRESS
    # self.local_variable_int_counter = LOCAL_VARIABLE_INT_ADDRESS
    # self.local_temporal_int_counter = LOCAL_TEMPORAL_INT_ADDRESS
    # self.local_variable_float_counter = LOCAL_VARIABLE_FLOAT_ADDRESS
    # self.local_temporal_float_counter = LOCAL_TEMPORAL_FLOAT_ADDRESS
    # self.local_variable_char_counter = LOCAL_VARIABLE_CHAR_ADDRESS
    # self.local_temporal_char_counter = LOCAL_TEMPORAL_CHAR_ADDRESS
    # self.local_temporal_bool_counter = LOCAL_TEMPORAL_BOOL_ADDRESS
    # self.constant_int_counter = CONSTANT_INT_ADDRESS
    # self.constant_float_counter = CONSTANT_FLOAT_ADDRESS
    # self.constant_char_counter = CONSTANT_CHAR_ADDRESS
    # self.class_global_variable_int_counter = CLASS_GLOBAL_VARIABLE_INT_ADDRESS
    # self.class_global_temporal_int_counter = CLASS_GLOBAL_TEMPORAL_INT_ADDRESS
    # self.class_global_variable_float_counter = CLASS_GLOBAL_VARIABLE_FLOAT_ADDRESS
    # self.class_global_temporal_float_counter = CLASS_GLOBAL_TEMPORAL_FLOAT_ADDRESS
    # self.class_global_variable_char_counter = CLASS_GLOBAL_VARIABLE_CHAR_ADDRESS
    # self.class_global_temporal_char_counter = CLASS_GLOBAL_TEMPORAL_CHAR_ADDRESS
    # self.class_global_temporal_bool_counter = CLASS_GLOBAL_TEMPORAL_BOOL_ADDRESS
    # self.class_local_variable_int_counter = CLASS_LOCAL_VARIABLE_INT_ADDRESS
    # self.class_local_temporal_int_counter = CLASS_LOCAL_TEMPORAL_INT_ADDRESS
    # self.class_local_variable_float_counter = CLASS_LOCAL_VARIABLE_FLOAT_ADDRESS
    # self.class_local_temporal_float_counter = CLASS_LOCAL_TEMPORAL_FLOAT_ADDRESS
    # self.class_local_variable_char_counter = CLASS_LOCAL_VARIABLE_CHAR_ADDRESS
    # self.class_local_temporal_char_counter = CLASS_LOCAL_TEMPORAL_CHAR_ADDRESS
    # self.class_local_temporal_bool_counter = CLASS_LOCAL_TEMPORAL_BOOL_ADDRESS
    # self.directory = {}

  # Initialize counters for memoryDirectory
  # def reset_all_memory(self):
  #   self.global_variable_int_counter = GLOBAL_VARIABLE_INT_ADDRESS
  #   self.global_temporal_int_counter = GLOBAL_TEMPORAL_INT_ADDRESS
  #   self.global_variable_float_counter = GLOBAL_VARIABLE_FLOAT_ADDRESS
  #   self.global_temporal_float_counter = GLOBAL_TEMPORAL_FLOAT_ADDRESS
  #   self.global_variable_char_counter = GLOBAL_VARIABLE_CHAR_ADDRESS
  #   self.global_temporal_char_counter = GLOBAL_TEMPORAL_CHAR_ADDRESS
  #   self.global_temporal_bool_counter = GLOBAL_TEMPORAL_BOOL_ADDRESS
  #   self.local_variable_int_counter = LOCAL_VARIABLE_INT_ADDRESS
  #   self.local_temporal_int_counter = LOCAL_TEMPORAL_INT_ADDRESS
  #   self.local_variable_float_counter = LOCAL_VARIABLE_FLOAT_ADDRESS
  #   self.local_temporal_float_counter = LOCAL_TEMPORAL_FLOAT_ADDRESS
  #   self.local_variable_char_counter = LOCAL_VARIABLE_CHAR_ADDRESS
  #   self.local_temporal_char_counter = LOCAL_TEMPORAL_CHAR_ADDRESS
  #   self.local_temporal_bool_counter = LOCAL_TEMPORAL_BOOL_ADDRESS
  #   self.constant_int_counter = CONSTANT_INT_ADDRESS
  #   self.constant_float_counter = CONSTANT_FLOAT_ADDRESS
  #   self.constant_char_counter = CONSTANT_CHAR_ADDRESS
  #   self.class_global_variable_int_counter = CLASS_GLOBAL_VARIABLE_INT_ADDRESS
  #   self.class_global_temporal_int_counter = CLASS_GLOBAL_TEMPORAL_INT_ADDRESS
  #   self.class_global_variable_float_counter = CLASS_GLOBAL_VARIABLE_FLOAT_ADDRESS
  #   self.class_global_temporal_float_counter = CLASS_GLOBAL_TEMPORAL_FLOAT_ADDRESS
  #   self.class_global_variable_char_counter = CLASS_GLOBAL_VARIABLE_CHAR_ADDRESS
  #   self.class_global_temporal_char_counter = CLASS_GLOBAL_TEMPORAL_CHAR_ADDRESS
  #   self.class_global_temporal_bool_counter = CLASS_GLOBAL_TEMPORAL_BOOL_ADDRESS
  #   self.class_local_variable_int_counter = CLASS_LOCAL_VARIABLE_INT_ADDRESS
  #   self.class_local_temporal_int_counter = CLASS_LOCAL_TEMPORAL_INT_ADDRESS
  #   self.class_local_variable_float_counter = CLASS_LOCAL_VARIABLE_FLOAT_ADDRESS
  #   self.class_local_temporal_float_counter = CLASS_LOCAL_TEMPORAL_FLOAT_ADDRESS
  #   self.class_local_variable_char_counter = CLASS_LOCAL_VARIABLE_CHAR_ADDRESS
  #   self.class_local_temporal_char_counter = CLASS_LOCAL_TEMPORAL_CHAR_ADDRESS
  #   self.class_local_temporal_bool_counter = CLASS_LOCAL_TEMPORAL_BOOL_ADDRESS
  #   self.directory = {}
    
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
  

