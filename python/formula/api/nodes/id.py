"""
Id node for FORMULA identifiers.
"""

from typing import List, Iterator

from ...common.enums import NodeKind
from ...common.immutable_array import ImmutableArray
from .node import Node
from .span import Span


class Id(Node):
    """
    Represents an identifier in FORMULA.

    Identifiers can be simple (e.g., "foo") or qualified (e.g., "foo.bar.baz").
    """

    def __init__(self, span: Span, name: str):
        """
        Create an identifier node.

        Args:
            span: Source location
            name: The identifier name (may be qualified with dots)

        Raises:
            AssertionError: If name is empty or whitespace
        """
        assert name and name.strip(), "Identifier name cannot be empty"
        super().__init__(span)
        self._name = name
        self._fragments = ImmutableArray(name.split('.'))

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.ID

    @property
    def child_count(self) -> int:
        """Identifiers have no children."""
        return 0

    @property
    def name(self) -> str:
        """Get the full identifier name."""
        return self._name

    @property
    def fragments(self) -> ImmutableArray[str]:
        """Get the identifier fragments (split by dots)."""
        return self._fragments

    @property
    def is_qualified(self) -> bool:
        """Check if this is a qualified identifier (contains dots)."""
        return len(self._fragments) > 1

    def unqualify(self) -> 'Id':
        """
        Remove the first component of a qualified identifier.

        Returns:
            A new Id without the first fragment, or self if not qualified
        """
        if len(self._fragments) == 1:
            return self

        sub_str = '.'.join(str(f) for f in self._fragments[1:])
        return Id(self.span, sub_str)

    def children(self) -> Iterator[Node]:
        """Get children (none for Id nodes)."""
        return iter([])

    def __str__(self) -> str:
        """Get string representation."""
        return self._name

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Id({self._name!r})"
