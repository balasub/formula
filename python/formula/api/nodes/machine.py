"""
Machine node for FORMULA machine declarations.
"""

from typing import List, Iterator

from ...common.enums import NodeKind
from .node import Node
from .param import Param
from .mod_ref import ModRef
from .step import Step
from .update import Update
from .property import Property
from .config import Config
from .span import Span


class Machine(Node):
    """
    Represents a machine declaration in FORMULA.

    Machines define state machines over models with initialization, transitions, and properties.

    Examples:
        machine MyMachine() of MyDomain { ... }
    """

    def __init__(self, span: Span, name: str):
        """
        Create a machine node.

        Args:
            span: Source location
            name: The machine name
        """
        assert name and name.strip(), "Machine name cannot be empty"
        super().__init__(span)
        self._name = name
        self._inputs: List[Param] = []
        self._state_domains: List[ModRef] = []
        self._boot_sequence: List[Step] = []
        self._initials: List[Update] = []
        self._nexts: List[Update] = []
        self._properties: List[Property] = []
        self._config = Config(span)

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.MACHINE

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        return (
            1  # config
            + len(self._inputs)
            + len(self._state_domains)
            + len(self._boot_sequence)
            + len(self._initials)
            + len(self._nexts)
            + len(self._properties)
        )

    @property
    def name(self) -> str:
        """Get the machine name."""
        return self._name

    @property
    def inputs(self) -> List[Param]:
        """Get the input parameters."""
        return self._inputs

    @property
    def state_domains(self) -> List[ModRef]:
        """Get the state domain references."""
        return self._state_domains

    @property
    def boot_sequence(self) -> List[Step]:
        """Get the boot sequence."""
        return self._boot_sequence

    @property
    def initials(self) -> List[Update]:
        """Get the initial state updates."""
        return self._initials

    @property
    def nexts(self) -> List[Update]:
        """Get the next state updates."""
        return self._nexts

    @property
    def properties(self) -> List[Property]:
        """Get the properties."""
        return self._properties

    @property
    def config(self) -> Config:
        """Get the configuration."""
        return self._config

    @config.setter
    def config(self, value: Config):
        """Set the configuration."""
        self._config = value

    def add_input(self, param: Param, add_last: bool = True):
        """Add an input parameter."""
        if add_last:
            self._inputs.append(param)
        else:
            self._inputs.insert(0, param)

    def add_state_domain(self, domain: ModRef, add_last: bool = True):
        """Add a state domain reference."""
        if add_last:
            self._state_domains.append(domain)
        else:
            self._state_domains.insert(0, domain)

    def add_boot_step(self, step: Step, add_last: bool = True):
        """Add a boot sequence step."""
        if add_last:
            self._boot_sequence.append(step)
        else:
            self._boot_sequence.insert(0, step)

    def add_initial(self, update: Update, add_last: bool = True):
        """Add an initial state update."""
        if add_last:
            self._initials.append(update)
        else:
            self._initials.insert(0, update)

    def add_next(self, update: Update, add_last: bool = True):
        """Add a next state update."""
        if add_last:
            self._nexts.append(update)
        else:
            self._nexts.insert(0, update)

    def add_property(self, prop: Property, add_last: bool = True):
        """Add a property."""
        if add_last:
            self._properties.append(prop)
        else:
            self._properties.insert(0, prop)

    def children(self) -> Iterator[Node]:
        """Get all children."""
        for inp in self._inputs:
            yield inp
        for domain in self._state_domains:
            yield domain
        yield self._config
        for step in self._boot_sequence:
            yield step
        for initial in self._initials:
            yield initial
        for next_update in self._nexts:
            yield next_update
        for prop in self._properties:
            yield prop

    def __str__(self) -> str:
        """Get string representation."""
        return f"machine {self._name}"

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Machine({self._name!r}, {len(self._state_domains)} domains, {len(self._properties)} props)"
