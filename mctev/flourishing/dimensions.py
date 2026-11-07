"""
Human flourishing as a five-dimensional vector.

    H(x) = (W, P, A, S, M)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np


DIMENSIONS = ["W", "P", "A", "S", "M"]

DIMENSION_NAMES: Dict[str, str] = {
    "W": "wellbeing",
    "P": "psychological_functioning",
    "A": "agency",
    "S": "social_connectedness",
    "M": "meaning",
}


@dataclass(frozen=True)
class FlourishingProfile:
    """A point in the five-dimensional flourishing space."""

    values: np.ndarray

    def __post_init__(self) -> None:
        v = np.asarray(self.values, dtype=float)
        if v.shape != (5,):
            raise ValueError(
                f"Expected vector of length 5, got {v.shape}"
            )
        if np.any(v < 0) or np.any(v > 1 + 1e-9):
            raise ValueError("Flourishing values must lie in [0, 1]")
        object.__setattr__(self, "values", np.clip(v, 0.0, 1.0))

    def __getitem__(self, key: str) -> float:
        return float(self.values[DIMENSIONS.index(key)])

    def as_dict(self) -> Dict[str, float]:
        return {DIMENSION_NAMES[k]: float(self[k]) for k in DIMENSIONS}

    @classmethod
    def from_dict(cls, d: Dict[str, float]) -> "FlourishingProfile":
        v = np.zeros(5)
        for k, val in d.items():
            key = k.upper()
            if key not in DIMENSIONS:
                raise KeyError(
                    f"Unknown flourishing dimension: {k!r}"
                )
            v[DIMENSIONS.index(key)] = float(val)
        return cls(values=v)

    def __repr__(self) -> str:
        items = ", ".join(f"{k}={self[k]:.2f}" for k in DIMENSIONS)
        return f"FlourishingProfile({items})"


@dataclass(frozen=True)
class FlourishingThresholds:
    """Componentwise thresholds τ_H = (τ_W, τ_P, τ_A, τ_S, τ_M)."""

    thresholds: np.ndarray

    def __post_init__(self) -> None:
        t = np.asarray(self.thresholds, dtype=float)
        if t.shape != (5,):
            raise ValueError(
                f"Expected vector of length 5, got {t.shape}"
            )
        object.__setattr__(self, "thresholds", t)

    def is_flourishing(self, profile: FlourishingProfile) -> bool:
        return bool(np.all(profile.values >= self.thresholds - 1e-9))

    def deficit(self, profile: FlourishingProfile) -> float:
        d = self.thresholds - profile.values
        return float(np.sum(np.clip(d, 0.0, None)))

    @classmethod
    def default(cls) -> "FlourishingThresholds":
        return cls(thresholds=np.array([0.5, 0.5, 0.5, 0.5, 0.5]))

    @classmethod
    def from_dict(cls, d: Dict[str, float]) -> "FlourishingThresholds":
        v = np.zeros(5)
        for k, val in d.items():
            key = k.upper()
            if key not in DIMENSIONS:
                raise KeyError(f"Unknown dimension: {k!r}")
            v[DIMENSIONS.index(key)] = float(val)
        return cls(thresholds=v)
