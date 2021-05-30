def error(msg):
  print("Error: "+msg)
  exit()

# Defines range of the different types of adresses 
ranges = {
  'variable': 3000,
  'temporal': 1000,
  'constant': 1000,
  'instance': 1000
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
    3: 13000,            # Temporal global Bool (13,000 - 13,999)
    5: 14000            # Temporal global Pointer (14,000 - 14,999)
  }
}

# Defines the base addresses for local variables and temporals of each data type
LOCALS_BASE_ADDRESS = {
  'variable': {
    0: 15000,             # Int local address (15,000 - 17,999)
    1: 18000,             # Float local address (18,000 - 20,999)
    2: 21000              # Char local address (21,000 - 23,999)
  },
  'temporal': {
    0: 24000,             # Temporal local INT (24,000 - 24,999)
    1: 25000,             # Temporal local Float (25,000 - 25,999)
    2: 26000,             # Temporal local Char (26,000 - 26,999)
    3: 27000,             # Temporal local Bool (27,000 - 27,999)
    5: 28000              # Temporal local pointer (28,000 - 28, 999)
  }
}

# Defines the base addresses for constants of each data type
CONSTANTS_BASE_ADDRESS =  {
                            0: 29000,           # Int constant address (29,000 - 29,999)
                            1: 30000,           # Float constant address (30,000 - 30,999)
                            2: 31000,           # Char global address (31,000 - 31,999)
                            4: 32000            # String global address (32,000 - 32,999)
                          }

# Defines class instances base 
OBJECTS_BASE_ADDRESS = 33000                   # Class instances address (33,000 - 33,999)