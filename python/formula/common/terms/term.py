"""
Term class for FORMULA.
"""

from typing import List, Optional, TYPE_CHECKING

from ..enums import Groundness, SymbolKind, BaseSortKind, CnstKind
from ..immutable_array import ImmutableArray
from ..symbols.symbol import Symbol
from ..symbols.base_sort_symb import BaseSortSymb
from ..symbols.base_cnst_symb import BaseCnstSymb

if TYPE_CHECKING:
    from .term_index import TermIndex


class Term:
    """
    Represents a term in the FORMULA language.

    A term consists of a symbol and its arguments.
    Terms can be ground (no variables), contain variables, or represent types.
    """

    # Family constants for term equivalence classes
    FAMILY_NUMERIC = 0
    FAMILY_STRING = 1
    FAMILY_USR_CNST = 2
    FAMILY_APP = 3

    def __init__(self, symbol: Symbol, args, owner: 'TermIndex'):
        """
        Create a term.

        Args:
            symbol: The symbol for this term
            args: The argument terms (must match symbol arity) - list or tuple
            owner: The term index that owns this term

        Raises:
            AssertionError: If args length doesn't match symbol arity
        """
        assert len(args) == symbol.arity, \
            f"Argument count {len(args)} doesn't match symbol arity {symbol.arity}"

        self._uid: int = -1
        self._owner = owner
        self._symbol = symbol
        # Convert to tuple if it's a list
        if isinstance(args, (list, tuple)):
            self._args = ImmutableArray(args)
        else:
            self._args = args  # Already an ImmutableArray
        self._groundness = self._compute_groundness()

    @property
    def uid(self) -> int:
        """
        Get the unique ID for this term.

        Raises:
            AssertionError: If term hasn't been assigned a UID yet
        """
        assert self._uid != -1, "Term UID not set"
        return self._uid

    @uid.setter
    def uid(self, value: int):
        """
        Set the unique ID for this term.

        Args:
            value: The UID value

        Raises:
            AssertionError: If UID is already set
        """
        assert self._uid == -1, "Term UID already set"
        self._uid = value

    @property
    def symbol(self) -> Symbol:
        """Get the symbol for this term."""
        return self._symbol

    @property
    def args(self) -> ImmutableArray['Term']:
        """Get the argument terms."""
        return self._args

    @property
    def groundness(self) -> Groundness:
        """Get the groundness of this term."""
        return self._groundness

    @property
    def owner(self) -> 'TermIndex':
        """Get the term index that owns this term."""
        return self._owner

    @property
    def family(self) -> int:
        """
        Get the term family for equivalence classification.

        Terms are grouped into families based on their symbol kind.
        """
        symbol_kind = self._symbol.kind

        if symbol_kind == SymbolKind.BASE_CNST_SYMB:
            bc = self._symbol
            if isinstance(bc, BaseCnstSymb):
                if bc.cnst_kind == CnstKind.NUMERIC:
                    return self.FAMILY_NUMERIC
                elif bc.cnst_kind == CnstKind.STRING:
                    return self.FAMILY_STRING
            raise NotImplementedError(f"Unknown constant kind")

        elif symbol_kind == SymbolKind.BASE_SORT_SYMB:
            bs = self._symbol
            if isinstance(bs, BaseSortSymb):
                return self.FAMILY_STRING if bs.sort_kind == BaseSortKind.STRING else self.FAMILY_NUMERIC
            raise NotImplementedError(f"Unknown sort kind")

        elif symbol_kind == SymbolKind.USER_CNST_SYMB:
            return self.FAMILY_USR_CNST

        else:
            return self.FAMILY_APP

    def _compute_groundness(self) -> Groundness:
        """
        Compute the groundness of this term.

        Returns:
            The groundness value
        """
        symbol = self._symbol

        if symbol.arity == 0:
            # Zero-arity symbols
            if symbol.kind == SymbolKind.BASE_CNST_SYMB:
                return Groundness.GROUND
            elif symbol.kind in (SymbolKind.BASE_SORT_SYMB, SymbolKind.UNN_SYMB, SymbolKind.USER_SORT_SYMB):
                return Groundness.TYPE
            elif symbol.kind == SymbolKind.USER_CNST_SYMB:
                return Groundness.VARIABLE if symbol.is_variable else Groundness.GROUND
            elif symbol.kind in (SymbolKind.CON_SYMB, SymbolKind.MAP_SYMB):
                raise ValueError("Constructor symbols must have arguments")
            else:
                raise NotImplementedError(f"Unknown symbol kind: {symbol.kind}")

        # For terms with arguments, check special cases first
        # Note: We need to check against special symbols from the owner (TermIndex)
        # For now, we'll implement the general case

        # General case: compute based on argument groundness
        result = Groundness.GROUND
        for arg in self._args:
            if arg.groundness == Groundness.VARIABLE:
                assert result != Groundness.TYPE, "Cannot mix variables and types"
                result = Groundness.VARIABLE
            elif arg.groundness == Groundness.TYPE:
                assert result != Groundness.VARIABLE, "Cannot mix types and variables"
                result = Groundness.TYPE

        # Special handling for type-related symbols would go here
        # (checking against owner.TypeRelSymbol, owner.RangeSymbol, etc.)

        return result

    @staticmethod
    def compare(t1: 'Term', t2: 'Term') -> int:
        """
        Compare two terms by their UIDs.

        Args:
            t1: First term
            t2: Second term

        Returns:
            -1 if t1 < t2, 0 if equal, 1 if t1 > t2
        """
        if t1._uid < t2._uid:
            return -1
        elif t1._uid > t2._uid:
            return 1
        else:
            return 0

    @staticmethod
    def is_symbolic_term(term: 'Term') -> bool:
        """
        Check if a term is symbolic (contains variables or symbolic operations).

        Args:
            term: The term to check

        Returns:
            True if the term is symbolic
        """
        if term.groundness == Groundness.VARIABLE:
            return True

        symbol = term.symbol
        if (symbol.is_sym_count or symbol.is_sym_and or symbol.is_sym_and_all or
            symbol.is_sym_max or symbol.is_sym_min or symbol.is_sym_max_all or
            symbol.is_sym_min_all or symbol.is_sym_or or symbol.is_sym_or_all):
            return True

        for child in term.args:
            if Term.is_symbolic_term(child):
                return True

        return False

    def __eq__(self, other: object) -> bool:
        """
        Check equality.

        Uses structural equality if UIDs not set, UID-based equality otherwise.
        """
        if not isinstance(other, Term):
            return False

        # If both have UIDs, use UID-based equality
        if self._uid != -1 and other._uid != -1:
            return self._uid == other._uid

        # Otherwise use structural equality
        if self._symbol != other._symbol:
            return False

        if len(self._args) != len(other._args):
            return False

        for a1, a2 in zip(self._args, other._args):
            if a1 is not a2:  # Use identity for args with UIDs
                return False

        return True

    def __hash__(self) -> int:
        """
        Get hash code.

        Uses structural hash if UID not set, UID-based hash otherwise.
        """
        if self._uid != -1:
            return hash(self._uid)

        # Structural hash
        h = hash(self._symbol.id)
        for arg in self._args:
            # Use arg's UID if available, otherwise identity
            h ^= hash(arg._uid if arg._uid != -1 else id(arg))
        return h

    def __repr__(self) -> str:
        """Get string representation."""
        if len(self._args) == 0:
            return f"{self._symbol.printable_name}"
        else:
            args_str = ", ".join(repr(arg) for arg in self._args)
            return f"{self._symbol.printable_name}({args_str})"
