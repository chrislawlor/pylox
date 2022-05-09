from io import StringIO

import pytest

from pylox.lox import Lox


@pytest.fixture
def lox():
    out = StringIO()
    err = StringIO()
    return Lox(out=out, err=err)


@pytest.mark.parametrize(
    "program", ["var a;", "print 1 + 2;", "1 + 3;", '"one" + "two";', "var a; a = 1;"]
)
def test_run_valid_programs(lox: Lox, program):
    lox.run(program)

    errors = lox.err.getvalue()

    assert errors == ""
