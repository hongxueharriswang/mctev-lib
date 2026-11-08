"""Architecture objects for the capital-punishment case study."""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from typing import Callable, List

from mctev.core.configuration import CulturalConfiguration
from mctev.core.situational import Action, Situation, ConstraintPredicate


@dataclass
class Architecture(ABC):
    """
    Base for the constraint architectures A_R and A_A.

    Attributes
    ----------
    name : str
    categorical_prohibitions : List[str]
        Action names that are prohibited categorically (used by R1).
    constraint_predicate : ConstraintPredicate
        The deontological constraint C(s; A, τ^S).
    """

    name: str
    categorical_prohibitions: List[str] = field(default_factory=list)
    constraint_predicate: ConstraintPredicate = None  # type: ignore[assignment]

    def excludes_categorically(self, action_name: str) -> bool:
        return action_name in self.categorical_prohibitions


@dataclass
class RetentionistArchitecture(Architecture):
    """
    A_R: no categorical prohibition of capital punishment; retentionist
    non-vacuity checked via (R1)-(R3) in `conditions.py`.
    """

    def __post_init__(self) -> None:
        if self.name == "":
            self.name = "A_R"


@dataclass
class AbolitionistArchitecture(Architecture):
    """
    A_A: intentional irreversible deprivation of life prohibited
    categorically (R1 fails by construction).
    """

    def __post_init__(self) -> None:
        if "capital_punishment" not in self.categorical_prohibitions:
            self.categorical_prohibitions = (
                list(self.categorical_prohibitions) + ["capital_punishment"]
            )
        if self.name == "":
            self.name = "A_A"