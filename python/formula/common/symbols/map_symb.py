"""
Map symbol for function/relation types.
"""

from typing import Dict, Optional, List, Tuple

from ..enums import SymbolKind, MapKind
from .symbol import Symbol


class MapSymb(Symbol):
    """
    Represents a map (function/relation) symbol in FORMULA.

    Maps define functions or relations between domain and codomain.

    Examples:
        fun parent: Person -> Person
        inj id: Integer -> Integer
        bij swap: (Integer, Integer) -> (Integer, Integer)
    """

    def __init__(
        self,
        name: str,
        dom_arity: int,
        cod_arity: int,
        map_kind: MapKind = MapKind.FUN,
        is_partial: bool = False,
    ):
        """
        Create a map symbol.

        Args:
            name: The map name
            dom_arity: Domain arity (number of input arguments)
            cod_arity: Codomain arity (number of output arguments)
            map_kind: The kind of map (fun, inj, bij, sur)
            is_partial: Whether this is a partial map
        """
        super().__init__()
        self._name = name
        self._dom_arity = dom_arity
        self._cod_arity = cod_arity
        self._map_kind = map_kind
        self._is_partial = is_partial
        self._label_map: Dict[str, int] = {}
        self._dom_attrs: List[Tuple[bool, Optional[str]]] = [(False, None)] * dom_arity
        self._cod_attrs: List[Tuple[bool, Optional[str]]] = [(False, None)] * cod_arity

    @property
    def kind(self) -> SymbolKind:
        """Get the symbol kind."""
        return SymbolKind.MAP_SYMB

    @property
    def arity(self) -> int:
        """Get the total arity (domain + codomain)."""
        return self._dom_arity + self._cod_arity

    @property
    def dom_arity(self) -> int:
        """Get the domain arity."""
        return self._dom_arity

    @property
    def cod_arity(self) -> int:
        """Get the codomain arity."""
        return self._cod_arity

    @property
    def printable_name(self) -> str:
        """Get a human-readable name."""
        return self._name

    @property
    def name(self) -> str:
        """Get the map name."""
        return self._name

    @property
    def map_kind(self) -> MapKind:
        """Get the map kind."""
        return self._map_kind

    @property
    def is_partial(self) -> bool:
        """Check if this is a partial map."""
        return self._is_partial

    def get_label_index(self, label: str) -> Optional[int]:
        """
        Get the index of a labeled argument.

        Args:
            label: The field label

        Returns:
            The index of the field, or None if not found
        """
        return self._label_map.get(label)

    def is_any_arg(self, index: int) -> bool:
        """
        Check if an argument has the 'any' modifier.

        Args:
            index: The argument index

        Returns:
            True if the argument is marked as 'any'
        """
        assert 0 <= index < self.arity, "Index out of bounds"
        if index < self._dom_arity:
            return self._dom_attrs[index][0]
        else:
            return self._cod_attrs[index - self._dom_arity][0]

    def __repr__(self) -> str:
        """Get string representation."""
        return f"MapSymb({self._name!r}, {self._map_kind}, {self._dom_arity}->{self._cod_arity})"
