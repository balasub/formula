"""
Config node for configuration settings in FORMULA.
"""

from typing import List, Iterator, TYPE_CHECKING

from ...common.enums import NodeKind
from .node import Node
from .span import Span

if TYPE_CHECKING:
    from .setting import Setting


class Config(Node):
    """
    Represents a configuration block in FORMULA.

    Configurations contain key-value settings enclosed in square brackets.

    Examples:
        [solver=Z3, timeout=1000]
        [debug=TRUE]
    """

    def __init__(self, span: Span):
        """
        Create a config node.

        Args:
            span: Source location
        """
        super().__init__(span)
        self._settings: List['Setting'] = []

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.CONFIG

    @property
    def child_count(self) -> int:
        """Get the number of setting children."""
        return len(self._settings)

    @property
    def settings(self) -> List['Setting']:
        """Get the list of settings."""
        return self._settings

    def add_setting(self, setting: 'Setting', add_last: bool = True):
        """
        Add a setting to this configuration.

        Args:
            setting: The setting node
            add_last: If True, add at end; if False, add at beginning
        """
        if add_last:
            self._settings.append(setting)
        else:
            self._settings.insert(0, setting)

    def children(self) -> Iterator[Node]:
        """Get all setting children."""
        return iter(self._settings)

    def __str__(self) -> str:
        """Get string representation."""
        if not self._settings:
            return "[]"
        settings_str = ", ".join(str(s) for s in self._settings)
        return f"[{settings_str}]"

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Config({len(self._settings)} settings)"
