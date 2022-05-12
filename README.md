# Pylox

A Python implementation of the Lox programming language, defined in the excellent [Crafting Interpreters](https://craftinginterpreters.com/) by Robert Nystrom ([@munificentbob](https://twitter.com/intent/user?screen_name=munificentbob))

Pylox is a tree-walk interpreter, with a recursive descent parser, based heavily on the `jlox` interpreter from the book, which is implemented in Java.

My goal for writing Pylox is to learn techniques for writing scanners, parsers, and interpreters. Writing this in Python helps me to ensure that I'm gaining an understanding of the underlying concepts, and not just rote typing the examples from the book. It sticks close to the Java implementation, mostly to avoid getting stuck if I get something wrong. For this reason, this implementation values correctness over being Pythonic, or any performance considerations.

## Usage

REPL:

```bash
$ pylox
>
```

or evaluate a Lox script:

```bash
$ pylox my_script.lox
```


## Lox Grammar

Lox has a context-free grammar, defined using the following notation:


|symbol       |description|
|-------------|-----------------------------|
|rule         |name followed by an arrow (→), followed by a sequnce of symbols|
|terminals    |quoted strings  |
|non-terminals| lowercase words|
|\|           | Logical OR|
|(            | Grouping|
|*            | Previous production repeats zero or more times|
|+            | Previous production appears at least once|
|?            | Previous production appears zero or one times|
|;            | ends a rule|

```
program         → declaration* EOF

declaration     → funDecl
                | varDecl
                | statement ;

statement       → exprStmt
                | forStmt ;
                | ifStmt
                | printStmt ;
                | whileStmt ;
                | block ;

exprStmt        → expression ";" ;

forStmt         → "for" "(" ( varDecl | exprStmt | ";" )
                  expression? ";"
                  expression? ";" ")" statement ;

ifStmt          → "if" "(" expression ")" statement
                ( "else" statement )? ;

printStmt       → "print" expression ";" ;

whileStmt       → "while" "(" expression ")" statement;

block           → "{" declaration "}" ;

funDecl         → "fun" function ;

function        → IDENTIFIER "(" parameters? ")" block ;

varDecl         → "var" IDENTIFIER ( "=" expression )? ";" ;

expression      → assignment ;

assignment      → IDENTIFIER "=" assignment
                | logic_or ;

logic_or        → logic_and ( "or" logic_and )* ;

logic_and       → equality ( "and" equality )* ;

equality        → comparison ( ( "!=" | "==" ) comparison )* ;

comparison      → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;

term            → factor ( ( "-" | "+" ) factor )* ;

factor          → unary ( ( "/" | "*" ) unary )* ;

unary           → ( "!" | "-" ) unary
                | call ;

call            → primary ( "(" arguments? ")" )* ;

arguments       → expression ( "," expression )* ;

primary         → NUMBER | STRING | "true" | "false" | "nil"
                | "(" expression ")"
                | IDENTIFIER ;

```
