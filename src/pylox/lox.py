import sys
from functools import singledispatchmethod
from pathlib import Path
from typing import List

from .interpreter import Interpreter, LoxRuntimeError
from .parser import Parser
from .scanner import Scanner
from .token import Token
from .token import TokenType as T


class Lox:
    PROMPT = "> "

    def __init__(self, out=sys.stdout, err=sys.stderr):
        self.interpreter = Interpreter(self, out=out)
        self.had_error = False
        self.had_runtime_error = False
        self.out = out
        self.err = err

    def run_file(self, path: Path):
        with open(path) as f:
            self.run(f.read())

        if self.had_error:
            sys.exit(65)

        if self.had_runtime_error:
            sys.exit(70)

    def run_prompt(self):
        while True:
            source = input(self.PROMPT)
            if not source:
                continue
            tokens = self.scan(source)
            print(f"{tokens=}")
            parser = Parser(self, tokens)

            if T.SEMICOLON.value not in source:
                # Try evaluating as expression
                expr = parser.expression()
                value = self.interpreter.evaluate(expr)
                print(value, file=self.out)
            else:
                statements = parser.parse()
                self.interpreter.interpret(statements)
            self.had_error = False

    def run(self, source: str):
        tokens = self.scan(source)
        parser = Parser(self, tokens)

        statements = parser.parse()

        # Stop if there was a syntax error
        if self.had_error:
            return

        self.interpreter.interpret(statements)

    def scan(self, source: str) -> List[Token]:
        scanner = Scanner(self, source)
        return scanner.scan_tokens()

    @singledispatchmethod
    def error(self, arg, message: str):
        raise NotImplementedError("Invalid error argument.")

    @error.register
    def _(self, line: int, message: str):
        self.report(line, "", message)

    @error.register
    def _(self, token: Token, message: str):
        if token.type == T.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)

    def runtime_error(self, error: LoxRuntimeError):
        print(f"{error}\n[line {error.token.line}]", file=self.err)
        self.had_runtime_error = True

    def report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}", file=self.err)
        self.had_error = True
