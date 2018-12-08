# kids-calculus
Kids Calculus is a generator of arithmetic expressions for kids. The generator provides expressions using the operators `+`, `-`, and `*`. The command line version provides the level of difficulties. Subtraction and then multiplication are introduced as the difficulty increases.

## Usage
The `calculus.py` module is a python script that can be used as a command line tool for generating series of arithmetic expressions.
```
usage: Kids Calculus [-h] [-l {1,2,3,4,5,6,7,8,9,10}] [-c COUNT]
                     [-f {html,text}] [-o OUTPUT] [-t TITLE] [-s SUBTITLE]

A generator of arithmetic expressions for kids.

optional arguments:
  -h, --help            show this help message and exit
  -l {1,2,3,4,5,6,7,8,9,10}, --level {1,2,3,4,5,6,7,8,9,10}
                        Level of difficulty in range [1; 10]. 1 to 3 is meant
                        for 4 to 5 years old. 4 to 5 is meant for 6 to 8 years
                        old. 6 to 8 is meant for 8 to 12 years old. 9 to 10 is
                        meant for 12 years old and more.
  -c COUNT, --count COUNT
                        The number of arithmetic expressions to generate.
  -f {html,text}, --format {html,text}
                        The output format.
  -o OUTPUT, --output OUTPUT
                        The file path used to output the generated arithmetic
                        expressions. Default to stdout if none given.
  -t TITLE, --title TITLE
                        A custom title for the generated content. A default
                        title is automatically generated, unless an explicit
                        empty string is given.
  -s SUBTITLE, --subtitle SUBTITLE
                        A custom subtitle for the generated content. A default
                        subtitle is automatically generated, unless an
                        explicit empty string is given.

```        

Here are a few usage examples.

```
python calculus.py --level 5 --format html -output calculus.html --title "Calculus for Simon" --count 20
```
Generates an HTML file named `calculus.html` in the current folder. The file will contain 20 expressions. The expression difficulty is 5/10, which is meant for a 6 to 8 years old kid.

```
python calculus.py -l 3 --f text --title "Calculus for Simon" -c 5
```
Prints 5 expressions of dicculty 3/10 to the standard output:

```
Calculus for Simon
=====

Level 3/10, 2018-12-08
-----

5 + 5 =
3 - 0 =
0 + 6 =
3 + 4 - 4 =
4 + 6 + 0 =
```

## API

The `calculus.py` module provides two classes that can be used to integrate this generator into another project:
* `CalculusGenerator`: A generator of random, simple arithmetic expressions.
* `CalculusOptions`: Represents the set of options available for generating arithmetic expressions with `CalculusGenerator`.

The `get_options_for_level(level)` function provides an empirical heuristic for picking an appropriate option set according to the requested level of difficulty. This code is internal API and may change at any time in order to provide a smoother progression in the difficulty.
