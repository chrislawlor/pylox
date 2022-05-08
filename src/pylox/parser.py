from typing import List

from . import ast
from .token import Token
from .token import TokenType as T


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, lox, tokens: List[Token]):
        from .lox import Lox

        self.lox: Lox = lox
        self.tokens = tokens
        self.current = 0

    def parse(self) -> List[ast.Stmt]:
        statements: List[ast.Stmt] = []
        while not self.is_at_end():
            statements.append(self.statement())
        return statements

    def expression(self) -> ast.Expr:
        return self.equality()

    def statement(self) -> ast.Stmt:
        if self.match(T.PRINT):
            return self.print_statement()
        return self.expression_statement()

    def print_statement(self) -> ast.Stmt:
        value = self.expression()
        self.consume(T.SEMICOLON, 'Expect ";" after value.')
        return ast.PrintStmt(value)

    def expression_statement(self) -> ast.Stmt:
        expr = self.expression()
        self.consume(T.SEMICOLON, 'Expect ";" after expression.')
        return ast.ExpressionStmt(expr)

    def equality(self) -> ast.Expr:
        expr = self.comparison()

        while self.match(T.BANG_EQUAL, T.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = ast.BinaryExpr(expr, operator, right)

        return expr

    def comparison(self) -> ast.Expr:
        expr = self.term()

        while self.match(T.GREATER, T.GREATER_EQUAL, T.LESS, T.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = ast.BinaryExpr(expr, operator, right)

        return expr

    def term(self) -> ast.Expr:
        expr = self.factor()

        while self.match(T.MINUS, T.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = ast.BinaryExpr(expr, operator, right)

        return expr

    def factor(self) -> ast.Expr:
        expr = self.unary()

        while self.match(T.SLASH, T.STAR):
            operator = self.previous()
            right = self.unary()
            expr = ast.BinaryExpr(expr, operator, right)

        return expr

    def unary(self) -> ast.Expr:
        if self.match(T.BANG, T.MINUS):
            operator = self.previous()
            right = self.unary()
            return ast.UnaryExpr(operator, right)
        return self.primary()

    def primary(self) -> ast.Expr:
        if self.match(T.FALSE):
            return ast.LiteralExpr(False)
        if self.match(T.TRUE):
            return ast.LiteralExpr(True)

        if self.match(T.NUMBER, T.STRING):
            return ast.LiteralExpr(self.previous().literal)

        if self.match(T.LEFT_PAREN):
            expr = self.expression()
            self.consume(T.RIGHT_PAREN, 'Expect ")" after expression.')
            return ast.GroupingExpr(expr)

        raise self.error(self.peek(), "Expect expression.")

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
        if self.is_at_end():
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

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == T.SEMICOLON:
                return

            match self.peek().type:
                case (  # noqa: E211
                    T.CLASS
                    | T.FUN
                    | T.VAR
                    | T.FOR
                    | T.IF
                    | T.WHILE
                    | T.PRINT
                    | T.RETURN
                ):
                    return

            self.advance()
