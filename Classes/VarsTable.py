
from Classes.Variable import Variable
# from Variable import Variable

# Class used to 
class VarsTable:
  # Constructor method
  def __init__(self):
    self.__table = {}

  # Returns the dictionary of elements
  def get_vars_table(self):
    return self.__table

  def get_number_of_variables(self):
    return len(self.__table)

  def search(self, id):
    """Searches for an id inside the table"""
    if not id in self.__table: 
      return False
    else:
      return self.__table[id]

  def add_item(self, id, data_type, address, dimensions):
    if not id in self.__table:
      self.__table[id] = Variable(data_type, address, dimensions)
      return True
    else:
      return False

  def print(self):
    print(self.__table)