"""
Union symbol for user-defined union types.
"""

from typing import Optional

from ..enums import SymbolKind
from .symbol import Symbol


class UnnSymb(Symbol):
    """
    Represents a union type symbol in FORMULA.

    Union types define types that are the union of other types.

    Examples:
        MyUnion ::= Integer + String
        Color ::= {red, green, blue}
    """

    def __init__(self, name: str, is_auto_gen: bool = False):
        """
        Create a union symbol.

        Args:
            name: The union type name
            is_auto_gen: Whether this was auto-generated
        """
        super().__init__()
        self._name = name
        self._is_auto_gen = is_auto_gen

    @property
    def kind(self) -> SymbolKind:
        """Get the symbol kind."""
        return SymbolKind.UNN_SYMB

    @property
    def arity(self) -> int:
        """Union types have no arguments."""
        return 0

    @property
    def printable_name(self) -> str:
        """Get a human-readable name."""
        return self._name

    @property
    def name(self) -> str:
        """Get the union type name."""
        return self._name

    @property
    def is_auto_gen(self) -> bool:
        """Check if this was auto-generated."""
        return self._is_auto_gen

    def __repr__(self) -> str:
        """Get string representation."""
        auto_str = " (auto)" if self._is_auto_gen else ""
        return f"UnnSymb({self._name!r}{auto_str})"
