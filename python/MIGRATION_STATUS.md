# FORMULA .NET to Python Migration Status

This document tracks the progress of converting FORMULA from .NET to Python.

## Overview

**Original Codebase**: ~110,000 lines of C# across 209 files
**Target**: Python 3.9+ with ANTLR4 and Z3

## Completed Work

### ✅ Phase 1: Project Foundation (Commits 1-2)
- [x] Python project structure with `pyproject.toml`
- [x] Module directories (parser, common, compiler, solver, api)
- [x] ANTLR4 parser generation from existing grammar files
  - `FormulaLexer.py` (~24K lines)
  - `FormulaParser.py` (~211K lines)
  - `FormulaParserVisitor.py` (~15K lines)
- [x] Dependencies setup (antlr4-python3-runtime, z3-solver)
- [x] Parser generation script (`scripts/generate_parser.sh`)

### ✅ Phase 2: Core Data Structures (Commit 2)
- [x] **Enumerations** (`formula/common/enums.py`)
  - Groundness, SymbolKind, BaseSortKind, CnstKind
  - ContractKind, ComposeKind, RelKind, MapKind
  - NodeKind, OpKind, SeverityKind, InstallKind

- [x] **Rational Numbers** (`formula/common/rational.py`)
  - Rational class wrapping Python's Fraction
  - LiftedRational for optional values
  - Full arithmetic operations

- [x] **Immutable Collections** (`formula/common/immutable_array.py`)
  - ImmutableArray generic type

- [x] **Symbol Classes** (`formula/common/symbols/`)
  - Symbol base class with properties
  - BaseSortSymb (built-in types: Integer, Real, String, etc.)
  - BaseCnstSymb (constants: numeric and string)

- [x] **Term Classes** (`formula/common/terms/`)
  - Term class for expressions
  - Groundness computation
  - Term family classification
  - Symbolic term detection

### ✅ Phase 3: AST Node Classes (Commits 3-4)
- [x] **Base Infrastructure** (`formula/api/nodes/`)
  - Span: Source location tracking
  - ProgramName: Program identification
  - Node: Abstract base class with classification properties

- [x] **Basic Nodes**
  - Id: Identifiers (simple and qualified)
  - Cnst: Constants (numeric and string)
  - Range: Integer ranges (e.g., 1..10)

- [x] **Expression Nodes** (Commit 5)
  - FuncTerm: Function applications
  - Union: Type unions
  - ModRef: Module references

- [x] **Rule Nodes**
  - Body: Rule bodies and contracts
  - Config: Configuration blocks
  - Rule: Rules and facts

### ✅ Phase 4: Parser Validation (Commit 7)
- [x] Basic parser tests (`formula/tests/test_parser_basic.py`)
  - 7 tests covering core syntax
  - All tests passing
  - Validates ANTLR4 integration

## Current Status

**Total Commits**: 7
**Python Files Created**: ~30
**Lines of Python Code**: ~4,000
**Test Coverage**: Basic parser tests passing

## Architecture

```
python/formula/
├── parser/              # ANTLR4-generated (auto-generated)
│   ├── FormulaLexer.py
│   ├── FormulaParser.py
│   └── FormulaParserVisitor.py
├── common/              # Core data structures ✅
│   ├── enums.py
│   ├── rational.py
│   ├── immutable_array.py
│   ├── symbols/
│   │   ├── symbol.py
│   │   ├── base_sort_symb.py
│   │   └── base_cnst_symb.py
│   └── terms/
│       └── term.py
├── api/                 # AST nodes ✅ (partial)
│   └── nodes/
│       ├── node.py
│       ├── span.py
│       ├── id.py
│       ├── cnst.py
│       ├── range.py
│       ├── func_term.py
│       ├── mod_ref.py
│       ├── union.py
│       ├── body.py
│       ├── config.py
│       └── rule.py
├── compiler/            # ⏳ Pending
├── solver/              # ⏳ Pending
└── tests/               # ✅ (basic)
    └── test_parser_basic.py
```

## Remaining Work

### 🔨 In Progress
- Additional AST node types (Domain, Model, Transform, Machine, etc.)

### ⏳ To Do

#### High Priority
1. **Parser Integration** (Next Phase)
   - Visitor implementation to build AST from parse trees
   - AST factory methods
   - Error handling and reporting

2. **Additional Symbol Types**
   - UserCnstSymb, UserSortSymb
   - ConSymb, MapSymb, UnnSymb
   - BaseOpSymb
   - SymbolTable

3. **Complete AST Nodes** (~25 remaining)
   - Domain, Model, Transform, Machine, TSystem
   - ContractItem, ModelFact, Property, Update, Step
   - Find, RelConstr, Compr
   - ConDecl, MapDecl, UnnDecl
   - Field, Enum, Setting, Param
   - ModApply, Quote, QuoteRun
   - Program, Folder

4. **Term Index and Management**
   - TermIndex class
   - Term canonicalization
   - Term factories

#### Medium Priority
5. **Compiler Components**
   - Type checking
   - Linters
   - Constraint compilation
   - Symbol resolution

6. **Solver Engine**
   - Z3 integration
   - Constraint solving strategies
   - Rule execution engine
   - Type embedding

#### Lower Priority
7. **API Layer**
   - Query interfaces
   - Plugin system
   - Result types
   - AST queries

8. **Testing Infrastructure**
   - Port existing .4ml test files
   - Unit tests for all modules
   - Integration tests
   - Performance tests

## Migration Strategy

### Systematic Approach
1. ✅ Generate parser from existing grammar
2. ✅ Convert core data structures
3. ✅ Create basic AST node types
4. 🔨 Implement AST construction from parse trees
5. ⏳ Add compiler components
6. ⏳ Integrate Z3 solver
7. ⏳ Port test suite
8. ⏳ Validate against original implementation

### Commit Strategy
- Small, focused commits
- Each commit is buildable and testable
- Commits are pushed regularly to remote
- Clear commit messages explaining changes

## Testing

### Current Tests
```bash
cd python
python -m formula.tests.test_parser_basic
```

Output:
```
✓ Empty program
✓ Simple domain
✓ Domain with fact
✓ Constants
✓ Function applications
✓ Simple rule
✓ Type declarations

7 passed, 0 failed
```

## Dependencies

- Python >= 3.9
- antlr4-python3-runtime == 4.13.1
- z3-solver >= 4.12.0
- typing-extensions >= 4.0.0

## Next Steps

1. Create visitor classes to build AST from ANTLR4 parse trees
2. Add remaining AST node types (Domain, Model, etc.)
3. Implement symbol table and type system
4. Begin compiler integration
5. Integrate Z3 solver
6. Expand test coverage

## Notes

- The ANTLR4 grammar is shared between .NET and Python implementations
- Any changes to the grammar require regenerating both parsers
- Python implementation follows similar architecture to .NET version
- Some .NET-specific patterns (e.g., `out` parameters) adapted to Python idioms
- Using Python dataclasses and properties instead of C# properties
- Following Python naming conventions (snake_case for methods, PascalCase for classes)
