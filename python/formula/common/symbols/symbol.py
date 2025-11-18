"""
Base Symbol class for FORMULA.
"""

from abc import ABC, abstractmethod
from typing import Optional

from ..enums import SymbolKind


class Symbol(ABC):
    """
    Base class for all symbols in FORMULA.

    Symbols represent types, constants, and operations.
    Each symbol has a unique ID and arity (number of arguments).
    """

    def __init__(self):
        """Create a new symbol (not yet fully constructed)."""
        self._id: int = -1

    @property
    def id(self) -> int:
        """
        Get the unique ID for this symbol.

        Raises:
            AssertionError: If the symbol is not fully constructed
        """
        assert self._id >= 0, "Symbol not fully constructed"
        return self._id

    @id.setter
    def id(self, value: int):
        """
        Set the unique ID for this symbol.

        Args:
            value: The ID value (must be >= 0)

        Raises:
            AssertionError: If ID is already set or value is invalid
        """
        assert value >= 0, "Symbol ID must be non-negative"
        assert self._id == -1, "Symbol ID already set"
        self._id = value

    @property
    def is_fully_constructed(self) -> bool:
        """Check if the symbol has been fully constructed and assigned an ID."""
        return self._id >= 0

    @property
    @abstractmethod
    def kind(self) -> SymbolKind:
        """Get the kind of symbol."""
        pass

    @property
    @abstractmethod
    def printable_name(self) -> str:
        """Get a human-readable name for this symbol."""
        pass

    @property
    @abstractmethod
    def arity(self) -> int:
        """Get the number of arguments this symbol takes."""
        pass

    @property
    def is_variable(self) -> bool:
        """Check if this symbol represents a variable."""
        return False

    @property
    def is_reserved_operation(self) -> bool:
        """Check if this is a reserved operation."""
        return False

    @property
    def is_derived_constant(self) -> bool:
        """Check if this is a derived constant."""
        return False

    @property
    def is_new_constant(self) -> bool:
        """Check if this is a new constant."""
        return False

    @property
    def is_non_var_constant(self) -> bool:
        """Check if this is a non-variable constant."""
        return False

    @property
    def is_type_unn(self) -> bool:
        """Check if this is a type union."""
        return False

    @property
    def is_range(self) -> bool:
        """Check if this is a range symbol."""
        return False

    @property
    def is_select(self) -> bool:
        """Check if this is a select operation."""
        return False

    @property
    def is_relabel(self) -> bool:
        """Check if this is a relabel operation."""
        return False

    @property
    def is_sym_count(self) -> bool:
        """Check if this is a count operation."""
        return False

    @property
    def is_sym_and(self) -> bool:
        """Check if this is an AND operation."""
        return False

    @property
    def is_sym_or(self) -> bool:
        """Check if this is an OR operation."""
        return False

    @property
    def is_sym_or_all(self) -> bool:
        """Check if this is an OR-ALL operation."""
        return False

    @property
    def is_sym_and_all(self) -> bool:
        """Check if this is an AND-ALL operation."""
        return False

    @property
    def is_sym_max(self) -> bool:
        """Check if this is a MAX operation."""
        return False

    @property
    def is_sym_max_all(self) -> bool:
        """Check if this is a MAX-ALL operation."""
        return False

    @property
    def is_sym_min(self) -> bool:
        """Check if this is a MIN operation."""
        return False

    @property
    def is_sym_min_all(self) -> bool:
        """Check if this is a MIN-ALL operation."""
        return False

    @property
    def is_data_constructor(self) -> bool:
        """Check if this is a data constructor (ConSymb or MapSymb)."""
        return self.kind in (SymbolKind.CON_SYMB, SymbolKind.MAP_SYMB)

    @staticmethod
    def compare(s1: 'Symbol', s2: 'Symbol') -> int:
        """
        Compare two symbols by their IDs.

        Args:
            s1: First symbol
            s2: Second symbol

        Returns:
            Negative if s1 < s2, 0 if equal, positive if s1 > s2
        """
        return s1.id - s2.id

    def __eq__(self, other: object) -> bool:
        """Check equality based on ID."""
        if isinstance(other, Symbol):
            return self._id == other._id
        return False

    def __hash__(self) -> int:
        """Get hash based on ID."""
        return hash(self._id)

    def __lt__(self, other: 'Symbol') -> bool:
        """Compare symbols by ID."""
        return self.id < other.id
