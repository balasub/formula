"""
Step node for machine boot sequences and transform systems.
"""

from typing import List, Iterator, Optional

from ...common.enums import NodeKind
from .node import Node
from .id import Id
from .mod_apply import ModApply
from .config import Config
from .span import Span


class Step(Node):
    """
    Represents a step in a machine boot sequence or transform system.

    Steps assign the result of a module application to state variables.

    Examples:
        s1 = Transform1().
        s1, s2 = Transform2(x, y).
    """

    def __init__(self, span: Span, rhs: ModApply):
        """
        Create a step node.

        Args:
            span: Source location
            rhs: The module application on the right-hand side
        """
        super().__init__(span)
        self._lhs: List[Id] = []
        self._rhs = rhs
        self._config: Optional[Config] = None

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.STEP

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        count = 1 + len(self._lhs)  # rhs + lhs ids
        if self._config is not None:
            count += 1
        return count

    @property
    def lhs(self) -> List[Id]:
        """Get the left-hand side identifiers."""
        return self._lhs

    @property
    def rhs(self) -> ModApply:
        """Get the right-hand side module application."""
        return self._rhs

    @rhs.setter
    def rhs(self, value: ModApply):
        """Set the right-hand side."""
        self._rhs = value

    @property
    def config(self) -> Optional[Config]:
        """Get the configuration (if any)."""
        return self._config

    @config.setter
    def config(self, value: Optional[Config]):
        """Set the configuration."""
        self._config = value

    def add_lhs(self, id_node: Id, add_last: bool = True):
        """
        Add a left-hand side identifier.

        Args:
            id_node: The identifier
            add_last: If True, add at end; if False, add at beginning
        """
        if add_last:
            self._lhs.append(id_node)
        else:
            self._lhs.insert(0, id_node)

    def children(self) -> Iterator[Node]:
        """Get all children."""
        if self._config is not None:
            yield self._config
        for id_node in self._lhs:
            yield id_node
        yield self._rhs

    def __str__(self) -> str:
        """Get string representation."""
        if not self._lhs:
            return f"{self._rhs}."
        lhs_str = ", ".join(str(id_node) for id_node in self._lhs)
        return f"{lhs_str} = {self._rhs}."

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Step({len(self._lhs)} lhs, rhs={self._rhs!r})"
