"""Dependency graph operations: cycle detection, closure, topological order."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.entities import Document


class CycleError(Exception):
    """Raised when a dependency cycle is found."""


def assert_acyclic(documents: dict[str, "Document"]) -> None:
    """DFS with white/grey/black colouring; raise CycleError if a cycle exists.

    White = unvisited, grey = in stack, black = done.
    """
    WHITE, GREY, BLACK = 0, 1, 2
    colour: dict[str, int] = {doc_id: WHITE for doc_id in documents}
    path: list[str] = []

    def dfs(node: str) -> None:
        colour[node] = GREY
        path.append(node)
        for neighbour in documents[node].prerequisites:
            if neighbour not in documents:
                continue  # Dangling ref — caught by integrity check
            if colour[neighbour] == GREY:
                # Found cycle — extract the cycle portion
                cycle_start = path.index(neighbour)
                cycle = path[cycle_start:] + [neighbour]
                raise CycleError(" → ".join(cycle))
            if colour[neighbour] == WHITE:
                dfs(neighbour)
        path.pop()
        colour[node] = BLACK

    for doc_id in documents:
        if colour[doc_id] == WHITE:
            dfs(doc_id)


def prerequisite_closure(doc_id: str, documents: dict[str, "Document"], max_depth: int = 20) -> set[str]:
    """Return the set of all transitive prerequisites of doc_id (excluding doc_id itself)."""
    visited: set[str] = set()

    def _recurse(node: str, depth: int) -> None:
        if depth > max_depth:
            return
        for prereq in documents.get(node, type("", (), {"prerequisites": []})()).prerequisites:  # type: ignore[attr-defined]
            if prereq not in visited and prereq in documents:
                visited.add(prereq)
                _recurse(prereq, depth + 1)

    _recurse(doc_id, 0)
    return visited


def _safe_prerequisites(doc_id: str, documents: dict[str, "Document"]) -> list[str]:
    doc = documents.get(doc_id)
    return doc.prerequisites if doc else []


def build_tree(
    doc_id: str, documents: dict[str, "Document"], max_depth: int = 6, _depth: int = 0
) -> dict:
    """Build a nested dependency tree for UI display."""
    doc = documents.get(doc_id)
    if doc is None:
        return {"id": doc_id, "name": doc_id, "children": []}
    children = []
    if _depth < max_depth:
        for prereq_id in doc.prerequisites:
            children.append(build_tree(prereq_id, documents, max_depth, _depth + 1))
    return {
        "id": doc.id,
        "name": doc.name,
        "kind": doc.kind,
        "verified": doc.verified,
        "children": children,
    }


def topological_order(doc_ids: list[str], documents: dict[str, "Document"]) -> list[str]:
    """Return doc_ids (and their prerequisites) in prerequisite-first order using Kahn's algorithm.

    Shared prerequisites appear only once. Ties broken by name (stable, deterministic).
    """
    # Expand to include transitive prerequisites
    all_ids: set[str] = set(doc_ids)
    for doc_id in doc_ids:
        all_ids |= prerequisite_closure(doc_id, documents)

    # Build adjacency (child -> parents) and in-degree in the subgraph
    # Edge: doc A *needs* doc B → B must come before A → B → A in topological order
    # In-degree counts: how many prerequisites each node has within the subgraph
    in_degree: dict[str, int] = {node: 0 for node in all_ids}
    dependents: dict[str, list[str]] = {node: [] for node in all_ids}  # prereq -> [nodes that need it]

    for node in all_ids:
        for prereq in _safe_prerequisites(node, documents):
            if prereq in all_ids:
                in_degree[node] += 1
                dependents[prereq].append(node)

    # Kahn's algorithm — start with nodes of in-degree 0 (leaves), sorted by name
    queue = sorted(
        [node for node in all_ids if in_degree[node] == 0],
        key=lambda x: documents[x].name if x in documents else x,
    )
    result: list[str] = []
    while queue:
        node = queue.pop(0)
        result.append(node)
        for dependent in sorted(dependents[node], key=lambda x: documents[x].name if x in documents else x):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
                queue.sort(key=lambda x: documents[x].name if x in documents else x)

    return result
