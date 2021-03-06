from typing import Any, Dict, Optional

from .exceptions import LoxRuntimeError
from .token import Token


class Environment:
    def __init__(self, enclosing: Optional["Environment"] = None):
        self.values: Dict[str, Any] = {}
        self.enclosing = enclosing

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing is not None:
            return self.enclosing.assign(name, value)

        raise LoxRuntimeError(f"Undefined variable '{name.lexeme}'.", name)

    def define(self, key: str, value: Any) -> None:
        self.values[key] = value

    def get(self, token: Token) -> Any:
        if token.lexeme in self.values:
            return self.values[token.lexeme]

        if self.enclosing is not None:
            return self.enclosing.get(token)

        raise LoxRuntimeError(f"Undefined variable '{token.lexeme}'.", token)
