from Table import Table # Import Table class

class SymbolTable:
  def __init__(self):
    self.dir = {}

  # Check if scope exists
  def scope_exists(self, scope):
    return self.dir.get(scope, False)

  # Check if var is in global or specific scope
  def var_exists(self, scope, var_id):
    if var_id in self.dir[scope]:
      return True
    elif var_id in self.dir['global']:
      return True
    else:
      return False

  # Add a scope to the SymbolTable
  def add_scope(self, scope, data_type):
    if self.scope_exists(scope):
      return False
    else:
      self.dir[scope] = Table(data_type)
      return True

  # Add scope to table
  # def add_scope(self, scope, var_id, data_type):

  # Add item to scope
  def add_item(self, scope, var_id, data_type):
    if not self.scope_exists(scope):
      return False
    else:
      return self.dir[scope].add_item(var_id, data_type)

  # Delete object
  def remove(self):
    del self

  # Get scope's items
  def get_scope(self, scope):
    if not self.scope_exists(scope):
      return False
    else:
      return self.dir[scope]

  def print(self):
    print(self.dir)