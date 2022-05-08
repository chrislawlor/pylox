from .token import Token


class LoxRuntimeError(Exception):
    def __init__(self, message, token: Token):
        super().__init__(message)
        self.token = token


class ParseError(Exception):
    pass
