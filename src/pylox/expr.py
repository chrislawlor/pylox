# This file is generated via generate_ast.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol

from .token import Token


class Visitor(Protocol):
    def visitBinaryExpr(self, expr: "Binary"):
        ...

    def visitGroupingExpr(self, expr: "Grouping"):
        ...

    def visitLiteralExpr(self, expr: "Literal"):
        ...

    def visitUnaryExpr(self, expr: "Unary"):
        ...


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor):
        ...


@dataclass
class Binary(Expr):
    left: Expr
    operator: Any
    right: Expr

    def accept(self, visitor: Visitor):
        visitor.visit_binary_expr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: Visitor):
        visitor.visit_grouping_expr(self)


@dataclass
class Literal(Expr):
    value: Any

    def accept(self, visitor: Visitor):
        visitor.visit_literal_expr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor):
        visitor.visit_unary_expr(self)