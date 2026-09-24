"""Unit tests for validators — run with: python -m pytest tests/"""
from dental_app.utils.validators import validate_email, validate_phone


def test_valid_phones():
    assert validate_phone("09123456789")
    assert validate_phone("09000000000")


def test_invalid_phones():
    assert not validate_phone("0912345678")     # too short
    assert not validate_phone("091234567890")   # too long
    assert not validate_phone("08123456789")    # wrong prefix
    assert not validate_phone("09abc456789")    # non-digits
    assert not validate_phone("")


def test_valid_emails():
    assert validate_email("user@example.com")
    assert validate_email("a.b-c@sub.domain.ph")


def test_invalid_emails():
    assert not validate_email("notanemail")
    assert not validate_email("missing@tld")
    assert not validate_email("")
