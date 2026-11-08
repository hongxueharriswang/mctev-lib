"""
Slavery case study, revised for qualified viability Q_{-i}.

The diagnosis now separates:

    - descriptive persistence (S^viab)
    - qualified viability (S^qual) relative to Q_{-dist}
    - flourishing classification under M_c and τ^H
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np

from mctev.core.moral_functions import (
    MoralFunction, MoralFunctionProfile, MORAL_FUNCTION_ORDER,
)
from mctev.core.thresholds import (
    FlourishingThresholds, ViabilityThresholds,
)
from mctev.core.qualifying import (
    QualifyingCondition, QualifyingConditions, proxy_audit,
)


# ---------------------------------------------------------------------------
# Q_{-dist}: member-inclusive viability, excludes distribution
# ---------------------------------------------------------------------------

@dataclass
class SlaveryMemberInclusive(QualifyingCondition):
    """
    Q_{-dist}: qualifying condition for evaluating f_dist on slavery.

    Requires that the minimum member welfare (measured on the
    non-distribution dimensions) exceed a threshold. This condition
    excludes distribution explicitly (the target function).
    """

    target_function: MoralFunction = MoralFunction.RESOURCE_DISTRIBUTION
    minimum_welfare: float = 0.3

    def __call__(self, state: np.ndarray) -> float:
        # Use cooperation, conflict, care as proxies for non-distribution welfare
        proxies = state[:2].tolist() + [state[3]]
        return float(np.min(proxies) - self.minimum_welfare)

    def description(self) -> str:
        return (
            f"member-inclusive welfare on non-distribution dimensions "
            f">= {self.minimum_welfare}"
        )

    def constitutive_inputs(self) -> list:
        return ["cooperation_indicator", "conflict_indicator", "care_indicator"]


@dataclass
class SlaveryDiagnosis:
    descriptive_profile: MoralFunctionProfile
    descriptive_violations: dict
    descriptive_severity: float
    qualified_condition: Optional[QualifyingCondition]
    proxy_audit_report: Optional[object]

    def summary(self) -> str:
        lines = ["Slavery diagnosis (MCTEV v0.2.0)", "=" * 45]
        lines.append("Descriptive profile (S^viab):")
        for f, v in self.descriptive_profile.as_dict().items():
            lines.append(f"  {f:15s}: {v:.2f}")
        lines.append("-" * 45)
        lines.append(
            f"Descriptive violations: {list(self.descriptive_violations)}"
        )
        lines.append(f"Descriptive severity:   {self.descriptive_severity:.3f}")
        if self.qualifying_condition is not None:
            lines.append(
                f"Qualifying condition: {self.qualifying_condition.description()}"
            )
        if self.proxy_audit_report is not None:
            lines.append("Proxy audit:")
            lines.append("  " + self.proxy_audit_report.summary().replace(
                "\n", "\n  "
            ))
        return "\n".join(lines)


def evaluate_slavery() -> SlaveryDiagnosis:
    """
    Evaluate slavery.

    Descriptive profile is unchanged from v0.1.0. The new fields report
    the qualifying condition and its proxy audit.
    """
    profile = MoralFunctionProfile.from_dict({
        "cooperation": 0.1,
        "conflict": 0.1,
        "distribution": 0.1,
        "care": 0.2,
        "information": 0.1,
        "sustainability": 0.3,
    })
    threshold = 0.3
    violations = {
        f.value: profile[f] for f in MoralFunction
        if profile[f] < threshold
    }
    severity = (
        sum(threshold - v for v in violations.values()) / len(MoralFunction)
    )

    # Build the qualifying conditions vector with Q_{-dist}
    conditions = QualifyingConditions()
    conditions[MoralFunction.RESOURCE_DISTRIBUTION] = SlaveryMemberInclusive()
    audit = proxy_audit(conditions, MoralFunction.RESOURCE_DISTRIBUTION)

    return SlaveryDiagnosis(
        descriptive_profile=profile,
        descriptive_violations=violations,
        descriptive_severity=float(severity),
        qualified_condition=conditions[MoralFunction.RESOURCE_DISTRIBUTION],
        proxy_audit_report=audit,
    )