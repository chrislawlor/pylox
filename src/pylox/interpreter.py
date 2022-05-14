import sys
import time
from abc import ABC, abstractmethod
from typing import Any, List

from . import ast
from .environment import Environment
from .exceptions import LoxRuntimeError
from .token import Token
from .token import TokenType as T


class LoxDivisionByZero(LoxRuntimeError):
    pass


class Return(Exception):
    def __init__(self, value):
        self.value = value


class Callable(ABC):
    @abstractmethod
    def arity(self) -> int:
        ...

    @abstractmethod
    def call(self, interpreter: "Interpreter", *arguments: Any) -> Any:
        ...


class Function(Callable):
    def __init__(self, declaration: ast.FunctionStmt):
        self.declaration = declaration

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter: "Interpreter", *arguments: Any) -> Any:
        environment = Environment(interpreter.globals)
        for param, argument in zip(self.declaration.params, arguments):
            environment.define(param.lexeme, argument)

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as ret:
            return ret.value

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"


class Interpreter(ast.ExprVisitor, ast.StmtVisitor):
    def __init__(self, lox, out=sys.stdout):
        from .lox import Lox

        self.lox: Lox = lox
        self.globals = Environment()  # fixed reference to outermost environment
        self.environment = self.globals  # changes as we enter and exit blocks
        self.out = out

        # Native functions

        class _clock(Callable):
            def arity(self):
                return 0

            def call(self, interpreter, *args):
                return time.time()

            def __str__(self):
                return "<native fn _clock>"

        self.globals.define("clock", _clock())

    def interpret(self, statements: List[ast.Stmt]) -> None:
        try:
            for statement in statements:
                self.execute(statement)
        except LoxRuntimeError as error:
            self.lox.runtime_error(error)

    def evaluate(self, expr: ast.Expr):
        return expr.accept(self)

    def execute_block(self, statements: List[ast.Stmt], environment: Environment):
        previous = self.environment

        try:
            self.environment = environment

            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def execute(self, stmt: ast.Stmt):
        stmt.accept(self)

    def visit_block_stmt(self, stmt: ast.BlockStmt):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_expression_stmt(self, stmt: ast.ExpressionStmt):
        self.evaluate(stmt.expression)

    def visit_function_stmt(self, stmt: ast.FunctionStmt):
        function = Function(stmt)
        self.environment.define(stmt.name.lexeme, function)

    def visit_if_stmt(self, stmt: ast.IfStmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)

    def visit_print_stmt(self, stmt: ast.PrintStmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value), file=self.out)

    def visit_return_stmt(self, stmt: ast.ReturnStmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)

        raise Return(value)

    def visit_var_stmt(self, stmt: ast.VarStmt):
        value = None
        if stmt.intitializer is not None:
            value = self.evaluate(stmt.intitializer)

        self.environment.define(stmt.name.lexeme, value)

    def visit_while_stmt(self, stmt: ast.WhileStmt):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)

    def visit_assign_expr(self, expr: ast.AssignExpr) -> Any:
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

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

    def visit_call_expr(self, expr: ast.CallExpr):
        function = self.evaluate(expr.callee)

        arguments = [self.evaluate(arg) for arg in expr.arguments]

        if not isinstance(function, Callable):
            raise LoxRuntimeError("Can only call functions and classes.", expr.paren)

        if len(arguments) > function.arity():
            raise LoxRuntimeError(
                f"Expected {function.arity()} arguments but got {len(arguments)}.",
                expr.paren,
            )

        return function.call(self, *arguments)

    def visit_grouping_expr(self, expr: ast.GroupingExpr):
        return self.evaluate(expr.expression)

    def visit_literal_expr(self, expr: ast.LiteralExpr):
        return expr.value

    def visit_logical_expr(self, expr: ast.LogicalExpr):
        left = self.evaluate(expr.left)

        if expr.operator.type == T.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        return self.evaluate(expr.right)

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
        return self.environment.get(expr.name)

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
