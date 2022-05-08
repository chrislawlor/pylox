from io import StringIO

import pytest

from pylox.lox import Lox


@pytest.fixture
def lox():
    out = StringIO()
    err = StringIO()
    return Lox(out=out, err=err)


@pytest.mark.parametrize(
    "statement", ["var a;", "print 1 + 2;", "1 + 3;", '"one" + "two";']
)
def test_run_valid_statements(lox, statement):
    lox.run(statement)
