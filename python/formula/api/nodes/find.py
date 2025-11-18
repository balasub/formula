"""
Find node for pattern matching constraints.
"""

from typing import Iterator, Optional

from ...common.enums import NodeKind
from .node import Node
from .id import Id
from .span import Span


class Find(Node):
    """
    Represents a pattern matching constraint in FORMULA.

    Find constraints match patterns and optionally bind results to variables.

    Examples:
        p(x)           (match pattern)
        y is q(x)      (match and bind to y)
    """

    def __init__(self, span: Span, match: Node, binding: Optional[Id] = None):
        """
        Create a find constraint.

        Args:
            span: Source location
            match: The pattern to match (must be function or atom)
            binding: Optional identifier to bind the match to

        Raises:
            AssertionError: If match is not a function or atom
        """
        assert match.is_func_or_atom, "Match must be a function or atom"
        super().__init__(span)
        self._match = match
        self._binding = binding

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.FIND

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        return 1 if self._binding is None else 2

    @property
    def match(self) -> Node:
        """Get the match pattern."""
        return self._match

    @property
    def binding(self) -> Optional[Id]:
        """Get the binding identifier (if any)."""
        return self._binding

    def children(self) -> Iterator[Node]:
        """Get all children."""
        if self._binding is not None:
            yield self._binding
        yield self._match

    def __str__(self) -> str:
        """Get string representation."""
        if self._binding:
            return f"{self._binding} is {self._match}"
        return str(self._match)

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Find({self._match!r}, binding={self._binding!r})"
