"""
The full Level-2 cultural-institutional configuration λ_c.

    λ_c = (θ_c, τ^V, τ^S, τ^H, ρ_c, M_c)

replaces the earlier `CulturalParameters` (which held only θ_c).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Mapping, Optional

import numpy as np

from mctev.core.moral_functions import (
    MoralFunction, MORAL_FUNCTION_ORDER, N_FUNCTIONS, function_index,
)
from mctev.core.thresholds import (
    ViabilityThresholds, SafeguardThresholds, FlourishingThresholds,
)
from mctev.core.selection import SelectionConvention
from mctev.core.measurement import MeasurementOperator, LinearMeasurement


@dataclass(frozen=True)
class CulturalConfiguration:
    """
    Full Level-2 configuration λ_c relative to a fixed architecture A.

    Attributes
    ----------
    weights : np.ndarray
        θ_c ∈ Δ^5, the compensatory weighting component.
    viability_thresholds : ViabilityThresholds
        τ^V, the dynamical viability thresholds.
    safeguard_thresholds : SafeguardThresholds
        τ^S, the safeguard thresholds.
    flourishing_thresholds : FlourishingThresholds
        τ^H, the flourishing thresholds.
    selection_convention : SelectionConvention
        ρ_c, the selection convention.
    measurement_operator : MeasurementOperator
        M_c, the measurement operator for flourishing.
    name : str
        Optional label for reporting.
    """

    weights: np.ndarray
    viability_thresholds: ViabilityThresholds
    safeguard_thresholds: SafeguardThresholds
    flourishing_thresholds: FlourishingThresholds
    selection_convention: SelectionConvention
    measurement_operator: MeasurementOperator
    name: str = "custom"

    def __post_init__(self) -> None:
        w = np.asarray(self.weights, dtype=float)
        if w.shape != (N_FUNCTIONS,):
            raise ValueError(
                f"Expected weights of length {N_FUNCTIONS}, got {w.shape}"
            )
        if np.any(w < 0):
            raise ValueError("Weights must be non-negative")
        if not np.isclose(w.sum(), 1.0, atol=1e-6):
            raise ValueError(
                f"Weights must sum to 1 (simplex normalization); "
                f"got sum = {w.sum()}"
            )
        object.__setattr__(self, "weights", w)

    def __getitem__(self, f: MoralFunction) -> float:
        return float(self.weights[function_index(f)])

    def to_dict(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "weights": {
                f.value: float(self[f]) for f in MORAL_FUNCTION_ORDER
            },
            "viability_thresholds": self.viability_thresholds.as_dict(),
            "safeguard_thresholds": self.safeguard_thresholds.as_dict(),
            "flourishing_thresholds": self.flourishing_thresholds.as_dict(),
            "selection_convention": self.selection_convention.value,
            "measurement_operator": type(self.measurement_operator).__name__,
        }

    def __repr__(self) -> str:
        return (
            f"CulturalConfiguration(name={self.name!r}, "
            f"weights={list(np.round(self.weights, 3))}, "
            f"ρ={self.selection_convention.value})"
        )


# =============================================================================
# Convenience constructors
# =============================================================================

def default_configuration(
    name: str = "default",
    weights: Optional[Iterable[float]] = None,
    viability_value: float = 0.3,
    safeguard_values: Optional[Mapping[str, float]] = None,
    flourishing_value: float = 0.5,
    selection: SelectionConvention = SelectionConvention.STATUS_QUO,
    measurement: Optional[MeasurementOperator] = None,
) -> CulturalConfiguration:
    """
    Build a configuration with sensible defaults.

    All three threshold families are provided explicitly; the selection
    convention defaults to status quo; the measurement operator defaults
    to identity on the five core dimensions.
    """
    if weights is None:
        w = np.full(N_FUNCTIONS, 1.0 / N_FUNCTIONS)
    else:
        w = np.asarray(list(weights), dtype=float)
        if not np.isclose(w.sum(), 1.0, atol=1e-6):
            w = w / w.sum()

    if measurement is None:
        measurement = LinearMeasurement(to_core=lambda x: np.asarray(x)[:5])

    return CulturalConfiguration(
        weights=w,
        viability_thresholds=ViabilityThresholds.uniform(viability_value),
        safeguard_thresholds=SafeguardThresholds.from_dict(
            safeguard_values or {}
        ),
        flourishing_thresholds=FlourishingThresholds.uniform(flourishing_value),
        selection_convention=selection,
        measurement_operator=measurement,
        name=name,
    )