"""
Set-specific finite-horizon survival probability (manuscript Section 10.4):

    q_{T, K_out}^π(x) = P_x^π[ X_t ∈ K_out  ∀ t ∈ [0, T] ]
"""

from __future__ import annotations

from typing import Callable, Optional

import numpy as np

from mctev.core.configuration import CulturalConfiguration
from mctev.core.moral_functions import N_FUNCTIONS
from mctev.instability.safe_sets import SafeSet
from mctev.viability.dynamics import Dynamics


def set_specific_survival(
    x0: np.ndarray,
    outcome_set: SafeSet,
    dynamics: Dynamics,
    configuration: CulturalConfiguration,
    horizon_steps: int = 1000,
    dt: float = 0.01,
    noise_scale: float = 0.02,
    policy: Optional[Callable] = None,
    rng: Optional[np.random.Generator] = None,
) -> float:
    """
    Simulate one trajectory and return 1.0 if the trajectory stays inside
    the outcome set for the whole horizon, else 0.0.
    """
    rng = rng or np.random.default_rng(0)
    x = np.asarray(x0, dtype=float).copy()
    for _ in range(horizon_steps):
        if not outcome_set.contains(x):
            return 0.0
        x = dynamics.step(x, configuration, dt)
        noise = rng.normal(0, noise_scale, size=N_FUNCTIONS)
        x = np.clip(x + np.sqrt(dt) * noise, 0.0, 1.0)
    return 1.0