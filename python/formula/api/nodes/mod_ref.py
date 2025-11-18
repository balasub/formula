"""
ModRef node for module references in FORMULA.
"""

from typing import Optional, Iterator

from ...common.enums import NodeKind
from .node import Node
from .span import Span


class ModRef(Node):
    """
    Represents a module reference in FORMULA.

    Module references are used to refer to other modules (domains, models, etc.)
    and can optionally rename them and specify a file location.

    Examples:
        Foo           - simple reference
        Bar :: Foo    - rename Foo to Bar
        Foo at "file" - reference with location
    """

    def __init__(self, span: Span, name: str, rename: Optional[str] = None,
                 location: Optional[str] = None):
        """
        Create a module reference.

        Args:
            span: Source location
            name: The module name
            rename: Optional rename (if renaming the module)
            location: Optional file location
        """
        assert name, "Module name cannot be empty"
        super().__init__(span)
        self._name = name
        self._rename = rename
        self._location = location

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.MOD_REF

    @property
    def child_count(self) -> int:
        """Module references have no children."""
        return 0

    @property
    def name(self) -> str:
        """Get the module name."""
        return self._name

    @property
    def rename(self) -> Optional[str]:
        """Get the rename (if any)."""
        return self._rename

    @property
    def location(self) -> Optional[str]:
        """Get the file location (if any)."""
        return self._location

    def children(self) -> Iterator[Node]:
        """Get children (none for ModRef nodes)."""
        return iter([])

    def __str__(self) -> str:
        """Get string representation."""
        result = ""
        if self._rename:
            result = f"{self._rename} :: "
        result += self._name
        if self._location:
            result += f' at "{self._location}"'
        return result

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"ModRef({self._name!r}, rename={self._rename!r}, location={self._location!r})"
