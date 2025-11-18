"""
Body node for rule bodies and contract specifications in FORMULA.
"""

from typing import List, Iterator

from ...common.enums import NodeKind
from .node import Node
from .span import Span


class Body(Node):
    """
    Represents a rule body or contract specification in FORMULA.

    A body consists of a sequence of constraints separated by commas.
    Multiple bodies can be separated by semicolons in a rule.

    Examples:
        x > 0, y < 10
        p(x), q(y, z)
    """

    def __init__(self, span: Span):
        """
        Create a body node.

        Args:
            span: Source location
        """
        super().__init__(span)
        self._constraints: List[Node] = []

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.BODY

    @property
    def child_count(self) -> int:
        """Get the number of constraint children."""
        return len(self._constraints)

    @property
    def constraints(self) -> List[Node]:
        """Get the list of constraints."""
        return self._constraints

    def add_constraint(self, constraint: Node, add_last: bool = True):
        """
        Add a constraint to this body.

        Args:
            constraint: The constraint node
            add_last: If True, add at end; if False, add at beginning

        Raises:
            AssertionError: If node is not a constraint
        """
        assert constraint.is_constraint, "Node must be a constraint"
        if add_last:
            self._constraints.append(constraint)
        else:
            self._constraints.insert(0, constraint)

    def children(self) -> Iterator[Node]:
        """Get all constraint children."""
        return iter(self._constraints)

    def __str__(self) -> str:
        """Get string representation."""
        if not self._constraints:
            return ""
        return ", ".join(str(c) for c in self._constraints)

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Body({len(self._constraints)} constraints)"
