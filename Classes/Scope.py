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
    self.number_of_temporals = 0

  # Returns the dictionary of elements
  def get_table(self):
    return self.vars_table.get_vars_table()

  def get_data_type(self):
    return self.data_type

  def set_number_of_temporals(self, number_of_temporals):
    self.number_of_temporals = number_of_temporals

  def get_number_of_temporals(self):
    return self.number_of_temporals
  
  def set_initial_address(self, initial_address):
    self.initial_address = initial_address
  
  def get_initial_address(self):
    return self.initial_address

  def get_number_of_parameters(self):
    return len(self.params_table)
  
  def add_parameter(self, var_id, var_data_type, address):
    self.params_table.append(var_data_type)
    return self.vars_table.add_item(var_id, var_data_type, address)

  def add_item(self, var_id, var_data_type, address):
    return self.vars_table.add_item(var_id, var_data_type, address)

  def search(self, var_id):
    return self.vars_table.search(var_id)

  # Delete object
  def remove_vars_table(self):
    del self.vars_table

  def print(self):
    print(self.vars_table)
    # self.vars_table.print()
    # print(self.vars_table)
    # print("VarTable:"+self.vars_table+", data_type:"+self.data_type+", parameters"+self.params_table)
