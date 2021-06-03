# GELU

GELU is an Object Oriented Programming language developed with the purpose of becoming a friendly and uncomplicated tool for anyone who is just starting to learn how to program. It provides mechanisms for the definition of classes, attributes, methods, as well as variables, assignments, conditions, loops, writes, among other basic statements and expressions.

---

## Install

This section describes how to run your own GELU programs. You must have Python 3.2 or later installed and configured in your system first.

### Compiler installation

Install the compiler.

```shell
$ git clone https://github.com/LuisChaballero/GELU.git
```

## Compile GELU

Before compiling, you must have an input ```txt``` file inside GELU directory. 

Then you need to setup your file path in ```comp.py``` as follows.
```python
# Read text file
f = open(os.path.join(os.path.dirname(__file__), './your_path/', 'your_file_name'), 'r')
data = f.read()
```

## Run GELU

Once you have set up your environment and input file, you can compile with this command.

```shell
$ python3 comp.py
```

## Features

* Variable declaration
* Function declarations
* Conditionals
* If-else statements
* For loops
* While loops
* Arithmetic operations
* Relational operations
* Logical operations
* Int, Float and Char data types
* Array declaration
* Two-dimensional array declaration
* Print
* Read

## Video demo

To learn how to start programming with in GELU take a look at this quick guide on how to make your first Hello World [Video](https://youtu.be/IO2jLVMmtPo)

## Documentation

For more information about GELU syntax, read the [user manual](./manual.md)

### Contributors

* [Luis Caballero](https://github.com/luischaballero)
* [Gerardo Silva](https://github.com/gerardoasilva)