import pytest

from pylox.lox import Lox
from pylox.scanner import Scanner
from pylox.token import TokenType as T


def get_scanner(source: str) -> Scanner:
    return Scanner(Lox(), source)


@pytest.mark.parametrize(
    "char,expected",
    [("a", True), ("1", False), ("A", True), ("_", True), ("z", True), ("Z", True)],
)
def test_is_alpha(char: str, expected: bool):
    scanner = get_scanner("")
    assert scanner._is_alpha(char) is expected


def test_is_at_end():
    scanner = get_scanner("")
    assert scanner._is_at_end() is True

    scanner = get_scanner("{")
    assert scanner._is_at_end() is False
    char = scanner._advance()
    assert char == "{"
    assert scanner._is_at_end() is True


def test_match():
    scanner = get_scanner("{")
    is_match = scanner._match("{")
    assert is_match is True
    assert scanner.current == 1
    assert scanner._is_at_end() is True

    scanner = get_scanner("{{")
    is_match = scanner._match("{")
    assert is_match is True
    assert scanner.current == 1
    assert scanner._is_at_end() is False

    scanner = get_scanner("/")
    is_match = scanner._match("{")
    assert is_match is False
    assert scanner.current == 0


def test_scan_token_by_token():
    scanner = get_scanner("+-*")
    scanner._scan_token()
    assert [t.type_ for t in scanner.tokens] == [T.PLUS]
    scanner._scan_token()
    assert [t.type_ for t in scanner.tokens] == [T.PLUS, T.MINUS]
    scanner._scan_token()
    assert [t.type_ for t in scanner.tokens] == [T.PLUS, T.MINUS, T.STAR]


def test_scan_token_by_token_with_slash():
    scanner = get_scanner("/-")
    scanner._scan_token()
    assert [t.type_ for t in scanner.tokens] == [T.SLASH]
    scanner._scan_token()
    assert [t.type_ for t in scanner.tokens] == [T.SLASH, T.MINUS]


def test_string():
    scanner = get_scanner('"string"')
    scanner.scan_tokens()
    assert len(scanner.tokens) == 2
    token = scanner.tokens[0]
    assert token.type_ == T.STRING
    assert token.lexeme == '"string"'
    assert token.literal == "string"


def test_number_int():
    scanner = get_scanner("123")
    scanner.scan_tokens()
    assert len(scanner.tokens) == 2
    token = scanner.tokens[0]
    assert token.type_ == T.NUMBER
    assert token.lexeme == "123"
    assert token.literal == 123


def test_number_float():
    scanner = get_scanner("123.0")
    scanner.scan_tokens()
    assert len(scanner.tokens) == 2
    token = scanner.tokens[0]
    assert token.type_ == T.NUMBER
    assert token.lexeme == "123.0"
    assert token.literal == 123.0


@pytest.mark.parametrize(
    "source,expected_token_types",
    [
        ("{}", [T.LEFT_BRACE, T.RIGHT_BRACE, T.EOF]),
        ("()", [T.LEFT_PAREN, T.RIGHT_PAREN, T.EOF]),
        ("+-", [T.PLUS, T.MINUS, T.EOF]),
        ("/", [T.SLASH, T.EOF]),
        ("// This is a comment", [T.EOF]),
        ("==", [T.EQUAL_EQUAL, T.EOF]),
        ("<=", [T.LESS_EQUAL, T.EOF]),
        (">=", [T.GREATER_EQUAL, T.EOF]),
        ("!=", [T.BANG_EQUAL, T.EOF]),
        ("\t\r", [T.EOF]),
        ('"string"', [T.STRING, T.EOF]),
        ("123", [T.NUMBER, T.EOF]),
        ("or", [T.OR, T.EOF]),
        ("print", [T.PRINT, T.EOF]),
    ],
)
def test_scan_tokens(source, expected_token_types):
    scanner = get_scanner(source)
    tokens = scanner.scan_tokens()
    token_types = [t.type_ for t in tokens]
    assert token_types == expected_token_types
