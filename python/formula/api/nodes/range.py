"""
Range node for integer ranges in FORMULA.
"""

from typing import Iterator

from ...common.enums import NodeKind
from ...common.rational import Rational
from .node import Node
from .span import Span


class Range(Node):
    """
    Represents an integer range in FORMULA.

    Ranges are used in enumeration types to specify a continuous
    sequence of integers, e.g., 1..10.
    """

    def __init__(self, span: Span, end1: Rational, end2: Rational):
        """
        Create a range node.

        Args:
            span: Source location
            end1: First endpoint
            end2: Second endpoint

        Raises:
            AssertionError: If endpoints are not integers
        """
        assert end1.is_integer() and end2.is_integer(), "Range endpoints must be integers"

        super().__init__(span)

        # Order endpoints so lower <= upper
        if end1 <= end2:
            self._lower = end1
            self._upper = end2
        else:
            self._lower = end2
            self._upper = end1

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.RANGE

    @property
    def child_count(self) -> int:
        """Ranges have no children."""
        return 0

    @property
    def lower(self) -> Rational:
        """Get the lower bound (inclusive)."""
        return self._lower

    @property
    def upper(self) -> Rational:
        """Get the upper bound (inclusive)."""
        return self._upper

    def children(self) -> Iterator[Node]:
        """Get children (none for Range nodes)."""
        return iter([])

    def __str__(self) -> str:
        """Get string representation."""
        return f"{self._lower}..{self._upper}"

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Range({self._lower}, {self._upper})"
