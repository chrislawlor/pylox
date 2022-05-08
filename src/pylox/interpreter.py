import sys
from typing import Any, List

from . import ast
from .environment import Environment
from .exceptions import LoxRuntimeError
from .token import Token
from .token import TokenType as T


class LoxDivisionByZero(LoxRuntimeError):
    pass


class Interpreter(ast.ExprVisitor, ast.StmtVisitor):
    def __init__(self, lox, out=sys.stdout):
        from .lox import Lox

        self.lox: Lox = lox
        self.environment = Environment()
        self.out = out

    def interpret(self, statements: List[ast.Stmt]) -> None:
        try:
            for statement in statements:
                self.execute(statement)
        except LoxRuntimeError as error:
            self.lox.runtime_error(error)

    def evaluate(self, expr: ast.Expr):
        return expr.accept(self)

    def execute(self, stmt: ast.Stmt):
        stmt.accept(self)

    def visit_expression_stmt(self, stmt: ast.ExpressionStmt):
        self.evaluate(stmt.expression)

    def visit_print_stmt(self, stmt: ast.PrintStmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value), file=self.out)

    def visit_var_stmt(self, stmt: ast.VarStmt):
        value = None
        if stmt.intitializer is not None:
            value = self.evaluate(stmt.intitializer)

        self.environment[stmt.name.lexeme] = value

    def visit_binary_expr(self, expr: ast.BinaryExpr):
        # Lox evaluates expressions in left-to-right order
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case T.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return left > right
            case T.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left >= right
            case T.LESS:
                self.check_number_operands(expr.operator, left, right)
                return left < right
            case T.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left <= right
            case T.BANG_EQUAL:
                return not self.is_equal(left, right)
            case T.EQUAL_EQUAL:
                return self.is_equal(left, right)
            case T.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return left - right
            case T.PLUS:
                # We add numbers, or concatenate strings but don't handle str + number
                if self.is_number(left) and self.is_number(right):
                    return left + right
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
            case T.SLASH:
                self.check_number_operands(expr.operator, left, right)
                if right == 0:
                    raise LoxDivisionByZero("Divison by zero", expr.operator)
                return left / right
            case T.STAR:
                self.check_number_operands(expr.operator, left, right)
                return left * right

            case _:
                # Unreachable
                return None

    def visit_grouping_expr(self, expr: ast.GroupingExpr):
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr: ast.LiteralExpr):
        return expr.value

    def visit_unary_expr(self, expr: ast.UnaryExpr):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case T.BANG:
                return not self.is_truthy(right)
            case T.MINUS:
                return -right

        # Unreachable
        return None

    def visit_variable_expr(self, expr: ast.VariableExpr) -> Any:
        return self.environment[expr.name]

    def check_number_operand(self, operator: Token, operand):
        if self.is_number(operand):
            return
        raise LoxRuntimeError("Operand must be a number", operator)

    def check_number_operands(self, operator: Token, left, right):
        if self.is_number(left) and self.is_number(right):
            return
        raise LoxRuntimeError("Operands must be numbers", operator)

    def is_number(self, value) -> bool:
        # For whatever reason,
        #     isinstance(value, int | float)
        # is fine, but
        #     Number = int | float
        #     isinstance(value, Number)
        # is not. So, to avoid sprinking "int | float" all over,
        # we add this method.
        return isinstance(value, int | float)

    def is_truthy(self, obj: Any) -> bool:
        # In Lox, None and False are falsey, everything else is truthy
        if obj is None:
            return False
        if isinstance(obj, bool):
            return bool(obj)

        return True

    def is_equal(self, a, b) -> bool:
        return a == b

    def stringify(self, obj) -> str:
        if obj is None:
            return "nil"

        if obj is True:
            return "true"

        if obj is False:
            return "false"

        return str(obj)
