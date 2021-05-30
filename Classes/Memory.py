from Utilities import error
# Class definition for memoryHandler to...
class Memory:
  
  # memoryDirectory constructor
  def __init__(self):
    self.__memory = {}

  # Method to add element into memory
  def push(self, virtual_address, value):
    self.__memory[virtual_address] = value

  # Method to retreive element value from address in memory
  def value(self, virtual_address):
    return self.__memory.get(virtual_address, None)
  
  # Methosd to validate if an address exists
  def address_exists(self, virtual_addres):
    return self.__memory.get(virtual_addres, False)