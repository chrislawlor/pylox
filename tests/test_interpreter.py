from io import StringIO
from unittest.mock import MagicMock

import pytest

from pylox import expr as Expr
from pylox.interpreter import Interpreter, LoxDivisionByZero, LoxRuntimeError
from pylox.lox import Lox
from pylox.token import Token
from pylox.token import TokenType as T


@pytest.fixture
def interpreter() -> Interpreter:
    return Interpreter(Lox())


def test_interpret():
    output = StringIO()
    interpreter = Interpreter(Lox(), out=output)
    expr = Expr.Literal(1.0)

    interpreter.interpret(expr)

    assert output.getvalue() == "1.0\n"


def test_runtime_error_reports():
    lox = MagicMock(spec=Lox)
    interpreter = Interpreter(lox)

    # Should raise a LoxDivisionByZero error
    expr = Expr.Binary(
        left=Expr.Literal(1),
        operator=Token(T.SLASH, "/", None, line=1),
        right=Expr.Literal(0),
    )

    interpreter.interpret(expr)

    lox.runtime_error.assert_called_once()


@pytest.mark.parametrize(
    "value,expected",
    [(True, "true"), (False, "false"), (None, "nil"), (1, "1"), (1.0, "1.0")],
)
def test_stringify(interpreter: Interpreter, value, expected):
    assert interpreter.stringify(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [([], True), ({}, True), (True, True), (None, False), (False, False), (0, True)],
)
def test_is_truthy(interpreter: Interpreter, value, expected: bool):
    assert interpreter.is_truthy(value) == expected


@pytest.mark.parametrize(
    "value,expected", [(0, True), (1, True), (1.0, True), ("0", False)]
)
def test_is_number(interpreter: Interpreter, value, expected: bool):
    assert interpreter.is_number(value) == expected


@pytest.mark.parametrize("left,right", [(1, "1"), ("1", 1)])
def test_check_number_operands_ordering_invariant(
    interpreter: Interpreter, left, right
):
    with pytest.raises(LoxRuntimeError):
        token = MagicMock(spec=Token)
        interpreter.check_number_operands(token, left, right)


def test_visit_unary_expr_minus(interpreter: Interpreter):
    expr = Expr.Unary(Token(T.MINUS, "-", None, line=1), Expr.Literal(1))

    value = interpreter.visit_unary_expr(expr)

    assert value == -1


def test_visit_unary_expr_bang(interpreter: Interpreter):
    expr = Expr.Unary(Token(T.BANG, "!", None, line=1), Expr.Literal(True))

    value = interpreter.visit_unary_expr(expr)

    assert value is False


def test_visit_literal_expr(interpreter: Interpreter):
    expr = Expr.Literal(1)

    value = interpreter.visit_literal_expr(expr)

    assert value == 1


def test_visit_grouping_expr(interpreter: Interpreter):
    expr = Expr.Grouping(Expr.Literal(1))

    value = interpreter.visit_grouping_expr(expr)

    assert value == 1


@pytest.mark.parametrize(
    "left,right,expected", [(1, 0, True), (0, 1, False), (1, 1, False)]
)
def test_visit_binary_expr_greater(interpreter: Interpreter, left, right, expected):
    expr = Expr.Binary(
        left=Expr.Literal(left),
        operator=Token(T.GREATER, ">", None, line=1),
        right=Expr.Literal(right),
    )

    value = interpreter.visit_binary_expr(expr)

    assert value is expected


@pytest.mark.parametrize(
    "left,right,expected", [(1, 0, True), (0, 1, False), (1, 1, True)]
)
def test_visit_binary_expr_greater_equal(
    interpreter: Interpreter, left, right, expected
):
    expr = Expr.Binary(
        left=Expr.Literal(left),
        operator=Token(T.GREATER_EQUAL, ">=", None, line=1),
        right=Expr.Literal(right),
    )

    value = interpreter.visit_binary_expr(expr)

    assert value is expected


@pytest.mark.parametrize(
    "left,right,expected", [(1, 0, False), (0, 1, True), (1, 1, False)]
)
def test_visit_binary_expr_less(interpreter: Interpreter, left, right, expected):
    expr = Expr.Binary(
        left=Expr.Literal(left),
        operator=Token(T.LESS, "<", None, line=1),
        right=Expr.Literal(right),
    )

    value = interpreter.visit_binary_expr(expr)

    assert value is expected


@pytest.mark.parametrize(
    "left,right,expected", [(1, 0, False), (0, 1, True), (1, 1, True)]
)
def test_visit_binary_expr_less_equal(interpreter: Interpreter, left, right, expected):
    expr = Expr.Binary(
        left=Expr.Literal(left),
        operator=Token(T.LESS_EQUAL, "<=", None, line=1),
        right=Expr.Literal(right),
    )

    value = interpreter.visit_binary_expr(expr)

    assert value is expected


@pytest.mark.parametrize(
    "left,right,expected",
    [(1, 0, True), (0, 1, True), (1, 1, False), ("1", "1", False), ("1", "0", True)],
)
def test_visit_binary_expr_bang_equal(interpreter: Interpreter, left, right, expected):
    expr = Expr.Binary(
        left=Expr.Literal(left),
        operator=Token(T.BANG_EQUAL, "!=", None, line=1),
        right=Expr.Literal(right),
    )

    value = interpreter.visit_binary_expr(expr)

    assert value is expected


@pytest.mark.parametrize(
    "left,right,expected",
    [(1, 0, False), (0, 1, False), (1, 1, True), ("1", "1", True), ("1", "0", False)],
)
def test_visit_binary_expr_equal_equal(interpreter: Interpreter, left, right, expected):
    expr = Expr.Binary(
        left=Expr.Literal(left),
        operator=Token(T.EQUAL_EQUAL, "==", None, line=1),
        right=Expr.Literal(right),
    )

    value = interpreter.visit_binary_expr(expr)

    assert value is expected


@pytest.mark.parametrize(
    "left,right,expected",
    [(3, 2, 1), (1, 0, 1), (1, 2, -1)],
)
def test_visit_binary_expr_minus(interpreter: Interpreter, left, right, expected):
    expr = Expr.Binary(
        left=Expr.Literal(left),
        operator=Token(T.MINUS, "-", None, line=1),
        right=Expr.Literal(right),
    )

    value = interpreter.visit_binary_expr(expr)

    assert value is expected


@pytest.mark.parametrize(
    "left,right,expected",
    [(3, 2, 5), (1, 0, 1), (-1, 2, 1), ("ham", "let", "hamlet")],
)
def test_visit_binary_expr_plus(interpreter: Interpreter, left, right, expected):
    expr = Expr.Binary(
        left=Expr.Literal(left),
        operator=Token(T.PLUS, "+", None, line=1),
        right=Expr.Literal(right),
    )

    value = interpreter.visit_binary_expr(expr)

    assert value == expected


@pytest.mark.parametrize(
    "left,right,expected",
    [(1, 1, 1), (0, 1, 0), (-4, 2, -2)],
)
def test_visit_binary_expr_slash(interpreter: Interpreter, left, right, expected):
    expr = Expr.Binary(
        left=Expr.Literal(left),
        operator=Token(T.SLASH, "/", None, line=1),
        right=Expr.Literal(right),
    )

    value = interpreter.visit_binary_expr(expr)

    assert value == expected


def test_division_by_zero_raises(interpreter: Interpreter):
    expr = Expr.Binary(
        left=Expr.Literal(1),
        operator=Token(T.SLASH, "/", None, line=1),
        right=Expr.Literal(0),
    )

    with pytest.raises(LoxDivisionByZero):
        interpreter.visit_binary_expr(expr)


@pytest.mark.parametrize(
    "left,right,expected",
    [(1, 1, 1), (0, 1, 0), (-4, 2, -8)],
)
def test_visit_binary_expr_star(interpreter: Interpreter, left, right, expected):
    expr = Expr.Binary(
        left=Expr.Literal(left),
        operator=Token(T.STAR, "*", None, line=1),
        right=Expr.Literal(right),
    )

    value = interpreter.visit_binary_expr(expr)

    assert value == expected
