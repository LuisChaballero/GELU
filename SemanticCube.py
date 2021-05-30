## Type_Operands equivalents
# 0 = INT
# 1 = FLOAT
# 2 = CHAR
# 3 = BOOL
# 4 = STTRING
# 5 = POINTER
# -1 = ERROR

semantic_cube = [
            # INT as Left operand
            [#   +    -   *   /   >   <   ==   <>   &    |       <- Operators
                [0,   0,  0,  0,  3,  3,  3,   3,  -1,  -1],   # <- INT as Right Operand
                [1,   1,  1,  1,  3,  3,  3,   3,  -1,  -1],   # <- FLOAT as Right Operand
                [-1, -1, -1, -1, -1, -1, -1,  -1,  -1,  -1],   # <- CHAR as Right Operand
                [-1, -1, -1, -1, -1, -1, -1,  -1,  -1,  -1]   # <- BOOL as Right Operand
            ],

            # FLOAT as Left operator
            [#   +   -    *   /   >   <   ==   <>   &    |       <- Operators
                [1,  1,   1,  1,  3,  3,  3,   3,  -1,  -1],   # <- INT as Right Operand
                [1,  1,   1,  1,  3,  3,  3,   3,  -1,  -1],   # <- FLOAT as Right Operand
                [-1, -1, -1, -1, -1, -1, -1,  -1,  -1,  -1],   # <- CHAR as Right Operand
                [-1, -1, -1, -1, -1, -1, -1,  -1,  -1,  -1]    # <- BOOL as Right Operand
            ],

            # CHAR as Left operator
            [#    +   -   *   /   >   <   ==   <>   &    |       <- Operators
                [-1, -1, -1, -1, -1, -1, -1,  -1,  -1,  -1],   # <- INT as Right Operand
                [-1, -1, -1, -1, -1, -1, -1,  -1,  -1,  -1],   # <- FLOAT as Right Operand
                [-1, -1, -1, -1, -1, -1,  3,   3,  -1,  -1],   # <- CHAR as Right Operand
                [-1, -1, -1, -1, -1, -1, -1,  -1,  -1,  -1]    # <- BOOL as Right Operand
            ],

            # BOOL as Left operator
            [#    +   -   *   /   >   <   ==   <>   &    |       <- Operators
                [-1, -1, -1, -1, -1, -1, -1,  -1,  -1,  -1],   # <- INT as Right Operand
                [-1, -1, -1, -1, -1, -1, -1,  -1,  -1,  -1],   # <- FLOAT as Right Operand
                [-1, -1, -1, -1, -1, -1, -1,  -1,  -1,  -1],   # <- CHAR as Right Operand
                [-1, -1, -1, -1, -1, -1,  3,   3,   3,   3]    # <- BOOL as Right Operand
            ]
        ]

def transform_operator(operator):
  if(operator == '+'):
      return 0
  elif(operator == '-'):
      return 1
  elif(operator == '*'):
      return 2
  elif(operator == '/'):
      return 3   
  elif(operator == '<'):
      return 4
  elif(operator == '>'):
      return 5
  elif(operator == '=='): # Operator not yet implemented 
      return 6
  elif(operator == '<>'): 
      return 7
  elif(operator == '&'): 
      return 8
  elif(operator == '|'): 
      return 9

def result_type(left_operand_type, right_operand_type, operator):
  op = transform_operator(operator)

  if(left_operand_type == -1 or right_operand_type == -1): # In case of type None
      return -1

  return semantic_cube[left_operand_type][right_operand_type][op]
