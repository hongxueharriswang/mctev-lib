"""
Level 2: Cultural parameter configurations θ_c.

Each culture c is represented by a weight vector over the six candidate
moral functions. Cultures differ in how they weight and prioritize the
Level 1 functions, not in whether they recognize them.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping

import numpy as np

from mctev.core.moral_functions import (
    MORAL_FUNCTION_ORDER,
    N_FUNCTIONS,
    MoralFunction,
    function_index,
)


@dataclass(frozen=True)
class CulturalParameters:
    """Cultural parameter vector θ_c ∈ ℝ^6."""

    weights: np.ndarray
    name: str = "custom"

    def __post_init__(self) -> None:
        w = np.asarray(self.weights, dtype=float)
        if w.shape != (N_FUNCTIONS,):
            raise ValueError(
                f"Expected vector of length {N_FUNCTIONS}, got {w.shape}"
            )
        if np.any(w < 0):
            raise ValueError("Cultural weights must be non-negative")
        object.__setattr__(self, "weights", w)

    def __getitem__(self, f: MoralFunction) -> float:
        return float(self.weights[function_index(f)])

    def normalized(self) -> "CulturalParameters":
        s = self.weights.sum()
        if s <= 0:
            raise ValueError("Cannot normalize zero-sum parameters")
        return CulturalParameters(weights=self.weights / s, name=self.name)

    def distance(self, other: "CulturalParameters") -> float:
        """L2 distance in parameter space."""
        return float(np.linalg.norm(self.weights - other.weights))

    def to_dict(self) -> Dict[str, float]:
        return {f.value: float(self[f]) for f in MORAL_FUNCTION_ORDER}

    @classmethod
    def from_dict(
        cls, d: Mapping[str, float], name: str = "custom"
    ) -> "CulturalParameters":
        vec = np.zeros(N_FUNCTIONS)
        for k, v in d.items():
            f = MoralFunction(k)
            vec[function_index(f)] = float(v)
        return cls(weights=vec, name=name)

    @classmethod
    def uniform(cls, name: str = "uniform") -> "CulturalParameters":
        return cls(
            weights=np.full(N_FUNCTIONS, 1.0 / N_FUNCTIONS), name=name
        )

    def __repr__(self) -> str:
        items = ", ".join(
            f"{f.value}={self[f]:.2f}" for f in MORAL_FUNCTION_ORDER
        )
        return f"CulturalParameters(name={self.name!r}, {items})"


def _vec(coop: float, conflict: float, dist: float, care: float,
         info: float, sustain: float) -> np.ndarray:
    return np.array([coop, conflict, dist, care, info, sustain], dtype=float)


CULTURAL_TYPES: Dict[str, CulturalParameters] = {
    "universalist": CulturalParameters(
        weights=_vec(0.30, 0.20, 0.20, 0.15, 0.10, 0.05),
        name="universalist",
    ),
    "collectivist": CulturalParameters(
        weights=_vec(0.25, 0.15, 0.15, 0.30, 0.10, 0.05),
        name="collectivist",
    ),
    "individualist": CulturalParameters(
        weights=_vec(0.20, 0.15, 0.20, 0.10, 0.20, 0.15),
        name="individualist",
    ),
    "self_regarding": CulturalParameters(
        weights=_vec(1.00, 0.00, 0.00, 0.00, 0.00, 0.00),
        name="self_regarding",
    ),
}


def get_cultural_type(name: str) -> CulturalParameters:
    """Retrieve a canonical cultural type by name."""
    key = name.lower().strip()
    if key not in CULTURAL_TYPES:
        raise KeyError(
            f"Unknown cultural type {name!r}. "
            f"Available: {list(CULTURAL_TYPES)}"
        )
    return CULTURAL_TYPES[key]


@dataclass(frozen=True)
class CulturalParametersRegion:
    """
    A simple convex region in cultural parameter space.

    Represents the set Θ_viable of viable cultural configurations.
    """

    lower: np.ndarray
    upper: np.ndarray

    def __post_init__(self) -> None:
        lo = np.asarray(self.lower, dtype=float)
        hi = np.asarray(self.upper, dtype=float)
        if lo.shape != (N_FUNCTIONS,) or hi.shape != (N_FUNCTIONS,):
            raise ValueError("Bounds must have shape (6,)")
        if np.any(lo > hi):
            raise ValueError("Lower bounds must not exceed upper bounds")
        object.__setattr__(self, "lower", lo)
        object.__setattr__(self, "upper", hi)

    def contains(self, params: CulturalParameters) -> bool:
        w = params.weights
        return bool(
            np.all(w >= self.lower - 1e-9)
            and np.all(w <= self.upper + 1e-9)
        )

    @classmethod
    def default(cls) -> "CulturalParametersRegion":
        return cls(
            lower=np.zeros(N_FUNCTIONS),
            upper=np.ones(N_FUNCTIONS),
        )
