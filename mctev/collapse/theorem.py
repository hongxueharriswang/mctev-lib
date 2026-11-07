"""
Empirical evaluation of the Constraint Violation Theorem.

    P(τ_exit > T) ≤ C exp(−λ T)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
from scipy.optimize import curve_fit

from mctev.core.cultural_params import CulturalParameters
from mctev.core.moral_functions import N_FUNCTIONS
from mctev.viability.constraints import ViabilityConstraints
from mctev.viability.dynamics import Dynamics


@dataclass
class ExitTimeResult:
    """Container for exit-time simulation results."""

    exit_times: np.ndarray
    horizon: float
    noise_scale: float
    n_trials: int

    @property
    def censor_rate(self) -> float:
        return float(np.mean(np.isclose(self.exit_times, self.horizon)))

    def survival_function(
        self, n_points: int = 100
    ) -> tuple:
        times = np.linspace(0, self.horizon, n_points)
        S = np.array([np.mean(self.exit_times > t) for t in times])
        return times, S

    def fit_exponential(self) -> tuple:
        times, S = self.survival_function(n_points=50)
        mask = S > 1e-6
        if mask.sum() < 3:
            return float("nan"), float("nan")

        def model(t: np.ndarray, C: float, lam: float) -> np.ndarray:
            return C * np.exp(-lam * t)

        try:
            popt, _ = curve_fit(
                model,
                times[mask],
                S[mask],
                p0=(1.0, 1.0 / max(times[mask].max(), 1e-3)),
                maxfev=10_000,
            )
            return float(popt[0]), float(popt[1])
        except RuntimeError:
            return float("nan"), float("nan")

    def summary(self) -> str:
        C, lam = self.fit_exponential()
        return (
            f"ExitTimeResult(n={self.n_trials}, "
            f"horizon={self.horizon}, noise={self.noise_scale})\n"
            f"  mean exit time: {self.exit_times.mean():.3f}\n"
            f"  censor rate: {self.censor_rate:.2%}\n"
            f"  exponential fit: C={C:.3f}, λ={lam:.3f}"
        )


@dataclass
class ConstraintViolationAnalyzer:
    """Empirically evaluate the Constraint Violation Theorem."""

    constraints: ViabilityConstraints
    dynamics: Dynamics
    params: CulturalParameters
    noise_scale: float = 0.02
    dt: float = 0.01
    rng: Optional[np.random.Generator] = None

    def __post_init__(self) -> None:
        if self.rng is None:
            self.rng = np.random.default_rng(0)

    def run_trial(
        self,
        x0: np.ndarray,
        horizon_steps: int,
    ) -> float:
        x = np.asarray(x0, dtype=float).copy()
        for t in range(horizon_steps):
            if not self.constraints.is_satisfied(x):
                return t * self.dt
            drift = self.dynamics.step(x, self.params, self.dt)
            noise = self.rng.normal(
                0, self.noise_scale, size=N_FUNCTIONS
            )
            x = np.clip(drift + np.sqrt(self.dt) * noise, 0.0, 1.0)
        return horizon_steps * self.dt

    def simulate(
        self,
        x0_samples: np.ndarray,
        horizon_steps: int = 1000,
    ) -> ExitTimeResult:
        n = len(x0_samples)
        exit_times = np.empty(n)
        for i, x0 in enumerate(x0_samples):
            exit_times[i] = self.run_trial(x0, horizon_steps)
        return ExitTimeResult(
            exit_times=exit_times,
            horizon=horizon_steps * self.dt,
            noise_scale=self.noise_scale,
            n_trials=n,
        )


def compare_viable_vs_violating(
    viable_params: CulturalParameters,
    violating_params: CulturalParameters,
    constraints: ViabilityConstraints,
    dynamics: Dynamics,
    n_trials: int = 200,
    horizon_steps: int = 2000,
    noise_scale: float = 0.02,
    seed: int = 0,
) -> dict:
    """Compare survival curves for viable vs violating configurations."""
    rng = np.random.default_rng(seed)
    x0_samples = rng.uniform(0.2, 0.8, size=(n_trials, N_FUNCTIONS))

    analyzer_viable = ConstraintViolationAnalyzer(
        constraints=constraints,
        dynamics=dynamics,
        params=viable_params,
        noise_scale=noise_scale,
        rng=np.random.default_rng(seed + 1),
    )
    analyzer_violating = ConstraintViolationAnalyzer(
        constraints=constraints,
        dynamics=dynamics,
        params=violating_params,
        noise_scale=noise_scale,
        rng=np.random.default_rng(seed + 2),
    )

    res_viable = analyzer_viable.simulate(x0_samples, horizon_steps)
    res_violating = analyzer_violating.simulate(
        x0_samples, horizon_steps
    )

    return {"viable": res_viable, "violating": res_violating}
