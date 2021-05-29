# Class used to 
from Classes.VarsTable import VarsTable
# from VarsTable import VarsTable

class Scope:
  # Constructor method
  def __init__(self, data_type):
    self.__data_type = data_type
    self.__vars_table = VarsTable()
    self.__params_table = []
    self.__initial_address = None
    self.__number_of_variables = [0,0,0]   # [int, float, char]
    self.__number_of_temporals = [0,0,0,0] # [int, float, char, bool]

  # Method to get the vars_table dictionary
  def get_table(self):
    return self.__vars_table.get_vars_table()

  # Method to get the data type of the scope
  def get_data_type(self):
    return self.__data_type

  # Method to get the number of temporal variables inside the scope
  def get_number_of_temporals(self, data_type, number_of_variables):
    if 0 <= data_type <= 3:
      return self.__number_of_temporals[data_type] 
  
  # Method to add 1 to the number of temporals inside the scope
  def add_temporal_count(self, data_type, number_of_variables):
    if 0 <= data_type <= 3:
      self.__number_of_temporals[data_type] += 1
  
  # Method to set the reference of the first quadruple of the scope
  def set_initial_address(self, initial_address):
    self.__initial_address = initial_address
  
  # Method to get the reference of the first quadruple of the scope
  def get_initial_address(self):
    return self.__initial_address

  def get_params_table(self):
    return self.__params_table

  # Method to get the number of parameters of the scope
  def get_number_of_parameters(self):
    return len(self.__params_table)

  # Method to add 1 to the number of local variables inside the scope
  def add_to_variable_count(self, data_type):
    if 0 <= data_type <= 2:
      self.__number_of_variables[data_type] += 1

  # Method to add 1 to the count of variables or temporals in the scope depending of the data type
  def add_to_count(self, data_type, variable_type, size_allocation=1):
    if variable_type == 'variable':
      self.__number_of_variables[data_type] += size_allocation
    elif variable_type == 'temporal':
      self.__number_of_temporals[data_type] += size_allocation
  
  # Method to add the parameter as a local variable 
  def add_parameter(self, var_id, var_data_type, address, dimensions):
    self.__params_table.append(var_data_type)
    return self.__vars_table.add_item(var_id, var_data_type, address, dimensions)

  # Method to add a local variable to the variable table of the scope
  def add_item(self, var_id, var_data_type, address, dimensions):
    return self.__vars_table.add_item(var_id, var_data_type, address, dimensions)

  # Method to get a specific variable from the scope's variable table
  def search(self, var_id):
    return self.__vars_table.search(var_id)

  # Delete the scope's variable table
  def remove_vars_table(self):
    del self.__vars_table
  
  # Print scope's variable table
  def print(self):
    print(self.__vars_table)
