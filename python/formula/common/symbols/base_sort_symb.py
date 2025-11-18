"""
Base sort symbol for built-in types.
"""

from ..enums import SymbolKind, BaseSortKind
from .symbol import Symbol


class BaseSortSymb(Symbol):
    """
    Represents a built-in sort (type) symbol.

    Built-in sorts include Integer, Real, String, Natural, etc.
    """

    # Mapping from BaseSortKind to printable names
    _SORT_NAMES = {
        BaseSortKind.NEG_INTEGER: "NegInteger",
        BaseSortKind.POS_INTEGER: "PosInteger",
        BaseSortKind.NATURAL: "Natural",
        BaseSortKind.INTEGER: "Integer",
        BaseSortKind.REAL: "Real",
        BaseSortKind.STRING: "String",
    }

    def __init__(self, sort_kind: BaseSortKind):
        """
        Create a base sort symbol.

        Args:
            sort_kind: The kind of built-in sort
        """
        super().__init__()
        self._sort_kind = sort_kind

    @property
    def kind(self) -> SymbolKind:
        """Get the symbol kind."""
        return SymbolKind.BASE_SORT_SYMB

    @property
    def arity(self) -> int:
        """Base sorts have no arguments."""
        return 0

    @property
    def sort_kind(self) -> BaseSortKind:
        """Get the specific kind of base sort."""
        return self._sort_kind

    @property
    def printable_name(self) -> str:
        """Get a human-readable name for this sort."""
        return self._SORT_NAMES.get(self._sort_kind, str(self._sort_kind))

    def __repr__(self) -> str:
        """Get string representation."""
        return f"BaseSortSymb({self._sort_kind})"
