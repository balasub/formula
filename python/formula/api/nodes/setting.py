"""
Setting node for configuration key-value pairs.
"""

from typing import Iterator

from ...common.enums import NodeKind
from .node import Node
from .id import Id
from .cnst import Cnst
from .span import Span


class Setting(Node):
    """
    Represents a configuration setting in FORMULA.

    Settings are key-value pairs used in configuration blocks.

    Examples:
        solver = "Z3"
        timeout = 1000
        debug = TRUE
    """

    def __init__(self, span: Span, key: Id, value: Cnst):
        """
        Create a setting node.

        Args:
            span: Source location
            key: The setting key (identifier)
            value: The setting value (constant)
        """
        super().__init__(span)
        self._key = key
        self._value = value

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.SETTING

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        return 2  # key and value

    @property
    def key(self) -> Id:
        """Get the setting key."""
        return self._key

    @property
    def value(self) -> Cnst:
        """Get the setting value."""
        return self._value

    def children(self) -> Iterator[Node]:
        """Get all children."""
        yield self._key
        yield self._value

    def __str__(self) -> str:
        """Get string representation."""
        return f"{self._key} = {self._value}"

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Setting({self._key!r}, {self._value!r})"
