"""
Program node for FORMULA programs.
"""

from typing import List, Iterator

from ...common.enums import NodeKind
from .node import Node
from .span import Span, ProgramName
from .config import Config


class Program(Node):
    """
    Represents a FORMULA program (root of the AST).

    A program contains:
    - A program name
    - Optional configuration
    - A collection of modules (domains, models, transforms, machines)
    """

    def __init__(self, span: Span, name: ProgramName):
        """
        Create a program node.

        Args:
            span: Source location
            name: The program name
        """
        super().__init__(span)
        self._name = name
        self._config = Config(span)
        self._modules: List[Node] = []

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.PROGRAM

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        return 1 + len(self._modules)  # config + modules

    @property
    def name(self) -> ProgramName:
        """Get the program name."""
        return self._name

    @property
    def config(self) -> Config:
        """Get the program configuration."""
        return self._config

    @config.setter
    def config(self, value: Config):
        """Set the program configuration."""
        self._config = value

    @property
    def modules(self) -> List[Node]:
        """Get the list of modules."""
        return self._modules

    def add_module(self, module: Node, add_last: bool = True):
        """
        Add a module to the program.

        Args:
            module: The module node (must be a domain, model, transform, or machine)
            add_last: If True, add at end; if False, add at beginning

        Raises:
            AssertionError: If module is not a module node
        """
        assert module.is_module, "Node must be a module"
        if add_last:
            self._modules.append(module)
        else:
            self._modules.insert(0, module)

    def children(self) -> Iterator[Node]:
        """Get all children."""
        yield self._config
        for module in self._modules:
            yield module

    def __str__(self) -> str:
        """Get string representation."""
        return f"program {self._name}"

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Program({self._name!r}, {len(self._modules)} modules)"
