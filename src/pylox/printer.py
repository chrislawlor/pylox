from io import StringIO

from . import ast


class AstPrinter(ast.ExprVisitor):
    def print(self, expr: ast.Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: ast.BinaryExpr) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: ast.GroupingExpr) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: ast.LiteralExpr) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: ast.UnaryExpr):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: ast.Expr) -> str:
        buffer = StringIO()

        buffer.write("(")
        buffer.write(name)

        for expr in exprs:
            buffer.write(" ")
            buffer.write(expr.accept(self))
        buffer.write(")")

        return buffer.getvalue()
