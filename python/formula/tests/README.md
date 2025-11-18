# FORMULA Python Tests

This directory contains tests for the Python port of FORMULA.

## Running Tests

### Basic Parser Tests

To run the basic parser tests:

```bash
cd python
python -m formula.tests.test_parser_basic
```

Or using pytest (once installed):

```bash
cd python
pytest formula/tests/
```

## Test Coverage

Currently implemented:
- **test_parser_basic.py**: Basic ANTLR4 parser functionality tests
  - Empty programs
  - Domain declarations
  - Facts and rules
  - Constants (numeric, string, rational)
  - Function applications
  - Type declarations

## To Be Added

- AST construction tests
- Symbol table tests
- Type checking tests
- Solver tests
- Integration tests with .4ml files from the main test suite
