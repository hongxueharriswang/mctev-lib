"""
Level 3: Situational judgments.

Given a cultural parameter vector θ_c and a situation s, an agent
computes a judgment

    j(s; θ_c) = argmax_a Σ_f θ_{c,f} u_f(a, s)   subject to  a ∈ C(s)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Hashable, Iterable, List, Optional

from mctev.core.cultural_params import CulturalParameters
from mctev.core.moral_functions import MoralUtilityLibrary


@dataclass
class Action:
    """A named action, optionally carrying a payload."""

    name: str
    payload: Any = None

    def __hash__(self) -> int:
        return hash((self.name, id(self.payload)))


@dataclass
class Situation:
    """A situation with a name and an optional context dictionary."""

    name: str
    context: dict = field(default_factory=dict)


@dataclass
class SituationalJudgment:
    """
    A situational judgment solver.

    Parameters
    ----------
    utilities : MoralUtilityLibrary
        Per-function utility functions u_f(a, s).
    constraints : Optional[Callable[[Situation, Action], bool]]
        Deontological constraint predicate C(s); ``True`` means admissible.
    """

    utilities: MoralUtilityLibrary
    constraints: Optional[Callable[[Situation, Action], bool]] = None

    def admissible_actions(
        self,
        actions: Iterable[Action],
        situation: Situation,
    ) -> List[Action]:
        if self.constraints is None:
            return list(actions)
        return [a for a in actions if self.constraints(situation, a)]

    def score(
        self,
        action: Action,
        situation: Situation,
        params: CulturalParameters,
    ) -> float:
        """Compute Σ_f θ_{c,f} u_f(a, s)."""
        return self.utilities.evaluate(action, situation, params.weights)

    def judge(
        self,
        situation: Situation,
        actions: Iterable[Action],
        params: CulturalParameters,
    ) -> Optional[Action]:
        """Return the highest-scoring admissible action, or None."""
        candidates = self.admissible_actions(actions, situation)
        if not candidates:
            return None
        scored = [(self.score(a, situation, params), a) for a in candidates]
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]

    def rank(
        self,
        situation: Situation,
        actions: Iterable[Action],
        params: CulturalParameters,
    ) -> List[tuple]:
        """Return actions ranked by score, descending."""
        candidates = self.admissible_actions(actions, situation)
        scored = [(self.score(a, situation, params), a) for a in candidates]
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored
