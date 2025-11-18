"""
Enumerations used throughout the FORMULA system.
"""

from enum import Enum, auto


class Groundness(Enum):
    """Indicates whether a term is ground, variable, or a type."""
    GROUND = auto()
    VARIABLE = auto()
    TYPE = auto()


class SymbolKind(Enum):
    """The kind of symbol."""
    BASE_SORT_SYMB = auto()  # Built-in sort symbols
    BASE_CNST_SYMB = auto()  # Built-in constant symbols
    BASE_OP_SYMB = auto()    # Built-in operation symbols
    USER_CNST_SYMB = auto()  # User-defined constant symbols
    USER_SORT_SYMB = auto()  # User-defined sort symbols
    UNN_SYMB = auto()        # Union symbols
    CON_SYMB = auto()        # Constructor symbols
    MAP_SYMB = auto()        # Map symbols


class BaseSortKind(Enum):
    """Built-in sort kinds."""
    NEG_INTEGER = auto()
    POS_INTEGER = auto()
    NATURAL = auto()
    INTEGER = auto()
    REAL = auto()
    STRING = auto()


class UserCnstSymbKind(Enum):
    """User-defined constant symbol kinds."""
    NEW = auto()       # New constants
    DERIVED = auto()   # Derived constants
    VARIABLE = auto()  # Variables


class CnstKind(Enum):
    """Constant kinds."""
    NUMERIC = auto()
    STRING = auto()


class ContractKind(Enum):
    """Contract kinds for specifications."""
    CONFORMS_PROP = auto()
    ENSURES_PROP = auto()
    REQUIRES_PROP = auto()
    REQUIRES_SOME = auto()
    REQUIRES_AT_LEAST = auto()
    REQUIRES_AT_MOST = auto()


class ComposeKind(Enum):
    """Module composition kinds."""
    NONE = auto()
    INCLUDES = auto()
    EXTENDS = auto()


class RelKind(Enum):
    """Relational constraint kinds."""
    NO = auto()   # Negation
    EQ = auto()   # Equality
    NEQ = auto()  # Inequality
    LE = auto()   # Less than or equal
    LT = auto()   # Less than
    GE = auto()   # Greater than or equal
    GT = auto()   # Greater than
    TYP = auto()  # Type constraint


class MapKind(Enum):
    """Map function kinds."""
    FUN = auto()  # Function
    INJ = auto()  # Injective
    BIJ = auto()  # Bijective
    SUR = auto()  # Surjective


class SeverityKind(Enum):
    """Severity levels for diagnostics."""
    INFO = 0
    WARNING = 1
    ERROR = 2


class NodeKind(Enum):
    """AST node kinds."""
    CNST = auto()
    ID = auto()
    RANGE = auto()
    QUOTE_RUN = auto()
    CARD_PAIR = auto()
    QUOTE = auto()
    FUNC_TERM = auto()
    FIND = auto()
    MODEL_FACT = auto()
    COMPR = auto()
    REL_CONSTR = auto()
    BODY = auto()
    RULE = auto()
    CONTRACT_ITEM = auto()
    SETTING = auto()
    CONFIG = auto()
    FIELD = auto()
    ENUM = auto()
    UNION = auto()
    CON_DECL = auto()
    MAP_DECL = auto()
    UNN_DECL = auto()
    STEP = auto()
    MOD_REF = auto()
    MOD_APPLY = auto()
    PARAM = auto()
    DOMAIN = auto()
    TRANSFORM = auto()
    T_SYSTEM = auto()
    MODEL = auto()
    MACHINE = auto()
    PROPERTY = auto()
    UPDATE = auto()
    PROGRAM = auto()
    FOLDER = auto()
    ANY_NODE_KIND = auto()


class OpKind(Enum):
    """Built-in operation kinds."""
    ADD = auto()
    AND = auto()
    AND_ALL = auto()
    COUNT = auto()
    DIV = auto()
    GCD = auto()
    GCD_ALL = auto()
    IMPL = auto()
    IS_SUBSTRING = auto()
    LCM = auto()
    LCM_ALL = auto()
    LST_LENGTH = auto()
    LST_REVERSE = auto()
    LST_FIND = auto()
    LST_FIND_ALL = auto()
    LST_FIND_ALL_NOT = auto()
    LST_GET_AT = auto()
    MAX = auto()
    MAX_ALL = auto()
    MIN = auto()
    MIN_ALL = auto()
    MOD = auto()
    MUL = auto()
    NEG = auto()
    NOT = auto()
    OR = auto()
    OR_ALL = auto()
    PROD = auto()
    PROD_ALL = auto()
    RELABEL = auto()
    SELECT = auto()
    SIGN = auto()
    STRING_REVERSE = auto()
    STRING_TO_LOWER = auto()
    STRING_TO_UPPER = auto()
    STRING_LENGTH = auto()
    SUB = auto()
    SUM = auto()
    SUM_ALL = auto()
    TO_LIST = auto()
    TO_NATURAL = auto()
    TO_ORDINAL = auto()
    TO_STRING = auto()
    TUPLE_GET = auto()
    SYM_AND = auto()
    SYM_AND_ALL = auto()
    SYM_OR = auto()
    SYM_OR_ALL = auto()
    SYM_COUNT = auto()
    SYM_MAX = auto()
    SYM_MAX_ALL = auto()
    SYM_MIN = auto()
    SYM_MIN_ALL = auto()


class ReservedOpKind(Enum):
    """Reserved operation kinds for internal compiler operations."""
    RANGE = auto()       # Range(x, y): Construct a type for integers in [x, y]
    TYPE_UNN = auto()    # TypeUnn(x, y): Union of types x and y
    RELABEL = auto()     # Relabel(p, p', x): Relabel constructor application prefixes
    SELECT = auto()      # Select(x, y): Get argument named y from data term x
    FIND = auto()        # Find(t, p, tp): Find operation binding t, pattern p, type tp
    CONJ = auto()        # Conj(x, y): Conjunction of two body constraints
    CONJ_R = auto()      # ConjR(x, y): Conjunction of two disjoint partial rules
    DISJ = auto()        # Disj(x, y): Disjunction of two partial rules
    PROJ = auto()        # Proj(rule, vars): Projection of a partial rule
    P_RULE = auto()      # PRule(f1, f2, body): Partial rule with finds f1, f2
    C_RULE = auto()      # CRule(h, compr, rule): Rule computing comprehension
    RULE = auto()        # Rule(h, rule): Complete rule as a term
    COMPR = auto()       # Compr(heads, reads, disj): Comprehension


class InstallKind(Enum):
    """Module installation status."""
    COMPILED = auto()
    FAILED = auto()
    CACHED = auto()
    UNINSTALLED = auto()
