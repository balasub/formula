"""
User-defined sort symbol.
"""

from typing import Optional

from ..enums import SymbolKind
from .symbol import Symbol


class UserSortSymb(Symbol):
    """
    Represents a user-defined sort symbol in FORMULA.

    User sorts wrap other user-defined symbols (like constructors or unions)
    to create type symbols.

    The data_symbol represents the underlying user symbol that defines
    the structure of this sort.
    """

    def __init__(self, data_symbol: Symbol, name: Optional[str] = None):
        """
        Create a user sort symbol.

        Args:
            data_symbol: The underlying user symbol that defines this sort
            name: Optional override name (defaults to data_symbol's name)
        """
        super().__init__()
        self._data_symbol = data_symbol
        self._name = name if name is not None else data_symbol.printable_name

    @property
    def kind(self) -> SymbolKind:
        """Get the symbol kind."""
        return SymbolKind.USER_SORT_SYMB

    @property
    def arity(self) -> int:
        """User sorts have no arguments."""
        return 0

    @property
    def printable_name(self) -> str:
        """Get a human-readable name."""
        return self._name

    @property
    def name(self) -> str:
        """Get the sort name."""
        return self._name

    @property
    def data_symbol(self) -> Symbol:
        """Get the underlying data symbol."""
        return self._data_symbol

    def __repr__(self) -> str:
        """Get string representation."""
        return f"UserSortSymb({self._name!r})"
