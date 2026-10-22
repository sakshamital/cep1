"""Request validation helpers."""
from __future__ import annotations

import re

_ID_RE = re.compile(r"^[a-z0-9_]{1,64}$")
_CONTROL_RE = re.compile(r"[\x00-\x1F\x7F]")
VALID_STATUSES = {"available", "missing"}


class ValidationError(Exception):
    """Raised when request data fails validation."""

    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.details = details or {}


def validate_query(q: str) -> str:
    """Validate and clean a search query string. Returns cleaned string."""
    if not isinstance(q, str):
        raise ValidationError("Query must be a string")
    q = _CONTROL_RE.sub("", q)
    if len(q) > 80:
        raise ValidationError("Query is too long (max 80 characters)")
    return q


def validate_id(value: str, field: str = "id") -> str:
    """Validate that a value matches the expected ID format."""
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a string")
    if not _ID_RE.match(value):
        raise ValidationError(
            f"Invalid {field} format. Must match ^[a-z0-9_]{{1,64}}$",
            {"field": field, "value": value},
        )
    return value


def validate_statuses(statuses: object) -> dict[str, str]:
    """Validate the statuses dict from a readiness request body."""
    if not isinstance(statuses, dict):
        raise ValidationError("'statuses' must be a JSON object", {"field": "statuses"})
    if len(statuses) > 200:
        raise ValidationError("Too many status entries (max 200)", {"field": "statuses"})
    for key, val in statuses.items():
        if not isinstance(key, str) or not _ID_RE.match(key):
            raise ValidationError(
                f"Invalid document id in statuses: {key!r}",
                {"field": "statuses", "key": key},
            )
        if val not in VALID_STATUSES:
            raise ValidationError(
                f"Invalid status value {val!r} for '{key}'. Must be 'available' or 'missing'.",
                {"field": "statuses", "key": key, "value": val},
            )
    return statuses  # type: ignore[return-value]


def validate_category(category: object, allowed: list[str]) -> str | None:
    """Validate an applicant category against allowed values."""
    if category is None:
        return None
    if not isinstance(category, str):
        raise ValidationError("'applicant_category' must be a string")
    if allowed and category not in allowed:
        raise ValidationError(
            f"Invalid applicant_category {category!r}. Allowed: {allowed}",
            {"field": "applicant_category", "allowed": allowed},
        )
    return category


def validate_limit(limit: object, default: int = 8, maximum: int = 50) -> int:
    """Validate and clamp the 'limit' query parameter."""
    if limit is None:
        return default
    try:
        val = int(limit)
    except (TypeError, ValueError):
        raise ValidationError("'limit' must be an integer")
    return max(1, min(val, maximum))
