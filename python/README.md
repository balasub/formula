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

```bash
# Install dependencies
pip install -e ".[dev]"

# Generate ANTLR4 parser (requires Java)
./scripts/generate_parser.sh
```

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

This Python port is being developed in stages:
- [x] Project structure and setup
- [ ] Parser generation and integration
- [ ] Core data structures
- [ ] AST node classes
- [ ] Compiler
- [ ] Solver
- [ ] API
- [ ] Testing infrastructure

## Original Project

The original .NET implementation can be found in `Src/Core/`.

## License

See LICENSE file for details.
