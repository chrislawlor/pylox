import pytest

from pylox import ast
from pylox.printer import AstPrinter
from pylox.token import Token
from pylox.token import TokenType as T


@pytest.fixture
def printer():
    return AstPrinter()


def test_parenthesize(printer):

    result = printer.parenthesize("literal", ast.LiteralExpr(123))

    assert result == "(literal 123)"


def test_print_nil(printer):
    expression = ast.LiteralExpr(None)
    assert expression.value is None

    output = printer.print(expression)

    assert output == "nil"


def test_printer(printer):
    expression = ast.BinaryExpr(
        ast.UnaryExpr(Token(T.MINUS, "-", None, 1), ast.LiteralExpr(123)),
        Token(T.STAR, "*", None, 1),
        ast.GroupingExpr(ast.LiteralExpr(45.67)),
    )

    output = printer.print(expression)

    assert output == "(* (- 123) (group 45.67))"
