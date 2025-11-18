"""
Transform node for FORMULA transform declarations.
"""

from typing import List, Iterator

from ...common.enums import NodeKind
from .node import Node
from .param import Param
from .rule import Rule
from .contract_item import ContractItem
from .config import Config
from .span import Span


class Transform(Node):
    """
    Represents a transform declaration in FORMULA.

    Transforms are functions that take models/values as input and produce models as output.

    Examples:
        transform MyTransform() returns (out :: MyDomain) { ... }
        transform Process(x: Integer) returns (result :: Result) { ... }
    """

    def __init__(self, span: Span, name: str):
        """
        Create a transform node.

        Args:
            span: Source location
            name: The transform name
        """
        super().__init__(span)
        self._name = name
        self._inputs: List[Param] = []
        self._outputs: List[Param] = []
        self._rules: List[Rule] = []
        self._type_decls: List[Node] = []
        self._contracts: List[ContractItem] = []
        self._config = Config(span)

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.TRANSFORM

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        return (
            1  # config
            + len(self._inputs)
            + len(self._outputs)
            + len(self._rules)
            + len(self._type_decls)
            + len(self._contracts)
        )

    @property
    def name(self) -> str:
        """Get the transform name."""
        return self._name

    @property
    def inputs(self) -> List[Param]:
        """Get the input parameters."""
        return self._inputs

    @property
    def outputs(self) -> List[Param]:
        """Get the output parameters."""
        return self._outputs

    @property
    def rules(self) -> List[Rule]:
        """Get the rules."""
        return self._rules

    @property
    def type_decls(self) -> List[Node]:
        """Get the type declarations."""
        return self._type_decls

    @property
    def contracts(self) -> List[ContractItem]:
        """Get the contracts."""
        return self._contracts

    @property
    def config(self) -> Config:
        """Get the configuration."""
        return self._config

    @config.setter
    def config(self, value: Config):
        """Set the configuration."""
        self._config = value

    def add_input(self, param: Param, add_last: bool = True):
        """Add an input parameter."""
        if add_last:
            self._inputs.append(param)
        else:
            self._inputs.insert(0, param)

    def add_output(self, param: Param, add_last: bool = True):
        """Add an output parameter."""
        if add_last:
            self._outputs.append(param)
        else:
            self._outputs.insert(0, param)

    def add_rule(self, rule: Rule, add_last: bool = True):
        """Add a rule."""
        if add_last:
            self._rules.append(rule)
        else:
            self._rules.insert(0, rule)

    def add_type_decl(self, decl: Node, add_last: bool = True):
        """Add a type declaration."""
        assert decl.is_type_decl, "Must be a type declaration"
        if add_last:
            self._type_decls.append(decl)
        else:
            self._type_decls.insert(0, decl)

    def add_contract(self, contract: ContractItem, add_last: bool = True):
        """Add a contract."""
        if add_last:
            self._contracts.append(contract)
        else:
            self._contracts.insert(0, contract)

    def children(self) -> Iterator[Node]:
        """Get all children."""
        for inp in self._inputs:
            yield inp
        for out in self._outputs:
            yield out
        yield self._config
        for contract in self._contracts:
            yield contract
        for decl in self._type_decls:
            yield decl
        for rule in self._rules:
            yield rule

    def __str__(self) -> str:
        """Get string representation."""
        return f"transform {self._name}"

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Transform({self._name!r}, {len(self._inputs)} inputs, {len(self._outputs)} outputs)"
