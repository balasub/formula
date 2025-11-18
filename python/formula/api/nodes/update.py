"""
Update node for machine state updates.
"""

from typing import List, Iterator, Optional

from ...common.enums import NodeKind
from .node import Node
from .id import Id
from .mod_apply import ModApply
from .config import Config
from .span import Span


class Update(Node):
    """
    Represents a state update in a machine.

    Updates specify how state variables transition, with optional nondeterministic choices.

    Examples:
        s = Model1().
        s = Model1(); Model2().  (nondeterministic choice)
    """

    def __init__(self, span: Span):
        """
        Create an update node.

        Args:
            span: Source location
        """
        super().__init__(span)
        self._states: List[Id] = []
        self._choices: List[ModApply] = []
        self._config: Optional[Config] = None

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.UPDATE

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        count = len(self._states) + len(self._choices)
        if self._config is not None:
            count += 1
        return count

    @property
    def states(self) -> List[Id]:
        """Get the state identifiers being updated."""
        return self._states

    @property
    def choices(self) -> List[ModApply]:
        """Get the nondeterministic choices."""
        return self._choices

    @property
    def config(self) -> Optional[Config]:
        """Get the configuration (if any)."""
        return self._config

    @config.setter
    def config(self, value: Optional[Config]):
        """Set the configuration."""
        self._config = value

    def add_state(self, state: Id, add_last: bool = True):
        """
        Add a state identifier.

        Args:
            state: The state identifier
            add_last: If True, add at end; if False, add at beginning
        """
        if add_last:
            self._states.append(state)
        else:
            self._states.insert(0, state)

    def add_choice(self, choice: ModApply, add_last: bool = True):
        """
        Add a choice.

        Args:
            choice: The module application choice
            add_last: If True, add at end; if False, add at beginning
        """
        if add_last:
            self._choices.append(choice)
        else:
            self._choices.insert(0, choice)

    def children(self) -> Iterator[Node]:
        """Get all children."""
        if self._config is not None:
            yield self._config
        for state in self._states:
            yield state
        for choice in self._choices:
            yield choice

    def __str__(self) -> str:
        """Get string representation."""
        states_str = ", ".join(str(s) for s in self._states)
        choices_str = "; ".join(str(c) for c in self._choices)
        return f"{states_str} = {choices_str}."

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Update({len(self._states)} states, {len(self._choices)} choices)"
