
from Classes.Scope import Scope
# from Scope import Scope

class FunctionDirectory:
  def __init__(self):
    self.dir = {} # function_name : Scope()

  # Check if scope exists
  def scope_exists(self, scope):
    return self.dir.get(scope, False)

  # Check if var is in global or specific scope
  def var_exists(self, scope, var_id):
    if self.dir[scope].search(var_id):
      return self.dir[scope].search(var_id)
    else:
      return False
    # if var_id in self.dir[scope]:
    #   return True
    # elif var_id in self.dir['global']:
    #   return True
    # else:
    #   return False

  # Add a scope to the FunctionDirectory
  def add_scope(self, scope, data_type):
    if self.scope_exists(scope):
      return False
    else:
      self.dir[scope] = Scope(data_type)
      return True

  def add_parameter(self,scope, var_id, var_data_type, address, isArray, m1):
    if not self.scope_exists(scope):
      return False
    else:
      return self.dir[scope].add_parameter(var_id, var_data_type, address, isArray, m1)

  # Add item to scope
  def add_item(self, scope, var_id, var_data_type, address, isArray, m1):
    if not self.scope_exists(scope):
      return False
    else:
      return self.dir[scope].add_item(var_id, var_data_type, address, isArray, m1)

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