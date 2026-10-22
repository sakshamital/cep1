"""Search service: normalisation, synonym expansion, scoring, typo tolerance."""
from __future__ import annotations

import difflib
import re
import unicodedata
from typing import Optional

from app.models.entities import SearchHit
from app.services.repository import get_repo

_PUNCT_RE = re.compile(r"[^\w\s]", re.UNICODE)


def _normalise(text: str) -> str:
    """Lowercase, Unicode NFKD normalise, strip punctuation and extra spaces."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = _PUNCT_RE.sub(" ", text)
    return re.sub(r"\s+", " ", text).strip()


def _tokenise(text: str) -> list[str]:
    return _normalise(text).split()


def _expand_synonyms(tokens: list[str], synonyms: dict[str, list[str]]) -> list[str]:
    """Expand each token using synonym map, adding synonyms as extra tokens."""
    expanded = list(tokens)
    for token in tokens:
        for syn in synonyms.get(token, []):
            norm_syns = _tokenise(syn)
            for ns in norm_syns:
                if ns not in expanded:
                    expanded.append(ns)
    return expanded


def _score(
    query_norm: str,
    query_tokens: list[str],
    target_name: str,
    target_aliases: list[str],
) -> tuple[float, str]:
    """Compute a relevance score and the field matched on.

    Returns (score, matched_on) where matched_on is 'name', 'alias', 'tokens', 'fuzzy'.
    """
    name_norm = _normalise(target_name)
    alias_norms = [_normalise(a) for a in target_aliases]

    # Exact match
    if query_norm == name_norm:
        return 100.0, "name"
    for alias in alias_norms:
        if query_norm == alias:
            return 100.0, "alias"

    # Starts with
    if name_norm.startswith(query_norm):
        return 85.0, "name"
    for alias in alias_norms:
        if alias.startswith(query_norm):
            return 85.0, "alias"

    # All query tokens present
    name_tokens = set(_tokenise(name_norm))
    all_aliases_tokens = set()
    for alias in alias_norms:
        all_aliases_tokens |= set(_tokenise(alias))

    q_set = set(query_tokens)
    if q_set and q_set <= name_tokens:
        coverage = len(q_set) / len(name_tokens) if name_tokens else 0
        return 70.0 + coverage * 10, "name"
    if q_set and q_set <= all_aliases_tokens:
        return 70.0, "alias"

    # Partial overlap (Jaccard)
    combined_tokens = name_tokens | all_aliases_tokens
    if combined_tokens and q_set:
        jaccard = len(q_set & combined_tokens) / len(q_set | combined_tokens)
        if jaccard > 0:
            return 50.0 * jaccard, "name"

    # Fuzzy match (token level)
    best_ratio = 0.0
    for q_tok in query_tokens:
        for t_tok in combined_tokens:
            ratio = difflib.SequenceMatcher(None, q_tok, t_tok).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
    if best_ratio >= 0.72:
        return 40.0 * best_ratio, "fuzzy"

    return 0.0, ""


def search(
    query: str,
    type_filter: Optional[str] = None,
    limit: int = 8,
) -> list[SearchHit]:
    """Search services and documents by query string.

    Returns a sorted list of SearchHit objects (score descending, then name).
    Empty or <2 character queries return [].
    """
    q = query.strip()
    if len(q) < 2:
        return []

    repo = get_repo()
    synonyms = repo.get_synonyms()
    q_norm = _normalise(q)
    q_tokens = _expand_synonyms(_tokenise(q_norm), synonyms)

    hits: list[SearchHit] = []

    # Search services
    if type_filter in (None, "service"):
        for svc in repo.get_all_services().values():
            score, matched_on = _score(q_norm, q_tokens, svc.name, svc.aliases)
            if score >= 30:
                hits.append(SearchHit(
                    id=svc.id,
                    name=svc.name,
                    kind="service",
                    score=score,
                    matched_on=matched_on,
                    description=svc.description[:120] if svc.description else "",
                    type=svc.type,
                ))

    # Search documents
    if type_filter in (None, "document"):
        for doc in repo.get_all_documents().values():
            score, matched_on = _score(q_norm, q_tokens, doc.name, doc.aliases)
            if score >= 30:
                used_by_ids = repo.get_services_using_document(doc.id)
                used_by = []
                for sid in used_by_ids:
                    s = repo.get_service(sid)
                    if s:
                        used_by.append({"id": s.id, "name": s.name})
                hits.append(SearchHit(
                    id=doc.id,
                    name=doc.name,
                    kind="document",
                    score=score,
                    matched_on=matched_on,
                    description=doc.description[:120] if doc.description else "",
                    type=doc.kind,
                    used_by_services=used_by,
                ))

    # Sort: score desc, then name asc
    hits.sort(key=lambda h: (-h.score, h.name))
    return hits[:limit]
