"""
Rule node for rules and facts in FORMULA.
"""

from typing import List, Iterator, Optional

from ...common.enums import NodeKind
from .node import Node
from .body import Body
from .config import Config
from .span import Span


class Rule(Node):
    """
    Represents a rule or fact in FORMULA.

    Rules have the form: head1, head2, ... :- body1; body2; ...
    Facts are rules with no bodies (just heads).

    Examples:
        p(x).                    (fact)
        p(x) :- q(x).           (rule)
        p(x), q(x) :- r(x); s(x). (rule with multiple heads and bodies)
    """

    def __init__(self, span: Span):
        """
        Create a rule node.

        Args:
            span: Source location
        """
        super().__init__(span)
        self._heads: List[Node] = []
        self._bodies: List[Body] = []
        self._config: Optional[Config] = None

    @property
    def node_kind(self) -> NodeKind:
        """Get the node kind."""
        return NodeKind.RULE

    @property
    def child_count(self) -> int:
        """Get the number of children."""
        count = len(self._heads) + len(self._bodies)
        if self._config is not None:
            count += 1
        return count

    @property
    def is_fact(self) -> bool:
        """Check if this is a fact (rule with no bodies)."""
        return len(self._bodies) == 0

    @property
    def heads(self) -> List[Node]:
        """Get the list of head terms."""
        return self._heads

    @property
    def bodies(self) -> List[Body]:
        """Get the list of bodies."""
        return self._bodies

    @property
    def config(self) -> Optional[Config]:
        """Get the configuration (if any)."""
        return self._config

    @config.setter
    def config(self, value: Optional[Config]):
        """Set the configuration."""
        self._config = value

    def add_head(self, head: Node, add_last: bool = True):
        """
        Add a head term to this rule.

        Args:
            head: The head node (must be a function or atom)
            add_last: If True, add at end; if False, add at beginning

        Raises:
            AssertionError: If node is not a function or atom
        """
        assert head.is_func_or_atom, "Head must be a function or atom"
        if add_last:
            self._heads.append(head)
        else:
            self._heads.insert(0, head)

    def add_body(self, body: Body, add_last: bool = True):
        """
        Add a body to this rule.

        Args:
            body: The body node
            add_last: If True, add at end; if False, add at beginning
        """
        if add_last:
            self._bodies.append(body)
        else:
            self._bodies.insert(0, body)

    def children(self) -> Iterator[Node]:
        """Get all children (config, heads, and bodies)."""
        if self._config is not None:
            yield self._config
        for head in self._heads:
            yield head
        for body in self._bodies:
            yield body

    def __str__(self) -> str:
        """Get string representation."""
        heads_str = ", ".join(str(h) for h in self._heads)
        if self.is_fact:
            return f"{heads_str}."
        else:
            bodies_str = "; ".join(str(b) for b in self._bodies)
            return f"{heads_str} :- {bodies_str}."

    def __repr__(self) -> str:
        """Get detailed representation."""
        return f"Rule({len(self._heads)} heads, {len(self._bodies)} bodies)"
