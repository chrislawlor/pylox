import sys
from typing import Any

from . import expr as Expr
from .token import Token
from .token import TokenType as T


class LoxRuntimeError(Exception):
    def __init__(self, message, token: Token):
        super().__init__(message)
        self.token = token


class LoxDivisionByZero(LoxRuntimeError):
    pass


class Interpreter(Expr.Visitor):
    def __init__(self, lox, out=sys.stdout):
        from .lox import Lox

        self.lox: Lox = lox
        self.out = out

    def interpret(self, expression: Expr.Expr) -> None:
        try:
            value = self.evaluate(expression)
            print(self.stringify(value), file=self.out)
        except LoxRuntimeError as error:
            self.lox.runtime_error(error)

    def evaluate(self, expr: Expr.Expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr: Expr.Binary):
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

    def visit_grouping_expr(self, expr: Expr.Grouping):
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr: Expr.Literal):
        return expr.value

    def visit_unary_expr(self, expr: Expr.Unary):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case T.BANG:
                return not self.is_truthy(right)
            case T.MINUS:
                return -right

        # Unreachable
        return None

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
