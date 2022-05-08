from typing import Any, Dict

from .exceptions import LoxRuntimeError
from .token import Token


class Environment:
    def __init__(self):
        self.values: Dict[str, Any] = {}

    def assign(self, name: Token, value: Any) -> None:
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        raise LoxRuntimeError(f"Undefined variable '{name.lexeme}'.", name)

    def define(self, key: str, value: Any) -> None:
        self.values[key] = value

    def get(self, token: Token) -> Any:
        try:
            return self.values[token.lexeme]
        except KeyError:
            raise LoxRuntimeError(f"Undefined variable '{token.lexeme}'.", token)
