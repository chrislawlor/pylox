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


@pytest.mark.parametrize(
    "program,expected",
    [
        ("print -1;", "-1"),
        ('print "A" or "B";', "A"),
        ('print false or "A";', "A"),
        ('print "A" and "B";', "B"),
        ('print false and "A";', "false"),
        ("var a = 1;print a;", "1"),
        ("var a = 3 - 2;print a;", "1"),
        ("var a = 0; a = a + 1;print a;", "1"),
        ("var a = 1;{var a = 2;print a;}print a;", "2\n1"),
        ("if (true) print true; else print false;", "true"),
        ("if (false) print false; else print true;", "true"),
        ("var a = 0;while (a < 2) { print a;a = a + 1; }", "0\n1"),
        ("for (var a = 1; a < 3; a = a + 1) { print a; }", "1\n2"),
    ],
)
def test_program_for_expected_output(lox: Lox, program: str, expected: str):
    lox.run(program)

    out = lox.out.getvalue()[:-1]  # Strip the newline

    assert out == expected
