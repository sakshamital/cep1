"""Tests for SSRF prevention, IP filtering, and safe URL resolution."""
import pytest
from app.services.security_check import (
    SSRFValidationError,
    is_ip_blocked,
    validate_and_resolve_url,
)


def test_blocked_ip_ranges():
    """Verify private, loopback, and metadata IPs are detected as blocked."""
    assert is_ip_blocked("127.0.0.1") is True
    assert is_ip_blocked("127.0.1.5") is True
    assert is_ip_blocked("10.0.0.1") is True
    assert is_ip_blocked("192.168.1.100") is True
    assert is_ip_blocked("172.16.5.10") is True
    assert is_ip_blocked("169.254.169.254") is True  # Cloud metadata
    assert is_ip_blocked("::1") is True
    assert is_ip_blocked("0.0.0.0") is True

    # Public IP
    assert is_ip_blocked("8.8.8.8") is False
    assert is_ip_blocked("1.1.1.1") is False


def test_validate_url_schemes():
    """Verify non-http(s) schemes are blocked."""
    with pytest.raises(SSRFValidationError, match="scheme"):
        validate_and_resolve_url("file:///etc/passwd")

    with pytest.raises(SSRFValidationError, match="scheme"):
        validate_and_resolve_url("ftp://ftp.example.gov.in/data")

    with pytest.raises(SSRFValidationError, match="scheme"):
        validate_and_resolve_url("gopher://127.0.0.1:70")


def test_validate_prohibited_hostnames():
    """Verify localhost and internal hostnames are blocked."""
    with pytest.raises(SSRFValidationError):
        validate_and_resolve_url("http://localhost/admin")

    with pytest.raises(SSRFValidationError):
        validate_and_resolve_url("http://127.0.0.1:5000/api")

    with pytest.raises(SSRFValidationError):
        validate_and_resolve_url("http://169.254.169.254/latest/meta-data/")

    with pytest.raises(SSRFValidationError):
        validate_and_resolve_url("http://internal.service.local/status")


def test_validate_public_url():
    """Verify public URLs pass validation."""
    url, ip = validate_and_resolve_url("https://aaplesarkar.mahaonline.gov.in")
    assert url.startswith("https://")
    assert ip != ""
