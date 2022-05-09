from typing import Tuple

import pytest

from pylox.environment import Environment
from pylox.exceptions import LoxRuntimeError
from pylox.token import Token
from pylox.token import TokenType as T


@pytest.fixture
def environments() -> Tuple[Environment, Environment]:
    global_env = Environment()
    scope_env = Environment(enclosing=global_env)
    return global_env, scope_env


def get_token(lexeme: str) -> Token:
    return Token(T.VAR, lexeme=lexeme, literal=None, line=1)


def test_define_var(environments: Tuple[Environment, Environment]):
    outer, _ = environments
    value = object()

    outer.define("a", value)

    assert "a" in outer.values
    assert outer.values["a"] == value


def test_can_redefine_var(environments: Tuple[Environment, Environment]):
    outer, _ = environments
    value1 = object()
    value2 = object()
    assert value1 != value2
    outer.define("a", value1)
    outer.define("a", value2)

    assert "a" in outer.values
    assert outer.values["a"] == value2


def test_cannot_assign_undefined_var(environments: Tuple[Environment, Environment]):
    outer, _ = environments
    a = get_token("a")

    with pytest.raises(LoxRuntimeError):
        outer.assign(a, object())


def test_can_assign_defined_var(environments: Tuple[Environment, Environment]):
    outer, _ = environments
    value1 = object()
    value2 = object()
    assert value1 != value2
    outer.define("a", value1)
    assert outer.values["a"] == value1
    a = get_token("a")
    outer.assign(a, value2)

    assert outer.values["a"] == value2


def test_can_retrive_var_from_outer_scope(
    environments: Tuple[Environment, Environment]
):
    outer, inner = environments
    value = object()
    outer.define("a", value)
    a = get_token("a")

    retrieved = inner.get(a)

    assert retrieved == value


def test_inner_scope_shadows_outer_scope(environments: Tuple[Environment, Environment]):
    outer, inner = environments
    outer_val = object()
    inner_val = object()
    outer.define("a", outer_val)
    inner.define("a", inner_val)
    a = get_token("a")

    assert inner.get(a) == inner_val
    assert outer.get(a) == outer_val


def test_get_undefined_var_raises(environments: Tuple[Environment, Environment]):
    outer, _ = environments
    token = get_token("a")
    assert "a" not in outer.values

    with pytest.raises(LoxRuntimeError):
        outer.get(token)
