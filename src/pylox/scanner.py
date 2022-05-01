from typing import List, Any, Optional

from .token import Token
from .token import TokenType as T


class Scanner:
    def __init__(self, lox, source: str):
        from .lox import Lox

        self.lox: Lox = lox
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> List[Token]:
        while not self._is_at_end():
            # self.start = self.current
            self._scan_token()

        self.tokens.append(Token(T.EOF, "", None, self.line))
        return self.tokens

    def _scan_token(self):
        self.start = self.current
        c = self._advance()
        print(f"Advanced to {c} self.current = {self.current}")

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

            case _:
                self.lox.error(self.line, "Unexpected character.")

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

    def _add_token(self, type_: T, literal: Optional[Any] = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type_, text, literal, self.line))
