# Class used to 
from Classes.VarsTable import VarsTable
# from VarsTable import VarsTable

class Scope:
  # Constructor method
  def __init__(self, data_type):
    self.data_type = data_type
    self.vars_table = VarsTable()
    self.params_table = []
    self.initial_address = None
    self.number_of_local_variables = {
      "int": 0,
      "float": 0,
      "char": 0
    }
    self.number_of_temporals = {
      "int": 0,
      "float": 0,
      "char": 0,
      "bool":0
    }

  # Method to get the vars_table dictionary
  def get_table(self):
    return self.vars_table.get_vars_table()

  # Method to get the data type of the scope
  def get_data_type(self):
    return self.data_type

  # Method to get the number of temporal variables inside the scope
  def get_number_of_temporals(self, data_type, number_of_variables):
    if data_type == "int" or data_type == "float" or data_type == "char" or data_type == "bool":
      return self.number_of_temporals[data_type] 
  
  # Method to add 1 to the number of temporals inside the scope
  def add_temporal_count(self, data_type, number_of_variables):
    if data_type == "int" or data_type == "float" or data_type == "char" or data_type == "bool":
      self.number_of_temporals[data_type] += 1
  
  # Method to set the reference of the first quadruple of the scope
  def set_initial_address(self, initial_address):
    self.initial_address = initial_address
  
  # Method to get the reference of the first quadruple of the scope
  def get_initial_address(self):
    return self.initial_address

  # Method to get the number of parameters of the scope
  def get_number_of_parameters(self):
    return len(self.params_table)

  # Method to get the number of local variables inside the scope
  def get_total_number_of_local_variables(self):
    return self.vars_table.get_number_of_variables()

  # Method to get the number of local variables of a specific type inside the scope
  def get_number_of_local_variables_of_type(self, data_type):
    if data_type == "int" or data_type == "float" or data_type == "char":
      return self.number_of_local_variables[data_type]

  # Method to add 1 to the number of local variables inside the scope
  def add_local_variable_count(self, data_type):
    if data_type == "int" or data_type == "float" or data_type == "char":
      self.number_of_local_variables[data_type] += 1
  
  # Method to get the size of memory required by the scope
  def get_memory_size(self):
    # Adds the total coun of each type of variable
    return self.get_number_of_local_variables() + self.get_number_of_parameters() + self.get_number_of_temporals()
  
  # Method to add the parameter as a local variable 
  def add_parameter(self, var_id, var_data_type, address, isArray, m1):
    self.params_table.append(var_data_type)
    return self.vars_table.add_item(var_id, var_data_type, address, isArray, m1)

  # Method to add a local variable to the variable table of the scope
  def add_item(self, var_id, var_data_type, address, isArray, m1):
    return self.vars_table.add_item(var_id, var_data_type, address, isArray, m1)

  # Method to get a specific variable from the scope's variable table
  def search(self, var_id):
    return self.vars_table.search(var_id)

  # Delete the scope's variable table
  def remove_vars_table(self):
    del self.vars_table
  
  # Print scope's variable table
  def print(self):
    print(self.vars_table)
