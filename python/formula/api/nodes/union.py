"""
Union node for type unions in FORMULA.
"""

from typing import List, Iterator

from ...common.enums import NodeKind
from .node import Node
from .span import Span


class Union(Node):
    """
    Represents a type union in FORMULA.

    Unions combine multiple type components using the + operator.

    Examples:
        Integer + Real
        {a, b, c} + String
        Foo + Bar + Baz
    """

    def __init__(self, span: Span):
        """
        Create a union node.

        Args:
            span: Source location
        """
        super().__init__(span)
        self._components: List[Node] = []

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.UNION

    @property
    def child_count(self) -> int:
        """Get the number of component children."""
        return len(self._components)

    @property
    def components(self) -> List[Node]:
        """Get the list of union components."""
        return self._components

    def add_component(self, component: Node, add_last: bool = True):
        """
        Add a component to this union.

        Args:
            component: The component node (must be a union component type)
            add_last: If True, add at end; if False, add at beginning

        Raises:
            AssertionError: If component is not a valid union component
        """
        assert component.is_union_component, "Node must be a union component"
        if add_last:
            self._components.append(component)
        else:
            self._components.insert(0, component)

    def children(self) -> Iterator[Node]:
        """Get all component children."""
        return iter(self._components)

    def __str__(self) -> str:
        """Get string representation."""
        if not self._components:
            return "Empty"
        return " + ".join(str(c) for c in self._components)

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Union({len(self._components)} components)"
