"""
TermIndex for managing and canonicalizing terms.

The TermIndex ensures that structurally identical terms share the same
representation, providing efficient equality testing and memory usage.
"""

from typing import Dict, Set, Tuple, Optional, List

from ..enums import SymbolKind, UserCnstSymbKind, BaseSortKind
from ..symbols import (
    Symbol,
    BaseCnstSymb,
    BaseSortSymb,
    UserCnstSymb,
    BaseOpSymb,
)
from ..rational import Rational
from .term import Term


class TermIndex:
    """
    Manages term creation and canonicalization.

    The TermIndex ensures that each unique term is created only once,
    providing structure sharing and efficient equality testing.
    """

    # Empty args tuple for constants
    EMPTY_ARGS: Tuple[Term, ...] = ()

    def __init__(self):
        """Create a new term index."""
        # Term counter for unique IDs
        self._n_terms = 0

        # Symbol ID counter
        self._next_symbol_id = 0

        # Maps for constant symbols
        self._string_cnsts: Dict[str, BaseCnstSymb] = {}
        self._rational_cnsts: Dict[Rational, BaseCnstSymb] = {}
        self._variables: Dict[str, UserCnstSymb] = {}

        # Term bins: maps symbols to sets of terms with that symbol
        self._bins: Dict[int, Set[Term]] = {}  # keyed by symbol.id

        # Common built-in symbols (created on demand)
        self._integer_sort: Optional[BaseSortSymb] = None
        self._real_sort: Optional[BaseSortSymb] = None
        self._string_sort: Optional[BaseSortSymb] = None
        self._natural_sort: Optional[BaseSortSymb] = None

        # Common constants (created on demand)
        self._true_value: Optional[Term] = None
        self._false_value: Optional[Term] = None
        self._zero_value: Optional[Term] = None
        self._one_value: Optional[Term] = None
        self._empty_string: Optional[Term] = None

    @property
    def count(self) -> int:
        """Get the total number of terms created."""
        return self._n_terms

    @property
    def true_value(self) -> Term:
        """Get the canonical true constant."""
        if self._true_value is None:
            # Create symbolic constant 'TRUE'
            symb = self._get_or_create_variable("TRUE", is_auto_gen=True)
            self._true_value = self._mk_apply_internal(symb, self.EMPTY_ARGS)
        return self._true_value

    @property
    def false_value(self) -> Term:
        """Get the canonical false constant."""
        if self._false_value is None:
            # Create symbolic constant 'FALSE'
            symb = self._get_or_create_variable("FALSE", is_auto_gen=True)
            self._false_value = self._mk_apply_internal(symb, self.EMPTY_ARGS)
        return self._false_value

    @property
    def zero_value(self) -> Term:
        """Get the canonical zero constant."""
        if self._zero_value is None:
            self._zero_value = self.mk_cnst(Rational(0))
        return self._zero_value

    @property
    def one_value(self) -> Term:
        """Get the canonical one constant."""
        if self._one_value is None:
            self._one_value = self.mk_cnst(Rational(1))
        return self._one_value

    @property
    def empty_string_value(self) -> Term:
        """Get the canonical empty string constant."""
        if self._empty_string is None:
            self._empty_string = self.mk_cnst("")
        return self._empty_string

    def mk_cnst(self, value) -> Term:
        """
        Create or retrieve a constant term.

        Args:
            value: A Rational or string value

        Returns:
            The canonical term for this constant
        """
        if isinstance(value, Rational):
            return self._mk_rational_cnst(value)
        elif isinstance(value, str):
            return self._mk_string_cnst(value)
        else:
            raise TypeError(f"Unsupported constant type: {type(value)}")

    def mk_var(self, name: str, is_auto_gen: bool = False) -> Term:
        """
        Create or retrieve a variable term.

        Args:
            name: The variable name
            is_auto_gen: Whether this is an auto-generated variable

        Returns:
            The canonical term for this variable
        """
        symb = self._get_or_create_variable(name, is_auto_gen)
        return self._mk_apply_internal(symb, self.EMPTY_ARGS)

    def mk_apply(self, symbol: Symbol, args: Tuple[Term, ...]) -> Term:
        """
        Create or retrieve a function application term.

        Args:
            symbol: The function symbol
            args: The argument terms (must all belong to this index)

        Returns:
            The canonical term for this application

        Raises:
            ValueError: If args don't all belong to this index
        """
        # Verify all args belong to this index
        for arg in args:
            if arg.owner is not self:
                raise ValueError("All argument terms must belong to this TermIndex")

        return self._mk_apply_internal(symbol, args)

    def get_integer_sort(self) -> BaseSortSymb:
        """Get the Integer built-in sort symbol."""
        if self._integer_sort is None:
            self._integer_sort = BaseSortSymb(BaseSortKind.INTEGER)
            self._integer_sort._id = self._next_symbol_id
            self._next_symbol_id += 1
        return self._integer_sort

    def get_real_sort(self) -> BaseSortSymb:
        """Get the Real built-in sort symbol."""
        if self._real_sort is None:
            self._real_sort = BaseSortSymb(BaseSortKind.REAL)
            self._real_sort._id = self._next_symbol_id
            self._next_symbol_id += 1
        return self._real_sort

    def get_string_sort(self) -> BaseSortSymb:
        """Get the String built-in sort symbol."""
        if self._string_sort is None:
            self._string_sort = BaseSortSymb(BaseSortKind.STRING)
            self._string_sort._id = self._next_symbol_id
            self._next_symbol_id += 1
        return self._string_sort

    def get_natural_sort(self) -> BaseSortSymb:
        """Get the Natural built-in sort symbol."""
        if self._natural_sort is None:
            self._natural_sort = BaseSortSymb(BaseSortKind.NATURAL)
            self._natural_sort._id = self._next_symbol_id
            self._next_symbol_id += 1
        return self._natural_sort

    # ========================================================================
    # Internal implementation methods
    # ========================================================================

    def _mk_string_cnst(self, value: str) -> Term:
        """Create or retrieve a string constant."""
        if value not in self._string_cnsts:
            symb = BaseCnstSymb(value)
            symb._id = self._next_symbol_id
            self._next_symbol_id += 1
            self._string_cnsts[value] = symb

        symb = self._string_cnsts[value]
        return self._mk_apply_internal(symb, self.EMPTY_ARGS)

    def _mk_rational_cnst(self, value: Rational) -> Term:
        """Create or retrieve a rational constant."""
        if value not in self._rational_cnsts:
            symb = BaseCnstSymb(value)
            symb._id = self._next_symbol_id
            self._next_symbol_id += 1
            self._rational_cnsts[value] = symb

        symb = self._rational_cnsts[value]
        return self._mk_apply_internal(symb, self.EMPTY_ARGS)

    def _get_or_create_variable(
        self, name: str, is_auto_gen: bool = False
    ) -> UserCnstSymb:
        """Get or create a variable symbol."""
        if name not in self._variables:
            symb = UserCnstSymb(name, UserCnstSymbKind.VARIABLE, is_auto_gen)
            symb._id = self._next_symbol_id
            self._next_symbol_id += 1
            self._variables[name] = symb

        return self._variables[name]

    def _mk_apply_internal(self, symbol: Symbol, args: Tuple[Term, ...]) -> Term:
        """
        Internal method to create or retrieve a term.

        This performs term canonicalization by checking if an equivalent
        term already exists before creating a new one.
        """
        # Get the bin for this symbol
        bin_set = self._get_bin(symbol)

        # Create a candidate term
        candidate = Term(symbol, args, self)

        # Check if an equivalent term already exists
        for existing in bin_set:
            if existing == candidate:
                # Found existing term, return it
                return existing

        # Term doesn't exist, add it to the bin
        candidate._uid = self._n_terms
        self._n_terms += 1
        bin_set.add(candidate)

        return candidate

    def _get_bin(self, symbol: Symbol) -> Set[Term]:
        """Get or create the bin for a symbol."""
        symbol_id = symbol.id
        if symbol_id not in self._bins:
            self._bins[symbol_id] = set()
        return self._bins[symbol_id]

    def get_all_terms(self) -> List[Term]:
        """
        Get all terms in this index.

        Returns:
            List of all terms, sorted by UID
        """
        all_terms = []
        for bin_set in self._bins.values():
            all_terms.extend(bin_set)

        # Sort by UID
        all_terms.sort(key=lambda t: t.uid)
        return all_terms

    def get_terms_with_symbol(self, symbol: Symbol) -> List[Term]:
        """
        Get all terms with a specific symbol.

        Args:
            symbol: The symbol to search for

        Returns:
            List of terms with this symbol
        """
        bin_set = self._bins.get(symbol.id, set())
        return list(bin_set)

    def __repr__(self) -> str:
        """Get string representation."""
        return f"TermIndex({self._n_terms} terms, {len(self._bins)} symbols)"
