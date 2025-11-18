"""
Rational number implementation for FORMULA.
"""

from fractions import Fraction
from typing import Union, Optional


class Rational:
    """
    A rational number representation.

    This is a wrapper around Python's built-in Fraction class
    with additional methods needed for FORMULA.
    """

    def __init__(self, numerator: int = 0, denominator: int = 1):
        """
        Create a rational number.

        Args:
            numerator: The numerator
            denominator: The denominator (must be non-zero)
        """
        self._fraction = Fraction(numerator, denominator)

    @property
    def numerator(self) -> int:
        """Get the numerator."""
        return self._fraction.numerator

    @property
    def denominator(self) -> int:
        """Get the denominator."""
        return self._fraction.denominator

    @classmethod
    def from_fraction(cls, fraction: Fraction) -> 'Rational':
        """Create a Rational from a Fraction."""
        result = cls.__new__(cls)
        result._fraction = fraction
        return result

    @classmethod
    def from_int(cls, value: int) -> 'Rational':
        """Create a Rational from an integer."""
        return cls(value, 1)

    @classmethod
    def from_string(cls, s: str) -> 'Rational':
        """
        Parse a rational from a string.

        Supports formats like "3/4", "5", "1.5"
        """
        if '/' in s:
            parts = s.split('/')
            return cls(int(parts[0]), int(parts[1]))
        elif '.' in s:
            return cls.from_fraction(Fraction(s))
        else:
            return cls(int(s), 1)

    def __add__(self, other: Union['Rational', int]) -> 'Rational':
        if isinstance(other, int):
            other = Rational.from_int(other)
        return Rational.from_fraction(self._fraction + other._fraction)

    def __sub__(self, other: Union['Rational', int]) -> 'Rational':
        if isinstance(other, int):
            other = Rational.from_int(other)
        return Rational.from_fraction(self._fraction - other._fraction)

    def __mul__(self, other: Union['Rational', int]) -> 'Rational':
        if isinstance(other, int):
            other = Rational.from_int(other)
        return Rational.from_fraction(self._fraction * other._fraction)

    def __truediv__(self, other: Union['Rational', int]) -> 'Rational':
        if isinstance(other, int):
            other = Rational.from_int(other)
        return Rational.from_fraction(self._fraction / other._fraction)

    def __neg__(self) -> 'Rational':
        return Rational.from_fraction(-self._fraction)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Rational):
            return self._fraction == other._fraction
        elif isinstance(other, int):
            return self._fraction == other
        return False

    def __lt__(self, other: Union['Rational', int]) -> bool:
        if isinstance(other, int):
            other = Rational.from_int(other)
        return self._fraction < other._fraction

    def __le__(self, other: Union['Rational', int]) -> bool:
        if isinstance(other, int):
            other = Rational.from_int(other)
        return self._fraction <= other._fraction

    def __gt__(self, other: Union['Rational', int]) -> bool:
        if isinstance(other, int):
            other = Rational.from_int(other)
        return self._fraction > other._fraction

    def __ge__(self, other: Union['Rational', int]) -> bool:
        if isinstance(other, int):
            other = Rational.from_int(other)
        return self._fraction >= other._fraction

    def __hash__(self) -> int:
        return hash(self._fraction)

    def __str__(self) -> str:
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"

    def __repr__(self) -> str:
        return f"Rational({self.numerator}, {self.denominator})"

    def is_integer(self) -> bool:
        """Check if this rational is an integer."""
        return self.denominator == 1

    def to_float(self) -> float:
        """Convert to a floating-point number."""
        return float(self._fraction)


class LiftedRational:
    """
    A rational number that can also be undefined.

    This is used for operations that may not have a defined result.
    """

    def __init__(self, value: Optional[Rational] = None):
        """
        Create a lifted rational.

        Args:
            value: The rational value, or None for undefined
        """
        self._value = value

    @property
    def is_defined(self) -> bool:
        """Check if this value is defined."""
        return self._value is not None

    @property
    def value(self) -> Optional[Rational]:
        """Get the value (may be None)."""
        return self._value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LiftedRational):
            if self._value is None:
                return other._value is None
            return self._value == other._value
        return False

    def __str__(self) -> str:
        if self._value is None:
            return "undefined"
        return str(self._value)

    def __repr__(self) -> str:
        return f"LiftedRational({self._value!r})"
