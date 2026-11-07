"""
Dynamics F(x, θ_c): state evolution as a function of cultural parameters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np

from mctev.core.cultural_params import CulturalParameters
from mctev.core.moral_functions import N_FUNCTIONS


class Dynamics(ABC):
    """Abstract base class for state dynamics."""

    @abstractmethod
    def __call__(
        self, x: np.ndarray, params: CulturalParameters
    ) -> np.ndarray:
        """Return dx/dt = F(x, θ_c)."""

    def step(
        self,
        x: np.ndarray,
        params: CulturalParameters,
        dt: float = 0.01,
    ) -> np.ndarray:
        return x + dt * self(x, params)


@dataclass
class LinearDynamics(Dynamics):
    """Linear dynamics with logistic self-limitation."""

    A: np.ndarray = None
    B: np.ndarray = None
    c: float = 0.5

    def __post_init__(self) -> None:
        if self.A is None:
            self.A = -0.1 * np.eye(N_FUNCTIONS)
        if self.B is None:
            self.B = 0.5 * np.eye(N_FUNCTIONS)
        self.A = np.asarray(self.A, dtype=float)
        self.B = np.asarray(self.B, dtype=float)

    def __call__(
        self, x: np.ndarray, params: CulturalParameters
    ) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        pull = self.B @ params.weights
        return self.A @ x + pull - self.c * x * (1 - x)


@dataclass
class NonlinearCouplingDynamics(Dynamics):
    """Dynamics with coupling between indicators."""

    coupling: np.ndarray = None
    gain: float = 0.5
    decay: float = 0.1

    def __post_init__(self) -> None:
        if self.coupling is None:
            C = np.zeros((N_FUNCTIONS, N_FUNCTIONS))
            C[0, 2] = 0.3
            C[0, 4] = 0.2
            C[2, 3] = 0.3
            C[5, 0] = 0.2
            self.coupling = C
        self.coupling = np.asarray(self.coupling, dtype=float)

    def __call__(
        self, x: np.ndarray, params: CulturalParameters
    ) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        drive = self.gain * params.weights + self.coupling @ x
        return drive - self.decay * x
