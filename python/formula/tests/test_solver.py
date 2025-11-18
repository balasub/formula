"""
Tests for Z3 solver integration.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import z3
from formula.solver import Z3Solver
from formula.common import TermIndex, Rational, BaseOpSymb
from formula.common.enums import OpKind, RelKind


def test_z3_solver_creation():
    """Test creating a Z3 solver."""
    solver = Z3Solver()

    assert solver is not None
    assert solver.solver is not None
    assert solver.term_index is not None

    print("✓ Z3Solver creation works")


def test_z3_basic_constraint():
    """Test adding and solving a basic constraint."""
    solver = Z3Solver()

    # Create a simple constraint: x > 0
    x = z3.Int('x')
    solver.add_constraint(x > 0)

    # Check satisfiability
    result = solver.check()
    assert result == z3.sat

    # Get model
    model = solver.get_model()
    assert model is not None
    print(f"  x = {model.eval(x)}")

    print("✓ Z3 basic constraint solving works")


def test_z3_unsatisfiable():
    """Test detecting unsatisfiable constraints."""
    solver = Z3Solver()

    # Create contradictory constraints
    x = z3.Int('x')
    solver.add_constraint(x > 10)
    solver.add_constraint(x < 5)

    # Should be unsatisfiable
    result = solver.check()
    assert result == z3.unsat

    print("✓ Z3 unsatisfiable detection works")


def test_z3_term_conversion_constants():
    """Test converting FORMULA constant terms to Z3."""
    index = TermIndex()
    solver = Z3Solver(index)

    # Create a numeric constant
    num_term = index.mk_cnst(Rational(42))
    z3_expr = solver.term_to_z3(num_term)

    assert z3_expr is not None
    # The expression should evaluate to approximately 42
    assert abs(float(z3_expr.as_fraction()) - 42.0) < 0.001

    print("✓ Z3 constant term conversion works")


def test_z3_term_conversion_variables():
    """Test converting FORMULA variable terms to Z3."""
    index = TermIndex()
    solver = Z3Solver(index)

    # Create a variable
    var_term = index.mk_var("x")
    z3_expr = solver.term_to_z3(var_term)

    assert z3_expr is not None
    assert str(z3_expr) == "x"

    # Same variable should return same Z3 variable
    var_term2 = index.mk_var("x")  # Should be canonicalized
    z3_expr2 = solver.term_to_z3(var_term2)
    assert z3_expr is z3_expr2

    print("✓ Z3 variable term conversion works")


def test_z3_term_conversion_operations():
    """Test converting FORMULA operation terms to Z3."""
    index = TermIndex()
    solver = Z3Solver(index)

    # Create terms: x + 5
    x = index.mk_var("x")
    five = index.mk_cnst(Rational(5))

    # Create addition operation
    add_op = BaseOpSymb(OpKind.ADD, 2)
    add_op._id = 1000
    add_term = index.mk_apply(add_op, (x, five))

    # Convert to Z3
    z3_expr = solver.term_to_z3(add_term)
    assert z3_expr is not None

    # Should be able to use in constraint
    solver.add_constraint(z3_expr > 10)
    result = solver.check()
    assert result == z3.sat

    model = solver.get_model()
    if model:
        x_val = model.eval(solver._z3_vars["x"])
        print(f"  x = {x_val} (x + 5 > 10)")

    print("✓ Z3 operation term conversion works")


def test_z3_arithmetic_expressions():
    """Test Z3 arithmetic expression solving."""
    index = TermIndex()
    solver = Z3Solver(index)

    # Create: (x + y) * 2 = 10
    x = index.mk_var("x")
    y = index.mk_var("y")
    two = index.mk_cnst(Rational(2))
    ten = index.mk_cnst(Rational(10))

    # Build (x + y)
    add_op = BaseOpSymb(OpKind.ADD, 2)
    add_op._id = 1001
    x_plus_y = index.mk_apply(add_op, (x, y))

    # Build (x + y) * 2
    mul_op = BaseOpSymb(OpKind.MUL, 2)
    mul_op._id = 1002
    result_term = index.mk_apply(mul_op, (x_plus_y, two))

    # Convert to Z3
    lhs = solver.term_to_z3(result_term)
    rhs = solver.term_to_z3(ten)

    # Add equality constraint
    solver.add_constraint(lhs == rhs)

    # Also add: x > 0, y > 0
    x_z3 = solver.term_to_z3(x)
    y_z3 = solver.term_to_z3(y)
    solver.add_constraint(x_z3 > 0)
    solver.add_constraint(y_z3 > 0)

    # Solve
    result = solver.check()
    assert result == z3.sat

    model = solver.get_model()
    if model:
        x_val = model.eval(solver._z3_vars["x"])
        y_val = model.eval(solver._z3_vars["y"])
        print(f"  Solution: x = {x_val}, y = {y_val}")
        # Verify: (x + y) * 2 = 10, so x + y = 5

    print("✓ Z3 arithmetic expressions work")


def test_z3_relational_constraints():
    """Test Z3 relational constraint solving."""
    index = TermIndex()
    solver = Z3Solver(index)

    # Create: x > y and y > 5
    x = index.mk_var("x")
    y = index.mk_var("y")
    five = index.mk_cnst(Rational(5))

    # x > y
    gt_op = BaseOpSymb(RelKind.GT, 2)
    gt_op._id = 2001
    x_gt_y = index.mk_apply(gt_op, (x, y))

    # y > 5
    gt_op2 = BaseOpSymb(RelKind.GT, 2)
    gt_op2._id = 2002
    y_gt_5 = index.mk_apply(gt_op2, (y, five))

    # Convert and solve
    z3_constraint1 = solver.term_to_z3(x_gt_y)
    z3_constraint2 = solver.term_to_z3(y_gt_5)

    solver.add_constraint(z3_constraint1)
    solver.add_constraint(z3_constraint2)

    result = solver.check()
    assert result == z3.sat

    model = solver.get_model()
    if model:
        x_val = model.eval(solver._z3_vars["x"])
        y_val = model.eval(solver._z3_vars["y"])
        print(f"  Solution: x = {x_val}, y = {y_val}")
        # Verify: x > y > 5

    print("✓ Z3 relational constraints work")


def test_z3_solver_reset():
    """Test resetting the solver state."""
    solver = Z3Solver()

    # Add some constraints
    x = z3.Int('x')
    solver.add_constraint(x > 0)

    # Check
    assert solver.check() == z3.sat

    # Reset
    solver.reset()

    # After reset, should have no constraints
    assert len(solver.solver.assertions()) == 0
    assert len(solver._z3_vars) == 0

    print("✓ Z3 solver reset works")


def test_z3_integration_scenario():
    """Test a complete integration scenario."""
    index = TermIndex()
    solver = Z3Solver(index)

    # Solve: Find x, y, z such that:
    # x + y + z = 15
    # x * y = z
    # x, y, z > 0

    x = index.mk_var("x")
    y = index.mk_var("y")
    z = index.mk_var("z")
    fifteen = index.mk_cnst(Rational(15))
    zero = index.mk_cnst(Rational(0))

    # Build x + y
    add1 = BaseOpSymb(OpKind.ADD, 2)
    add1._id = 3001
    x_plus_y = index.mk_apply(add1, (x, y))

    # Build (x + y) + z
    add2 = BaseOpSymb(OpKind.ADD, 2)
    add2._id = 3002
    sum_term = index.mk_apply(add2, (x_plus_y, z))

    # Build x * y
    mul = BaseOpSymb(OpKind.MUL, 2)
    mul._id = 3003
    product_term = index.mk_apply(mul, (x, y))

    # Constraint 1: x + y + z = 15
    eq1 = BaseOpSymb(RelKind.EQ, 2)
    eq1._id = 3004
    constraint1 = index.mk_apply(eq1, (sum_term, fifteen))

    # Constraint 2: x * y = z
    eq2 = BaseOpSymb(RelKind.EQ, 2)
    eq2._id = 3005
    constraint2 = index.mk_apply(eq2, (product_term, z))

    # Constraint 3: x > 0
    gt1 = BaseOpSymb(RelKind.GT, 2)
    gt1._id = 3006
    constraint3 = index.mk_apply(gt1, (x, zero))

    # Constraint 4: y > 0
    gt2 = BaseOpSymb(RelKind.GT, 2)
    gt2._id = 3007
    constraint4 = index.mk_apply(gt2, (y, zero))

    # Constraint 5: z > 0
    gt3 = BaseOpSymb(RelKind.GT, 2)
    gt3._id = 3008
    constraint5 = index.mk_apply(gt3, (z, zero))

    # Add all constraints
    solver.add_constraint(solver.term_to_z3(constraint1))
    solver.add_constraint(solver.term_to_z3(constraint2))
    solver.add_constraint(solver.term_to_z3(constraint3))
    solver.add_constraint(solver.term_to_z3(constraint4))
    solver.add_constraint(solver.term_to_z3(constraint5))

    # Solve
    result = solver.check()
    assert result == z3.sat

    model = solver.get_model()
    if model:
        x_val = model.eval(solver._z3_vars["x"])
        y_val = model.eval(solver._z3_vars["y"])
        z_val = model.eval(solver._z3_vars["z"])
        print(f"  Solution: x = {x_val}, y = {y_val}, z = {z_val}")

    print("✓ Z3 integration scenario works")


if __name__ == "__main__":
    print("Running Z3 solver tests...\n")

    test_z3_solver_creation()
    test_z3_basic_constraint()
    test_z3_unsatisfiable()
    test_z3_term_conversion_constants()
    test_z3_term_conversion_variables()
    test_z3_term_conversion_operations()
    test_z3_arithmetic_expressions()
    test_z3_relational_constraints()
    test_z3_solver_reset()
    test_z3_integration_scenario()

    print("\nAll Z3 solver tests passed! ✓")
