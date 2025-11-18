"""
Base Node class for FORMULA AST.
"""

from abc import ABC, abstractmethod
from typing import Optional, Any

from ...common.enums import NodeKind, ContractKind
from .span import Span


class Node(ABC):
    """
    Base class for all AST nodes in FORMULA.

    Nodes represent the structure of FORMULA programs, including
    domains, models, transforms, rules, terms, etc.
    """

    CANCEL_CHECK_FREQ = 500

    def __init__(self, span: Optional[Span] = None):
        """
        Create a new node.

        Args:
            span: The source location span for this node
        """
        self._span = span if span is not None else Span.unknown()
        self._compiler_data: Optional[Any] = None
        self._cached_hash_code: Optional[int] = None

    @property
    @abstractmethod
    def node_kind(self) -> NodeKind:
        """Get the kind of this node."""
        pass

    @property
    @abstractmethod
    def child_count(self) -> int:
        """Get the number of child nodes."""
        pass

    @property
    def span(self) -> Span:
        """Get the source location span for this node."""
        return self._span

    @property
    def compiler_data(self) -> Optional[Any]:
        """Get compiler-specific data attached to this node."""
        return self._compiler_data

    @compiler_data.setter
    def compiler_data(self, value: Any):
        """Set compiler-specific data for this node."""
        self._compiler_data = value

    # Node classification properties

    @property
    def is_quote_item(self) -> bool:
        """Check if this is a quote item (function, atom, or quote run)."""
        return self.is_func_or_atom or self.node_kind == NodeKind.QUOTE_RUN

    @property
    def is_contract_spec(self) -> bool:
        """Check if this is a contract specification."""
        return self.node_kind in (NodeKind.BODY, NodeKind.CARD_PAIR)

    @property
    def is_param_type(self) -> bool:
        """Check if this can be used as a parameter type."""
        return self.is_type_term or self.node_kind == NodeKind.MOD_REF

    @property
    def is_type_term(self) -> bool:
        """Check if this is a type term."""
        return self.node_kind == NodeKind.UNION or self.is_union_component

    @property
    def is_union_component(self) -> bool:
        """Check if this can be a component of a union."""
        return self.node_kind in (NodeKind.ID, NodeKind.ENUM)

    @property
    def is_enum_element(self) -> bool:
        """Check if this can be an enumeration element."""
        return self.node_kind in (NodeKind.ID, NodeKind.CNST, NodeKind.RANGE)

    @property
    def is_atom(self) -> bool:
        """Check if this is an atomic term (ID or constant)."""
        return self.node_kind in (NodeKind.ID, NodeKind.CNST)

    @property
    def is_func_or_atom(self) -> bool:
        """Check if this is a function or atomic term."""
        return self.node_kind in (
            NodeKind.ID, NodeKind.CNST, NodeKind.FUNC_TERM,
            NodeKind.COMPR, NodeKind.QUOTE
        )

    @property
    def is_mod_app_arg(self) -> bool:
        """Check if this can be a module application argument."""
        return self.node_kind in (
            NodeKind.ID, NodeKind.CNST, NodeKind.FUNC_TERM,
            NodeKind.MOD_REF, NodeKind.QUOTE
        )

    @property
    def is_dom_or_trans(self) -> bool:
        """Check if this is a domain or transform."""
        return self.node_kind in (NodeKind.DOMAIN, NodeKind.TRANSFORM)

    @property
    def is_module(self) -> bool:
        """Check if this is a module (domain, transform, system, model, or machine)."""
        return self.node_kind in (
            NodeKind.DOMAIN, NodeKind.TRANSFORM, NodeKind.T_SYSTEM,
            NodeKind.MODEL, NodeKind.MACHINE
        )

    @property
    def is_type_decl(self) -> bool:
        """Check if this is a type declaration."""
        return self.node_kind in (NodeKind.CON_DECL, NodeKind.MAP_DECL, NodeKind.UNN_DECL)

    @property
    def is_constraint(self) -> bool:
        """Check if this is a constraint."""
        return self.node_kind in (NodeKind.FIND, NodeKind.REL_CONSTR)

    @property
    def is_config_settable(self) -> bool:
        """Check if this node can have configuration settings."""
        return (
            self.node_kind in (
                NodeKind.RULE, NodeKind.STEP, NodeKind.UPDATE,
                NodeKind.PROPERTY, NodeKind.CONTRACT_ITEM, NodeKind.MODEL_FACT
            )
            or self.is_type_decl
        )

    def can_have_contract(self, kind: ContractKind) -> bool:
        """
        Check if this node can have a contract of the given kind.

        Args:
            kind: The contract kind to check

        Returns:
            True if this node can have the specified contract
        """
        if kind == ContractKind.CONFORMS_PROP:
            return self.node_kind == NodeKind.DOMAIN
        elif kind in (ContractKind.ENSURES_PROP, ContractKind.REQUIRES_PROP):
            return self.node_kind in (NodeKind.TRANSFORM, NodeKind.MODEL)
        elif kind in (ContractKind.REQUIRES_SOME, ContractKind.REQUIRES_AT_LEAST,
                     ContractKind.REQUIRES_AT_MOST):
            return self.node_kind == NodeKind.MODEL
        else:
            raise NotImplementedError(f"Unknown contract kind: {kind}")

    def __eq__(self, other: object) -> bool:
        """Check equality with another node."""
        # Nodes are equal if they're the same object
        return self is other

    def __hash__(self) -> int:
        """Get hash code for this node."""
        if self._cached_hash_code is None:
            self._cached_hash_code = id(self)
        return self._cached_hash_code
