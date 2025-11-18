"""
Model node for FORMULA model declarations.
"""

from typing import List, Iterator, Optional

from ...common.enums import NodeKind, ComposeKind
from .node import Node
from .mod_ref import ModRef
from .contract_item import ContractItem
from .model_fact import ModelFact
from .config import Config
from .span import Span


class Model(Node):
    """
    Represents a model declaration in FORMULA.

    Models are instances of domains with specific facts and constraints.

    Examples:
        model MyModel of MyDomain { }
        partial model MyModel of MyDomain extends BaseModel { ... }
    """

    def __init__(
        self,
        span: Span,
        name: str,
        domain: ModRef,
        is_partial: bool = False,
        compose_kind: ComposeKind = ComposeKind.NONE,
    ):
        """
        Create a model node.

        Args:
            span: Source location
            name: The model name
            domain: Reference to the domain this model instantiates
            is_partial: Whether this is a partial model
            compose_kind: How this model composes with others
        """
        assert name and name.strip(), "Model name cannot be empty"
        super().__init__(span)
        self._name = name
        self._domain = domain
        self._is_partial = is_partial
        self._compose_kind = compose_kind
        self._compositions: List[ModRef] = []
        self._contracts: List[ContractItem] = []
        self._facts: List[ModelFact] = []
        self._config = Config(span)

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.MODEL

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        return (
            1  # domain
            + len(self._compositions)
            + len(self._contracts)
            + len(self._facts)
            + 1  # config
        )

    @property
    def name(self) -> str:
        """Get the model name."""
        return self._name

    @property
    def domain(self) -> ModRef:
        """Get the domain reference."""
        return self._domain

    @domain.setter
    def domain(self, value: ModRef):
        """Set the domain reference."""
        self._domain = value

    @property
    def is_partial(self) -> bool:
        """Check if this is a partial model."""
        return self._is_partial

    @property
    def compose_kind(self) -> ComposeKind:
        """Get the composition kind."""
        return self._compose_kind

    @compose_kind.setter
    def compose_kind(self, value: ComposeKind):
        """Set the composition kind."""
        self._compose_kind = value

    @property
    def compositions(self) -> List[ModRef]:
        """Get the list of composed modules."""
        return self._compositions

    @property
    def contracts(self) -> List[ContractItem]:
        """Get the list of contracts."""
        return self._contracts

    @property
    def facts(self) -> List[ModelFact]:
        """Get the list of facts."""
        return self._facts

    @property
    def config(self) -> Config:
        """Get the configuration."""
        return self._config

    @config.setter
    def config(self, value: Config):
        """Set the configuration."""
        self._config = value

    def add_composition(self, comp: ModRef, add_last: bool = True):
        """Add a composition reference."""
        if add_last:
            self._compositions.append(comp)
        else:
            self._compositions.insert(0, comp)

    def add_contract(self, contract: ContractItem, add_last: bool = True):
        """Add a contract."""
        if add_last:
            self._contracts.append(contract)
        else:
            self._contracts.insert(0, contract)

    def add_fact(self, fact: ModelFact, add_last: bool = True):
        """Add a fact."""
        if add_last:
            self._facts.append(fact)
        else:
            self._facts.insert(0, fact)

    def children(self) -> Iterator[Node]:
        """Get all children."""
        yield self._domain
        for comp in self._compositions:
            yield comp
        yield self._config
        for contract in self._contracts:
            yield contract
        for fact in self._facts:
            yield fact

    def __str__(self) -> str:
        """Get string representation."""
        prefix = "partial " if self._is_partial else ""
        return f"{prefix}model {self._name} of {self._domain}"

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Model({self._name!r}, domain={self._domain!r}, {len(self._facts)} facts)"
