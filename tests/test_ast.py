from pylox import ast
from pylox.token import Token
from pylox.token import TokenType as T


def test_hashable_expr():
    var_expr = ast.VariableExpr(name=Token(T.IDENTIFIER, "a", None, 1))

    {var_expr: True}
