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
  5: 'pointer',
  6: 'instance'
}

# Defines the base addresses for global variables and temporals of each data type
GLOBALS_BASE_ADDRESS = {
    'variable': {
        0: 1000,            # Int global address (1,000 - 3,999)
        1: 4000,            # Float global address (5,000 - 7,999)
        2: 7000             # Char global address (9,000 - 11,999)
    },
    'temporal':  {
        0: 10000,            # Temporal global INT (4,000 - 4,999)
        1: 11000,            # Temporal global Float (8,000 - 8,999)
        2: 12000,            # Temporal global Char (12,000 - 12,999)
        3: 13000,            # Temporal global Bool (13,000 - 13,999)
        5: 14000             # Temporal global Pointer (14,000 - 14,999)
    },
    'instance': 15000             # Global instance (15,000 - 15,999)
}

# Defines the base addresses for local variables and temporals of each data type
LOCALS_BASE_ADDRESS = {
    'variable': {
        0: 16000,             # Int local address (16,000 - 18,999)
        1: 19000,             # Float local address (19,000 - 21,999)
        2: 22000              # Char local address (21,000 - 24,999)
    },
    'temporal': {
        0: 25000,             # Temporal local INT (25,000 - 25,999)
        1: 26000,             # Temporal local Float (26,000 - 26,999)
        2: 27000,             # Temporal local Char (27,000 - 27,999)
        3: 28000,             # Temporal local Bool (28,000 - 28,999)
        5: 29000              # Temporal local pointer (29,000 - 29, 999)
    },
    'instance': 30000              # Local instance (30,000 - 30,999)
}

# Defines the base addresses for constants of each data type
CONSTANTS_BASE_ADDRESS = {
    0: 31000,           # Int constant address (31,000 - 31,999)
    1: 32000,           # Float constant address (32,000 - 32,999)
    2: 33000,           # Char global address (33,000 - 33,999)
    4: 34000            # String global address (34,000 - 34,999)
}

# Defines class instances base
# Class instances address (35,000 - 35,999)
# OBJECTS_BASE_ADDRESS = 35000e