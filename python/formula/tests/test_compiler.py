"""
Tests for compiler components (SymbolTable, Namespace).
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from formula.compiler import Namespace, SymbolTable
from formula.common import (
    BaseSortSymb,
    UserCnstSymb,
    Rational,
)
from formula.common.enums import BaseSortKind, UserCnstSymbKind


def test_namespace_creation():
    """Test creating namespaces."""
    root = Namespace("", None)
    assert root.name == ""
    assert root.parent is None

    child = root.get_or_create_child("Domain1")
    assert child.name == "Domain1"
    assert child.parent is root

    print("✓ Namespace creation works")


def test_namespace_hierarchy():
    """Test namespace hierarchy."""
    root = Namespace("", None)
    domain = root.get_or_create_child("MyDomain")
    subdomain = domain.get_or_create_child("SubDomain")

    # Check hierarchy
    assert subdomain.parent is domain
    assert domain.parent is root

    # Check full names
    assert root.full_name == ""
    assert domain.full_name == "MyDomain"
    assert subdomain.full_name == "MyDomain.SubDomain"

    print("✓ Namespace hierarchy works")


def test_namespace_symbol_management():
    """Test adding and retrieving symbols from namespaces."""
    ns = Namespace("TestNS", None)

    # Create a symbol
    var = UserCnstSymb("x", UserCnstSymbKind.VARIABLE)

    # Add to namespace
    assert ns.add_symbol("x", var) is True
    assert ns.add_symbol("x", var) is False  # Duplicate

    # Retrieve symbol
    retrieved = ns.get_symbol("x")
    assert retrieved is var

    # Non-existent symbol
    assert ns.get_symbol("y") is None

    print("✓ Namespace symbol management works")


def test_symbol_table_creation():
    """Test creating a symbol table."""
    table = SymbolTable("TestModule")

    assert table.module_name == "TestModule"
    assert table.is_valid is True
    assert table.root is not None
    assert table.module_space is not None

    print("✓ SymbolTable creation works")


def test_symbol_table_built_ins():
    """Test built-in symbols in symbol table."""
    table = SymbolTable("TestModule")

    # Get built-in sorts
    int_sort = table.get_sort_symbol(BaseSortKind.INTEGER)
    assert int_sort is not None
    assert int_sort.printable_name == "Integer"

    real_sort = table.get_sort_symbol(BaseSortKind.REAL)
    assert real_sort is not None
    assert real_sort.printable_name == "Real"

    string_sort = table.get_sort_symbol(BaseSortKind.STRING)
    assert string_sort is not None
    assert string_sort.printable_name == "String"

    print("✓ SymbolTable built-in symbols work")


def test_symbol_table_constants():
    """Test constant management in symbol table."""
    table = SymbolTable("TestModule")

    # Create string constants
    s1 = table.get_or_create_string_constant("hello")
    s2 = table.get_or_create_string_constant("hello")
    assert s1 is s2  # Should be same object (cached)

    s3 = table.get_or_create_string_constant("world")
    assert s3 is not s1

    # Create rational constants
    r1 = table.get_or_create_rational_constant(Rational(42))
    r2 = table.get_or_create_rational_constant(Rational(42))
    assert r1 is r2  # Should be same object (cached)

    r3 = table.get_or_create_rational_constant(Rational(99))
    assert r3 is not r1

    # Check collections
    assert len(table.string_cnsts) == 2
    assert len(table.rational_cnsts) == 2

    print("✓ SymbolTable constant management works")


def test_symbol_table_add_symbol():
    """Test adding symbols to symbol table."""
    table = SymbolTable("TestModule")

    # Create a symbol
    var = UserCnstSymb("myVar", UserCnstSymbKind.VARIABLE)

    # Add to table (should go to module namespace)
    assert table.add_symbol("myVar", var) is True
    assert table.add_symbol("myVar", var) is False  # Duplicate

    # Verify it's in module space
    retrieved = table.module_space.get_symbol("myVar")
    assert retrieved is var

    print("✓ SymbolTable add_symbol works")


def test_symbol_table_resolution():
    """Test symbol resolution."""
    table = SymbolTable("TestModule")

    # Add a symbol
    var = UserCnstSymb("x", UserCnstSymbKind.VARIABLE)
    table.add_symbol("x", var)

    # Resolve it
    symbol, conflict = table.resolve("x")
    assert symbol is var
    assert conflict is None

    # Resolve non-existent
    symbol, conflict = table.resolve("nonexistent")
    assert symbol is None
    assert conflict is None

    print("✓ SymbolTable resolution works")


def test_symbol_table_operations():
    """Test getting operation symbols."""
    from formula.common.enums import OpKind, RelKind, ReservedOpKind

    table = SymbolTable("TestModule")

    # Get arithmetic operation
    add_op = table.get_op_symbol(OpKind.ADD)
    assert add_op is not None
    assert add_op.arity == 2

    # Get relational operation
    eq_rel = table.get_rel_symbol(RelKind.EQ)
    assert eq_rel is not None
    assert eq_rel.arity == 2

    # Get reserved operation
    range_op = table.get_reserved_op_symbol(ReservedOpKind.RANGE)
    assert range_op is not None
    assert range_op.arity == 2

    print("✓ SymbolTable operation symbols work")


def test_symbol_table_integration():
    """Test symbol table integration scenario."""
    table = SymbolTable("MyDomain")

    # Add some symbols
    var_x = UserCnstSymb("x", UserCnstSymbKind.VARIABLE)
    var_y = UserCnstSymb("y", UserCnstSymbKind.VARIABLE)

    table.add_symbol("x", var_x)
    table.add_symbol("y", var_y)

    # Create some constants
    c1 = table.get_or_create_rational_constant(Rational(10))
    c2 = table.get_or_create_string_constant("test")

    # Get all symbols
    all_symbols = table.get_all_symbols()
    assert len(all_symbols) > 0

    # Verify symbol count increased
    assert table.n_symbols > 0

    print(f"✓ SymbolTable integration works ({table.n_symbols} symbols)")


if __name__ == "__main__":
    print("Running compiler component tests...\n")

    test_namespace_creation()
    test_namespace_hierarchy()
    test_namespace_symbol_management()
    test_symbol_table_creation()
    test_symbol_table_built_ins()
    test_symbol_table_constants()
    test_symbol_table_add_symbol()
    test_symbol_table_resolution()
    test_symbol_table_operations()
    test_symbol_table_integration()

    print("\nAll compiler tests passed! ✓")
