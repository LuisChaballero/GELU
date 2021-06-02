# GELU

GELU is an Object Oriented Programming language developed with the purpose of becoming a friendly and uncomplicated tool for anyone who is just starting to learn how to program. It provides mechanisms for the definition of classes, attributes, methods and single inheritance, as well as assignment, condition, loops, writes, among other basic statements and expressions.

---

## Install

```shell
$ git comand goes here
```

## Compile GELU

```how to compile```

## Run GELU

```how to run```

## Features

* Features
* Go
* Here

## Examples

Examples go here

```python
def example():
  print("This is an example")
```

### Contributors

* [Luis Caballero](https://github.com/luischaballero)
* [Gerardo Silva](https://github.com/gerardoasilva)

---

## Rubric

### Levels
| # | Level | Description|
| --- | --- | --- |
| 0 | Pésimo | No existe (no fue desarrollado) ni siquiera en compilación |
| 1 | Malo | Existe solo en compilación, no lograron ejecutar ese elemento |
| 2 | Regular | Existe y ejecuta pero de manera inconsistente (a veces funciona, a veces no, o requiere demasiadas restricciones) |
| 3 | Bueno | Existe y ejecuta el elemento aunque es ineficiente (desperdicio de memoria, mal tiempo de ejecución, etc.) |
| 4 | Muy bueno | Existe y ejecuta de manera eficiente |

### Dimensions
- [X] Expresiones aritméticas/Lógicas y Relacionales
- [ ] Estatutos de Interacción (Entrada / Salida)
- [X] Estatutos de Control de Flujo (Ciclos, Decisiones)
- [X] Elementos de cambio de contexto (Funciones/Métodos parametrizables)
- [X] Manejo de Elementos NO-Atómicos (Arreglos, Listas, ..) 
- [ ] Elementos propios del tipo de proyecto (Output gráfico, Móvil, Objetos, Otros, etc.)
- [ ] Documentación completa y bien presentada
- [ ] Descripción de estructuras de datos usadas durante la compilación
- [ ] Descripción del Mapa de Memoria en Ejecución
- [ ] Explicación de pruebas que comprueban funcionamiento
- [ ] Manual de usuario del lenguaje y Videos demostrativos.


## Testing

- [X] Factorial
- [X] Fibonacci iterative
- [X] Fibonacci recursive
- [X] Vector sort
- [ ] Vector find
- [ ] Matrix product
- [ ] OOP testing

---

## Bitácora

#### Primer avance - 9/04/2021

Project planning and requirements specifications. Defined the list of tokens, syntax diagrams as well as language grammar.

#### Segundo avance - 16/04/2021

The table of semantic considerations was defined. Implemented Variable Table as well as semantic considerations and precedence.

#### 19/04/2021

Implemented multiple variable declarations.

#### Tercer avance - 23/04/2021

Implemented intermediate code generation for basic expressions without considering parenthesis and relational operators. Started the local and global variable counter implementation.

#### 26/04/2021

Implemented Semantic Cube.

#### Cuarto avance - 01/05/2021

Intermediate code generation for non-linear statements IF and WHILE. FOR statement is still missing.  

#### 06/05/2021

Intermediate code generation for non-linear statement FOR.

#### Quinto avance  - 10/05/2021

Class Directory implementation. Modification of the grammar to add neural points for the class implementation. Adding attributes and methods to the Class Directory is still missing.

#### 11/05/2021

Additional functions implemented on Class Directory to add methods and attributes to a specific class. Adding parameters to the Variable Table is still missing.

#### 12/05/2021

Method parameters addition to Variable Table implemented.

#### Sexto avance - 15/05/2021

Modified implementation of Function Directory to allow addition parameters. Added neural points in function and method declarations for intermediate code generation. Modified the grammar, changed some Expressions for Exp. Function call quadruples still missing.

#### 16/05/2021

Modified the grammar to consider void method call. Implemented neural points to generate intermediate code for function calls. Function return type validation is still missing.

#### 21/05/2021

Implemented virtual addresses for temporals and added error detection when initializing an already existing variable.

#### 22/05/2021

Created the constant directory. Implemented Virtual Machine execution of arithmetic operations.

#### 23/05/2021

Modified the grammar to allow array and matrix declaration.

#### 24/05/2021

Added logic operations between expressions in semantic and their execution in Virtual Machine. Refactored the grammar to handle ambiguity and implemented negative constants.

#### 25/05/2021

Semantic Cube refactor, implemented a Utility file to keep the project’s relevant static information. Started Factor neural points implementation.

#### 26/05/2021

Refactor of Memory Helper class, created a new Memory class and splitted responsibilities among them. 

#### 27/05/2021

Modified Memory Helper to make stack overflow validations when assigning virtual addresses to variables in semantic. Created a new function to retrieve the data type and scope from a variable or constant depending on the range of their address in memory. Modified the memory structure and ranges to accept strings as constants and implemented their storage. Developed a routine in Virtual Machine to simplify the code for binary operation quadruples.

#### 28/05/2021

Array and matrix quadruples fixed, as well as the virtual memory address delegation. Modified the structure of the quadruples to contain their virtual address instead of the dimension lower limits.

#### 29/05/2021

Implemented pointer handling for matrix and array indexation. Added relational operator == in semantic. Developed a function in Virtual Machine to handle prints with multiple arguments as a single line write. Execution of assignment and cycles in Virtual Machine.

#### 30/05/2021

Implemented the execution of functions. Added error handling in Return quadruple. Still missing forced return in non-void functions.

#### 01/06/2021

Finished implementation of functions, arrays and matrices in execution. Tested functionality of functions and dimensional variables.