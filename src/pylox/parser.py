from typing import List

import pylox

from . import expr as Expr
from .token import Token
from .token import TokenType as T


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, lox: "pylox.lox.Lox", tokens: List[Token]):
        self.lox = lox
        self.tokens = tokens
        self.current = 0

    def expression(self) -> Expr.Expr:
        return self.equality()

    def equality(self) -> Expr.Expr:
        expr = self.comparison()

        while self.match(T.BANG_EQUAL, T.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr.Expr:
        expr = self.term()

        while self.match(T.GREATER, T.GREATER_EQUAL, T.LESS, T.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def term(self) -> Expr.Expr:
        expr = self.factor()

        while self.match(T.MINUS, T.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def factor(self) -> Expr.Expr:
        expr = self.unary()

        while self.match(T.SLASH, T.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def unary(self) -> Expr.Expr:
        if self.match(T.BANG, T.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.primary()

    def primary(self) -> Expr.Expr:
        if self.match(T.FALSE):
            return Expr.Literal(False)
        if self.match(T.TRUE):
            return Expr.Literal(True)

        if self.match(T.NUMBER, T.STRING):
            return Expr.Literal(self.previous().literal)

        if self.match(T.LEFT_PAREN):
            expr = self.expression()
            self.consume(T.RIGHT_PAREN, 'Expect ")" after expression.')
            return Expr.Grouping(expr)

        raise self.error(self.peek(), "Invalid primary match")

    def match(self, *types: T) -> bool:
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True
        return False

    def consume(self, type_: T, message: str):
        if self.check(type_):
            return self.advance()

        raise self.error(self.peek(), message)

    def check(self, type_: T) -> bool:
        if not self.is_at_end():
            return False
        return self.peek().type == type_

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == T.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def error(self, token: Token, message: str) -> ParseError:
        self.lox.error(token, message)
        return ParseError()
