"""Security validators for official source monitoring: SSRF shield, domain allowlisting, and safe redirects."""
from __future__ import annotations

import ipaddress
import logging
import re
import socket
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

# RFC1918, link-local, loopback, and cloud metadata IP ranges to strictly block
_BLOCKED_NETWORKS = [
    ipaddress.ip_network("0.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # AWS/GCP/Azure link-local metadata
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("224.0.0.0/4"),
    ipaddress.ip_network("240.0.0.0/4"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),        # IPv6 unique local
    ipaddress.ip_network("fe80::/10"),       # IPv6 link-local
]

# Prohibited hostnames
_PROHIBITED_HOSTNAMES = {
    "localhost",
    "metadata.google.internal",
    "instance-data",
    "169.254.169.254",
}


class SSRFValidationError(Exception):
    """Raised when a URL attempts to target a private, loopback, or unauthorized IP."""


def is_ip_blocked(ip_str: str) -> bool:
    """Check if an IP address string falls inside blocked/private network ranges."""
    try:
        ip = ipaddress.ip_address(ip_str)
        for net in _BLOCKED_NETWORKS:
            if ip in net:
                return True
        return False
    except ValueError:
        return True


def validate_and_resolve_url(url: str, allowed_schemes: tuple = ("http", "https")) -> tuple[str, str]:
    """Validate a URL against SSRF vulnerabilities and resolve to its public IP.
    
    Returns (cleaned_url, resolved_ip).
    Raises SSRFValidationError on forbidden scheme, private/loopback IP, or resolution failure.
    """
    if not url or not isinstance(url, str):
        raise SSRFValidationError("URL must be a non-empty string.")

    url = url.strip()
    parsed = urlparse(url)

    if parsed.scheme.lower() not in allowed_schemes:
        raise SSRFValidationError(f"Invalid URL scheme '{parsed.scheme}'. Only {allowed_schemes} are permitted.")

    hostname = parsed.hostname
    if not hostname:
        raise SSRFValidationError("URL must include a valid hostname.")

    hostname_lower = hostname.lower()

    if hostname_lower in _PROHIBITED_HOSTNAMES:
        raise SSRFValidationError(f"Access to prohibited hostname '{hostname}' is blocked.")

    if hostname_lower.endswith(".local") or hostname_lower.endswith(".internal"):
        raise SSRFValidationError(f"Internal domain name '{hostname}' is blocked.")

    # Check if hostname itself is directly an IP literal
    try:
        ip_obj = ipaddress.ip_address(hostname)
        if is_ip_blocked(str(ip_obj)):
            raise SSRFValidationError(f"Destination IP '{hostname}' belongs to a reserved or private network.")
        return url, str(ip_obj)
    except ValueError:
        pass  # Not an IP literal, proceed to DNS resolution

    # Resolve via DNS to verify target IP is public
    try:
        addr_info = socket.getaddrinfo(hostname, parsed.port or (443 if parsed.scheme == "https" else 80), proto=socket.IPPROTO_TCP)
        if not addr_info:
            raise SSRFValidationError(f"Could not resolve hostname '{hostname}'.")

        resolved_ips = []
        for family, _, _, _, sockaddr in addr_info:
            resolved_ip = sockaddr[0]
            resolved_ips.append(resolved_ip)
            if is_ip_blocked(resolved_ip):
                raise SSRFValidationError(
                    f"Hostname '{hostname}' resolves to private/reserved IP '{resolved_ip}'. Access blocked."
                )

        primary_ip = resolved_ips[0] if resolved_ips else ""
        return url, primary_ip
    except socket.gaierror as e:
        raise SSRFValidationError(f"DNS lookup failed for '{hostname}': {e}") from e
