"""
Viability constraints using the dynamical viability thresholds τ^V.

This module no longer holds safeguard thresholds (they live in
`mctev.core.thresholds.SafeguardThresholds`) or flourishing thresholds
(they live in `mctev.core.thresholds.FlourishingThresholds`).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict

import numpy as np

from mctev.core.moral_functions import (
    MORAL_FUNCTION_ORDER, MoralFunction,
)
from mctev.core.thresholds import ViabilityThresholds


ViabilityFn = Callable[[np.ndarray], float]


@dataclass
class ViabilityConstraints:
    """
    The state-viability constraint set V(λ_c) defined by τ^V.

    Attributes
    ----------
    viability_fns : Dict[MoralFunction, ViabilityFn]
        Per-function indicator V_i(x).
    thresholds : ViabilityThresholds
        The dynamical viability thresholds τ^V.
    """

    viability_fns: Dict[MoralFunction, ViabilityFn] = field(
        default_factory=dict
    )
    thresholds: ViabilityThresholds = field(
        default_factory=lambda: ViabilityThresholds.uniform(0.3)
    )

    def __setitem__(
        self, f: MoralFunction, fn: ViabilityFn
    ) -> None:
        self.viability_fns[f] = fn

    def with_thresholds(
        self, thresholds: ViabilityThresholds
    ) -> "ViabilityConstraints":
        return ViabilityConstraints(
            viability_fns=dict(self.viability_fns), thresholds=thresholds
        )

    def values(self, x: np.ndarray) -> Dict[MoralFunction, float]:
        return {f: fn(x) for f, fn in self.viability_fns.items()}

    def violations(
        self, x: np.ndarray, tol: float = 1e-9
    ) -> Dict[MoralFunction, float]:
        out: Dict[MoralFunction, float] = {}
        for f, fn in self.viability_fns.items():
            deficit = self.thresholds[f] - fn(x)
            if deficit > tol:
                out[f] = deficit
        return out

    def is_satisfied(self, x: np.ndarray, tol: float = 1e-9) -> bool:
        return len(self.violations(x, tol)) == 0

    def violation_score(self, x: np.ndarray) -> float:
        return float(sum(self.violations(x).values()))


def default_constraints(
    thresholds: ViabilityThresholds = None,
) -> ViabilityConstraints:
    """Default illustrative constraints on a 6-D indicator vector."""
    thresholds = thresholds or ViabilityThresholds.uniform(0.3)
    constraints = ViabilityConstraints(thresholds=thresholds)
    for i, f in enumerate(MORAL_FUNCTION_ORDER):
        constraints[f] = (lambda x, i=i: float(x[i]))
    return constraints