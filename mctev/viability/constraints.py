"""
Viability constraints V_i(x) ≥ τ_i.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict

import numpy as np

from mctev.core.moral_functions import MORAL_FUNCTION_ORDER, MoralFunction


ViabilityFn = Callable[[np.ndarray], float]


@dataclass
class ViabilityConstraints:
    """A set of viability constraints {V_i(x) ≥ τ_i}."""

    viability_fns: Dict[MoralFunction, ViabilityFn] = field(
        default_factory=dict
    )
    thresholds: Dict[MoralFunction, float] = field(default_factory=dict)

    def __setitem__(
        self,
        f: MoralFunction,
        pair: tuple,
    ) -> None:
        fn, tau = pair
        self.viability_fns[f] = fn
        self.thresholds[f] = float(tau)

    def __getitem__(self, f: MoralFunction) -> tuple:
        return self.viability_fns[f], self.thresholds[f]

    def values(self, x: np.ndarray) -> Dict[MoralFunction, float]:
        return {f: fn(x) for f, fn in self.viability_fns.items()}

    def violations(
        self,
        x: np.ndarray,
        tol: float = 1e-9,
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


def default_constraints() -> ViabilityConstraints:
    """Default illustrative constraints on a 6-D indicator vector."""
    constraints = ViabilityConstraints()
    for i, f in enumerate(MORAL_FUNCTION_ORDER):
        constraints[f] = (lambda x, i=i: float(x[i]), 0.3)
    return constraints
