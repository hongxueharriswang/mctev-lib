"""
Viability kernel computation.

The feasible moral region R is the viability kernel of (V, F).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np

from mctev.core.cultural_params import CulturalParameters
from mctev.core.moral_functions import N_FUNCTIONS
from mctev.viability.constraints import ViabilityConstraints
from mctev.viability.dynamics import Dynamics


@dataclass
class ViabilityKernel:
    """Approximate viability kernel R ⊆ ℝ^n."""

    constraints: ViabilityConstraints
    dynamics: Dynamics
    params: CulturalParameters
    horizon: int = 500
    dt: float = 0.01
    grid_size: int = 8
    _grid: Optional[np.ndarray] = None
    _mask: Optional[np.ndarray] = None

    def build_grid(self) -> np.ndarray:
        axes = [
            np.linspace(0.0, 1.0, self.grid_size)
            for _ in range(N_FUNCTIONS)
        ]
        mesh = np.meshgrid(*axes, indexing="ij")
        return np.stack([m.ravel() for m in mesh], axis=-1)

    def trajectory_stays_viable(self, x0: np.ndarray) -> bool:
        x = x0.copy()
        for _ in range(self.horizon):
            if not self.constraints.is_satisfied(x):
                return False
            x = self.dynamics.step(x, self.params, self.dt)
            x = np.clip(x, 0.0, 1.0)
        return True

    def build(self) -> np.ndarray:
        grid = self.build_grid()
        mask_flat = np.array(
            [self.trajectory_stays_viable(x) for x in grid], dtype=float
        )
        self._grid = grid
        self._mask = mask_flat
        return mask_flat.reshape((self.grid_size,) * N_FUNCTIONS)

    def contains(self, x: np.ndarray) -> bool:
        return self.trajectory_stays_viable(np.asarray(x, dtype=float))

    def fraction_viable(self) -> float:
        if self._mask is None:
            self.build()
        return float(self._mask.mean())

    def sample_viable(
        self,
        n_samples: int = 100,
        rng: Optional[np.random.Generator] = None,
    ) -> np.ndarray:
        rng = rng or np.random.default_rng(0)
        accepted = []
        attempts = 0
        while len(accepted) < n_samples and attempts < n_samples * 100:
            x = rng.uniform(0, 1, size=N_FUNCTIONS)
            if (
                self.constraints.is_satisfied(x)
                and self.trajectory_stays_viable(x)
            ):
                accepted.append(x)
            attempts += 1
        if not accepted:
            return np.empty((0, N_FUNCTIONS))
        return np.array(accepted)


def compute_viable_region(
    constraints: ViabilityConstraints,
    dynamics: Dynamics,
    params: CulturalParameters,
    grid_size: int = 8,
    horizon: int = 500,
) -> ViabilityKernel:
    """Convenience constructor."""
    kernel = ViabilityKernel(
        constraints=constraints,
        dynamics=dynamics,
        params=params,
        horizon=horizon,
        grid_size=grid_size,
    )
    kernel.build()
    return kernel
