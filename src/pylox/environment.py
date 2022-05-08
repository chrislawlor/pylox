from typing import Any

from .exceptions import LoxRuntimeError
from .token import Token


class Environment(dict):
    def __getitem__(self, token: Token) -> Any:
        try:
            return super().__getitem__(token.lexeme)
        except KeyError:
            raise LoxRuntimeError(f"Undefined variable '{token.lexeme}'.", token)

    def __setitem__(self, key: str, value: Any) -> None:
        return super().__setitem__(key, value)
