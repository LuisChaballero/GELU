from Classes.Scope import Scope
# from Scope import Scope

class FunctionDirectory:
  def __init__(self):
    self.__dir = {} # function_name : Scope()

  # Check if scope exists
  def scope_exists(self, scope):
    return self.__dir.get(scope, False)

  # Check if var is in global or specific scope
  def var_exists(self, scope, var_id):
    if self.__dir[scope].search(var_id):
      return self.__dir[scope].search(var_id)
    else:
      return False

  # Add a scope to the FunctionDirectory
  def add_scope(self, scope, data_type):
    if self.scope_exists(scope):
      return False
    else:
      self.__dir[scope] = Scope(data_type)
      return True

  def add_parameter(self,scope, var_id, var_data_type, address, dimensions):
    if not self.scope_exists(scope):
      return False
    else:
      return self.__dir[scope].add_parameter(var_id, var_data_type, address, dimensions)

  # Add item to scope
  def add_item(self, scope, var_id, var_data_type, address, dimensions):
    if not self.scope_exists(scope):
      return False
    else:
      return self.__dir[scope].add_item(var_id, var_data_type, address, dimensions)

  # Delete object
  def remove(self):
    del self

  # Get scope's items
  def get_scope(self, scope):
    if not self.scope_exists(scope):
      return False
    else:
      return self.__dir[scope]

  def print(self):
    print(self.__dir)