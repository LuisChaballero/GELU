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
- [ ] Expresiones aritméticas/Lógicas y Relacionales
- [ ] Estatutos de Interacción (Entrada / Salida)
- [ ] Estatutos de Control de Flujo (Ciclos, Decisiones)
- [ ] Elementos de cambio de contexto (Funciones/Métodos parametrizables)
- [ ] Manejo de Elementos NO-Atómicos (Arreglos, Listas, ..) 
- [ ] Elementos propios del tipo de proyecto (Output gráfico, Móvil, Objetos, Otros, etc.)
- [ ] Documentación completa y bien presentada
- [ ] Descripción de estructuras de datos usadas durante la compilación
- [ ] Descripción del Mapa de Memoria en Ejecución
- [ ] Explicación de pruebas que comprueban funcionamiento
- [ ] Manual de usuario del lenguaje y Videos demostrativos.


## Testing

- [ ] Factorial
- [ ] Fibonacci iterative
- [ ] Fibonacci recursive
- [ ] Vector sort
- [ ] Vector find
- [ ] Matrix product
- [ ] OOP testing

---

## Bitácora

#### Primer avance - 9/04/2021

Se llevó a cabo el planteamiento del proyecto y sus requerimientos, se definió la lista de tokens, los diagramas de sintaxis y la gramática del lenguaje.

#### Segundo avance - 16/04/2021

Se agrego la creación de tablas de símbolos y de variables. También se definió la tabla de consideraciones semánticas y las precedencia de los operadores.

#### 19/04/2021

Se implemento la declaración de variables multiples 

#### Tercer avance - 23/04/2021

Se implemento la generación del código intermedio para las expresiones básicas (Sin considerar paréntesis y operadores de comparación). Se agrego una implementación simple para los valores temporales sin utilizar el manejo de memoria.

#### 26/04/2021

Se implemento el cubo semántico de tipos.

#### Cuarto avance - 01/05/2021

Se implementaron los cuádruplos para los estatutos no lineales IF y WHILE. Queda pendiente el estatuto FOR y creación de cuádruplos para constantes.    

#### 06/05/2021

Se implemento el cuádruplo para el estatuto no lineal FOR.

#### Quinto avance  - 10/05/2021

Se creó el directorio para clases. Se modificó parte de la gramática para los puntos neurálgicos de la implementación de clases. Queda pendiente el añadir los atributos y métodos de cada clase al directorio de clases.

#### 11/05/2021

Se implementaron funciones adicionales en ClassDirectory. Se implementó la añadidura de los métodos y atributos de una clase al directorio de clases. Falta la añadidura de los parámetros de los métodos de las clases.

#### 12/05/2021

Se implementó la añadidura de los parámetros a los métodos de clases. 

#### Sexto avance - 15/05/2021

Se modificaron las clases de la implementación del directorio de funciones para manejar el guardado de parámetros, la dirección de inicialización. Se implementaron los cuádruplos en la declaración de funciones y métodos. Se modificó parte de la gramática en las expresiones (Algunos tenían que ser Exp en ves de Expresion). Queda pendiente los cuádruplos de las llamadas a función

#### 16/05/2021

Se modificó la gramática para considerar la llamada a métodos void de una clase. Se implementaron los cuádruplos de llamadas a funciones. Queda pendiente validar el tipo de retorno en las funciones

#### 21/05/2021

Se creo la clase de memoryHandler y se implementaron las direcciones virtuales para los operandos 

#### 21/05/2021

Se implementaron las direcciones virtuales para los temporales y se agrego la detección de errores cuando se inicializa una variable que ya existe. 

#### 22/05/2021

Se implemento el directorio de constantes y la ejecución de las operaciones aritméticas en la maquina virtual.

#### 23/05/2021

Se modificó la gramática para aceptar declaración de arreglos

#### 24/05/2021

Se implementaron las operaciones lógicas en las expresiones y la maquina virtual. Se hizo refactor para simplificar la gramática. Se implementaron las constantes negativas

#### 25/05/2021

Refactorización de clase SemanticCube. Se creú un archivo de utilidades para contener la información estática definida en el proyecto. Se comenzó la implementación de los puntos neurálgicos para arreglos en regla 'factor'.

#### 26/05/2021

Refactorización de la clase MemoryHelper, se creó una nueva clase Memory para implementar específicamente en Máquina Virtual.

#### 27/05/2021

Se hizo modificación de la clase MemoryHelper para hacer validaciones de stack overflow en el manejo de las direcciones virtuales. Se crearon nuevas funciones para obtener el tipo de dato y scope de una variable o constante por su scope. Se modificó el esquema de memoria para aceptar constantes strings, se implementó su guardado en memoria. Se trabajó una función en máquina vrtual para ejecutar todos los cuádruplos de operadores binarios.

#### 28/05/2021

Se corrigió la generación de cuádruplos para arreglos y matrices, así como la asignación de direcciones en memoria virtual. Se cambiaron los cuádruplos para no llevar los límites de dimensiones sino sus direcciones en memoria.

#### 29/05/2021

Se implementó el manejo de apuntadores para la indexación de arreglos y matrices. Se implementó el operador relacional de == en semántica. Se desarrolló la funcionalidad en máquina virtual para la escritura de múltples elementos en una misma línea. Se implementó el estatuto de asignación en máquina virtual. Se implementaron los ciclos for y while en máquina virtual.