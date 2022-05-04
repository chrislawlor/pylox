import re
from typing import Any, List, Optional

import pylox

from .token import Token
from .token import TokenType as T


class Scanner:

    KEYWORDS = {
        "and": T.AND,
        "class": T.CLASS,
        "else": T.ELSE,
        "false": T.FALSE,
        "for": T.FOR,
        "fun": T.FUN,
        "if": T.IF,
        "nil": T.NIL,
        "or": T.OR,
        "print": T.PRINT,
        "return": T.RETURN,
        "super": T.SUPER,
        "this": T.THIS,
        "true": T.TRUE,
        "var": T.VAR,
        "while": T.WHILE,
    }

    def __init__(self, lox: "pylox.lox.Lox", source: str):
        self.lox = lox
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

        self._ALPHA_RGX = re.compile(r"[A-Za-z_]")

    def scan_tokens(self) -> List[Token]:
        while not self._is_at_end():
            # self.start = self.current
            self._scan_token()

        self.tokens.append(Token(T.EOF, "", None, self.line))
        return self.tokens

    def _scan_token(self):
        self.start = self.current
        c = self._advance()

        match c:
            case "(":
                self._add_token(T.LEFT_PAREN)
            case ")":
                self._add_token(T.RIGHT_PAREN)
            case "{":
                self._add_token(T.LEFT_BRACE)
            case "}":
                self._add_token(T.RIGHT_BRACE)
            case ",":
                self._add_token(T.COMMA)
            case ".":
                self._add_token(T.DOT)
            case "-":
                self._add_token(T.MINUS)
            case "+":
                self._add_token(T.PLUS)
            case ";":
                self._add_token(T.SEMICOLON)
            case "*":
                self._add_token(T.STAR)
            case "!":
                self._add_token(T.BANG_EQUAL if self._match("=") else T.BANG)
            case "=":
                self._add_token(T.EQUAL_EQUAL if self._match("=") else T.EQUAL)
            case ">":
                self._add_token(T.GREATER_EQUAL if self._match("=") else T.GREATER)
            case "<":
                self._add_token(T.LESS_EQUAL if self._match("=") else T.LESS)
            case "/":
                if self._match("/"):
                    # A comment goes until the end of the line
                    while self._peek() != "\n" and not self._is_at_end():
                        self._advance()
                else:
                    self._add_token(T.SLASH)

            case " " | "\r" | "\t":
                pass

            case "\n":
                self.line += 1

            case '"':
                self._string()

            case _:
                if self._is_digit(c):
                    self._number()
                elif self._is_alpha(c):
                    self._identifier()
                else:
                    self.lox.error(self.line, "Unexpected character.")

    def _identifier(self):
        while self._is_alphanumeric(self._peek()):
            self._advance()

        text = self.source[self.start : self.current]
        type_ = self.KEYWORDS.get(text, T.IDENTIFIER)

        self._add_token(type_)

    def _number(self):
        type_ = int
        while self._is_digit(self._peek()):
            self._advance()

        # Look for fractional part
        if self._peek() == "." and self._is_digit(self._peek_next()):
            # Consumer the "."
            type_ = float
            self._advance()

            while self._is_digit(self._peek()):
                self._advance()

        self._add_token(T.NUMBER, type_(self.source[self.start : self.current]))

    def _string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self.line += 1
            self._advance()

        if self._is_at_end():
            self.lox.error(self.line, "Unterminated string.")
            return

        # The closing ".
        self._advance()

        # Trim surrounding quotes
        value = self.source[self.start + 1 : self.current - 1]
        self._add_token(T.STRING, value)

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        return char

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _is_alpha(self, c: str) -> bool:
        return bool(self._ALPHA_RGX.match(c))

    def _is_alphanumeric(self, c: str) -> bool:
        return self._is_alpha(c) or self._is_digit(c)

    def _is_digit(self, c: str) -> bool:
        return "0" <= c <= "9"

    def _add_token(self, type_: T, literal: Optional[Any] = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type_, text, literal, self.line))
