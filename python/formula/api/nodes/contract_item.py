"""
ContractItem node for contracts in FORMULA.
"""

from typing import List, Iterator, Optional, TYPE_CHECKING

from ...common.enums import NodeKind, ContractKind
from .node import Node
from .config import Config
from .body import Body
from .span import Span


class ContractItem(Node):
    """
    Represents a contract specification in FORMULA.

    Contracts can be conformance properties, requires, ensures, or cardinality constraints.

    Examples:
        ensures p(x).
        requires x > 0; y < 10.
        requires some 5 Person.
    """

    def __init__(self, span: Span, contract_kind: ContractKind):
        """
        Create a contract item.

        Args:
            span: Source location
            contract_kind: The kind of contract
        """
        super().__init__(span)
        self._contract_kind = contract_kind
        self._specification: List[Node] = []
        self._config: Optional[Config] = None

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.CONTRACT_ITEM

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        count = len(self._specification)
        if self._config is not None:
            count += 1
        return count

    @property
    def contract_kind(self) -> ContractKind:
        """Get the contract kind."""
        return self._contract_kind

    @property
    def specification(self) -> List[Node]:
        """Get the specification nodes (usually Body nodes)."""
        return self._specification

    @property
    def config(self) -> Optional[Config]:
        """Get the configuration (if any)."""
        return self._config

    @config.setter
    def config(self, value: Optional[Config]):
        """Set the configuration."""
        self._config = value

    @property
    def bodies(self) -> Iterator[Body]:
        """
        Get the bodies (only for non-cardinality contracts).

        Yields:
            Body nodes from the specification
        """
        for spec in self._specification:
            assert spec.node_kind == NodeKind.BODY, "Specification must be a Body node"
            yield spec  # type: ignore

    def add_specification(self, spec: Node, add_last: bool = True):
        """
        Add a specification node.

        Args:
            spec: The specification node
            add_last: If True, add at end; if False, add at beginning
        """
        if add_last:
            self._specification.append(spec)
        else:
            self._specification.insert(0, spec)

    def children(self) -> Iterator[Node]:
        """Get all children (config and specifications)."""
        if self._config is not None:
            yield self._config
        for spec in self._specification:
            yield spec

    def __str__(self) -> str:
        """Get string representation."""
        kind_str = self._contract_kind.name.lower()
        specs_str = "; ".join(str(s) for s in self._specification)
        return f"{kind_str} {specs_str}."

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"ContractItem({self._contract_kind}, {len(self._specification)} specs)"
