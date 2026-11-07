"""
Metrics for convergence, divergence, and cultural distance.
"""

from __future__ import annotations

from typing import Iterable, List

import numpy as np

from mctev.core.cultural_params import CulturalParameters


def convergence_index(profiles: Iterable[np.ndarray]) -> float:
    """Mean pairwise cosine similarity."""
    profiles = [np.asarray(p, dtype=float) for p in profiles]
    if len(profiles) < 2:
        return 1.0
    sims = []
    for i in range(len(profiles)):
        for j in range(i + 1, len(profiles)):
            a, b = profiles[i], profiles[j]
            denom = np.linalg.norm(a) * np.linalg.norm(b)
            if denom < 1e-9:
                sims.append(0.0)
            else:
                sims.append(float(a @ b / denom))
    return float(np.mean(sims))


def divergence_index(profiles: Iterable[np.ndarray]) -> float:
    """Complement of convergence_index."""
    return 1.0 - convergence_index(profiles)


def cultural_distance_matrix(
    params: List[CulturalParameters],
) -> np.ndarray:
    """Pairwise L2 distance matrix between cultural parameter vectors."""
    n = len(params)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            D[i, j] = params[i].distance(params[j])
    return D
