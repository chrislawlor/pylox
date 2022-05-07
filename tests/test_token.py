from pylox.token import Token
from pylox.token import TokenType as T


def test_token_repr():
    token = Token(T.BANG_EQUAL, "!=", None, 1)

    value = repr(token)

    assert value == 'Token(BANG_EQUAL, "!=", None, line=1)'


def test_token_repr_number():
    token = Token(T.NUMBER, "1.0", 1.0, line=1)

    value = repr(token)

    assert value == 'Token(NUMBER, "1.0", 1.0, line=1)'


def test_token_str():
    token = Token(T.BANG_EQUAL, "!=", None, 1)

    value = str(token)

    assert value == "BANG_EQUAL"


def test_token_str_with_literal():
    token = Token(T.STRING, '"string"', "string", line=1)

    value = str(token)

    assert value == 'STRING["string"]'
