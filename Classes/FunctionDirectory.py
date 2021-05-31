from Classes.Scope import Scope
# from Scope import Scope

class FunctionDirectory:
  def __init__(self):
    self.__dir = {} # function_name : Scope()

  def scope_exists(self, scope):
    """Checks if scope exists
    
        Parameters
        ----------
        scope : str
            The name of the scope to search for

        Returns
        -------
        Scope or bool
          The Scope or False"""
    return self.__dir.get(scope, False)

  def var_exists(self, scope, var_id):
    """Checks if variable is in a specific scope
        
        Parameters
        ----------
        scope : str
            The name of the scope to search on
        var_id :
            The name of the variable to search for
        
        Returns
        -------
        Variable or bool
          The Variable or False"""
    if self.__dir[scope].search(var_id):
      return self.__dir[scope].search(var_id)
    else:
      return False

  def add_scope(self, scope, data_type):
    """Adds a scope to the FunctionDirectory"""
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

  def add_item(self, scope, var_id, var_data_type, address, dimensions):
    """Adds item to scope"""
    if not self.scope_exists(scope):
      return False
    else:
      return self.__dir[scope].add_item(var_id, var_data_type, address, dimensions)

  def remove(self):
    """Deletes the object"""
    del self

  def get_scope(self, scope):
    """Gets scope from function directory"""
    if not self.scope_exists(scope):
      return False
    else:
      return self.__dir[scope]