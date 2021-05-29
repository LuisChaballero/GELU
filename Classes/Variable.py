# Class used to 
class Variable:
  # Constructor method
  def __init__(self, data_type, address, dimensions):
    self.__data_type = data_type
    self.__address = address
    self.__dimensions = dimensions # var->( 0, 0, 0), arr->(1, LimSup, 0), mat->(2, LimSup, LimSup)

  def get_data_type(self):
    return self.__data_type

  def get_address(self):
    return self.__address

  def get_dimensions(self):
    return self.__dimensions
