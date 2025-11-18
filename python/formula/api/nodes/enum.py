"""
Enum node for enumeration types in FORMULA.
"""

from typing import List, Iterator

from ...common.enums import NodeKind
from .node import Node
from .span import Span


class Enum(Node):
    """
    Represents an enumeration type in FORMULA.

    Enumerations define finite sets of values.

    Examples:
        {red, green, blue}
        {1, 2, 3}
        {1..10}
        {"a", "b", "c"}
    """

    def __init__(self, span: Span):
        """
        Create an enumeration node.

        Args:
            span: Source location
        """
        super().__init__(span)
        self._elements: List[Node] = []

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.ENUM

    @property
    def child_count(self) -> int:
        """Get the number of element children."""
        return len(self._elements)

    @property
    def elements(self) -> List[Node]:
        """Get the list of elements."""
        return self._elements

    def add_element(self, element: Node, add_last: bool = True):
        """
        Add an element.

        Args:
            element: The element node (must be a valid enum element)
            add_last: If True, add at end; if False, add at beginning

        Raises:
            AssertionError: If element is not a valid enum element
        """
        assert element.is_enum_element, "Element must be a valid enum element"
        if add_last:
            self._elements.append(element)
        else:
            self._elements.insert(0, element)

    def children(self) -> Iterator[Node]:
        """Get all element children."""
        return iter(self._elements)

    def __str__(self) -> str:
        """Get string representation."""
        if not self._elements:
            return "{}"
        elements_str = ", ".join(str(e) for e in self._elements)
        return f"{{{elements_str}}}"

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Enum({len(self._elements)} elements)"
