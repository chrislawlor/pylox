# This file is generated via generate_ast.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Optional

from .token import Token


class ExprVisitor(ABC):
    @abstractmethod
    def visit_assign_expr(self, expr: "AssignExpr"):
        ...

    @abstractmethod
    def visit_binary_expr(self, expr: "BinaryExpr"):
        ...

    @abstractmethod
    def visit_call_expr(self, expr: "CallExpr"):
        ...

    @abstractmethod
    def visit_grouping_expr(self, expr: "GroupingExpr"):
        ...

    @abstractmethod
    def visit_literal_expr(self, expr: "LiteralExpr"):
        ...

    @abstractmethod
    def visit_logical_expr(self, expr: "LogicalExpr"):
        ...

    @abstractmethod
    def visit_unary_expr(self, expr: "UnaryExpr"):
        ...

    @abstractmethod
    def visit_variable_expr(self, expr: "VariableExpr"):
        ...


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor):
        ...


@dataclass(frozen=True)
class AssignExpr(Expr):
    name: Token
    value: Expr

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_assign_expr(self)


@dataclass(frozen=True)
class BinaryExpr(Expr):
    left: Expr
    operator: Any
    right: Expr

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_binary_expr(self)


@dataclass(frozen=True)
class CallExpr(Expr):
    callee: Expr
    paren: Token
    arguments: List[Expr]

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_call_expr(self)


@dataclass
class GroupingExpr(Expr):
    expression: Expr

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_grouping_expr(self)


@dataclass(frozen=True)
class LiteralExpr(Expr):
    value: Any

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_literal_expr(self)


@dataclass(frozen=True)
class LogicalExpr(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_logical_expr(self)


@dataclass(frozen=True)
class UnaryExpr(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_unary_expr(self)


@dataclass(frozen=True)
class VariableExpr(Expr):
    name: Token

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_variable_expr(self)


class StmtVisitor(ABC):
    @abstractmethod
    def visit_block_stmt(self, stmt: "BlockStmt"):
        ...

    @abstractmethod
    def visit_expression_stmt(self, stmt: "ExpressionStmt"):
        ...

    @abstractmethod
    def visit_function_stmt(self, stmt: "FunctionStmt"):
        ...

    @abstractmethod
    def visit_if_stmt(self, stmt: "IfStmt"):
        ...

    @abstractmethod
    def visit_print_stmt(self, stmt: "PrintStmt"):
        ...

    @abstractmethod
    def visit_var_stmt(self, stmt: "VarStmt"):
        ...

    @abstractmethod
    def visit_while_stmt(self, stmt: "WhileStmt"):
        ...


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor: StmtVisitor):
        ...


@dataclass(frozen=True)
class BlockStmt(Stmt):
    statements: List[Stmt]

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_block_stmt(self)


@dataclass(frozen=True)
class ExpressionStmt(Stmt):
    expression: Expr

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_expression_stmt(self)


@dataclass(frozen=True)
class FunctionStmt(Stmt):
    name: Token
    params: List[Token]
    body: List[Stmt]

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_function_stmt(self)


@dataclass
class IfStmt(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Optional[Stmt]

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_if_stmt(self)


@dataclass(frozen=True)
class PrintStmt(Stmt):
    expression: Expr

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_print_stmt(self)


@dataclass(frozen=True)
class VarStmt(Stmt):
    name: Token
    intitializer: Optional[Expr]

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_var_stmt(self)


@dataclass(frozen=True)
class WhileStmt(Stmt):
    condition: Expr
    body: Stmt

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_while_stmt(self)
