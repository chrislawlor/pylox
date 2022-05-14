from collections import deque
from functools import singledispatchmethod
from typing import Deque, Dict, List

from . import ast
from .interpreter import Interpreter
from .token import Token


class Resolver(ast.StmtVisitor, ast.ExprVisitor):
    def __init__(self, lox, interpreter: Interpreter):
        from .lox import Lox

        self.lox: Lox = lox
        self.interpreter = interpreter
        self.scopes: Deque[Dict[str, bool]] = deque()

    def visit_block_stmt(self, stmt: ast.BlockStmt):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()

    def visit_expression_stmt(self, stmt: ast.ExpressionStmt):
        self.resolve(stmt.expression)

    def visit_function_stmt(self, stmt: ast.FunctionStmt):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt)

    def visit_if_stmt(self, stmt: ast.IfStmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)

    def visit_print_stmt(self, stmt: ast.PrintStmt):
        self.resolve(stmt.expression)

    def visit_return_stmt(self, stmt: ast.ReturnStmt):
        if stmt.value is not None:
            self.resolve(stmt.value)

    def visit_var_stmt(self, stmt: ast.VarStmt):
        self.declare(stmt.name)
        if stmt.intitializer is not None:
            self.resolve(stmt.intitializer)
        self.define(stmt.name)

    def visit_while_stmt(self, stmt: ast.WhileStmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.body)

    def visit_variable_expr(self, expr: ast.VariableExpr):
        if self.scopes and self.scopes[0][expr.name.lexeme] is False:
            self.lox.error(
                expr.name, "Can't read local variable in its own initializer."
            )

        self.resolve_local(expr, expr.name)

    def visit_assign_expr(self, expr: ast.AssignExpr):
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)

    def visit_binary_expr(self, expr: ast.BinaryExpr):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_call_expr(self, expr: ast.CallExpr):
        self.resolve(expr.callee)

        for arg in expr.arguments:
            self.resolve(arg)

    def visit_grouping_expr(self, expr: ast.GroupingExpr):
        self.resolve(expr.expression)

    def visit_literal_expr(self, expr: ast.LiteralExpr):
        return

    def visit_logical_expr(self, expr: ast.LogicalExpr):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_unary_expr(self, expr: ast.UnaryExpr):
        self.resolve(expr.right)

    @singledispatchmethod
    def resolve(self, statements: List[ast.Stmt]):
        for statement in statements:
            self.resolve(statement)

    @resolve.register
    def _(self, stmt: ast.Stmt):
        stmt.accept(self)

    @resolve.register
    def _(self, expr: ast.Expr):
        expr.accept(self)

    def resolve_function(self, function: ast.FunctionStmt):
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()

    def begin_scope(self):
        self.scopes.appendleft({})

    def end_scope(self):
        self.scopes.popleft()

    def declare(self, name: Token):
        if not self.scopes:
            return

        scope = self.scopes[0]
        scope[name.lexeme] = False

    def define(self, name: Token):
        if not self.scopes:
            return
        self.scopes[0][name.lexeme] = True

    def resolve_local(self, expr: ast.Expr, name: Token):
        for hops, scope in enumerate(self.scopes):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, hops)
