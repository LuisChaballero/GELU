
from Classes.FunctionDirectory import FunctionDirectory
# from FunctionDirectory import FunctionDirectory  # Import Table class

class ClassDirectory:
  def __init__(self):
    self.dir = {} # class_name : FunctionDirectory()

  # Add a class to the ClassDirectory
  def add_class(self, class_name):
    if self.scope_exists(class_name): # Class already exists
      return False
    else:
      self.dir[class_name] = FunctionDirectory()
      return self.dir[class_name]

  # Check if a class or attributes_Table exists
  def scope_exists(self, scope):
    return self.dir.get(scope, False)

  # Add an attributes Table to a class
  def add_attributes_Table(self, class_name, scope, data_type):
    if not self.scope_exists(class_name): # Class not found
      return False
    else:
      # self.dir[class_name].add_scope(scope, data_type)
      return self.dir[class_name].add_scope(scope, data_type) 
  
  # Add a method to a class
  def add_method(self, class_name, method_name, data_type):
    if self.dir[class_name].scope_exists(method_name): # Method already exists in class
      return False
    else:
      return self.dir[class_name].add_scope(method_name, data_type)
  
  ####### REMEMBER TO DO REFACTOR OF THIS FOLLOWING 2 METHODS ############ porque hacen lo mismo
  # Add an attribute of a class
  def add_attribute(self, class_name, vars_scope, var_id, data_type, address, dimensions):
    if not self.scope_exists(class_name):
      return False
    else:
      return self.dir[class_name].add_item(vars_scope, var_id, data_type, address, dimensions)

  # Add variable in a method 
  def add_variable(self, class_name, method_name, var_id, data_type, address, dimensions):
    if not self.scope_exists(class_name): # Class not found in directory
      return False
    else:
      return self.dir[class_name].add_item(method_name, var_id, data_type, address, dimensions)
  #########################################################################

    # Add variable in a method 
  def add_parameter(self, class_name, method_name, var_id, data_type, address, dimensions):
    if not self.scope_exists(class_name): # Class not found in directory
      return False
    else:
      return self.dir[class_name].add_parameter(method_name, var_id, data_type, address, dimensions)

  # Delete object
  def remove(self):
    del self

  # Get scope's items
  def get_class(self, class_name):
    if not self.scope_exists(class_name):
      return False
    else:
      return self.dir[class_name]

  def print(self):
    print(self.dir)