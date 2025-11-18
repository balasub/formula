"""
Basic parser tests for FORMULA.

These tests verify that the ANTLR4-generated parser can successfully
parse simple FORMULA programs.
"""

import sys
from io import StringIO
from antlr4 import InputStream, CommonTokenStream

from formula.parser import FormulaLexer, FormulaParser


def test_empty_program():
    """Test parsing an empty program."""
    input_text = ""
    input_stream = InputStream(input_text)
    lexer = FormulaLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = FormulaParser(token_stream)

    # Parse the program
    tree = parser.program()

    # Should successfully parse (no exceptions)
    assert tree is not None


def test_simple_domain():
    """Test parsing a simple empty domain."""
    input_text = """
    domain SimpleDomain
    {
    }
    """
    input_stream = InputStream(input_text)
    lexer = FormulaLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = FormulaParser(token_stream)

    # Parse the program
    tree = parser.program()

    # Should successfully parse
    assert tree is not None
    assert tree.moduleList() is not None


def test_domain_with_fact():
    """Test parsing a domain with a simple fact."""
    input_text = """
    domain TestDomain
    {
        foo.
    }
    """
    input_stream = InputStream(input_text)
    lexer = FormulaLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = FormulaParser(token_stream)

    # Parse the program
    tree = parser.program()

    # Should successfully parse
    assert tree is not None


def test_constant_terms():
    """Test parsing constants."""
    input_text = """
    domain Constants
    {
        42.
        "hello".
        3/4.
    }
    """
    input_stream = InputStream(input_text)
    lexer = FormulaLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = FormulaParser(token_stream)

    # Parse the program
    tree = parser.program()

    # Should successfully parse
    assert tree is not None


def test_function_application():
    """Test parsing function applications."""
    input_text = """
    domain Functions
    {
        f(x).
        g(1, 2, 3).
        h().
    }
    """
    input_stream = InputStream(input_text)
    lexer = FormulaLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = FormulaParser(token_stream)

    # Parse the program
    tree = parser.program()

    # Should successfully parse
    assert tree is not None


def test_simple_rule():
    """Test parsing a simple rule."""
    input_text = """
    domain Rules
    {
        p(x) :- q(x).
    }
    """
    input_stream = InputStream(input_text)
    lexer = FormulaLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = FormulaParser(token_stream)

    # Parse the program
    tree = parser.program()

    # Should successfully parse
    assert tree is not None


def test_type_declaration():
    """Test parsing a type declaration."""
    input_text = """
    domain Types
    {
        Color ::= {red, green, blue}.
        Point ::= (x: Integer, y: Integer).
    }
    """
    input_stream = InputStream(input_text)
    lexer = FormulaLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = FormulaParser(token_stream)

    # Parse the program
    tree = parser.program()

    # Should successfully parse
    assert tree is not None


def main():
    """Run all tests."""
    tests = [
        ("Empty program", test_empty_program),
        ("Simple domain", test_simple_domain),
        ("Domain with fact", test_domain_with_fact),
        ("Constants", test_constant_terms),
        ("Function applications", test_function_application),
        ("Simple rule", test_simple_rule),
        ("Type declarations", test_type_declaration),
    ]

    print("Running FORMULA parser tests...\n")
    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            print(f"✓ {name}")
            passed += 1
        except Exception as e:
            print(f"✗ {name}: {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
