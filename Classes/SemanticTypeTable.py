## Type_Operands equivalents
# 0 = INT
# 1 = FLOAT
# 2 = CHAR
# 3 = BOOL
# -1 = ERROR

class SemanticTypeTable:
    def __init__(self):
        self.semantic_type_table = (
            # INT as Left operand
            (#   +   -    *   /   >   <   ==   <>   &    |   !       <- Operators
                (0,  0,   0,  0,  3,  3,  3,   3,  -1,  -1, -1),   # <- INT as Right Operand
                (1,  1,   1,  1,  3,  3,  3,   3,  -1,  -1, -1),   # <- FLOAT as Right Operand
                (-1, -1, -1, -1, -1, -1, -1,  -1,  -1,  -1, -1)    # <- CHAR as Right Operand
            ),

            # FLOAT as Left operator
            (#   +   -    *   /   >   <   ==   <>   &    |   !       <- Operators
                (1,  1,   1,  1,  3,  3,  3,   3,  -1,  -1, -1),   # <- INT as Right Operand
                (1,  1,   1,  1,  3,  3,  3,   3,  -1,  -1, -1),   # <- FLOAT as Right Operand
                (-1, -1, -1, -1, -1, -1, -1,  -1,  -1,  -1, -1)    # <- CHAR as Right Operand
            ),

            # CHAR as Left operator
            (#    +   -   *   /   >   <   ==   <>   &    |   !       <- Operators
                (-1, -1, -1, -1, -1, -1, -1,  -1,  -1,  -1, -1),   # <- INT as Right Operand
                (-1, -1, -1, -1, -1, -1, -1,  -1,  -1,  -1, -1),   # <- FLOAT as Right Operand
                (-1, -1, -1, -1, -1, -1,  3,   3,  -1,  -1, -1)    # <- CHAR as Right Operand
            )
        )
    def transform_operand_type(self, operand_type):
        if(operand_type == 'int'):
            return 0
        elif(operand_type == 'float'):
            return 1
        elif(operand_type == 'char'):
            return 2
        else:
            return -1

    def transform_operator(self, operator):
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
        elif(operator == '='):
            return 6
        elif(operator == '<>'): 
            return 7
        elif(operator == 'AND'): # Operator not yet implemented 
            return 8
        elif(operator == 'OR'):  # Operator not yet implemented 
            return 9
        elif(operator == 'NOT'):  # Operator not yet implemented 
            return 10

    def transform_result_type(self, result):
        if(result == 0):
            return 'int'
        elif(result == 1):
            return 'float'   
        elif(result == 2):
            return 'char'
        elif(result == 3):
            return 'bool'
        elif(result == -1):
            return 'ERROR'  

    def result_type(self, left_operand_type, right_operand_type, operator):
        left_op = self.transform_operand_type(left_operand_type)
        right_op = self.transform_operand_type(right_operand_type)
        op = self.transform_operator(operator)

        if(left_op == -1 | right_op == -1):
            return 'ERROR'

        return self.transform_result_type(self.semantic_type_table[left_op][right_op][op]) 
