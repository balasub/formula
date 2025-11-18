"""
Base constant symbol for built-in constants.
"""

from typing import Union

from ..enums import SymbolKind, CnstKind
from ..rational import Rational
from .symbol import Symbol


class BaseCnstSymb(Symbol):
    """
    Represents a built-in constant symbol.

    Constants can be either numeric (Rational) or string values.
    """

    def __init__(self, value: Union[Rational, str]):
        """
        Create a base constant symbol.

        Args:
            value: Either a Rational number or a string
        """
        super().__init__()
        if isinstance(value, Rational):
            self._cnst_kind = CnstKind.NUMERIC
            self._raw = value
        elif isinstance(value, str):
            self._cnst_kind = CnstKind.STRING
            self._raw = value if value is not None else ""
        else:
            raise TypeError(f"Invalid constant type: {type(value)}")

    @property
    def kind(self) -> SymbolKind:
        """Get the symbol kind."""
        return SymbolKind.BASE_CNST_SYMB

    @property
    def arity(self) -> int:
        """Constants have no arguments."""
        return 0

    @property
    def cnst_kind(self) -> CnstKind:
        """Get the specific kind of constant."""
        return self._cnst_kind

    @property
    def raw(self) -> Union[Rational, str]:
        """Get the raw constant value."""
        return self._raw

    @property
    def is_new_constant(self) -> bool:
        """Base constants are considered 'new' constants."""
        return True

    @property
    def is_non_var_constant(self) -> bool:
        """Base constants are non-variable constants."""
        return True

    @property
    def printable_name(self) -> str:
        """Get a human-readable name for this constant."""
        if self._cnst_kind == CnstKind.NUMERIC:
            return str(self._raw)
        elif self._cnst_kind == CnstKind.STRING:
            return f'"{self._raw}"'
        else:
            raise NotImplementedError(f"Unknown constant kind: {self._cnst_kind}")

    def __repr__(self) -> str:
        """Get string representation."""
        return f"BaseCnstSymb({self._raw!r})"
