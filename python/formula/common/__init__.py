"""
FORMULA common module.

This module contains core data structures including:
- Terms: Fundamental building blocks for expressions
- Symbols: Type and value symbols
- Rules: Rule definitions and constraints
- Composites: Composite structures
"""

from .enums import (
    Groundness,
    SymbolKind,
    BaseSortKind,
    UserCnstSymbKind,
    CnstKind,
    ContractKind,
    ComposeKind,
    RelKind,
    MapKind,
    SeverityKind,
    NodeKind,
    OpKind,
    ReservedOpKind,
    InstallKind,
)
from .rational import Rational, LiftedRational
from .immutable_array import ImmutableArray
from .symbols import (
    Symbol,
    BaseSortSymb,
    BaseCnstSymb,
    UserCnstSymb,
    ConSymb,
    MapSymb,
    UnnSymb,
    UserSortSymb,
    BaseOpSymb,
)
from .terms import Term

__all__ = [
    # Enums
    "Groundness",
    "SymbolKind",
    "BaseSortKind",
    "UserCnstSymbKind",
    "CnstKind",
    "ContractKind",
    "ComposeKind",
    "RelKind",
    "MapKind",
    "SeverityKind",
    "NodeKind",
    "OpKind",
    "ReservedOpKind",
    "InstallKind",
    # Core types
    "Rational",
    "LiftedRational",
    "ImmutableArray",
    # Symbols
    "Symbol",
    "BaseSortSymb",
    "BaseCnstSymb",
    "UserCnstSymb",
    "ConSymb",
    "MapSymb",
    "UnnSymb",
    "UserSortSymb",
    "BaseOpSymb",
    # Terms
    "Term",
]
