from pathlib import Path
from typing import List, Tuple

from jinja2 import Template

DIR = Path(__file__).parent


AstNode = Tuple[str, List[Tuple[str, str]]]

EXPRESSIONS: List[AstNode] = [
    ("Binary", [("left", "Expr"), ("operator", "Any"), ("right", "Expr")]),
    ("Grouping", [("expression", "Expr")]),
    ("Literal", [("value", "Any")]),
    ("Unary", [("operator", "Token"), ("right", "Expr")]),
]


ASTs = {"Expr": EXPRESSIONS}


def define_ast(template: Template, base_class: str, nodes=List[AstNode]):
    module_name = base_class.lower()
    with open(DIR / "pylox" / f"{module_name}.py", "w") as f:
        f.write(template.render(base_class=base_class, nodes=nodes))


def load_template():
    with open(DIR / "ast.jinja2") as f:
        return Template(f.read())


def main():
    template = load_template()

    for base_class, nodes in ASTs.items():
        define_ast(template, base_class, nodes)


if __name__ == "__main__":
    main()
