"""
FuncTerm node for function applications in FORMULA.
"""

from typing import Union, List, Iterator

from ...common.enums import NodeKind, OpKind
from .node import Node
from .id import Id
from .span import Span


class FuncTerm(Node):
    """
    Represents a function application in FORMULA.

    A function term consists of a function (either an OpKind or an Id)
    applied to zero or more arguments.

    Examples:
        f(x, y)        - user function
        x + y          - built-in operation
        max(1, 2, 3)   - built-in function
    """

    # Mapping from operator names to OpKind (simplified subset)
    _OP_NAMES = {
        '+': OpKind.ADD,
        '-': OpKind.SUB,
        '*': OpKind.MUL,
        '/': OpKind.DIV,
        '%': OpKind.MOD,
        'max': OpKind.MAX,
        'min': OpKind.MIN,
        'count': OpKind.COUNT,
        'and': OpKind.AND,
        'or': OpKind.OR,
        'not': OpKind.NOT,
        'toNatural': OpKind.TO_NATURAL,
        'toString': OpKind.TO_STRING,
    }

    def __init__(self, span: Span, function: Union[Id, OpKind], args: List[Node] = None):
        """
        Create a function term.

        Args:
            span: Source location
            function: Either an Id or an OpKind
            args: List of argument nodes (default: empty list)
        """
        super().__init__(span)

        # If function is an Id, check if it's a known operation
        if isinstance(function, Id):
            op_kind = self._OP_NAMES.get(function.name)
            self._function: Union[Id, OpKind] = op_kind if op_kind is not None else function
        else:
            self._function = function

        self._args: List[Node] = args if args is not None else []

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.FUNC_TERM

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        count = len(self._args)
        if isinstance(self._function, Node):
            count += 1
        return count

    @property
    def function(self) -> Union[Id, OpKind]:
        """Get the function (Id or OpKind)."""
        return self._function

    @property
    def args(self) -> List[Node]:
        """Get the argument list."""
        return self._args

    def add_arg(self, arg: Node):
        """
        Add an argument to this function term.

        Args:
            arg: The argument node to add
        """
        self._args.append(arg)

    def children(self) -> Iterator[Node]:
        """Get all children (function if it's a Node, plus all args)."""
        if isinstance(self._function, Node):
            yield self._function
        for arg in self._args:
            yield arg

    def __str__(self) -> str:
        """Get string representation."""
        if isinstance(self._function, OpKind):
            func_str = self._function.name.lower()
        else:
            func_str = str(self._function)

        if len(self._args) == 0:
            return f"{func_str}()"

        args_str = ", ".join(str(arg) for arg in self._args)
        return f"{func_str}({args_str})"

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"FuncTerm({self._function!r}, args={len(self._args)})"
