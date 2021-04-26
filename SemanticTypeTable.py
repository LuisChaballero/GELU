## Type_Operands equivalents
# 0 = INT
# 1 = FLOAT
# 2 = CHAR
# 3 = BOOL
# -1 = ERROR

class SemanticTypeTable:
    def __init__(self):
        self.semantic_cube = (
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

    def transform_operator(self, operator):
        if(operator == 'MAS'):
            return 0
        elif(operator == 'MENOS'):
            return 1
        elif(operator == 'POR'):
            return 2
        elif(operator == 'ENTRE'):
            return 3   
        elif(operator == 'MENOR_QUE'):
            return 4
        elif(operator == 'MAYOR_QUE'):
            return 5
        elif(operator == 'IGUAL'):
            return 6
        elif(operator == 'NO_IGUAL'): 
            return 7
        elif(operator == 'AND'): # Operador no implementado 
            return 8
        elif(operator == 'OR'): # Operador no implementado
            return 9
        elif(operator == 'NOT'): # Operador no implementado
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

        return self.transform_result_type(self.semantic_cube[left_op][right_op][op]) 
