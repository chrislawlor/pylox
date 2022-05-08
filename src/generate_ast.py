from pathlib import Path
from typing import List, Tuple

from jinja2 import Template

DIR = Path(__file__).parent

#         (class, [(var_name, var_type)])
AstNode = Tuple[str, List[Tuple[str, str]]]

EXPRESSIONS: List[AstNode] = [
    ("Assign", [("name", "Token"), ("value", "Expr")]),
    ("Binary", [("left", "Expr"), ("operator", "Any"), ("right", "Expr")]),
    ("Grouping", [("expression", "Expr")]),
    ("Literal", [("value", "Any")]),
    ("Unary", [("operator", "Token"), ("right", "Expr")]),
    ("Variable", [("name", "Token")]),
]

STATEMENTS: List[AstNode] = [
    ("Expression", [("expression", "Expr")]),
    ("Print", [("expression", "Expr")]),
    ("Var", [("name", "Token"), ("intitializer", "Optional[Expr]")]),
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
