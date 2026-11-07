"""Small math helpers."""

from __future__ import annotations

import numpy as np


def normalize(v: np.ndarray, eps: float = 1e-9) -> np.ndarray:
    s = float(np.sum(v))
    if s < eps:
        return np.zeros_like(v)
    return v / s


def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    return a / b if abs(b) > 1e-12 else default


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    return float(a @ b / (na * nb))
