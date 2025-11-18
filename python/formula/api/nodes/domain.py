"""
Domain node for FORMULA domain declarations.
"""

from typing import List, Iterator

from ...common.enums import NodeKind, ComposeKind
from .node import Node
from .mod_ref import ModRef
from .rule import Rule
from .contract_item import ContractItem
from .config import Config
from .span import Span


class Domain(Node):
    """
    Represents a domain declaration in FORMULA.

    Domains define type systems, data structures, and constraints.

    Examples:
        domain SimpleDomain { }
        domain MyDomain extends BaseDomain { ... }
    """

    def __init__(self, span: Span, name: str, compose_kind: ComposeKind):
        """
        Create a domain node.

        Args:
            span: Source location
            name: The domain name
            compose_kind: How this domain composes with others (None, Includes, Extends)
        """
        assert name, "Domain name cannot be empty"
        super().__init__(span)
        self._name = name
        self._compose_kind = compose_kind
        self._compositions: List[ModRef] = []
        self._rules: List[Rule] = []
        self._type_decls: List[Node] = []
        self._conforms: List[ContractItem] = []
        self._config = Config(span)

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.DOMAIN

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        return (
            len(self._compositions)
            + len(self._rules)
            + len(self._type_decls)
            + len(self._conforms)
            + 1  # config
        )

    @property
    def name(self) -> str:
        """Get the domain name."""
        return self._name

    @property
    def compose_kind(self) -> ComposeKind:
        """Get the composition kind."""
        return self._compose_kind

    @property
    def compositions(self) -> List[ModRef]:
        """Get the list of composed modules."""
        return self._compositions

    @property
    def rules(self) -> List[Rule]:
        """Get the list of rules and facts."""
        return self._rules

    @property
    def type_decls(self) -> List[Node]:
        """Get the list of type declarations."""
        return self._type_decls

    @property
    def conforms(self) -> List[ContractItem]:
        """Get the list of conformance contracts."""
        return self._conforms

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

    def add_rule(self, rule: Rule, add_last: bool = True):
        """Add a rule or fact."""
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

    def add_conform(self, conform: ContractItem, add_last: bool = True):
        """Add a conformance contract."""
        if add_last:
            self._conforms.append(conform)
        else:
            self._conforms.insert(0, conform)

    def children(self) -> Iterator[Node]:
        """Get all children."""
        for comp in self._compositions:
            yield comp
        yield self._config
        for decl in self._type_decls:
            yield decl
        for rule in self._rules:
            yield rule
        for conform in self._conforms:
            yield conform

    def __str__(self) -> str:
        """Get string representation."""
        return f"domain {self._name}"

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Domain({self._name!r}, {len(self._rules)} rules, {len(self._type_decls)} types)"
