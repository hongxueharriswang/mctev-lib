"""
Qualifying conditions Q_{-i} and the proxy audit.

The manuscript distinguishes descriptive viability S^viab from qualified
viability S^qual (Section 6.3), and imposes a definitional-independence
condition on the qualifying condition used to derive a candidate function:

    Q_{-i} must not contain, as a constitutive input, either f_i itself
    or any proxy that presupposes f_i.

This module provides:

    - QualifyingCondition: an abstract base for Q_{-i}
    - QualifyingConditions: the vector (Q_{-1}, ..., Q_{-6})
    - proxy_audit: a diagnostic that flags potential circularity
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

import numpy as np

from mctev.core.moral_functions import MoralFunction


class QualifyingCondition(ABC):
    """
    Abstract qualifying condition Q_{-i}.

    Each concrete condition excludes the target function it is used to
    evaluate, per the non-circularity requirement of Section 6.3.2.
    """

    @abstractmethod
    def __call__(self, state: np.ndarray) -> float:
        """Return the qualifying score for a state."""

    @abstractmethod
    def description(self) -> str:
        """Human-readable description for proxy auditing."""

    @abstractmethod
    def constitutive_inputs(self) -> List[str]:
        """
        Names of the constitutive inputs (indicators, operators, sub-models)
        that enter the definition of Q_{-i}.

        The proxy audit uses this list to check that f_i or proxies of f_i
        do not appear among the inputs.
        """


@dataclass
class MemberInclusiveViability(QualifyingCondition):
    """
    Example qualifying condition: member-inclusive viability.

    Requires that no identifiable subpopulation falls below a
    minimum-wellbeing threshold on a designated indicator.
    """

    target_function: MoralFunction
    welfare_index: Callable[[np.ndarray], np.ndarray]
    minimum_member_welfare: float = 0.3
    _inputs: List[str] = field(default_factory=list)

    def __call__(self, state: np.ndarray) -> float:
        w = np.asarray(self.welfare_index(state), dtype=float)
        if w.size == 0:
            return 0.0
        return float(w.min() - self.minimum_member_welfare)

    def description(self) -> str:
        return (
            f"member-inclusive viability: min member welfare "
            f">= {self.minimum_member_welfare}"
        )

    def constitutive_inputs(self) -> List[str]:
        return self._inputs


@dataclass
class MinimumFlourishing(QualifyingCondition):
    """
    Example qualifying condition: minimum flourishing.

    Requires that the culturally measured flourishing indicator vector
    exceed a threshold on every dimension.
    """

    target_function: MoralFunction
    measurement_operator: "MeasurementOperator"  # type: ignore[name-defined]
    thresholds: np.ndarray
    _inputs: List[str] = field(default_factory=lambda: ["flourishing_indicators"])

    def __call__(self, state: np.ndarray) -> float:
        h = self.measurement_operator.measure(state)
        return float(np.min(h - self.thresholds))

    def description(self) -> str:
        return "minimum flourishing: all five dimensions above thresholds"

    def constitutive_inputs(self) -> List[str]:
        return list(self._inputs)


@dataclass
class QualifyingConditions:
    """
    The vector Q = (Q_{-1}, ..., Q_{-6}) of function-specific conditions.

    Indexing by target function returns the corresponding Q_{-i}.
    """

    conditions: Dict[MoralFunction, QualifyingCondition] = field(
        default_factory=dict
    )

    def __getitem__(self, target: MoralFunction) -> QualifyingCondition:
        if target not in self.conditions:
            raise KeyError(f"No qualifying condition registered for {target}")
        return self.conditions[target]

    def __setitem__(
        self, target: MoralFunction, condition: QualifyingCondition
    ) -> None:
        self.conditions[target] = condition

    def score(self, target: MoralFunction, state: np.ndarray) -> float:
        """Return Q_{-target}(state)."""
        return float(self[target](state))

    def registered_for(self) -> List[str]:
        return [f.value for f in self.conditions]


# =============================================================================
# Proxy audit
# =============================================================================

@dataclass
class ProxyAuditReport:
    target_function: MoralFunction
    condition_description: str
    constitutive_inputs: List[str]
    flagged_proxies: List[str]
    definitionally_independent: bool

    def summary(self) -> str:
        status = "PASS" if self.definitionally_independent else "FAIL"
        lines = [
            f"Proxy audit [{status}] for target f = {self.target_function.value}",
            f"  condition: {self.condition_description}",
            f"  constitutive inputs: {self.constitutive_inputs}",
        ]
        if self.flagged_proxies:
            lines.append(f"  flagged proxies: {self.flagged_proxies}")
        return "\n".join(lines)


# Names of proxies that commonly presuppose particular candidate functions
_COMMON_PROXY_NAMES: Dict[MoralFunction, List[str]] = {
    MoralFunction.COOPERATION: [
        "reciprocity_index", "reciprocal_contribution", "public_goods_contribution",
    ],
    MoralFunction.CONFLICT_MANAGEMENT: [
        "procedural_integrity", "retributive_balance", "adjudication_quality",
    ],
    MoralFunction.RESOURCE_DISTRIBUTION: [
        "gini_coefficient", "income_share", "resource_access",
    ],
    MoralFunction.REPRODUCTION_CARE: [
        "dependent_care_outcome", "child_welfare",
    ],
    MoralFunction.KNOWLEDGE_TRANSMISSION: [
        "information_integrity", "truth_tracking",
    ],
    MoralFunction.SUSTAINABILITY: [
        "resource_renewal_rate", "ecological_footprint",
    ],
}


def proxy_audit(
    conditions: QualifyingConditions,
    target: MoralFunction,
) -> ProxyAuditReport:
    """
    Run the proxy audit for one candidate function.

    Flags constitutive inputs of Q_{-target} that name either the target
    function itself or a common proxy for it. This is a heuristic check;
    full definitional independence may require inspection of the
    measurement operators and threshold rules (Supplement S12).
    """
    condition = conditions[target]
    inputs = condition.constitutive_inputs()

    forbidden = {target.value} | set(_COMMON_PROXY_NAMES.get(target, []))
    flagged = [name for name in inputs if name in forbidden]

    return ProxyAuditReport(
        target_function=target,
        condition_description=condition.description(),
        constitutive_inputs=inputs,
        flagged_proxies=flagged,
        definitionally_independent=len(flagged) == 0,
    )