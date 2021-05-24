#*Diseño de compiladores*
##*Proyecto final*

###*Integrantes:*
- Gerardo Silva A01136536
- Luis Caballero A01282700

##*Herramientas:*
- Python 
- Ply (lex&yacc)

##*Bitácora*

###*Primer avance* - 9/04/2021

Se llevó a cabo el planteamiento del proyecto y sus requerimientos, se definió la lista de tokens, los diagramas de sintaxis y la gramática del lenguaje.

###*Segundo avance* - 16/04/2021

Se agrego la creación de tablas de simbolos y de variables. Tambien se definió la tabla de consideraciones semanticas y las precedencia de los operadores.


##19/04/2021

Se implemento la declaración de variables multiples 

###*Tercer avance* - 23/04/2021

Se implemento la generación del código intermedio para las expresiones básicas (Sin considerar parentesis y operadores de comparación). Se agrego una implementación simple para los valores temporales sin utilizar el manejo de memoria.

##26/04/2021

Se implemento el cubo semantico de tipos.

###*Cuarto avance* - 01/05/2021

Se implementarion los cuadruplos para los estatutos no lineales IF y WHILE. Queda pediente el estatuto FOR y creación de cuadruplos para constantes.    

##06/05/2021

Se implemento el cuadruplo para el estatuto no lineal FOR.

###*Quinto avance* - 10/05/2021

Se creó el directorio para clases. Se modificó parte de la gramatica para los puntos neuralgicos de la implemetación de clases. Queda pendiente el añadir los atributos y metodos de cada clase al directorio de clases.

##11/05/2021

Se implementarion funciones adicionales en ClassDirectory. Se implementó la añadidura de los metodos y atributos de una clase al directorio de clases. Falta la añadidura de los parametros de los metodos de las clases.

##12/05/2021

Se implementó la añadidura de los parametros a los metodos de clases. 

###*Sexto avance* - 15/05/2021

Se modificaron las clases de la implementación del directorio de funciones para manejar el guardado de parametros, la dirección de inicialización. Se implementaron los cuadruplos en la delcaración de funciones y métodos. Se modificó parte de la gramatica en las expresiones (Algunos tenian que ser Exp en ves de Expresion). Queda pendiente los cuadruplos de las llamadas a función

##16/05/2021

Se modificó la gramatica para considerar la llamada a métodos void de una clase. Se implementaron los cuadruplos de llamadas a funciones. Queda pendiente validar el tipo de retorno en las funciones

##21/05/2021

Se creo la clase de memoryHandler y se implementaron las direcciones virtuales para los operandos 

##21/05/2021

Se implementaron las direcciones virtuales para los temporales y se agrego la deteccion de errores cuando se inicializa una variable que ya existe. 

##23/05/2021

Se implemento el directorio de constantes y la ejecución de las operaciones aritmeticas en la maquina virtual.

##23/05/2021

Se modificó la gramatica para aceptar declaracion de arreglos