from pathlib import Path
from typing import List, Tuple

from jinja2 import Template

DIR = Path(__file__).parent

#         (class, [(var_name, var_type)])
AstNode = Tuple[str, List[Tuple[str, str]]]

EXPRESSIONS: List[AstNode] = [
    ("Assign", [("name", "Token"), ("value", "Expr")]),
    ("Binary", [("left", "Expr"), ("operator", "Any"), ("right", "Expr")]),
    ("Call", [("callee", "Expr"), ("paren", "Token"), ("arguments", "List[Expr]")]),
    ("Grouping", [("expression", "Expr")]),
    ("Literal", [("value", "Any")]),
    ("Logical", [("left", "Expr"), ("operator", "Token"), ("right", "Expr")]),
    ("Unary", [("operator", "Token"), ("right", "Expr")]),
    ("Variable", [("name", "Token")]),
]

STATEMENTS: List[AstNode] = [
    ("Block", [("statements", "List[Stmt]")]),
    ("Expression", [("expression", "Expr")]),
    (
        "Function",
        [("name", "Token"), ("params", "List[Token]"), ("body", "List[Stmt]")],
    ),
    (
        "If",
        [
            ("condition", "Expr"),
            ("then_branch", "Stmt"),
            ("else_branch", "Optional[Stmt]"),
        ],
    ),
    ("Print", [("expression", "Expr")]),
    ("Return", [("keyword", "Token"), ("value", "Optional[Expr]")]),
    ("Var", [("name", "Token"), ("intitializer", "Optional[Expr]")]),
    ("While", [("condition", "Expr"), ("body", "Stmt")]),
]


AST_TYPES = [("Expr", EXPRESSIONS), ("Stmt", STATEMENTS)]


def load_template():
    with open(DIR / "ast.jinja2") as f:
        return Template(f.read())


def main():
    template = load_template()

    with open(DIR / "pylox" / "ast.py", "w") as f:
        f.write(template.render(types=AST_TYPES))


if __name__ == "__main__":
    main()
