from io import StringIO

from . import expr as Expr


class AstPrinter(Expr.Visitor):
    def print(self, expr: Expr.Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: Expr.Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Expr.Grouping) -> str:
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Expr.Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Expr.Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *exprs: Expr.Expr) -> str:
        buffer = StringIO()

        buffer.write("(")
        buffer.write(name)

        for expr in exprs:
            buffer.write(" ")
            buffer.write(expr.accept(self))
        buffer.write(")")

        return buffer.getvalue()
