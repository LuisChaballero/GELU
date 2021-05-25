# Class used to 
class Variable:
  # Constructor method
  def __init__(self, data_type, address, dimensions):
    self.data_type = data_type
    self.address = address
    self.dimensions = dimensions # var->( 0, 0, 0), arr->(1, LimSup, 0), mat->(2, LimSup, LimSup)

  def get_data_type(self):
    return self.data_type

  def get_address(self):
    return self.address

  def get_dimensions(self):
    return self.dimensions

  def print(self):
    print("data_type: "+self.data_type) # +"   address: "+self.address)
