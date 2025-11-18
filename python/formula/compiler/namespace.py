"""
Namespace for organizing symbols hierarchically.
"""

from typing import Dict, Optional, List, Set
from ..common.symbols import Symbol, UserCnstSymb


class Namespace:
    """
    Represents a namespace for organizing symbols.

    Namespaces form a hierarchy where symbols can be qualified
    by their namespace path (e.g., "Domain.SubNamespace.SymbolName").
    """

    def __init__(self, name: str, parent: Optional['Namespace'] = None):
        """
        Create a namespace.

        Args:
            name: The name of this namespace
            parent: The parent namespace (None for root)
        """
        self._name = name
        self._parent = parent
        self._symbols: Dict[str, Symbol] = {}
        self._children: Dict[str, 'Namespace'] = {}

    @property
    def name(self) -> str:
        """Get the namespace name."""
        return self._name

    @property
    def parent(self) -> Optional['Namespace']:
        """Get the parent namespace."""
        return self._parent

    @property
    def symbols(self) -> Dict[str, Symbol]:
        """Get all symbols in this namespace."""
        return self._symbols

    @property
    def children(self) -> Dict[str, 'Namespace']:
        """Get child namespaces."""
        return self._children

    @property
    def full_name(self) -> str:
        """Get the fully qualified namespace name."""
        if self._parent is None:
            return self._name
        parent_name = self._parent.full_name
        if parent_name:
            return f"{parent_name}.{self._name}"
        return self._name

    def add_symbol(self, name: str, symbol: Symbol) -> bool:
        """
        Add a symbol to this namespace.

        Args:
            name: The symbol name
            symbol: The symbol to add

        Returns:
            True if added successfully, False if name already exists
        """
        if name in self._symbols:
            return False

        self._symbols[name] = symbol
        return True

    def get_symbol(self, name: str) -> Optional[Symbol]:
        """
        Get a symbol from this namespace.

        Args:
            name: The symbol name

        Returns:
            The symbol, or None if not found
        """
        return self._symbols.get(name)

    def resolve_symbol(self, qualified_name: str) -> Optional[Symbol]:
        """
        Resolve a qualified symbol name.

        Args:
            qualified_name: The qualified name (e.g., "Namespace.Symbol")

        Returns:
            The symbol, or None if not found
        """
        parts = qualified_name.split('.')

        # If single part, look in this namespace
        if len(parts) == 1:
            return self.get_symbol(parts[0])

        # Otherwise, navigate through namespaces
        current = self
        for i, part in enumerate(parts[:-1]):
            if part not in current._children:
                return None
            current = current._children[part]

        # Look for symbol in final namespace
        return current.get_symbol(parts[-1])

    def get_or_create_child(self, name: str) -> 'Namespace':
        """
        Get or create a child namespace.

        Args:
            name: The child namespace name

        Returns:
            The child namespace
        """
        if name not in self._children:
            self._children[name] = Namespace(name, self)
        return self._children[name]

    def get_all_symbols(self, include_children: bool = False) -> List[Symbol]:
        """
        Get all symbols in this namespace.

        Args:
            include_children: If True, include symbols from child namespaces

        Returns:
            List of symbols
        """
        result = list(self._symbols.values())

        if include_children:
            for child in self._children.values():
                result.extend(child.get_all_symbols(include_children=True))

        return result

    def __repr__(self) -> str:
        """Get string representation."""
        return f"Namespace({self.full_name}, {len(self._symbols)} symbols)"
