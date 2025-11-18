"""
Field node for record/constructor fields.
"""

from typing import Iterator, Optional

from ...common.enums import NodeKind
from .node import Node
from .span import Span


class Field(Node):
    """
    Represents a field in a constructor or map declaration.

    Fields can be named or unnamed, and can have the 'any' modifier.

    Examples:
        x: Integer
        any Integer
        MyType
        name: any String
    """

    def __init__(self, span: Span, type_node: Node, name: Optional[str] = None, is_any: bool = False):
        """
        Create a field node.

        Args:
            span: Source location
            type_node: The field type (must be a type term)
            name: Optional field name
            is_any: Whether this field has the 'any' modifier

        Raises:
            AssertionError: If type_node is not a type term
        """
        assert type_node.is_type_term, "Type must be a type term"
        super().__init__(span)
        self._type = type_node
        self._name = name
        self._is_any = is_any

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.FIELD

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        return 1  # type

    @property
    def type_node(self) -> Node:
        """Get the type node."""
        return self._type

    @property
    def name(self) -> Optional[str]:
        """Get the field name (if any)."""
        return self._name

    @property
    def is_any(self) -> bool:
        """Check if this field has the 'any' modifier."""
        return self._is_any

    def children(self) -> Iterator[Node]:
        """Get all children."""
        yield self._type

    def __str__(self) -> str:
        """Get string representation."""
        any_str = "any " if self._is_any else ""
        if self._name:
            return f"{self._name}: {any_str}{self._type}"
        return f"{any_str}{self._type}"

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Field({self._name!r}, {self._type!r}, any={self._is_any})"
