"""
Param node for transform and machine parameters.
"""

from typing import Iterator, Optional

from ...common.enums import NodeKind
from .node import Node
from .id import Id
from .span import Span


class Param(Node):
    """
    Represents a parameter declaration in transforms and machines.

    Parameters can be either value parameters (with type) or model parameters.

    Examples:
        x: Integer
        MyModel :: SomeDomain
    """

    def __init__(self, span: Span, name: Id, type_node: Node, is_value_param: bool = True):
        """
        Create a parameter node.

        Args:
            span: Source location
            name: The parameter name
            type_node: The type (for value params) or ModRef (for model params)
            is_value_param: True if value parameter, False if model parameter
        """
        super().__init__(span)
        self._name = name
        self._type = type_node
        self._is_value_param = is_value_param

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.PARAM

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        return 2  # name and type

    @property
    def name(self) -> Id:
        """Get the parameter name."""
        return self._name

    @property
    def type_node(self) -> Node:
        """Get the type node."""
        return self._type

    @property
    def is_value_param(self) -> bool:
        """Check if this is a value parameter (vs. model parameter)."""
        return self._is_value_param

    def children(self) -> Iterator[Node]:
        """Get all children."""
        yield self._name
        yield self._type

    def __str__(self) -> str:
        """Get string representation."""
        if self._is_value_param:
            return f"{self._name}: {self._type}"
        else:
            return f"{self._name} :: {self._type}"

    def __repr__(self) -> str:
        """Get detailed representation."""
        param_type = "value" if self._is_value_param else "model"
        return f"Param({self._name!r}, type={self._type!r}, {param_type})"
