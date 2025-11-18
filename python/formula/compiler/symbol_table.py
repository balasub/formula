"""
Symbol table for managing symbols and namespaces.
"""

from typing import Dict, Optional, List, Set, Tuple
from enum import Enum

from ..common import (
    Symbol,
    BaseSortSymb,
    BaseCnstSymb,
    BaseOpSymb,
    UserCnstSymb,
    Rational,
)
from ..common.enums import BaseSortKind, OpKind, RelKind, ReservedOpKind
from .namespace import Namespace


class SymbolTable:
    """
    Manages symbols and namespaces for a FORMULA module.

    The symbol table organizes symbols hierarchically using namespaces
    and provides symbol resolution and lookup functionality.
    """

    # Compiler-generated symbol name prefix
    MANGLE_PREFIX = "~"

    # Special symbol names
    NOT_REL_CNSTR_NAME = "notRelational"
    NOT_FUN_CNSTR_NAME = "notFunctional"
    NOT_INJ_CNSTR_NAME = "notInjective"
    NOT_TOTAL_CNSTR_NAME = "notTotal"
    NOT_INV_TOTAL_CNSTR_NAME = "notInvTotal"
    CONFORMS_NAME = "conforms"
    REQUIRES_NAME = "requires"
    ENSURES_NAME = "ensures"
    SC_VALUE_NAME = MANGLE_PREFIX + "scValue"

    def __init__(self, module_name: str):
        """
        Create a symbol table for a module.

        Args:
            module_name: The name of the module
        """
        self._module_name = module_name
        self._n_symbols = 0
        self._is_valid = True

        # Root namespace contains unqualified symbols
        self._root = Namespace("", None)

        # Module namespace contains module-specific symbols
        self._module_space = self._root.get_or_create_child(module_name)

        # Built-in symbols
        self._base_sorts: Dict[BaseSortKind, BaseSortSymb] = {}
        self._base_ops: Dict[OpKind, BaseOpSymb] = {}
        self._res_base_ops: Dict[ReservedOpKind, BaseOpSymb] = {}
        self._rel_ops: Dict[RelKind, BaseOpSymb] = {}

        # Constant caches
        self._string_cnsts: Dict[str, BaseCnstSymb] = {}
        self._rational_cnsts: Dict[Rational, BaseCnstSymb] = {}

        # Initialize built-in symbols
        self._initialize_built_ins()

    @property
    def module_name(self) -> str:
        """Get the module name."""
        return self._module_name

    @property
    def root(self) -> Namespace:
        """Get the root namespace."""
        return self._root

    @property
    def module_space(self) -> Namespace:
        """Get the module-specific namespace."""
        return self._module_space

    @property
    def is_valid(self) -> bool:
        """Check if the symbol table is valid."""
        return self._is_valid

    @property
    def n_symbols(self) -> int:
        """Get the number of symbols."""
        return self._n_symbols

    @property
    def rational_cnsts(self) -> List[BaseCnstSymb]:
        """Get all rational constants."""
        return list(self._rational_cnsts.values())

    @property
    def string_cnsts(self) -> List[BaseCnstSymb]:
        """Get all string constants."""
        return list(self._string_cnsts.values())

    def _initialize_built_ins(self):
        """Initialize built-in symbols."""
        # Create built-in sort symbols
        for kind in BaseSortKind:
            symb = BaseSortSymb(kind)
            symb._id = self._n_symbols
            self._n_symbols += 1
            self._base_sorts[kind] = symb

        # Note: Base operations would be initialized here
        # For now, we'll create them on demand

    def get_sort_symbol(self, kind: BaseSortKind) -> BaseSortSymb:
        """
        Get a built-in sort symbol.

        Args:
            kind: The sort kind

        Returns:
            The sort symbol
        """
        return self._base_sorts[kind]

    def get_op_symbol(self, kind: OpKind) -> Optional[BaseOpSymb]:
        """
        Get a built-in operation symbol.

        Args:
            kind: The operation kind

        Returns:
            The operation symbol, or None if not found
        """
        if kind not in self._base_ops:
            # Create on demand
            # Determine arity based on operation
            arity = self._get_op_arity(kind)
            symb = BaseOpSymb(kind, arity)
            symb._id = self._n_symbols
            self._n_symbols += 1
            self._base_ops[kind] = symb

        return self._base_ops.get(kind)

    def get_reserved_op_symbol(self, kind: ReservedOpKind) -> Optional[BaseOpSymb]:
        """
        Get a reserved operation symbol.

        Args:
            kind: The reserved operation kind

        Returns:
            The operation symbol, or None if not found
        """
        if kind not in self._res_base_ops:
            # Create on demand
            arity = self._get_reserved_op_arity(kind)
            symb = BaseOpSymb(kind, arity)
            symb._id = self._n_symbols
            self._n_symbols += 1
            self._res_base_ops[kind] = symb

        return self._res_base_ops.get(kind)

    def get_rel_symbol(self, kind: RelKind) -> Optional[BaseOpSymb]:
        """
        Get a relational operation symbol.

        Args:
            kind: The relational kind

        Returns:
            The operation symbol, or None if not found
        """
        if kind not in self._rel_ops:
            # Create on demand
            # Relational operations are typically binary
            symb = BaseOpSymb(kind, 2)
            symb._id = self._n_symbols
            self._n_symbols += 1
            self._rel_ops[kind] = symb

        return self._rel_ops.get(kind)

    def _get_op_arity(self, kind: OpKind) -> int:
        """Get the arity for an operation kind."""
        # Most operations are binary
        binary_ops = {
            OpKind.ADD, OpKind.SUB, OpKind.MUL, OpKind.DIV, OpKind.MOD,
            OpKind.AND, OpKind.OR, OpKind.IMPL,
        }

        unary_ops = {
            OpKind.NEG, OpKind.NOT,
        }

        if kind in unary_ops:
            return 1
        elif kind in binary_ops:
            return 2
        else:
            # Variable arity operations
            return -1  # Will be determined by usage

    def _get_reserved_op_arity(self, kind: ReservedOpKind) -> int:
        """Get the arity for a reserved operation kind."""
        if kind == ReservedOpKind.RANGE:
            return 2  # Range(start, end)
        elif kind == ReservedOpKind.TYPE_UNN:
            return 2  # TypeUnn(type1, type2)
        elif kind == ReservedOpKind.SELECT:
            return 2  # Select(record, field)
        elif kind == ReservedOpKind.RELABEL:
            return 3  # Relabel(prefix, prefix', term)
        else:
            return -1  # Variable arity

    def get_or_create_string_constant(self, value: str) -> BaseCnstSymb:
        """
        Get or create a string constant symbol.

        Args:
            value: The string value

        Returns:
            The constant symbol
        """
        if value not in self._string_cnsts:
            symb = BaseCnstSymb(value)
            symb._id = self._n_symbols
            self._n_symbols += 1
            self._string_cnsts[value] = symb

        return self._string_cnsts[value]

    def get_or_create_rational_constant(self, value: Rational) -> BaseCnstSymb:
        """
        Get or create a rational constant symbol.

        Args:
            value: The rational value

        Returns:
            The constant symbol
        """
        if value not in self._rational_cnsts:
            symb = BaseCnstSymb(value)
            symb._id = self._n_symbols
            self._n_symbols += 1
            self._rational_cnsts[value] = symb

        return self._rational_cnsts[value]

    def add_symbol(self, name: str, symbol: Symbol, namespace: Optional[Namespace] = None) -> bool:
        """
        Add a symbol to the table.

        Args:
            name: The symbol name
            symbol: The symbol to add
            namespace: The namespace (defaults to module namespace)

        Returns:
            True if added successfully, False if name already exists
        """
        if namespace is None:
            namespace = self._module_space

        # Set symbol ID if not already set
        if not hasattr(symbol, '_id') or symbol._id is None or symbol._id < 0:
            symbol._id = self._n_symbols
            self._n_symbols += 1

        return namespace.add_symbol(name, symbol)

    def resolve(self, qualified_name: str) -> Tuple[Optional[Symbol], Optional[Symbol]]:
        """
        Resolve a qualified symbol name.

        Args:
            qualified_name: The qualified name (e.g., "Namespace.Symbol")

        Returns:
            Tuple of (primary_symbol, conflicting_symbol)
            If no conflict, second element is None
        """
        # Try root namespace first
        symbol = self._root.resolve_symbol(qualified_name)
        if symbol is not None:
            return (symbol, None)

        # Try module namespace
        symbol = self._module_space.resolve_symbol(qualified_name)
        if symbol is not None:
            return (symbol, None)

        return (None, None)

    def get_all_symbols(self) -> List[Symbol]:
        """
        Get all symbols in the table.

        Returns:
            List of all symbols
        """
        symbols = []
        symbols.extend(self._base_sorts.values())
        symbols.extend(self._base_ops.values())
        symbols.extend(self._res_base_ops.values())
        symbols.extend(self._rel_ops.values())
        symbols.extend(self._string_cnsts.values())
        symbols.extend(self._rational_cnsts.values())
        symbols.extend(self._root.get_all_symbols(include_children=True))
        return symbols

    def __repr__(self) -> str:
        """Get string representation."""
        return f"SymbolTable({self._module_name}, {self._n_symbols} symbols)"
