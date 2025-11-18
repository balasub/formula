"""
Compr node for set comprehensions in FORMULA.
"""

from typing import List, Iterator

from ...common.enums import NodeKind
from .node import Node
from .body import Body
from .span import Span


class Compr(Node):
    """
    Represents a set comprehension in FORMULA.

    Comprehensions define sets using patterns and constraints.

    Examples:
        { p(x) | x > 0 }
        { f(x, y) | p(x), q(y) }
        { x }  (simple set)
    """

    def __init__(self, span: Span):
        """
        Create a comprehension node.

        Args:
            span: Source location
        """
        super().__init__(span)
        self._heads: List[Node] = []
        self._bodies: List[Body] = []

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.COMPR

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        return len(self._heads) + len(self._bodies)

    @property
    def heads(self) -> List[Node]:
        """Get the head terms."""
        return self._heads

    @property
    def bodies(self) -> List[Body]:
        """Get the constraint bodies."""
        return self._bodies

    def add_head(self, head: Node, add_last: bool = True):
        """
        Add a head term.

        Args:
            head: The head node (must be function or atom)
            add_last: If True, add at end; if False, add at beginning

        Raises:
            AssertionError: If head is not a function or atom
        """
        assert head.is_func_or_atom, "Head must be a function or atom"
        if add_last:
            self._heads.append(head)
        else:
            self._heads.insert(0, head)

    def add_body(self, body: Body, add_last: bool = True):
        """
        Add a constraint body.

        Args:
            body: The body node
            add_last: If True, add at end; if False, add at beginning
        """
        if add_last:
            self._bodies.append(body)
        else:
            self._bodies.insert(0, body)

    def children(self) -> Iterator[Node]:
        """Get all children."""
        for head in self._heads:
            yield head
        for body in self._bodies:
            yield body

    def __str__(self) -> str:
        """Get string representation."""
        heads_str = ", ".join(str(h) for h in self._heads)
        if not self._bodies:
            return f"{{ {heads_str} }}"
        bodies_str = "; ".join(str(b) for b in self._bodies)
        return f"{{ {heads_str} | {bodies_str} }}"

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Compr({len(self._heads)} heads, {len(self._bodies)} bodies)"
