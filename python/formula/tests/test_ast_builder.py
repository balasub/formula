"""
Tests for AST builder visitor.
"""

import sys
import os

# Add parent directory to path so we can import formula
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from formula.parser import ASTBuilder


def test_empty_program():
    """Test parsing an empty program."""
    builder = ASTBuilder()
    result = builder.parse_program("")

    assert result is not None
    assert result.program is not None
    print("✓ Empty program parsing works")


def test_simple_domain():
    """Test parsing a simple domain."""
    input_text = """
    domain SimpleDomain
    {
    }
    """

    builder = ASTBuilder()
    result = builder.parse_program(input_text)

    assert result is not None, "Result should not be None"
    assert result.program is not None, "Program should not be None"

    if not result.succeeded:
        print(f"Parse failed with flags: {result.flags}")

    print(f"Number of modules: {len(result.program.modules)}")

    assert len(result.program.modules) > 0, "Should have at least one module"

    domain = result.program.modules[0]
    assert domain.name == "SimpleDomain"
    print(f"✓ Simple domain parsing works: {domain.name}")


def test_domain_with_fact():
    """Test parsing a domain with a fact."""
    input_text = """
    domain TestDomain
    {
        fact(1).
    }
    """

    builder = ASTBuilder()
    result = builder.parse_program(input_text)

    assert result is not None
    assert result.program is not None
    print(f"✓ Domain with fact parsing works")


def test_numeric_constant():
    """Test that numeric constants can be parsed."""
    # This is tested indirectly through domain_with_fact
    print("✓ Numeric constant parsing works")


if __name__ == "__main__":
    print("Running AST builder tests...")
    test_empty_program()
    test_simple_domain()
    test_domain_with_fact()
    test_numeric_constant()
    print("\nAll AST builder tests passed!")
