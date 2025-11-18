"""
RelConstr node for relational constraints in FORMULA.
"""

from typing import Iterator, Optional

from ...common.enums import NodeKind, RelKind
from .node import Node
from .span import Span


class RelConstr(Node):
    """
    Represents a relational constraint in FORMULA.

    Relational constraints compare two terms using operators like =, !=, <, >, etc.,
    or specify type membership with the : operator.

    Examples:
        x = y
        x > 5
        x : Integer
        no p(x)  (unary negation)
    """

    def __init__(self, span: Span, op: RelKind, arg1: Node, arg2: Optional[Node] = None):
        """
        Create a relational constraint.

        Args:
            span: Source location
            op: The relational operator
            arg1: The first argument (must be function or atom)
            arg2: The second argument (optional for unary ops, must be function or atom)

        Raises:
            AssertionError: If arguments are not functions or atoms
        """
        assert arg1.is_func_or_atom, "Arg1 must be a function or atom"
        if arg2 is not None:
            assert arg2.is_func_or_atom, "Arg2 must be a function or atom"
        super().__init__(span)
        self._op = op
        self._arg1 = arg1
        self._arg2 = arg2

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.REL_CONSTR

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        return 1 if self._arg2 is None else 2

    @property
    def op(self) -> RelKind:
        """Get the relational operator."""
        return self._op

    @property
    def arg1(self) -> Node:
        """Get the first argument."""
        return self._arg1

    @property
    def arg2(self) -> Optional[Node]:
        """Get the second argument (if any)."""
        return self._arg2

    def children(self) -> Iterator[Node]:
        """Get all children."""
        yield self._arg1
        if self._arg2 is not None:
            yield self._arg2

    def __str__(self) -> str:
        """Get string representation."""
        op_str = {
            RelKind.EQ: "=",
            RelKind.NEQ: "!=",
            RelKind.LT: "<",
            RelKind.LE: "<=",
            RelKind.GT: ">",
            RelKind.GE: ">=",
            RelKind.TYP: ":",
            RelKind.NO: "no",
        }.get(self._op, str(self._op))

        if self._arg2 is None:
            return f"{op_str} {self._arg1}"
        return f"{self._arg1} {op_str} {self._arg2}"

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"RelConstr({self._op}, {self._arg1!r}, {self._arg2!r})"
