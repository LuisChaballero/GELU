# Class used to 
class Variable:
  # Constructor method
  def __init__(self, data_type, address, isArray, m1):
    self.data_type = data_type
    self.address = address
    self.isArray = isArray
    self.m1 = m1

  def get_data_type(self):
    return self.data_type

  def get_address(self):
    return self.address

  def print(self):
    print("data_type: "+self.data_type) # +"   address: "+self.address)
