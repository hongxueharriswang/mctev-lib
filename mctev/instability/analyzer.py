"""
Boundary-Instability analysis with the three design types of
manuscript Section 10.6.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

import numpy as np

from mctev.core.configuration import CulturalConfiguration
from mctev.core.moral_functions import MoralFunction, N_FUNCTIONS
from mctev.instability.safe_sets import SafeSet
from mctev.instability.survival import set_specific_survival
from mctev.viability.dynamics import Dynamics


THREE_DESIGNS = {
    "indicator_specific": {
        "description": (
            "index = V_i(λ_c), outcome = V(λ_c): proximity to an "
            "indicator-threshold boundary predicts exit from the "
            "viability set."
        ),
    },
    "kernel_to_viability_exit": {
        "description": (
            "index = R(λ_c; Π), outcome = V(λ_c): proximity to the "
            "kernel boundary predicts exit from the viability set. "
            "Additional model-specific assumptions required."
        ),
    },
    "kernel_retention": {
        "description": (
            "index = R(λ_c; Π), outcome = R(λ_c; Π): proximity to the "
            "kernel boundary predicts exit from the kernel itself. "
            "Reported separately from Prediction 5."
        ),
    },
}


@dataclass
class InstabilityResult:
    design_name: str
    index_set_name: str
    outcome_set_name: str
    inward_distances: np.ndarray
    survival_probabilities: np.ndarray
    horizon: float
    noise_scale: float
    n_trials: int

    def delta_epsilon(self) -> float:
        """
        Δ_ε = q(x_b − ε_2 n) − q(x_b − ε_1 n) for the outermost pair.
        """
        if len(self.survival_probabilities) < 2:
            return float("nan")
        return float(
            self.survival_probabilities[-1] - self.survival_probabilities[0]
        )

    def summary(self) -> str:
        rows = [
            f"{self.design_name}: "
            f"index={self.index_set_name}, outcome={self.outcome_set_name}"
        ]
        for eps, q in zip(self.inward_distances, self.survival_probabilities):
            rows.append(f"  ε={eps:.3f} → q = {q:.3f}")
        rows.append(f"  Δ_ε = {self.delta_epsilon():+.3f}")
        return "\n".join(rows)


@dataclass
class BoundaryInstabilityAnalyzer:
    """
    Runs Design A and Design B comparisons with the index/outcome-set
    distinction of manuscript Section 10.6.

    Parameters
    ----------
    dynamics : Dynamics
    configuration : CulturalConfiguration
    index_set : SafeSet
        The set whose boundary is used to index proximity (K_index).
    outcome_set : SafeSet
        The set whose survival is evaluated (K_out).
    noise_scale : float
    dt : float
    """

    dynamics: Dynamics
    configuration: CulturalConfiguration
    index_set: SafeSet
    outcome_set: SafeSet
    noise_scale: float = 0.02
    dt: float = 0.01
    rng: Optional[np.random.Generator] = None

    def __post_init__(self) -> None:
        if self.rng is None:
            self.rng = np.random.default_rng(0)

    def design_B(
        self,
        boundary_point: np.ndarray,
        inward_distances: list = (0.02, 0.05, 0.10, 0.20),
        horizon_steps: int = 500,
        n_trials: int = 40,
    ) -> InstabilityResult:
        """Compute Δ_ε^{K_index → K_out} over inward distances."""
        normal = self.index_set.boundary_normal(boundary_point)
        survival = []
        for eps in inward_distances:
            x0 = boundary_point - eps * normal
            outcomes = np.array([
                set_specific_survival(
                    x0=x0,
                    outcome_set=self.outcome_set,
                    dynamics=self.dynamics,
                    configuration=self.configuration,
                    horizon_steps=horizon_steps,
                    dt=self.dt,
                    noise_scale=self.noise_scale,
                    rng=np.random.default_rng(self.rng.integers(0, 2**31)),
                )
                for _ in range(n_trials)
            ])
            survival.append(float(outcomes.mean()))
        return InstabilityResult(
            design_name="Design B",
            index_set_name=type(self.index_set).__name__,
            outcome_set_name=type(self.outcome_set).__name__,
            inward_distances=np.asarray(inward_distances),
            survival_probabilities=np.asarray(survival),
            horizon=horizon_steps * self.dt,
            noise_scale=self.noise_scale,
            n_trials=n_trials,
        )


# ---------------------------------------------------------------------------
# Convenience: build the three designs for a given configuration
# ---------------------------------------------------------------------------

def build_three_designs(
    dynamics: Dynamics,
    configuration: CulturalConfiguration,
    viability_constraints: "ViabilityConstraints",  # type: ignore[name-defined]
    viability_kernel: "ViabilityKernel",  # type: ignore[name-defined]
    function: MoralFunction = MoralFunction.COOPERATION,
) -> Dict[str, BoundaryInstabilityAnalyzer]:
    """
    Build the three analyzers for the given configuration and kernel.
    """
    from mctev.instability.safe_sets import (
        IndicatorSafeSet, KernelSafeSet,
    )

    # V(λ_c): outcome set for designs 1 and 2
    from mctev.instability.safe_sets import SafeSet

    class _ViabilitySet(SafeSet):
        def contains(self, x):
            return viability_constraints.is_satisfied(x)
        def signed_distance(self, x):
            return float(-viability_constraints.violation_score(x)) or 1e-6

    V_set = _ViabilitySet()
    R_set = KernelSafeSet(kernel=viability_kernel)
    Vi_set = IndicatorSafeSet(
        indicator_fn=viability_constraints.viability_fns[function],
        threshold=viability_constraints.thresholds[function],
        function=function,
    )

    return {
        "indicator_specific": BoundaryInstabilityAnalyzer(
            dynamics=dynamics,
            configuration=configuration,
            index_set=Vi_set,
            outcome_set=V_set,
        ),
        "kernel_to_viability_exit": BoundaryInstabilityAnalyzer(
            dynamics=dynamics,
            configuration=configuration,
            index_set=R_set,
            outcome_set=V_set,
        ),
        "kernel_retention": BoundaryInstabilityAnalyzer(
            dynamics=dynamics,
            configuration=configuration,
            index_set=R_set,
            outcome_set=R_set,
        ),
    }