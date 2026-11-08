"""
Type-appropriate dispersion measures (manuscript Section 14).

    D_F    function recognition
    D_θ    simplex weights (Aitchison primary, JS secondary)
    D_{τ^V} dynamical viability thresholds
    D_{τ^S} safeguard thresholds
    D_{τ^H} flourishing thresholds
    D_ρ    selection conventions (behavioral, on a shared benchmark)
    D_M    measurement operators (invariance test)
    D_J    judgments
"""

from __future__ import annotations

from typing import Callable, List, Optional

import numpy as np

from mctev.core.configuration import CulturalConfiguration
from mctev.core.moral_functions import MoralFunction
from mctev.core.situational import Action, Situation


# ---------------------------------------------------------------------------
# D_F: function recognition
# ---------------------------------------------------------------------------

def dispersion_function_recognition(
    recognized_sets: List[List[MoralFunction]],
) -> float:
    """Jaccard distance averaged over pairs of recognition sets."""
    if len(recognized_sets) < 2:
        return 0.0
    dists = []
    for i in range(len(recognized_sets)):
        for j in range(i + 1, len(recognized_sets)):
            a, b = set(recognized_sets[i]), set(recognized_sets[j])
            union = a | b
            if not union:
                dists.append(0.0)
            else:
                dists.append(1.0 - len(a & b) / len(union))
    return float(np.mean(dists))


# ---------------------------------------------------------------------------
# D_θ: simplex weights via Aitchison distance
# ---------------------------------------------------------------------------

def aitchison_distance(
    w1: np.ndarray, w2: np.ndarray, eps: float = 1e-9
) -> float:
    """Aitchison distance between two compositional vectors."""
    w1 = np.asarray(w1, dtype=float) + eps
    w2 = np.asarray(w2, dtype=float) + eps
    logr = np.log(w1) - np.log(w2)
    logr = logr - logr.mean()
    return float(np.linalg.norm(logr))


def dispersion_weights(
    weight_vectors: List[np.ndarray],
    metric: str = "aitchison",
) -> float:
    """D_θ: mean pairwise dispersion of simplex weight vectors."""
    if len(weight_vectors) < 2:
        return 0.0
    dists = []
    for i in range(len(weight_vectors)):
        for j in range(i + 1, len(weight_vectors)):
            if metric == "aitchison":
                dists.append(aitchison_distance(
                    weight_vectors[i], weight_vectors[j]
                ))
            else:
                # Jensen-Shannon divergence as secondary metric
                p = np.asarray(weight_vectors[i], dtype=float) + 1e-9
                q = np.asarray(weight_vectors[j], dtype=float) + 1e-9
                m = 0.5 * (p + q)
                js = 0.5 * np.sum(p * np.log(p / m)) + \
                     0.5 * np.sum(q * np.log(q / m))
                dists.append(float(np.sqrt(max(js, 0.0))))
    return float(np.mean(dists))


# ---------------------------------------------------------------------------
# Threshold dispersion (Mahalanobis or standardized Euclidean)
# ---------------------------------------------------------------------------

def dispersion_thresholds(
    threshold_vectors: List[np.ndarray],
    use_mahalanobis: bool = False,
) -> float:
    """Generic dispersion for threshold vectors."""
    if len(threshold_vectors) < 2:
        return 0.0
    X = np.array([np.asarray(v, dtype=float) for v in threshold_vectors])
    if use_mahalanobis and X.shape[0] > 1:
        cov = np.cov(X.T) + 1e-6 * np.eye(X.shape[1])
        inv = np.linalg.inv(cov)
    else:
        inv = np.eye(X.shape[1])
    dists = []
    for i in range(X.shape[0]):
        for j in range(i + 1, X.shape[0]):
            d = X[i] - X[j]
            dists.append(float(np.sqrt(d @ inv @ d)))
    return float(np.mean(dists))


def dispersion_viability_thresholds(configs: List[CulturalConfiguration]) -> float:
    """D_{τ^V}."""
    return dispersion_thresholds(
        [c.viability_thresholds.values for c in configs]
    )


def dispersion_safeguard_thresholds(
    configs: List[CulturalConfiguration],
) -> float:
    """D_{τ^S}: requires a canonical ordering of safeguard names."""
    names = sorted({
        name for c in configs for name in c.safeguard_thresholds.values
    })
    vecs = []
    for c in configs:
        v = np.array([
            c.safeguard_thresholds.get(name, 0.0) for name in names
        ])
        vecs.append(v)
    return dispersion_thresholds(vecs)


def dispersion_flourishing_thresholds(
    configs: List[CulturalConfiguration],
) -> float:
    """D_{τ^H}."""
    return dispersion_thresholds(
        [c.flourishing_thresholds.values for c in configs]
    )


# ---------------------------------------------------------------------------
# D_ρ: selection conventions on a shared benchmark
# ---------------------------------------------------------------------------

def dispersion_selection_conventions(
    configs: List[CulturalConfiguration],
    benchmark_situations: List[Situation],
    benchmark_maximizers: List[List[Action]],
) -> float:
    """
    D_ρ: behavioral disagreement on a shared benchmark.

    Both conventions are applied to the SAME maximizing set J_s, with
    weights, thresholds, measurement operators, and factual inputs held
    fixed. This isolates selection-convention dispersion from other
    sources of divergence.
    """
    from mctev.core.selection import select_action

    if len(configs) < 2:
        return 0.0

    # Precompute per-configuration choices on the shared benchmark
    choices = []
    for c in configs:
        row = []
        for sit, maxs in zip(benchmark_situations, benchmark_maximizers):
            if not maxs:
                row.append(None)
                continue
            chosen = select_action(
                convention=c.selection_convention,
                maximizers=maxs,
                situation=sit,
            )
            row.append(chosen.name if chosen else None)
        choices.append(row)

    # Pairwise disagreement rate
    dists = []
    for i in range(len(choices)):
        for j in range(i + 1, len(choices)):
            disagreements = sum(
                1 for a, b in zip(choices[i], choices[j]) if a != b
            )
            dists.append(disagreements / len(benchmark_situations))
    return float(np.mean(dists))


# ---------------------------------------------------------------------------
# D_M: measurement invariance
# ---------------------------------------------------------------------------

def dispersion_measurement_operators(
    configs: List[CulturalConfiguration],
    anchor_states: List[np.ndarray],
) -> float:
    """
    D_M: mean pairwise discrepancy at anchor states.

    If anchor states are not available, cross-context comparison is
    not admissible per Section 8.2; return NaN and warn.
    """
    if len(configs) < 2 or not anchor_states:
        return float("nan")
    dists = []
    for i in range(len(configs)):
        for j in range(i + 1, len(configs)):
            total = 0.0
            for x in anchor_states:
                hi = configs[i].measurement_operator.measure(x)
                hj = configs[j].measurement_operator.measure(x)
                total += float(np.linalg.norm(hi - hj))
            dists.append(total / len(anchor_states))
    return float(np.mean(dists))


# ---------------------------------------------------------------------------
# D_J: judgments
# ---------------------------------------------------------------------------

def dispersion_judgments(
    judgment_lists: List[List[str]],
) -> float:
    """
    D_J: action disagreement rate across judgment lists (by action name).
    """
    if len(judgment_lists) < 2:
        return 0.0
    dists = []
    for i in range(len(judgment_lists)):
        for j in range(i + 1, len(judgment_lists)):
            a, b = judgment_lists[i], judgment_lists[j]
            n = max(len(a), len(b))
            if n == 0:
                dists.append(0.0)
                continue
            disagreements = sum(
                1 for x, y in zip(a, b) if x != y
            ) + abs(len(a) - len(b))
            dists.append(disagreements / n)
    return float(np.mean(dists))


# ---------------------------------------------------------------------------
# Convenience: full dispersion vector
# ---------------------------------------------------------------------------

def full_dispersion_vector(
    configs: List[CulturalConfiguration],
    recognized_sets: Optional[List[List[MoralFunction]]] = None,
    anchor_states: Optional[List[np.ndarray]] = None,
    benchmark: Optional[dict] = None,
) -> dict:
    """Return all eight measures in a single dict."""
    result = {
        "D_theta": dispersion_weights([c.weights for c in configs]),
        "D_tau_V": dispersion_viability_thresholds(configs),
        "D_tau_S": dispersion_safeguard_thresholds(configs),
        "D_tau_H": dispersion_flourishing_thresholds(configs),
    }
    if recognized_sets is not None:
        result["D_F"] = dispersion_function_recognition(recognized_sets)
    if anchor_states is not None:
        result["D_M"] = dispersion_measurement_operators(configs, anchor_states)
    if benchmark is not None:
        result["D_rho"] = dispersion_selection_conventions(
            configs,
            benchmark["situations"],
            benchmark["maximizers"],
        )
        result["D_J"] = dispersion_judgments(benchmark["judgment_lists"])
    return result