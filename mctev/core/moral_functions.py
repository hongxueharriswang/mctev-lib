"""
Level 1: Candidate Universal Moral Functions.

Implements the six candidate universal moral functions derived in
Section 6 of the MCTEV paper:

    f_coop    - Cooperation: reciprocal contribution to collective goods
    f_conflict- Conflict management: structured regulation of social conflict
    f_dist    - Resource distribution: resource accessibility for all members
    f_care    - Reproduction and care: care for the young and dependent
    f_info    - Knowledge transmission: information integrity in transmission
    f_sustain - Sustainability: restraint in resource use

These are "candidate" functions, not uniquely determined necessities.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Mapping, Sequence

import numpy as np


class MoralFunction(Enum):
    """The six candidate universal moral functions."""

    COOPERATION = "cooperation"
    CONFLICT_MANAGEMENT = "conflict"
    RESOURCE_DISTRIBUTION = "distribution"
    REPRODUCTION_CARE = "care"
    KNOWLEDGE_TRANSMISSION = "information"
    SUSTAINABILITY = "sustainability"

    @property
    def description(self) -> str:
        return {
            MoralFunction.COOPERATION: (
                "Reciprocal contribution to collective goods"
            ),
            MoralFunction.CONFLICT_MANAGEMENT: (
                "Structured regulation of social conflict"
            ),
            MoralFunction.RESOURCE_DISTRIBUTION: (
                "Resource accessibility for all members"
            ),
            MoralFunction.REPRODUCTION_CARE: (
                "Care for the young and dependent"
            ),
            MoralFunction.KNOWLEDGE_TRANSMISSION: (
                "Information integrity in transmission"
            ),
            MoralFunction.SUSTAINABILITY: (
                "Restraint in resource use"
            ),
        }[self]


MORAL_FUNCTION_ORDER: List[MoralFunction] = [
    MoralFunction.COOPERATION,
    MoralFunction.CONFLICT_MANAGEMENT,
    MoralFunction.RESOURCE_DISTRIBUTION,
    MoralFunction.REPRODUCTION_CARE,
    MoralFunction.KNOWLEDGE_TRANSMISSION,
    MoralFunction.SUSTAINABILITY,
]

N_FUNCTIONS: int = len(MORAL_FUNCTION_ORDER)


def function_index(f: MoralFunction) -> int:
    """Index of ``f`` in the canonical ordering."""
    return MORAL_FUNCTION_ORDER.index(f)


@dataclass(frozen=True)
class MoralFunctionProfile:
    """
    A vector of contributions across the six candidate moral functions.

    Each entry is the degree to which a state, action, or situation
    realizes the corresponding function, on [0, 1].
    """

    values: np.ndarray

    def __post_init__(self) -> None:
        v = np.asarray(self.values, dtype=float)
        if v.shape != (N_FUNCTIONS,):
            raise ValueError(
                f"Expected vector of length {N_FUNCTIONS}, got {v.shape}"
            )
        if np.any(v < -1e-9) or np.any(v > 1 + 1e-9):
            raise ValueError("Profile entries must be in [0, 1]")
        object.__setattr__(self, "values", np.clip(v, 0.0, 1.0))

    def __getitem__(self, f: MoralFunction) -> float:
        return float(self.values[function_index(f)])

    def as_dict(self) -> Dict[str, float]:
        return {f.value: float(self[f]) for f in MORAL_FUNCTION_ORDER}

    def dominance(self) -> float:
        """Fraction of functions above the minimal threshold 0.5."""
        return float(np.mean(self.values >= 0.5))

    def to_array(self) -> np.ndarray:
        return self.values.copy()

    @classmethod
    def from_dict(cls, d: Mapping[str, float]) -> "MoralFunctionProfile":
        vec = np.zeros(N_FUNCTIONS)
        for k, v in d.items():
            try:
                f = MoralFunction(k)
            except ValueError as e:
                raise ValueError(f"Unknown moral function: {k!r}") from e
            vec[function_index(f)] = float(v)
        return cls(values=vec)

    @classmethod
    def from_array(cls, arr: Sequence[float]) -> "MoralFunctionProfile":
        return cls(values=np.asarray(arr, dtype=float))

    @classmethod
    def uniform(cls, value: float = 0.5) -> "MoralFunctionProfile":
        return cls(values=np.full(N_FUNCTIONS, value))

    @classmethod
    def zeros(cls) -> "MoralFunctionProfile":
        return cls(values=np.zeros(N_FUNCTIONS))

    def __repr__(self) -> str:
        items = ", ".join(
            f"{f.value}={self[f]:.2f}" for f in MORAL_FUNCTION_ORDER
        )
        return f"MoralFunctionProfile({items})"


UtilityFn = Callable[[object, object], float]


@dataclass
class MoralUtilityLibrary:
    """
    Library of per-function utility functions.

    Each utility function ``u_f(a, s)`` returns the expected contribution
    of action ``a`` to moral function ``f`` in situation ``s``.
    """

    utilities: Dict[MoralFunction, UtilityFn] = field(default_factory=dict)

    def __setitem__(self, f: MoralFunction, fn: UtilityFn) -> None:
        self.utilities[f] = fn

    def __getitem__(self, f: MoralFunction) -> UtilityFn:
        if f not in self.utilities:
            return lambda a, s: 0.0
        return self.utilities[f]

    def evaluate(
        self,
        action: object,
        situation: object,
        weights: np.ndarray,
    ) -> float:
        """Weighted sum of function utilities."""
        total = 0.0
        for i, f in enumerate(MORAL_FUNCTION_ORDER):
            total += float(weights[i]) * self[f](action, situation)
        return total
