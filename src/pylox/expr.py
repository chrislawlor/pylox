# This file is generated via generate_ast.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from .token import Token


class Visitor(ABC):
    @abstractmethod
    def visit_binary_expr(self, expr: "Binary"):
        ...

    @abstractmethod
    def visit_grouping_expr(self, expr: "Grouping"):
        ...

    @abstractmethod
    def visit_literal_expr(self, expr: "Literal"):
        ...

    @abstractmethod
    def visit_unary_expr(self, expr: "Unary"):
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
        return visitor.visit_binary_expr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_grouping_expr(self)


@dataclass
class Literal(Expr):
    value: Any

    def accept(self, visitor: Visitor):
        return visitor.visit_literal_expr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: Visitor):
        return visitor.visit_unary_expr(self)
