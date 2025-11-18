"""
ModApply node for module applications.
"""

from typing import List, Iterator

from ...common.enums import NodeKind
from .node import Node
from .mod_ref import ModRef
from .span import Span


class ModApply(Node):
    """
    Represents a module application in FORMULA.

    Module applications are used to instantiate transforms with arguments.

    Examples:
        MyTransform()
        MyTransform(foo, bar)
    """

    def __init__(self, span: Span, module: ModRef):
        """
        Create a module application.

        Args:
            span: Source location
            module: The module reference being applied
        """
        super().__init__(span)
        self._module = module
        self._args: List[Node] = []

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.MOD_APPLY

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        return 1 + len(self._args)  # module + args

    @property
    def module(self) -> ModRef:
        """Get the module reference."""
        return self._module

    @module.setter
    def module(self, value: ModRef):
        """Set the module reference."""
        self._module = value

    @property
    def args(self) -> List[Node]:
        """Get the argument list."""
        return self._args

    def add_arg(self, arg: Node, add_last: bool = True):
        """
        Add an argument.

        Args:
            arg: The argument node (must be a valid module application argument)
            add_last: If True, add at end; if False, add at beginning
        """
        assert arg.is_mod_app_arg, "Argument must be a valid module application argument"
        if add_last:
            self._args.append(arg)
        else:
            self._args.insert(0, arg)

    def children(self) -> Iterator[Node]:
        """Get all children."""
        yield self._module
        for arg in self._args:
            yield arg

    def __str__(self) -> str:
        """Get string representation."""
        if not self._args:
            return f"{self._module}()"
        args_str = ", ".join(str(arg) for arg in self._args)
        return f"{self._module}({args_str})"

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"ModApply({self._module!r}, {len(self._args)} args)"
