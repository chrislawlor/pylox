import pytest

from pylox import expr as Expr
from pylox.printer import AstPrinter
from pylox.token import Token
from pylox.token import TokenType as T


@pytest.fixture
def printer():
    return AstPrinter()


def test_parenthesize(printer):

    result = printer.parenthesize("literal", Expr.Literal(123))

    assert result == "(literal 123)"


def test_print_nil(printer):
    expression = Expr.Literal(None)
    assert expression.value is None

    output = printer.print(expression)

    assert output == "nil"


def test_printer(printer):
    expression = Expr.Binary(
        Expr.Unary(Token(T.MINUS, "-", None, 1), Expr.Literal(123)),
        Token(T.STAR, "*", None, 1),
        Expr.Grouping(Expr.Literal(45.67)),
    )

    output = printer.print(expression)

    assert output == "(* (- 123) (group 45.67))"
