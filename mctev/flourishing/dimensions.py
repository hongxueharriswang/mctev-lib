"""
Flourishing profile and measurement integration.

FlourishingThresholds now lives in `mctev.core.thresholds` (as the third
threshold family τ^H). This module provides the profile type and the
measurement integration with M_c.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Optional

import numpy as np

from mctev.core.measurement import MeasurementOperator
from mctev.core.thresholds import FlourishingThresholds


DIMENSIONS = ("W", "P", "A", "S", "M")


class FlourishingDimension:
    """Convenience holder for dimension constants."""

    WELLBEING = "W"
    PSYCHOLOGICAL = "P"
    AGENCY = "A"
    SOCIAL = "S"
    MEANING = "M"


@dataclass(frozen=True)
class FlourishingProfile:
    """A five-dimensional observed flourishing profile Ĥ_c(x)."""

    values: np.ndarray

    def __post_init__(self) -> None:
        v = np.asarray(self.values, dtype=float)
        if v.shape != (5,):
            raise ValueError(f"Expected vector of length 5, got {v.shape}")
        object.__setattr__(self, "values", np.clip(v, 0.0, 1.0))

    def __getitem__(self, key: str) -> float:
        k = key.upper()
        if k not in DIMENSIONS:
            raise KeyError(f"Unknown dimension: {key!r}")
        return float(self.values[DIMENSIONS.index(k)])

    @classmethod
    def from_measurement(
        cls, x: np.ndarray, operator: MeasurementOperator
    ) -> "FlourishingProfile":
        return cls(values=operator.measure(x))

    @classmethod
    def from_dict(cls, d: Mapping[str, float]) -> "FlourishingProfile":
        v = np.zeros(5)
        for k, val in d.items():
            key = k.upper()
            v[DIMENSIONS.index(key)] = float(val)
        return cls(values=v)

    def meets(self, thresholds: FlourishingThresholds) -> bool:
        return bool(np.all(self.values >= thresholds.values - 1e-9))