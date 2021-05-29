def error(msg):
  print("Error: "+msg)
  exit()

# Defines range of the different types of adresses 
ranges = {
  'variable': 3000,
  'temporal': 1000,
  'constant': 1000,
  'instance':  1000
}

# Defines the data types handled by the language
types = {
  0: 'int',
  1: 'float',
  2: 'char',
  3: 'bool',
  4: 'string',
  5: 'pointer'
}

# Defines the base addresses for global variables and temporals of each data type
GLOBALS_BASE_ADDRESS = {
  'variable': {
    0: 1000,              # Int global address (1,000 - 3,999)
    1: 4000,            # Float global address (5,000 - 7,999)
    2: 7000             # Char global address (9,000 - 11,999)
  },
  'temporal':  {
    0: 10000,              # Temporal global INT (4,000 - 4,999)
    1: 11000,            # Temporal global Float (8,000 - 8,999)
    2: 12000,            # Temporal global Char (12,000 - 12,999)
    3: 13000            # Temporal global Bool (13,000 - 13,999)
  }
}

# Defines the base addresses for local variables and temporals of each data type
LOCALS_BASE_ADDRESS = {
  'variable': {
    0: 14000,             # Int local address (14,000 - 16,999)
    1: 17000,             # Float local address (18,000 - 20,999)
    2: 20000              # Char local address (22,000 - 24,999)
  },
  'temporal': {
    0: 23000,             # Temporal local INT (17,000 - 17,999)
    1: 24000,             # Temporal local Float (21,000 - 21,999)
    2: 25000,             # Temporal local Char (25,000 - 25,999)
    3: 26000              # Temporal local Bool (26,000 - 26,999)
    
  }
}

# Defines the base addresses for constants of each data type
CONSTANTS_BASE_ADDRESS =  {
                            0: 27000,           # Int constant address (27,000 - 28,999)
                            1: 28000,           # Float constant address (28,000 - 28,999)
                            2: 29000,           # Char global address (29,000 - 29,999)
                            4: 30000            # String global address (30,000 - 30,999)
                          }

# Defines class instances base 
OBJECTS_BASE_ADDRESS = 31000                   # Class instances address (31,000 - 31,999)