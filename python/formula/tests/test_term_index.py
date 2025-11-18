"""
Tests for TermIndex.
"""

import sys
import os

# Add parent directory to path so we can import formula
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from formula.common import TermIndex, Rational


def test_term_index_creation():
    """Test creating a term index."""
    index = TermIndex()
    assert index is not None
    assert index.count == 0
    print("✓ TermIndex creation works")


def test_string_constant_canonicalization():
    """Test that string constants are canonicalized."""
    index = TermIndex()

    # Create the same string constant twice
    t1 = index.mk_cnst("hello")
    t2 = index.mk_cnst("hello")

    # Should be the exact same object (canonicalized)
    assert t1 is t2, "String constants should be canonicalized"
    assert index.count == 1, "Only one term should be created"

    # Different string should create different term
    t3 = index.mk_cnst("world")
    assert t3 is not t1, "Different strings should create different terms"
    assert index.count == 2, "Two terms should exist"

    print("✓ String constant canonicalization works")


def test_rational_constant_canonicalization():
    """Test that rational constants are canonicalized."""
    index = TermIndex()

    # Create the same rational constant twice
    t1 = index.mk_cnst(Rational(42))
    t2 = index.mk_cnst(Rational(42))

    # Should be the exact same object (canonicalized)
    assert t1 is t2, "Rational constants should be canonicalized"
    assert index.count == 1, "Only one term should be created"

    # Different rational should create different term
    t3 = index.mk_cnst(Rational(99))
    assert t3 is not t1, "Different rationals should create different terms"
    assert index.count == 2, "Two terms should exist"

    print("✓ Rational constant canonicalization works")


def test_variable_canonicalization():
    """Test that variables are canonicalized."""
    index = TermIndex()

    # Create the same variable twice
    v1 = index.mk_var("x")
    v2 = index.mk_var("x")

    # Should be the exact same object (canonicalized)
    assert v1 is v2, "Variables should be canonicalized"
    assert index.count == 1, "Only one term should be created"

    # Different variable should create different term
    v3 = index.mk_var("y")
    assert v3 is not v1, "Different variables should create different terms"
    assert index.count == 2, "Two terms should exist"

    print("✓ Variable canonicalization works")


def test_built_in_constants():
    """Test that built-in constants are accessible."""
    index = TermIndex()

    # Access built-in constants
    true_val = index.true_value
    false_val = index.false_value
    zero_val = index.zero_value
    one_val = index.one_value
    empty_str = index.empty_string_value

    assert true_val is not None
    assert false_val is not None
    assert zero_val is not None
    assert one_val is not None
    assert empty_str is not None

    # Accessing again should return same instances
    assert index.true_value is true_val
    assert index.false_value is false_val
    assert index.zero_value is zero_val
    assert index.one_value is one_val
    assert index.empty_string_value is empty_str

    print("✓ Built-in constants work")


def test_term_application():
    """Test creating function applications."""
    index = TermIndex()

    # Create some constant terms
    a = index.mk_cnst(Rational(1))
    b = index.mk_cnst(Rational(2))

    # Create a simple symbol for testing
    from formula.common import BaseOpSymb, OpKind

    add_symb = BaseOpSymb(OpKind.ADD, 2)
    add_symb._id = 1000  # Set an ID

    # Create an application: add(1, 2)
    app1 = index.mk_apply(add_symb, (a, b))
    assert app1 is not None
    assert len(app1.args) == 2
    assert app1.args[0] is a
    assert app1.args[1] is b

    # Creating the same application should return the same term
    app2 = index.mk_apply(add_symb, (a, b))
    assert app1 is app2, "Applications should be canonicalized"

    # Different arguments should create different term
    c = index.mk_cnst(Rational(3))
    app3 = index.mk_apply(add_symb, (a, c))
    assert app3 is not app1, "Different applications should create different terms"

    print("✓ Term application canonicalization works")


def test_built_in_sorts():
    """Test accessing built-in sort symbols."""
    index = TermIndex()

    int_sort = index.get_integer_sort()
    real_sort = index.get_real_sort()
    string_sort = index.get_string_sort()
    nat_sort = index.get_natural_sort()

    assert int_sort is not None
    assert real_sort is not None
    assert string_sort is not None
    assert nat_sort is not None

    # Accessing again should return same instances
    assert index.get_integer_sort() is int_sort
    assert index.get_real_sort() is real_sort
    assert index.get_string_sort() is string_sort
    assert index.get_natural_sort() is nat_sort

    print("✓ Built-in sorts work")


def test_get_all_terms():
    """Test getting all terms from the index."""
    index = TermIndex()

    # Create some terms
    t1 = index.mk_cnst("a")
    t2 = index.mk_cnst("b")
    t3 = index.mk_cnst(Rational(42))
    v1 = index.mk_var("x")

    all_terms = index.get_all_terms()
    assert len(all_terms) == 4, "Should have 4 terms"
    assert t1 in all_terms
    assert t2 in all_terms
    assert t3 in all_terms
    assert v1 in all_terms

    # Terms should be sorted by UID
    for i in range(len(all_terms) - 1):
        assert all_terms[i].uid < all_terms[i + 1].uid

    print("✓ Get all terms works")


def test_term_uids():
    """Test that terms get unique IDs."""
    index = TermIndex()

    t1 = index.mk_cnst("a")
    t2 = index.mk_cnst("b")
    t3 = index.mk_cnst("c")

    # Each term should have a unique UID
    assert t1.uid == 0
    assert t2.uid == 1
    assert t3.uid == 2

    # Creating duplicate should not create new UID
    t1_again = index.mk_cnst("a")
    assert t1_again.uid == t1.uid

    print("✓ Term UIDs work correctly")


if __name__ == "__main__":
    print("Running TermIndex tests...")
    test_term_index_creation()
    test_string_constant_canonicalization()
    test_rational_constant_canonicalization()
    test_variable_canonicalization()
    test_built_in_constants()
    test_term_application()
    test_built_in_sorts()
    test_get_all_terms()
    test_term_uids()
    print("\nAll TermIndex tests passed!")
