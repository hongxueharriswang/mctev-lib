"""
The MCTEV hierarchical system: couples Level 1, Level 2, and Level 3.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, Optional

from mctev.core.cultural_params import (
    CULTURAL_TYPES,
    CulturalParameters,
    CulturalParametersRegion,
)
from mctev.core.moral_functions import MoralUtilityLibrary
from mctev.core.situational import Action, Situation, SituationalJudgment


@dataclass
class MCTEVSystem:
    """A complete MCTEV system combining all three levels."""

    cultural_params: CulturalParameters
    utilities: MoralUtilityLibrary = field(default_factory=MoralUtilityLibrary)
    constraints: Optional[Callable[[Situation, Action], bool]] = None
    viable_region: CulturalParametersRegion = field(
        default_factory=CulturalParametersRegion.default
    )

    def situational_layer(self) -> SituationalJudgment:
        return SituationalJudgment(
            utilities=self.utilities,
            constraints=self.constraints,
        )

    def judge(
        self,
        situation: Situation,
        actions: Iterable[Action],
    ) -> Optional[Action]:
        return self.situational_layer().judge(
            situation, actions, self.cultural_params
        )

    def is_viable(self) -> bool:
        return self.viable_region.contains(self.cultural_params)

    @classmethod
    def from_type(
        cls,
        type_name: str,
        utilities: MoralUtilityLibrary,
        constraints: Optional[Callable[[Situation, Action], bool]] = None,
        viable_region: Optional[CulturalParametersRegion] = None,
    ) -> "MCTEVSystem":
        params = CULTURAL_TYPES[type_name.lower()]
        return cls(
            cultural_params=params,
            utilities=utilities,
            constraints=constraints,
            viable_region=viable_region
            or CulturalParametersRegion.default(),
        )

    def describe(self) -> str:
        lines = [
            f"MCTEVSystem(name={self.cultural_params.name!r})",
            f"  viable: {self.is_viable()}",
            f"  params: {self.cultural_params.to_dict()}",
        ]
        return "\n".join(lines)
