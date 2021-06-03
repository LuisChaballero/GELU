# GELU User Manual

The following user manual describes the syntax and semantics of the language GELU, its main purpose is to give a broad introduction to all the capabilities and features of this simple programming language.

## Table of contents

## Introduction

GELU is an object-oriented programming language that pretends to be a simpler version of C++ with inspiration from other programming languages like Python. It supports variable declarations, assignments, conditions, cycles, read, and write statements, as well as mathematical expressions with arithmetic, logical, and relational operators. It also offers mechanisms to handle one and two-dimensional arrays.

## Basic Program Structure

A basic GELU program consists in just a program name and a main function.

### Format

Global variable declarations need to be right after ```program name;```. Function declarations go after global variables and before the main function. Here's an example.

```
program test;

< Global Variable declaration >

< Function Declaration 
    < Local Variable declaration >
>

main() {
    # This is a comment.
    # Additional code...
}
```

### Functional example

Now a functional example.

```
program test2;

# Global variables
int a, b;

# Void functions
func void show() {
    # Local Variables
    float c, d;
    print("Hello World!");
}

# Main function
main() {
    # Void call function
    show();
}
```

## Variable declaration

GELU supports three different data types: ```int```, ```float```, ```char```

### Format

```
var <type> <var_name> ;
var <type> <var_name> ,  <var_name_02>  ;
```  

### Example
```
var int num;
var float n1, n2;
```
    
    Note that it is not possible to declare and assign a value to a variable all in the same line.

```
# Error
var float = 2.0;
```

### Variables with dimensions

GELU offers mechanisms to work with one and two-dimensional arrays. Their size is static and must be specified in the variable declaration.

```
# Correct format
var char array[7], matrix[3,4];

# Incorrect 
var int n;
var int arr[n];
```


## Expresions

Expresions' result data types include the three previously mentioned, as well as the bool type.

```
int a;
float b;

# Arithmetic Expression
a = 10 + 2 / 7; 
b = (12.7 + 2) * 2;

# Displays the result of the expression
print("a: ", a ,", b: ", b);

# Boolean Expression
# a equal to 7 AND b less than 0
if (a == 7 & b < 0){
    # Do something
} 
```

    Note that the result of a boolean expression can't be saved in a variable since its type is not supported. Its usage is show on [section 5](#expressions).

    

## Decision statements

This are GELU's statements that contain a boolean expression to produce non-linear statements.

``` 
# if a is greater than 10 AND less than 15
if ( a > 10 & a < 15 ) {
    print("Inside of IF");
}

# if a is different than 12
if (a <> 12) {
    print("a cant be 12");
}
else {
    print("a has a value of 12");
}
```
    
## Loop statements
    
### While loops

The code inside the while statement will continue to execute as long as the condition expression evaluates to True.  

```
# Correct implementation of while 
while( a > 10) {
    a = a / 2 + 3;
}

# Error: expression inside the while statement must return boolean
while(a) {
    a = 
}
```

### For loops

The For needs to have an assignation statement between a non-dimensional integer variable and a expression. At the end of each cycle the value of the variable will increase by one. The code inside the For statement will continue to execute as long as the second expression evaluates to False.

```
# Correct implementation of For
for a = 5 until (a > 10) {
    print(a);
}

# Error: Variable assignation inside the For must be an integer.
for a = 5.0 until (a > 10) {
    print(a);
}

# Error: Variable must not have any dimensions
for array[3] = 5.0 until (a > 10) {
    print(a);
}

# Having an indexation of a dimensional variable as an expression is valid
for a = array[3] until (a > 10) {
    print(a);
}
```

## Functions

Functions are a self contained modules that GELU supports to allow the programmer to execute a specific procedure with the ability to repeat and call themselves.

### Non-void functions

These functions can return one of the three supported data types in GELU.

```
func int sum(int a, int b) {
    return a+b;
}

main() {
    # Call of non-void function. Can be used as ana expression.
    print(sum(2, 3));
}
```

## Void functions

These functions have no return type. They only execute the code inside them but do not return anything.

```
func void sum(int a, int b) {
    print(a+b);
}

main() {
    # Call of void function
    sum(5, 10);
}
```

## Read 

In GELU you can read an inputs rom the terminal storing them in a determined variable. This statement is used to receive input from the user. If the user writes a different value than expected (Eg. a float instead of an integer), an error is given.

```
var int x, result;

main() {
    # Asks user to write an integer
    read x;

    result = x + 10;

    print("The result is ", result);
}
```

## More examples

You can take a look at [these examples](./Tests) if you want to see more about this programming language in action.
