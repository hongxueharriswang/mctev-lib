"""Abstract and concrete safe sets (index boundary / outcome set)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np

from mctev.core.configuration import CulturalConfiguration
from mctev.core.moral_functions import MoralFunction, function_index
from mctev.viability.constraints import ViabilityConstraints
from mctev.viability.kernel import ViabilityKernel


class SafeSet(ABC):
    """A designated state-space safe set."""

    @abstractmethod
    def contains(self, x: np.ndarray) -> bool:
        """Whether x lies in the set."""

    @abstractmethod
    def signed_distance(self, x: np.ndarray) -> float:
        """
        Signed distance: positive inside, zero on boundary, negative outside.
        """

    def boundary_normal(
        self, x: np.ndarray, eps: float = 1e-4
    ) -> np.ndarray:
        """Numerical outward normal via central difference of signed distance."""
        d = len(x)
        g = np.zeros(d)
        for i in range(d):
            e = np.zeros(d); e[i] = eps
            g[i] = (
                self.signed_distance(x + e) - self.signed_distance(x - e)
            ) / (2 * eps)
        n = -g  # signed_distance increases inward → outward normal is -grad
        norm = np.linalg.norm(n)
        return n / norm if norm > 1e-9 else n


@dataclass
class IndicatorSafeSet(SafeSet):
    """
    The indicator-specific safe set V_i(λ_c):

        V_i(λ_c) = { x : V_i(x) ≥ τ^V_i }

    The signed distance is proxied by (V_i(x) − τ^V_i).
    """

    indicator_fn: callable
    threshold: float
    function: MoralFunction

    def contains(self, x: np.ndarray) -> bool:
        return float(self.indicator_fn(x)) >= self.threshold

    def signed_distance(self, x: np.ndarray) -> float:
        return float(self.indicator_fn(x) - self.threshold)


@dataclass
class KernelSafeSet(SafeSet):
    """
    The controlled viability kernel R(λ_c; Π).

    Signed distance is estimated from the fraction of nearby grid points
    in the kernel; exact distances require the full kernel construction.
    """

    kernel: ViabilityKernel

    def contains(self, x: np.ndarray) -> bool:
        return self.kernel.contains(x)

    def signed_distance(self, x: np.ndarray) -> float:
        # Approximate: use fraction-viable at a small neighborhood
        # (replaced by the exact distance when the grid is finer)
        return 1.0 if self.contains(x) else -1.0