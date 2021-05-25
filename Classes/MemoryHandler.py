# Defines range of the different types of adresses 
ranges = {
  'variable': 3000,
  'temporal': 1000,
  'constant': 1000,
  'class': 1000
}

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
      0: GLOBAL_VARIABLE_INT_ADDRESS, 
      1: GLOBAL_VARIABLE_FLOAT_ADDRESS, 
      2: GLOBAL_VARIABLE_CHAR_ADDRESS
    }

    self.global_temporal_counters = {
      0: GLOBAL_TEMPORAL_INT_ADDRESS, 
      1: GLOBAL_TEMPORAL_FLOAT_ADDRESS, 
      2: GLOBAL_TEMPORAL_CHAR_ADDRESS,
      3: GLOBAL_TEMPORAL_BOOL_ADDRESS
    }
    
    self.local_variable_counters = {
      0: LOCAL_VARIABLE_INT_ADDRESS, 
      1: LOCAL_VARIABLE_FLOAT_ADDRESS, 
      2: LOCAL_VARIABLE_CHAR_ADDRESS
    }
    
    self.local_temporal_counters = {
      0: LOCAL_TEMPORAL_INT_ADDRESS, 
      1: LOCAL_TEMPORAL_FLOAT_ADDRESS, 
      2: LOCAL_TEMPORAL_CHAR_ADDRESS,
      3: LOCAL_TEMPORAL_BOOL_ADDRESS
    }

    # Directory to store constants of all types 
    self.constants_directory = [{}, {}, {}] # [int{}, float{}, char{}]
    self.constants_counters = [CONSTANT_INT_ADDRESS, CONSTANT_FLOAT_ADDRESS, CONSTANT_CHAR_ADDRESS]

# -------- VIRTUAL ADDRESS HANDLING ---------

  # Function to update NON-CLASS counters 
  # scope = 'global' or 'local'
  # item_type = 'variable' or 'temporal'
  def add_item(self, data_type, scope, item_type):
    if 0 <= data_type <= 2:
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
    elif data_type == 3:
      if scope == "global":
        self.global_temporal_counters[data_type] += 1
      else: # local
        self.local_temporal_counters[data_type] += 1

  # Function to get the next available address depending on the data_type, scope, and item_type
  def get_address(self, data_type, scope, item_type):
    if 0 <= data_type <= 2:
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
    elif data_type == 3:
      if scope == "global":
        return self.global_temporal_counters[data_type]
      else: # local
        return self.local_temporal_counters[data_type]

  # 
  def add_constant_item(self, data_type, data_value):
    # Check if there is an available address for data_type constants
    if self.constants_counters[data_type] < self.constants_counters[data_type] + ranges['constant']:
      # Add data_value: virtual_address to directory
      self.constants_directory[data_type][data_value] = self.constants_counters[data_type]
      self.push(self.constants_counters[data_type], data_value)
      # Update address count
      self.constants_counters[data_type] += 1

      return self.constants_directory[data_type][data_value]

    else: # 
      print("Too many constants of type")
      exit()

  def get_constant_address(self, data_type, constant_value):
    constant_address = self.constants_directory[data_type].get(constant_value, False)
    
    # Does not exist
    if constant_address == False:
      return self.add_constant_item(data_type, constant_value)
    else:
      return constant_address

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