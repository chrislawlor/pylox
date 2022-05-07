from typing import List

import pytest

from pylox.lox import Lox
from pylox.parser import ParseError, Parser
from pylox.printer import AstPrinter
from pylox.token import Token, TokenType


def create_tokens(*lexemes: str) -> List[Token]:
    tokens = []
    for lexeme in lexemes:
        literal = None
        try:
            type_ = TokenType(lexeme)
        except ValueError:
            try:
                int(lexeme)
                type_ = TokenType.NUMBER
                literal = lexeme
            except ValueError:
                type_ = TokenType.STRING
                literal = lexeme
        tokens.append(Token(type_=type_, lexeme=lexeme, literal=literal, line=1))

    tokens.append(Token(type_=TokenType.EOF, lexeme="\0", literal=None, line=2))
    return tokens


def test_parse_simple():
    tokens = create_tokens("1", "+", "2")
    parser = Parser(Lox(), tokens)

    expr = parser.parse()

    assert expr is not None

    assert AstPrinter().print(expr) == "(+ 1 2)"


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
