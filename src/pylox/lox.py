import sys
from pathlib import Path

from .scanner import Scanner


class Lox:
    PROMPT = "> "

    def __init__(self):
        self.had_error = False

    def run_file(self, path: Path):
        with open(path) as f:
            self.run(f.read())

        if self.had_error:
            sys.exit(65)

    def run_prompt(self):
        while True:
            source = input(self.PROMPT)
            self.run(source)
            self.had_error = False

    def run(self, source: str):
        scanner = Scanner(self, source)
        tokens = scanner.scan_tokens()

        # For now, just print the tokens
        for token in tokens:
            print(token)

    def error(self, line: int, message: str):
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str):
        print(f"[line {line}] Error{where}: {message}", file=sys.stdout)
        self.had_error = True
