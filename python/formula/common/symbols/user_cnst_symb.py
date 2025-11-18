"""
User-defined constant symbol.
"""

from typing import List, Optional

from ..enums import SymbolKind, UserCnstSymbKind
from .symbol import Symbol


class UserCnstSymb(Symbol):
    """
    Represents a user-defined constant symbol in FORMULA.

    User constants can be:
    - Variables: Unbound identifiers used in patterns
    - New constants: Declared as new values
    - Derived constants: Derived from other constructs

    Special kinds:
    - Type constants: Start with # (e.g., #Person)
    - Symbolic constants: Start with % (e.g., %state)
    """

    def __init__(self, name: str, user_cnst_kind: UserCnstSymbKind, is_auto_gen: bool = False):
        """
        Create a user constant symbol.

        Args:
            name: The constant name
            user_cnst_kind: The kind of user constant
            is_auto_gen: Whether this was auto-generated
        """
        super().__init__()
        self._name = name
        self._user_cnst_kind = user_cnst_kind
        self._is_auto_gen = is_auto_gen

    @property
    def kind(self) -> SymbolKind:
        """Get the symbol kind."""
        return SymbolKind.USER_CNST_SYMB

    @property
    def arity(self) -> int:
        """User constants have no arguments."""
        return 0

    @property
    def printable_name(self) -> str:
        """Get a human-readable name."""
        return self._name

    @property
    def name(self) -> str:
        """Get the constant name."""
        return self._name

    @property
    def user_cnst_kind(self) -> UserCnstSymbKind:
        """Get the user constant kind."""
        return self._user_cnst_kind

    @property
    def is_auto_gen(self) -> bool:
        """Check if this was auto-generated."""
        return self._is_auto_gen

    @property
    def is_variable(self) -> bool:
        """Check if this is a variable."""
        return self._user_cnst_kind == UserCnstSymbKind.VARIABLE

    @property
    def is_new_constant(self) -> bool:
        """Check if this is a new constant."""
        return self._user_cnst_kind == UserCnstSymbKind.NEW

    @property
    def is_derived_constant(self) -> bool:
        """Check if this is a derived constant."""
        return self._user_cnst_kind == UserCnstSymbKind.DERIVED

    @property
    def is_non_var_constant(self) -> bool:
        """Check if this is a non-variable constant."""
        return self._user_cnst_kind != UserCnstSymbKind.VARIABLE

    @property
    def is_type_constant(self) -> bool:
        """Check if this is a type constant (starts with #)."""
        return self._name and self._name[0] == '#'

    @property
    def is_symbolic_constant(self) -> bool:
        """Check if this is a symbolic constant (starts with %)."""
        return self._name and self._name[0] == '%'

    def __repr__(self) -> str:
        """Get string representation."""
        return f"UserCnstSymb({self._name!r}, {self._user_cnst_kind})"
