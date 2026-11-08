"""
Three threshold families.

The manuscript (Section 7.1) distinguishes three families of thresholds that
govern three distinct objects:

    τ^V  — dynamical viability thresholds  → membership in V(λ_c)
    τ^S  — safeguard thresholds            → action admissibility in C(s; A, τ^S)
    τ^H  — flourishing thresholds          → membership in F(λ_c)

The three families are not interchangeable. This module provides separate
dataclasses for each and a container that bundles them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Mapping, Optional

import numpy as np

from mctev.core.moral_functions import (
    MoralFunction, MORAL_FUNCTION_ORDER, N_FUNCTIONS, function_index,
)


# =============================================================================
# τ^V — dynamical viability thresholds
# =============================================================================

@dataclass(frozen=True)
class ViabilityThresholds:
    """
    Dynamical viability thresholds τ^V ∈ T_V^{L1} ⊆ ℝ^6.

    These define the state-space viability region:

        V(λ_c) = { x ∈ X : V_i(x; λ_c) ≥ τ^V_i  ∀ i }

    They are distinct from safeguard thresholds τ^S (which govern action
    admissibility) and from flourishing thresholds τ^H (which govern F).
    """

    values: np.ndarray  # shape (6,)

    def __post_init__(self) -> None:
        v = np.asarray(self.values, dtype=float)
        if v.shape != (N_FUNCTIONS,):
            raise ValueError(
                f"Expected vector of length {N_FUNCTIONS}, got {v.shape}"
            )
        object.__setattr__(self, "values", v)

    def __getitem__(self, f: MoralFunction) -> float:
        return float(self.values[function_index(f)])

    def as_dict(self) -> Dict[str, float]:
        return {f.value: self[f] for f in MORAL_FUNCTION_ORDER}

    @classmethod
    def uniform(cls, value: float = 0.3) -> "ViabilityThresholds":
        return cls(values=np.full(N_FUNCTIONS, value))

    @classmethod
    def from_dict(cls, d: Mapping[str, float]) -> "ViabilityThresholds":
        vec = np.zeros(N_FUNCTIONS)
        for k, v in d.items():
            vec[function_index(MoralFunction(k))] = float(v)
        return cls(values=vec)

    @classmethod
    def from_array(cls, a: Iterable[float]) -> "ViabilityThresholds":
        return cls(values=np.asarray(list(a), dtype=float))


# =============================================================================
# τ^S — safeguard thresholds
# =============================================================================

@dataclass(frozen=True)
class SafeguardThresholds:
    """
    Action-level safeguard thresholds τ^S ∈ T_S^{L1}.

    These constrain which actions are admissible in specific situations.
    Unlike τ^V (state-level) and τ^H (flourishing-level), τ^S applies inside
    the Level-3 constraint predicate:

        C(s; A, τ^S) ⊆ A(s)

    Each safeguard has its own threshold value. The set of safeguard names
    is architecture-specific; the library uses string keys so that any
    architecture can declare its own safeguards.
    """

    values: Dict[str, float] = field(default_factory=dict)

    def __getitem__(self, name: str) -> float:
        return float(self.values[name])

    def get(self, name: str, default: Optional[float] = None) -> Optional[float]:
        return self.values.get(name, default)

    def as_dict(self) -> Dict[str, float]:
        return dict(self.values)

    @classmethod
    def from_dict(cls, d: Mapping[str, float]) -> "SafeguardThresholds":
        return cls(values={k: float(v) for k, v in d.items()})

    def with_overrides(self, **overrides: float) -> "SafeguardThresholds":
        merged = dict(self.values)
        merged.update({k: float(v) for k, v in overrides.items()})
        return SafeguardThresholds(values=merged)


# =============================================================================
# τ^H — flourishing thresholds
# =============================================================================

@dataclass(frozen=True)
class FlourishingThresholds:
    """
    Flourishing thresholds τ^H ∈ T_H^{L1} ⊆ ℝ^5.

    These define the flourishing region:

        F(λ_c) = { x ∈ X : Ĥ_c(x) ≥ τ^H }

    where Ĥ_c is the culturally specific measurement operator M_c applied
    to the state. The five dimensions are W (wellbeing), P (psychological
    functioning), A (agency), S (social connectedness), and M (meaning).
    """

    values: np.ndarray  # shape (5,)

    DIMENSIONS = ("W", "P", "A", "S", "M")

    def __post_init__(self) -> None:
        v = np.asarray(self.values, dtype=float)
        if v.shape != (5,):
            raise ValueError(f"Expected vector of length 5, got {v.shape}")
        object.__setattr__(self, "values", v)

    def __getitem__(self, dim: str) -> float:
        key = dim.upper()
        if key not in self.DIMENSIONS:
            raise KeyError(f"Unknown dimension: {dim!r}")
        return float(self.values[self.DIMENSIONS.index(key)])

    def as_dict(self) -> Dict[str, float]:
        return {d: float(self.values[i]) for i, d in enumerate(self.DIMENSIONS)}

    @classmethod
    def uniform(cls, value: float = 0.5) -> "FlourishingThresholds":
        return cls(values=np.full(5, value))

    @classmethod
    def from_dict(cls, d: Mapping[str, float]) -> "FlourishingThresholds":
        vec = np.zeros(5)
        for k, v in d.items():
            key = k.upper()
            if key not in cls.DIMENSIONS:
                raise KeyError(f"Unknown dimension: {k!r}")
            vec[cls.DIMENSIONS.index(key)] = float(v)
        return cls(values=vec)


# =============================================================================
# Container
# =============================================================================

@dataclass(frozen=True)
class ThresholdFamilies:
    """
    Container for the three threshold families.

    Kept as a separate dataclass (rather than merged into CulturalConfiguration)
    so that thresholds can be inspected and reported independently.
    """

    viability: ViabilityThresholds
    safeguard: SafeguardThresholds
    flourishing: FlourishingThresholds

    def as_dict(self) -> Dict[str, Dict[str, float]]:
        return {
            "viability": self.viability.as_dict(),
            "safeguard": self.safeguard.as_dict(),
            "flourishing": self.flourishing.as_dict(),
        }