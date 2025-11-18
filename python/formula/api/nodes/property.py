"""
Property node for machine properties.
"""

from typing import Iterator, Optional

from ...common.enums import NodeKind
from .node import Node
from .config import Config
from .span import Span


class Property(Node):
    """
    Represents a property definition in a machine.

    Properties define assertions about machine states.

    Examples:
        property SafeState = isValid(s).
    """

    def __init__(self, span: Span, name: str, definition: Node):
        """
        Create a property node.

        Args:
            span: Source location
            name: The property name
            definition: The property definition (must be function or atom)

        Raises:
            AssertionError: If name is empty or definition is not function/atom
        """
        assert name and name.strip(), "Property name cannot be empty"
        assert definition.is_func_or_atom, "Definition must be a function or atom"
        super().__init__(span)
        self._name = name
        self._definition = definition
        self._config: Optional[Config] = None

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.PROPERTY

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        count = 1  # definition
        if self._config is not None:
            count += 1
        return count

    @property
    def name(self) -> str:
        """Get the property name."""
        return self._name

    @property
    def definition(self) -> Node:
        """Get the property definition."""
        return self._definition

    @property
    def config(self) -> Optional[Config]:
        """Get the configuration (if any)."""
        return self._config

    @config.setter
    def config(self, value: Optional[Config]):
        """Set the configuration."""
        self._config = value

    def children(self) -> Iterator[Node]:
        """Get all children."""
        if self._config is not None:
            yield self._config
        yield self._definition

    def __str__(self) -> str:
        """Get string representation."""
        return f"property {self._name} = {self._definition}."

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Property({self._name!r}, {self._definition!r})"
