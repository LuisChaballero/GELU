
from Classes.FunctionDirectory import FunctionDirectory
from Helpers.Utilities import error
# from FunctionDirectory import FunctionDirectory  # Import Table class

class ClassDirectory:
  def __init__(self):
    self.__dir = {} # class_name : FunctionDirectory()

  # Gets the functionDirectory by class number
  def find_by_number(self, class_number):
    for c in self.__dir.values():
      if c.get_class_number() == class_number:
        return c
    return None

  # 
  def get_attribute_from_class_number(self, class_number, attribute_id):
    functionDir = self.find_by_number(class_number)
    if functionDir == None:
      error("Class with class number %s does not exist" % class_number)

    variable = functionDir.get_scope('class_globals').search(attribute_id)
    if not variable:
      error("Attribute %s does not exist on class number %s" % (attribute_id, class_number))
    
    return variable

  # Add a class to the ClassDirectory
  def add_class(self, class_name, class_number):
    if self.scope_exists(class_name): # Class already exists
      return False
    else:
      self.__dir[class_name] = FunctionDirectory(class_number)
      return self.__dir[class_name]

  # Check if a class or attributes_Table exists
  def scope_exists(self, scope):
    return self.__dir.get(scope, False)

  # Method to get the number of classes in class directory
  def count(self):
    return len(self.__dir)

  # Add an attributes Table to a class
  def add_attributes_Table(self, class_name, scope, data_type):
    if not self.scope_exists(class_name): # Class not found
      return False
    else:
      # self.__dir[class_name].add_scope(scope, data_type)
      return self.__dir[class_name].add_scope(scope, data_type) 
  
  # Add a method to a class
  def add_method(self, class_name, method_name, data_type):
    if self.__dir[class_name].scope_exists(method_name): # Method already exists in class
      return False
    else:
      return self.__dir[class_name].add_scope(method_name, data_type)
  
  ####### REMEMBER TO DO REFACTOR OF THIS FOLLOWING 2 METHODS ############ porque hacen lo mismo
  # Add an attribute of a class
  def add_attribute(self, class_name, vars_scope, var_id, data_type, address, dimensions):
    if not self.scope_exists(class_name):
      return False
    else:
      return self.__dir[class_name].add_item(vars_scope, var_id, data_type, address, dimensions)

  # Add variable in a method 
  def add_variable(self, class_name, method_name, var_id, data_type, address, dimensions):
    if not self.scope_exists(class_name): # Class not found in directory
      return False
    else:
      return self.__dir[class_name].add_item(method_name, var_id, data_type, address, dimensions)
  #########################################################################

    # Add variable in a method 
  def add_parameter(self, class_name, method_name, var_id, data_type, address, dimensions):
    if not self.scope_exists(class_name): # Class not found in directory
      return False
    else:
      return self.__dir[class_name].add_parameter(method_name, var_id, data_type, address, dimensions)

  # Delete object
  def remove(self):
    del self

  # Get scope's items
  def get_class(self, class_name):
    if not self.scope_exists(class_name):
      return False
    else:
      return self.__dir[class_name]

  def print(self):
    print(self.__dir)