"""
Constructor symbol for user-defined constructors.
"""

from typing import Dict, Optional, List, Tuple

from ..enums import SymbolKind
from .symbol import Symbol


class ConSymb(Symbol):
    """
    Represents a constructor symbol in FORMULA.

    Constructors are used to build structured data values.

    Examples:
        Person(name, age)
        new Point(x, y)
        sub Color(r, g, b)
    """

    def __init__(self, name: str, arity: int, is_new: bool = False, is_sub: bool = False):
        """
        Create a constructor symbol.

        Args:
            name: The constructor name
            arity: The number of arguments
            is_new: Whether this is a 'new' constructor
            is_sub: Whether this is a 'sub' constructor
        """
        super().__init__()
        self._name = name
        self._arity = arity
        self._is_new = is_new
        self._is_sub = is_sub
        self._label_map: Dict[str, int] = {}
        self._field_attrs: List[Tuple[bool, Optional[str]]] = [(False, None)] * arity

    @property
    def kind(self) -> SymbolKind:
        """Get the symbol kind."""
        return SymbolKind.CON_SYMB

    @property
    def arity(self) -> int:
        """Get the number of arguments."""
        return self._arity

    @property
    def printable_name(self) -> str:
        """Get a human-readable name."""
        return self._name

    @property
    def name(self) -> str:
        """Get the constructor name."""
        return self._name

    @property
    def is_new(self) -> bool:
        """Check if this is a 'new' constructor."""
        return self._is_new

    @property
    def is_sub(self) -> bool:
        """Check if this is a 'sub' constructor."""
        return self._is_sub

    def get_label_index(self, label: str) -> Optional[int]:
        """
        Get the index of a labeled argument.

        Args:
            label: The field label

        Returns:
            The index of the field, or None if not found
        """
        return self._label_map.get(label)

    def set_label(self, index: int, label: str):
        """
        Set a label for an argument.

        Args:
            index: The argument index
            label: The field label
        """
        assert 0 <= index < self._arity, "Index out of bounds"
        self._label_map[label] = index
        is_any, _ = self._field_attrs[index]
        self._field_attrs[index] = (is_any, label)

    def is_any_arg(self, index: int) -> bool:
        """
        Check if an argument has the 'any' modifier.

        Args:
            index: The argument index

        Returns:
            True if the argument is marked as 'any'
        """
        assert 0 <= index < self._arity, "Index out of bounds"
        return self._field_attrs[index][0]

    def set_any_arg(self, index: int, is_any: bool = True):
        """
        Set whether an argument has the 'any' modifier.

        Args:
            index: The argument index
            is_any: Whether to mark as 'any'
        """
        assert 0 <= index < self._arity, "Index out of bounds"
        _, label = self._field_attrs[index]
        self._field_attrs[index] = (is_any, label)

    def __repr__(self) -> str:
        """Get string representation."""
        kind_str = "new " if self._is_new else "sub " if self._is_sub else ""
        return f"ConSymb({kind_str}{self._name!r}, arity={self._arity})"
