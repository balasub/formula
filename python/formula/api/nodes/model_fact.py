"""
ModelFact node for facts in models.
"""

from typing import Iterator, Optional

from ...common.enums import NodeKind
from .node import Node
from .id import Id
from .config import Config
from .span import Span


class ModelFact(Node):
    """
    Represents a fact in a FORMULA model.

    Facts can optionally bind the matched term to an identifier.

    Examples:
        foo(x, y).
        myFact is bar(1, 2).
    """

    def __init__(self, span: Span, match: Node, binding: Optional[Id] = None):
        """
        Create a model fact.

        Args:
            span: Source location
            match: The term being asserted (must be function or atom)
            binding: Optional identifier to bind the match to

        Raises:
            AssertionError: If match is not a function or atom
        """
        assert match.is_func_or_atom, "Match must be a function or atom"
        super().__init__(span)
        self._match = match
        self._binding = binding
        self._config: Optional[Config] = None

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.MODEL_FACT

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        count = 1  # match
        if self._binding is not None:
            count += 1
        if self._config is not None:
            count += 1
        return count

    @property
    def match(self) -> Node:
        """Get the matched term."""
        return self._match

    @property
    def binding(self) -> Optional[Id]:
        """Get the binding identifier (if any)."""
        return self._binding

    @property
    def config(self) -> Optional[Config]:
        """Get the configuration (if any)."""
        return self._config

    @config.setter
    def config(self, value: Optional[Config]):
        """Set the configuration."""
        self._config = value

    def children(self) -> Iterator[Node]:
        """Get all children (config, binding, and match)."""
        if self._config is not None:
            yield self._config
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
        return f"ModelFact({self._match!r}, binding={self._binding!r})"
