# EIDOS interpreter
-------------------
624 (Programming Languages) assignment to write an interpreter for Eidos 
programming language. Not fully functional, but basic programs work. And 
we can do line by line interpreting!

## Using the Interpreter
-----------------------
Program `eidos` is created to run similar to the python command. If you
run it without any inputs you will be place in an interpreter that you might 
confuse with python. Here you can run single line Eidos programs. We store the 
symbol table and allow 


### Interpreter mode:
Should work on nix systems. eidos file calls `/usr/bin/env bash` which calls
`python3 eidosInterpreter.py`. So if that fails you can call `python3 eidosInterpreter.py`
and you will get the same result as below.
```
$ ./eidos
Version: 0.1
NOT:  We cannot handle functions that take multiple lines.
      We can keep a history of values, but not delete them.
      Functions that take longer than 60 seconds will error out.
      Please type 'exit' or 'quit' to exit
eidos > x=1;
{'x': 1}
eidos > x=x+1;
{'x': 2}
eidos > x;
{'x': 2}
eidos > z=x+1;
{'z': 3}
eidos > z;
{'z': 3}
eidos > x;
{'x': 2}
eidos > exit
```

### Running an Eidos file:
Eidos file must end in ".e" to run, or else the program will tell you to change
the extension.

For example, if we ran the same program in a file we would get the following
```
$ ./eidos test.e
{'x': 5}
{'x': 7}
{'z': 14, 'x': 7}

```
Since we are in alpha, we do not worry that we are displaying the table of 
variables during each line. We will worry about this later

## Running a suite of tests
---------------------------
To run a bunch of Eidos files at once place them in a directory containing only
Eidos files. Then edit the `testCases.py` file's testDir variable. You can then
run
```
python3 testCases.py
```
and the program will display the output of each file and at the end will report
the number of failed programs out of the total number of programs that were run.


Note: The pass rate that is shown only shows programs that do not error out. 
It does not show that the programs have the correct output.

## Slides
---------
[624 Class presentation](https://docs.google.com/presentation/d/1a-Nna-p7qqNWKXLpfevQEJw2se58ehDeAAy23adKIW4/edit?usp=sharing)

## Authors
---------
Project by Steven Walton, He He (贺赫), and Priya Kudva. 

Team: Thunder Hamsters

University of Oregon
