from typing import Any, List

import pytest

from pylox import ast
from pylox.lox import Lox
from pylox.parser import ParseError, Parser
from pylox.printer import AstPrinter
from pylox.token import Token, TokenType


def create_tokens(*lexemes: str) -> List[Token]:
    tokens = []
    for lexeme in lexemes:
        literal: Any = None
        try:
            type_ = TokenType(lexeme)
        except ValueError:
            try:
                int(lexeme)
                type_ = TokenType.NUMBER
                literal = int(lexeme)
            except ValueError:
                type_ = TokenType.STRING
                literal = lexeme
        tokens.append(Token(type_=type_, lexeme=lexeme, literal=literal, line=1))

    tokens.append(Token(type_=TokenType.EOF, lexeme="\0", literal=None, line=2))
    return tokens


def test_parse_literal_expr():
    tokens = create_tokens("1", ";")
    parser = Parser(Lox(), tokens)

    statements = parser.parse()

    assert len(statements) == 1
    stmt = statements[0]
    print(f"{type(stmt)=}")
    assert isinstance(stmt, ast.ExpressionStmt)
    expr = stmt.expression
    assert isinstance(expr, ast.LiteralExpr)
    assert expr.value == 1


def test_parse_simple():
    tokens = create_tokens("1", "+", "2", ";")
    parser = Parser(Lox(), tokens)

    statements = parser.parse()

    assert len(statements) == 1

    expression_stmt = statements[0]
    assert isinstance(expression_stmt, ast.ExpressionStmt)

    assert AstPrinter().print(expression_stmt.expression) == "(+ 1 2)"


def test_consume_error():
    tokens = create_tokens("+")
    parser = Parser(Lox(), tokens)

    assert parser.peek().type == TokenType.PLUS
    with pytest.raises(ParseError):
        parser.consume(TokenType.MINUS, "Expected +")


def test_missing_right_paren_errors():
    tokens = create_tokens("(", "1")
    parser = Parser(Lox(), tokens)

    with pytest.raises(ParseError):
        parser.expression()


def test_synchronize_to_semicolon():
    tokens = create_tokens("1", "+", "2", ";", "3")
    parser = Parser(Lox(), tokens)

    parser.synchronize()

    assert parser.peek().lexeme == "3"


def test_synchronize_to_statement_boundary():
    tokens = create_tokens("2", "-", "1", "return", "true")
    parser = Parser(Lox(), tokens)

    parser.synchronize()

    assert parser.peek().lexeme == "return"


def test_parse_print_statement():
    tokens = create_tokens("print", "1", ";")
    parser = Parser(Lox(), tokens)

    statements = parser.parse()

    assert len(statements) == 1
    stmt = statements[0]

    assert isinstance(stmt, ast.PrintStmt)


def test_parse_complex():
    tokens = create_tokens("2", "*", "(", "4", "/", "2", ")", ";")
    parser = Parser(Lox(), tokens)

    statements = parser.parse()

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, ast.ExpressionStmt)
    expr = stmt.expression
    assert isinstance(expr, ast.BinaryExpr)
    assert expr.operator.type == TokenType.STAR
    left_expr = expr.left
    assert isinstance(left_expr, ast.LiteralExpr)
    assert left_expr.value == 2


def test_parse_unary():
    tokens = create_tokens("!", "true", ";")
    parser = Parser(Lox(), tokens)

    statements = parser.parse()

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, ast.ExpressionStmt)
    expr = stmt.expression
    assert isinstance(expr, ast.UnaryExpr)


def test_parse_return_nil():
    tokens = create_tokens("return", ";")
    parser = Parser(Lox(), tokens)

    statements = parser.parse()

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, ast.ReturnStmt)
    assert stmt.value is None


def test_parser_return_value():
    tokens = create_tokens("return", "1", ";")
    parser = Parser(Lox(), tokens)

    statements = parser.parse()

    assert len(statements) == 1
    stmt = statements[0]
    assert isinstance(stmt, ast.ReturnStmt)
    assert isinstance(stmt.value, ast.LiteralExpr)
    assert stmt.value.value == 1
