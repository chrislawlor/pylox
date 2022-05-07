from enum import Enum


class TokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    COMMA = ","
    DOT = "."
    MINUS = "-"
    PLUS = "+"
    SEMICOLON = ";"
    SLASH = "/"
    STAR = "*"

    # One or two character tokens
    BANG = "!"
    BANG_EQUAL = "!="
    EQUAL = "="
    EQUAL_EQUAL = "=="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="

    # Literals
    IDENTIFIER = "id"
    STRING = "str"
    NUMBER = "num"

    # Keywords
    AND = "and"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FUN = "fun"
    FOR = "for"
    IF = "if"
    NIL = "nil"
    OR = "or"
    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "var"
    WHILE = "while"

    EOF = "EOF"


class Token:
    def __init__(self, type_: TokenType, lexeme: str, literal: object, line: int):
        self.type = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        if self.literal:
            return f"{self.type.name}[{self.lexeme}]"
        return self.type.name

    def __repr__(self):
        return (
            f'Token({self.type.name}, "{self.lexeme}", '
            f"{self.literal}, line={self.line})"
        )
