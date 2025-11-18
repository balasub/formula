"""
FORMULA solver module.

This module contains the constraint solver and execution engine including:
- Z3 integration: Interface to Z3 theorem prover
- Strategies: Solving strategies
- Execution: Rule execution engine
- Type embedding: Type system integration with Z3
"""

from .z3_solver import Z3Solver

__all__ = [
    "Z3Solver",
]
