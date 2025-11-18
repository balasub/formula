"""
Z3 solver integration for FORMULA.

This module provides integration with the Z3 theorem prover for
constraint solving and model checking.
"""

from typing import List, Optional, Tuple, Any
import z3

from ..common import Term, TermIndex, Rational
from ..common.enums import SymbolKind, OpKind, RelKind


class Z3Solver:
    """
    Wrapper around Z3 for FORMULA constraint solving.

    This class provides methods to translate FORMULA terms and constraints
    into Z3 expressions and solve them.
    """

    def __init__(self, term_index: Optional[TermIndex] = None):
        """
        Create a Z3 solver instance.

        Args:
            term_index: Optional term index for term management
        """
        self._solver = z3.Solver()
        self._term_index = term_index or TermIndex()
        self._z3_vars: dict[str, z3.ExprRef] = {}
        self._term_cache: dict[int, z3.ExprRef] = {}  # Maps term UID to Z3 expr

    @property
    def solver(self) -> z3.Solver:
        """Get the underlying Z3 solver."""
        return self._solver

    @property
    def term_index(self) -> TermIndex:
        """Get the term index."""
        return self._term_index

    def reset(self):
        """Reset the solver state."""
        self._solver.reset()
        self._z3_vars.clear()
        self._term_cache.clear()

    def add_constraint(self, constraint: z3.BoolRef):
        """
        Add a constraint to the solver.

        Args:
            constraint: The Z3 boolean constraint
        """
        self._solver.add(constraint)

    def check(self) -> z3.CheckSatResult:
        """
        Check if the current constraints are satisfiable.

        Returns:
            z3.sat, z3.unsat, or z3.unknown
        """
        return self._solver.check()

    def get_model(self) -> Optional[z3.ModelRef]:
        """
        Get a model if the constraints are satisfiable.

        Returns:
            Z3 model, or None if unsat
        """
        if self.check() == z3.sat:
            return self._solver.model()
        return None

    def term_to_z3(self, term: Term) -> z3.ExprRef:
        """
        Convert a FORMULA term to a Z3 expression.

        Args:
            term: The FORMULA term

        Returns:
            Z3 expression
        """
        # Check cache first
        if term.uid in self._term_cache:
            return self._term_cache[term.uid]

        symbol = term.symbol
        symbol_kind = symbol.kind

        # Handle constants
        if symbol_kind == SymbolKind.BASE_CNST_SYMB:
            from ..common.symbols import BaseCnstSymb
            from ..common.enums import CnstKind
            if isinstance(symbol, BaseCnstSymb):
                if symbol.cnst_kind == CnstKind.NUMERIC:
                    # Convert rational to Z3 real
                    rat = symbol.raw
                    if isinstance(rat, Rational):
                        # Convert Rational to float using numerator/denominator
                        float_val = rat.numerator / rat.denominator
                        expr = z3.RealVal(float_val)
                    else:
                        expr = z3.RealVal(0)
                elif symbol.cnst_kind == CnstKind.STRING:
                    # Z3 string
                    expr = z3.StringVal(str(symbol.raw))
                else:
                    raise ValueError(f"Unknown constant type: {symbol}")
            else:
                raise ValueError(f"Expected BaseCnstSymb, got {type(symbol)}")

        # Handle variables
        elif symbol_kind == SymbolKind.USER_CNST_SYMB:
            from ..common.symbols import UserCnstSymb
            if isinstance(symbol, UserCnstSymb):
                var_name = symbol.name
                if var_name not in self._z3_vars:
                    # Create Z3 variable (default to integer for now)
                    self._z3_vars[var_name] = z3.Int(var_name)
                expr = self._z3_vars[var_name]
            else:
                raise ValueError(f"Expected UserCnstSymb, got {type(symbol)}")

        # Handle operations
        elif symbol_kind == SymbolKind.BASE_OP_SYMB:
            from ..common.symbols import BaseOpSymb
            if isinstance(symbol, BaseOpSymb):
                op_kind = symbol.op_kind

                # Convert arguments
                args = [self.term_to_z3(arg) for arg in term.args]

                # Handle different operation types
                if isinstance(op_kind, OpKind):
                    expr = self._handle_op_kind(op_kind, args)
                elif isinstance(op_kind, RelKind):
                    expr = self._handle_rel_kind(op_kind, args)
                else:
                    raise ValueError(f"Unknown operation kind: {op_kind}")
            else:
                raise ValueError(f"Expected BaseOpSymb, got {type(symbol)}")

        else:
            # For other symbol types, create a placeholder
            expr = z3.Int(f"term_{term.uid}")

        # Cache the result
        self._term_cache[term.uid] = expr
        return expr

    def _handle_op_kind(self, op_kind: OpKind, args: List[z3.ExprRef]) -> z3.ExprRef:
        """Handle OpKind operations."""
        if op_kind == OpKind.ADD:
            return args[0] + args[1]
        elif op_kind == OpKind.SUB:
            return args[0] - args[1]
        elif op_kind == OpKind.MUL:
            return args[0] * args[1]
        elif op_kind == OpKind.DIV:
            return args[0] / args[1]
        elif op_kind == OpKind.MOD:
            return args[0] % args[1]
        elif op_kind == OpKind.NEG:
            return -args[0]
        elif op_kind == OpKind.AND:
            return z3.And(args[0], args[1])
        elif op_kind == OpKind.OR:
            return z3.Or(args[0], args[1])
        elif op_kind == OpKind.NOT:
            return z3.Not(args[0])
        elif op_kind == OpKind.IMPL:
            return z3.Implies(args[0], args[1])
        else:
            raise ValueError(f"Unsupported operation: {op_kind}")

    def _handle_rel_kind(self, rel_kind: RelKind, args: List[z3.ExprRef]) -> z3.BoolRef:
        """Handle RelKind relations."""
        if rel_kind == RelKind.EQ:
            return args[0] == args[1]
        elif rel_kind == RelKind.NEQ:
            return args[0] != args[1]
        elif rel_kind == RelKind.LT:
            return args[0] < args[1]
        elif rel_kind == RelKind.LE:
            return args[0] <= args[1]
        elif rel_kind == RelKind.GT:
            return args[0] > args[1]
        elif rel_kind == RelKind.GE:
            return args[0] >= args[1]
        else:
            raise ValueError(f"Unsupported relation: {rel_kind}")

    def solve_and_print(self) -> bool:
        """
        Solve constraints and print the result.

        Returns:
            True if satisfiable, False otherwise
        """
        result = self.check()

        if result == z3.sat:
            print("SAT - Model found:")
            model = self.get_model()
            if model:
                for var_name, var_expr in sorted(self._z3_vars.items()):
                    val = model.eval(var_expr)
                    print(f"  {var_name} = {val}")
            return True
        elif result == z3.unsat:
            print("UNSAT - No solution exists")
            return False
        else:
            print("UNKNOWN - Solver could not determine satisfiability")
            return False

    def __repr__(self) -> str:
        """Get string representation."""
        return f"Z3Solver({len(self._z3_vars)} variables, {len(self._solver.assertions())} constraints)"
