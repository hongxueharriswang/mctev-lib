"""
Level 3: situational judgments with situation-dependent action sets.

Revised for the manuscript:

    - Action sets are situation-dependent: A(s), not a static list.
    - The selection convention ρ_c resolves ties among maximizers.
    - The judgment correspondence is J(s; A, λ_c); the selection function
      is σ_{ρ_c}.
    - The configuration λ_c = (θ_c, τ^V, τ^S, τ^H, ρ_c, M_c) is threaded
      through so that the safeguard thresholds τ^S act on C(s; A, τ^S).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Hashable, Iterable, List, Optional

import numpy as np

from mctev.core.configuration import CulturalConfiguration
from mctev.core.moral_functions import MoralUtilityLibrary
from mctev.core.selection import SelectionConvention, select_action


# A constraint predicate takes (situation, action, configuration) → bool
ConstraintPredicate = Callable[
    ["Situation", "Action", "CulturalConfiguration"], bool
]

# A generator takes a situation and returns the available actions A(s)
ActionGenerator = Callable[["Situation"], List["Action"]]


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
    Level-3 solver.

    Parameters
    ----------
    utilities : MoralUtilityLibrary
        Per-function utilities u_f(a, s).
    constraints : Optional[ConstraintPredicate]
        Deontological constraint predicate C(s; A, τ^S). If provided, it
        is expected to inspect configuration.safeguard_thresholds.
    """

    utilities: MoralUtilityLibrary
    constraints: Optional[ConstraintPredicate] = None

    def admissible_actions(
        self,
        actions: Iterable[Action],
        situation: Situation,
        configuration: CulturalConfiguration,
    ) -> List[Action]:
        if self.constraints is None:
            return list(actions)
        return [
            a for a in actions
            if self.constraints(situation, a, configuration)
        ]

    def score(
        self,
        action: Action,
        situation: Situation,
        configuration: CulturalConfiguration,
    ) -> float:
        return self.utilities.evaluate(
            action, situation, configuration.weights
        )

    def correspondence(
        self,
        situation: Situation,
        actions: Iterable[Action],
        configuration: CulturalConfiguration,
    ) -> List[Action]:
        """Return J(s; A, λ_c) — the set of maximizers."""
        admissible = self.admissible_actions(actions, situation, configuration)
        if not admissible:
            return []
        scores = [
            (self.score(a, situation, configuration), a) for a in admissible
        ]
        best = max(s for s, _ in scores)
        return [a for s, a in scores if np.isclose(s, best)]

    def judge(
        self,
        situation: Situation,
        actions: Iterable[Action],
        configuration: CulturalConfiguration,
        previous_action: Optional[Action] = None,
        rng: Optional[np.random.Generator] = None,
        lexicographic_key: Optional[callable] = None,
    ) -> Optional[Action]:
        """Apply the selection function σ_{ρ_c} to J(s; A, λ_c)."""
        maximizers = self.correspondence(situation, actions, configuration)
        if not maximizers:
            return None
        return select_action(
            convention=configuration.selection_convention,
            maximizers=maximizers,
            situation=situation,
            previous_action=previous_action,
            rng=rng,
            lexicographic_key=lexicographic_key,
        )

    def rank(
        self,
        situation: Situation,
        actions: Iterable[Action],
        configuration: CulturalConfiguration,
    ) -> List[tuple]:
        admissible = self.admissible_actions(actions, situation, configuration)
        scored = [
            (self.score(a, situation, configuration), a) for a in admissible
        ]
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored