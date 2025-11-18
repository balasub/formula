# FORMULA - Python Version

This is a Python port of the FORMULA formal specification language and verification tool.

## About FORMULA

FORMULA is a formal specification language for model-based design that provides:
- **Domains**: Type systems and constraint specifications
- **Models**: Instances of domains with facts and constraints
- **Transforms**: Rules for transforming models
- **Systems**: Compositions of transforms
- **Machines**: State machines over models

## Project Structure

```
formula/
├── parser/          # ANTLR4-generated parser and lexer
├── common/          # Core data structures (terms, symbols, rules)
├── compiler/        # Compilation and validation
├── solver/          # Constraint solving and execution engine
├── api/             # Public API and AST nodes
└── tests/           # Test suite
```

## Installation

### From Source

**IMPORTANT**: You must generate the ANTLR parser files before running tests or using the library.

```bash
# 1. Install dependencies
pip install -e ".[dev]"

# 2. Generate ANTLR4 parser (requires Java 8+)
cd /path/to/formula/python
./scripts/generate_parser.sh
```

This will:
- Download ANTLR 4.13.1 if not already present
- Generate `FormulaLexer.py`, `FormulaParser.py`, and `FormulaVisitor.py`
- Place generated files in `formula/parser/`

## Dependencies

- Python >= 3.9
- ANTLR4 runtime for Python
- Z3 theorem prover

## Development

This is a work-in-progress port from the original .NET implementation.

### Generating the Parser

The parser is generated from ANTLR4 grammar files:
- `Src/Core/API/Parser/FormulaLexer.g4`
- `Src/Core/API/Parser/FormulaParser.g4`

Use the provided script to regenerate:
```bash
./scripts/generate_parser.sh
```

## Migration Status

**Core migration: COMPLETE ✓**

This Python port has been developed in stages:
- [x] Project structure and setup
- [x] Parser generation and integration
- [x] Core data structures (symbols, terms, rules)
- [x] AST node classes (29 types)
- [x] Compiler (namespace, symbol table)
- [x] Solver (Z3 integration)
- [x] Testing infrastructure (50+ tests)

See `MIGRATION_STATUS.md` for detailed progress information.

## Original Project

The original .NET implementation can be found in `Src/Core/`.

## License

See LICENSE file for details.
