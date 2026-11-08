"""
MCTEVSystem — bundles the full configuration λ_c with the utility library.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional

from mctev.core.configuration import CulturalConfiguration
from mctev.core.moral_functions import MoralUtilityLibrary
from mctev.core.situational import (
    Action, Situation, SituationalJudgment, ConstraintPredicate,
)


@dataclass
class MCTEVSystem:
    """
    A complete MCTEV system at a fixed cultural-institutional configuration.

    Attributes
    ----------
    configuration : CulturalConfiguration
        λ_c, the full Level-2 configuration.
    utilities : MoralUtilityLibrary
        Per-function utilities.
    constraints : Optional[ConstraintPredicate]
        Deontological constraint predicate C(s; A, τ^S).
    """

    configuration: CulturalConfiguration
    utilities: MoralUtilityLibrary = field(default_factory=MoralUtilityLibrary)
    constraints: Optional[ConstraintPredicate] = None

    def situational_layer(self) -> SituationalJudgment:
        return SituationalJudgment(
            utilities=self.utilities, constraints=self.constraints
        )

    def judge(
        self,
        situation: Situation,
        actions: Iterable[Action],
        previous_action: Optional[Action] = None,
    ) -> Optional[Action]:
        return self.situational_layer().judge(
            situation,
            actions,
            self.configuration,
            previous_action=previous_action,
        )

    def describe(self) -> str:
        return (
            f"MCTEVSystem(configuration={self.configuration!r}, "
            f"has_constraints={self.constraints is not None})"
        )