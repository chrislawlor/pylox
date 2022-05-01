import pytest
from pylox.scanner import Scanner
from pylox.lox import Lox
from pylox.token import TokenType as T


def get_scanner(source: str) -> Scanner:
    return Scanner(Lox(), source)


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
    ],
)
def test_scan_tokens(source, expected_token_types):
    scanner = get_scanner(source)
    tokens = scanner.scan_tokens()
    token_types = [t.type_ for t in tokens]
    assert token_types == expected_token_types
