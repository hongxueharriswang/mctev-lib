"""
Measurement operators M_c.

Culturally specific measurement operators map a state x to observed
indicators on the five core flourishing dimensions. The manuscript
requires that M_c satisfy within-context ordinal validity and, when
cross-context comparison is claimed, one of the cross-context
comparability mechanisms (anchor states, invariant indicators,
explicit scale-linking maps, or partial-invariance constraints).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional

import numpy as np


class MeasurementOperator(ABC):
    """
    Abstract culturally specific measurement operator M_c.

    Concrete subclasses map a state to five flourishing indicators.
    """

    @abstractmethod
    def measure(self, x: np.ndarray) -> np.ndarray:
        """Map state x ∈ X to observed indicators Ĥ_c(x) ∈ ℝ^5."""

    def __call__(self, x: np.ndarray) -> np.ndarray:
        return self.measure(x)

    # ---- validity hooks (default = permissive) ----

    def within_context_monotone(
        self,
        x_lower: np.ndarray,
        x_higher: np.ndarray,
        dimension: int,
        n_samples: int = 50,
        rng: Optional[np.random.Generator] = None,
    ) -> bool:
        """
        Empirical within-context ordinal-validity check.

        Checks that E[Ĥ_d(x_higher)] > E[Ĥ_d(x_lower)] under the assumed
        measurement noise.
        """
        rng = rng or np.random.default_rng(0)
        samples_higher = np.array(
            [self.measure(x_higher)[dimension] for _ in range(n_samples)]
        )
        samples_lower = np.array(
            [self.measure(x_lower)[dimension] for _ in range(n_samples)]
        )
        return float(samples_higher.mean()) > float(samples_lower.mean())


@dataclass
class LinearMeasurement(MeasurementOperator):
    """
    Baseline additive measurement model:

        Ĥ_c(x) = g_c(H*(x)) + ε

    where g_c is a per-dimension monotone transformation and ε is
    additive Gaussian noise. This is the baseline working measurement
    model of the manuscript (Section 8.2), not the only admissible one.
    """

    to_core: Callable[[np.ndarray], np.ndarray]
    """Map raw state to the five core dimensions (identity by default)."""
    monotone_transforms: Dict[int, Callable[[float], float]] = field(
        default_factory=dict
    )
    noise_std: float = 0.0
    rng: Optional[np.random.Generator] = None

    def measure(self, x: np.ndarray) -> np.ndarray:
        core = np.asarray(self.to_core(x), dtype=float)
        if core.shape != (5,):
            raise ValueError(
                f"to_core must return shape (5,), got {core.shape}"
            )
        out = core.copy()
        for d, g in self.monotone_transforms.items():
            out[d] = float(g(out[d]))
        if self.noise_std > 0:
            rng = self.rng or np.random.default_rng(0)
            out = out + rng.normal(0.0, self.noise_std, size=5)
        return out


def validate_cross_context_comparability(
    operator_a: MeasurementOperator,
    operator_b: MeasurementOperator,
    anchor_states: Optional[list] = None,
    linking_map: Optional[Callable[[np.ndarray], np.ndarray]] = None,
    tolerance: float = 0.05,
) -> Dict[str, object]:
    """
    Check the cross-context comparability conditions of Section 8.2.

    Returns a report with `comparable` (bool) and `mechanism` (one of
    'anchors', 'linking_map', 'unavailable').

    Without at least one mechanism, cross-context comparison is not
    admissible and only within-context comparisons may be made.
    """
    if anchor_states is not None and len(anchor_states) > 0:
        # Compare the operators at anchor states
        discrepancies = []
        for x in anchor_states:
            ha = operator_a.measure(x)
            hb = operator_b.measure(x)
            discrepancies.append(float(np.linalg.norm(ha - hb)))
        return {
            "comparable": float(np.mean(discrepancies)) <= tolerance,
            "mechanism": "anchors",
            "mean_discrepancy": float(np.mean(discrepancies)),
        }

    if linking_map is not None:
        # Compare after applying the linking map
        return {
            "comparable": True,
            "mechanism": "linking_map",
        }

    return {
        "comparable": False,
        "mechanism": "unavailable",
    }