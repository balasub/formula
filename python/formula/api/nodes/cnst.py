"""
Cnst node for FORMULA constants.
"""

from typing import Iterator, Union

from ...common.enums import NodeKind, CnstKind
from ...common.rational import Rational
from .node import Node
from .span import Span


class Cnst(Node):
    """
    Represents a constant value in FORMULA.

    Constants can be either numeric (Rational) or string values.
    """

    def __init__(self, span: Span, value: Union[Rational, str]):
        """
        Create a constant node.

        Args:
            span: Source location
            value: The constant value (Rational or string)
        """
        super().__init__(span)

        if isinstance(value, Rational):
            self._raw = value
            self._cnst_kind = CnstKind.NUMERIC
        elif isinstance(value, str):
            self._raw = value
            self._cnst_kind = CnstKind.STRING
        else:
            raise TypeError(f"Invalid constant type: {type(value)}")

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.CNST

    @property
    def child_count(self) -> int:
        """Constants have no children."""
        return 0

    @property
    def cnst_kind(self) -> CnstKind:
        """Get the kind of constant."""
        return self._cnst_kind

    @property
    def raw(self) -> Union[Rational, str]:
        """Get the raw constant value."""
        return self._raw

    def get_numeric_value(self) -> Rational:
        """
        Get the numeric value.

        Returns:
            The Rational value

        Raises:
            AssertionError: If this is not a numeric constant
        """
        assert self._cnst_kind == CnstKind.NUMERIC, "Not a numeric constant"
        return self._raw  # type: ignore

    def get_string_value(self) -> str:
        """
        Get the string value.

        Returns:
            The string value

        Raises:
            AssertionError: If this is not a string constant
        """
        assert self._cnst_kind == CnstKind.STRING, "Not a string constant"
        return self._raw  # type: ignore

    def children(self) -> Iterator[Node]:
        """Get children (none for Cnst nodes)."""
        return iter([])

    def __str__(self) -> str:
        """Get string representation."""
        if self._cnst_kind == CnstKind.STRING:
            return f'"{self._raw}"'
        else:
            return str(self._raw)

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Cnst({self._raw!r})"
