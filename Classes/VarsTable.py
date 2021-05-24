
from Classes.Variable import Variable
# from Variable import Variable

# Class used to 
class VarsTable:
  # Constructor method
  def __init__(self):
    self.table = {}

  # Returns the dictionary of elements
  def get_vars_table(self):
    return self.table

  def get_number_of_variables(self):
    return len(self.table)

  def search(self, id):
    if not id in self.table: 
      return False
    else:
      return self.table[id]
      # return self.table[id].get_data_type()
    # return self.table.get(id, False)

  def add_item(self, id, data_type, address, isArray, m1):
    if not id in self.table:
      self.table[id] = Variable(data_type, address, isArray, m1)
      return True
    else:
      return False

  def print(self):
    print(self.table)