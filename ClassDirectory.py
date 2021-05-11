# from Table import Table
from SymbolTable import SymbolTable # Import Table class

class ClassDirectory:
  def __init__(self):
    self.dir = {}

  # Check if scope/class exists
  def class_exists(self, scope):
    return self.dir.get(scope, False)

  # Add a scope/class to the ClassDirectory
  def add_class(self, scope):
    if self.scope_exists(scope):
      return False
    else:
      self.dir[scope] = SymbolTable()
      return self.dir[scope]
    #   return True

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