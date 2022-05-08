# This file is generated via generate_ast.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .token import Token


class ExprVisitor(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr: "BinaryExpr"):
        ...

    @abstractmethod
    def visit_grouping_expr(self, expr: "GroupingExpr"):
        ...

    @abstractmethod
    def visit_literal_expr(self, expr: "LiteralExpr"):
        ...

    @abstractmethod
    def visit_unary_expr(self, expr: "UnaryExpr"):
        ...


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor):
        ...


@dataclass
class BinaryExpr(Expr):
    left: Expr
    operator: Any
    right: Expr

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_binary_expr(self)


@dataclass
class GroupingExpr(Expr):
    expression: Expr

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_grouping_expr(self)


@dataclass
class LiteralExpr(Expr):
    value: Any

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_literal_expr(self)


@dataclass
class UnaryExpr(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_unary_expr(self)


class StmtVisitor(ABC):
    @abstractmethod
    def visit_expression_stmt(self, stmt: "ExpressionStmt"):
        ...

    @abstractmethod
    def visit_print_stmt(self, stmt: "PrintStmt"):
        ...


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: StmtVisitor):
        ...


@dataclass
class ExpressionStmt(Stmt):
    expression: Expr

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_expression_stmt(self)


@dataclass
class PrintStmt(Stmt):
    expression: Expr

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_print_stmt(self)
