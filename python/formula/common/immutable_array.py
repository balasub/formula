"""
Immutable array implementation for FORMULA.
"""

from typing import TypeVar, Generic, Iterator, List, Optional, Callable

T = TypeVar('T')


class ImmutableArray(Generic[T]):
    """
    An immutable array implementation.

    This provides an immutable wrapper around a tuple for better performance
    and to ensure data cannot be modified after creation.
    """

    def __init__(self, items: List[T]):
        """
        Create an immutable array.

        Args:
            items: The list of items to store
        """
        self._items = tuple(items)

    @property
    def length(self) -> int:
        """Get the number of items in the array."""
        return len(self._items)

    def __len__(self) -> int:
        """Get the number of items in the array."""
        return len(self._items)

    def __getitem__(self, index: int) -> T:
        """Get an item by index."""
        return self._items[index]

    def __iter__(self) -> Iterator[T]:
        """Iterate over the items."""
        return iter(self._items)

    def __eq__(self, other: object) -> bool:
        """Check equality with another array."""
        if isinstance(other, ImmutableArray):
            return self._items == other._items
        return False

    def __hash__(self) -> int:
        """Get hash code for the array."""
        return hash(self._items)

    def __repr__(self) -> str:
        """Get string representation."""
        return f"ImmutableArray({list(self._items)!r})"

    def to_list(self) -> List[T]:
        """Convert to a Python list."""
        return list(self._items)

    def any(self, predicate: Optional[Callable[[T], bool]] = None) -> bool:
        """
        Check if any item matches a predicate.

        Args:
            predicate: The predicate function, or None to check if array is non-empty

        Returns:
            True if any item matches or array is non-empty
        """
        if predicate is None:
            return len(self._items) > 0
        return any(predicate(item) for item in self._items)

    def all(self, predicate: Callable[[T], bool]) -> bool:
        """
        Check if all items match a predicate.

        Args:
            predicate: The predicate function

        Returns:
            True if all items match
        """
        return all(predicate(item) for item in self._items)
