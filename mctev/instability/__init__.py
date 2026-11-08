"""
Boundary-Instability Hypothesis with distinct index-boundary and outcome-set
designs (manuscript Section 10).

The three designs of Section 10.6 are implemented as different
(index_set, outcome_set) pairs:

    1. Indicator-specific:         index = V_i(λ_c),  outcome = V(λ_c)
    2. Kernel-to-viability-exit:   index = R(λ_c; Π), outcome = V(λ_c)
    3. Kernel-retention:           index = R(λ_c; Π), outcome = R(λ_c; Π)
"""

from mctev.instability.safe_sets import (
    SafeSet, IndicatorSafeSet, KernelSafeSet,
)
from mctev.instability.survival import set_specific_survival
from mctev.instability.analyzer import (
    BoundaryInstabilityAnalyzer, InstabilityResult, THREE_DESIGNS,
)

__all__ = [
    "SafeSet", "IndicatorSafeSet", "KernelSafeSet",
    "set_specific_survival",
    "BoundaryInstabilityAnalyzer", "InstabilityResult", "THREE_DESIGNS",
]