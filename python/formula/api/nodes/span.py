"""
Span and ProgramName classes for tracking source locations.
"""

from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class ProgramName:
    """
    Represents the name and location of a program.

    Attributes:
        name: The name of the program
        uri: The URI of the program file
    """
    name: str
    uri: str

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Span:
    """
    Represents a location span in source code.

    Attributes:
        start_line: Starting line number (1-indexed)
        start_col: Starting column number (1-indexed)
        end_line: Ending line number (1-indexed)
        end_col: Ending column number (1-indexed)
        program: The program this span belongs to
    """
    start_line: int
    start_col: int
    end_line: int
    end_col: int
    program: Optional[ProgramName] = None

    @staticmethod
    def unknown() -> 'Span':
        """Create an unknown span."""
        return Span(0, 0, 0, 0, None)

    @staticmethod
    def compare(s: 'Span', t: 'Span') -> int:
        """
        Compare two spans.

        Args:
            s: First span
            t: Second span

        Returns:
            -1 if s < t, 0 if equal, 1 if s > t
        """
        # Compare programs first
        if s.program != t.program:
            if s.program is None:
                return -1
            if t.program is None:
                return 1
            # Compare URIs
            if s.program.uri < t.program.uri:
                return -1
            elif s.program.uri > t.program.uri:
                return 1

        # Compare positions
        if s.start_line != t.start_line:
            return -1 if s.start_line < t.start_line else 1
        elif s.start_col != t.start_col:
            return -1 if s.start_col < t.start_col else 1
        elif s.end_line != t.end_line:
            return -1 if s.end_line < t.end_line else 1
        elif s.end_col != t.end_col:
            return -1 if s.end_col < t.end_col else 1

        return 0

    def __str__(self) -> str:
        """Get string representation of the span."""
        if self.program:
            return f"{self.program.name}({self.start_line},{self.start_col})-({self.end_line},{self.end_col})"
        else:
            return f"({self.start_line},{self.start_col})-({self.end_line},{self.end_col})"
