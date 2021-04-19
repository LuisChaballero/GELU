# Class used to 
class Table:
  # Constructor method
  def __init__(self, data_type):
    self.table = {}
    self.data_type = data_type

  # Returns the dictionary of elements
  def get_table(self):
    return self.table
  

  def search(self, var_id):
    return self.table.get(var_id, False)

  def add_item(self, var_id, data_type):
    if not var_id in self.table:
      self.table[var_id] = data_type
      return True
    else:
      return False

  def print(self):
    print(self.table)
