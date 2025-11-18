"""
Built-in operation symbol for operators and reserved operations.
"""

from typing import Union, Callable, Optional, Any

from ..enums import SymbolKind, OpKind, RelKind, ReservedOpKind
from .symbol import Symbol


class BaseOpSymb(Symbol):
    """
    Represents a built-in operation symbol in FORMULA.

    Base operations can be:
    - Standard operations (OpKind): arithmetic, logical, string, list operations
    - Relational operations (RelKind): comparison operators
    - Reserved operations (ReservedOpKind): internal compiler operations

    Examples:
        + (addition), - (subtraction), * (multiplication)
        =, !=, <, >, <=, >=
        and, or, not
        select, range, typeUnn
    """

    def __init__(
        self,
        op_kind: Union[OpKind, RelKind, ReservedOpKind],
        arity: int,
        validator: Optional[Callable] = None,
        evaluator: Optional[Callable] = None,
    ):
        """
        Create a base operation symbol.

        Args:
            op_kind: The kind of operation (OpKind, RelKind, or ReservedOpKind)
            arity: The number of arguments this operation takes
            validator: Optional function to validate operation usage
            evaluator: Optional function to evaluate the operation
        """
        super().__init__()
        self._op_kind = op_kind
        self._arity = arity
        self._validator = validator
        self._evaluator = evaluator

    @property
    def kind(self) -> SymbolKind:
        """Get the symbol kind."""
        return SymbolKind.BASE_OP_SYMB

    @property
    def arity(self) -> int:
        """Get the operation arity."""
        return self._arity

    @property
    def printable_name(self) -> str:
        """Get a human-readable name."""
        return self._get_op_string()

    @property
    def op_kind(self) -> Union[OpKind, RelKind, ReservedOpKind]:
        """Get the operation kind."""
        return self._op_kind

    @property
    def is_reserved_operation(self) -> bool:
        """Check if this is a reserved operation."""
        return isinstance(self._op_kind, ReservedOpKind)

    @property
    def is_select(self) -> bool:
        """Check if this is the select operation."""
        return (
            isinstance(self._op_kind, ReservedOpKind)
            and self._op_kind == ReservedOpKind.SELECT
        )

    @property
    def is_type_unn(self) -> bool:
        """Check if this is the type union operation."""
        return (
            isinstance(self._op_kind, ReservedOpKind)
            and self._op_kind == ReservedOpKind.TYPE_UNN
        )

    @property
    def is_range(self) -> bool:
        """Check if this is the range operation."""
        return (
            isinstance(self._op_kind, ReservedOpKind)
            and self._op_kind == ReservedOpKind.RANGE
        )

    @property
    def is_relabel(self) -> bool:
        """Check if this is the relabel operation."""
        return (
            isinstance(self._op_kind, ReservedOpKind)
            and self._op_kind == ReservedOpKind.RELABEL
        )

    @property
    def is_sym_and(self) -> bool:
        """Check if this is the symbolic and operation."""
        return isinstance(self._op_kind, OpKind) and self._op_kind == OpKind.SYM_AND

    @property
    def is_sym_and_all(self) -> bool:
        """Check if this is the symbolic and-all operation."""
        return (
            isinstance(self._op_kind, OpKind) and self._op_kind == OpKind.SYM_AND_ALL
        )

    @property
    def is_sym_or(self) -> bool:
        """Check if this is the symbolic or operation."""
        return isinstance(self._op_kind, OpKind) and self._op_kind == OpKind.SYM_OR

    @property
    def is_sym_or_all(self) -> bool:
        """Check if this is the symbolic or-all operation."""
        return isinstance(self._op_kind, OpKind) and self._op_kind == OpKind.SYM_OR_ALL

    @property
    def is_sym_count(self) -> bool:
        """Check if this is the symbolic count operation."""
        return isinstance(self._op_kind, OpKind) and self._op_kind == OpKind.SYM_COUNT

    @property
    def is_sym_max(self) -> bool:
        """Check if this is the symbolic max operation."""
        return isinstance(self._op_kind, OpKind) and self._op_kind == OpKind.SYM_MAX

    @property
    def is_sym_max_all(self) -> bool:
        """Check if this is the symbolic max-all operation."""
        return (
            isinstance(self._op_kind, OpKind) and self._op_kind == OpKind.SYM_MAX_ALL
        )

    @property
    def is_sym_min(self) -> bool:
        """Check if this is the symbolic min operation."""
        return isinstance(self._op_kind, OpKind) and self._op_kind == OpKind.SYM_MIN

    @property
    def is_sym_min_all(self) -> bool:
        """Check if this is the symbolic min-all operation."""
        return (
            isinstance(self._op_kind, OpKind) and self._op_kind == OpKind.SYM_MIN_ALL
        )

    def _get_op_string(self) -> str:
        """Get a string representation of the operation."""
        # Simple mapping for common operators
        # This can be expanded with a full operator string table
        if isinstance(self._op_kind, OpKind):
            op_map = {
                OpKind.ADD: "+",
                OpKind.SUB: "-",
                OpKind.MUL: "*",
                OpKind.DIV: "/",
                OpKind.MOD: "mod",
                OpKind.NEG: "-",
                OpKind.AND: "and",
                OpKind.OR: "or",
                OpKind.NOT: "not",
                OpKind.MAX: "max",
                OpKind.MIN: "min",
            }
            return op_map.get(self._op_kind, self._op_kind.name.lower())
        elif isinstance(self._op_kind, RelKind):
            rel_map = {
                RelKind.EQ: "=",
                RelKind.NEQ: "!=",
                RelKind.LT: "<",
                RelKind.LE: "<=",
                RelKind.GT: ">",
                RelKind.GE: ">=",
                RelKind.TYP: ":",
                RelKind.NO: "no",
            }
            return rel_map.get(self._op_kind, self._op_kind.name.lower())
        elif isinstance(self._op_kind, ReservedOpKind):
            return self._op_kind.name.lower()
        else:
            return str(self._op_kind)

    def __repr__(self) -> str:
        """Get string representation."""
        return f"BaseOpSymb({self._get_op_string()!r}, arity={self._arity})"
