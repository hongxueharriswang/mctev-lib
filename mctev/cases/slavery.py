"""
Case study 1: Slavery as constraint violation.
"""

from __future__ import annotations

from dataclasses import dataclass

from mctev.core.moral_functions import (
    MoralFunction,
    MoralFunctionProfile,
)


@dataclass
class SlaveryDiagnosis:
    """Diagnostic report for slavery under MCTEV."""

    profile: MoralFunctionProfile
    violations: dict
    severity: float

    def summary(self) -> str:
        lines = ["Slavery diagnosis (MCTEV Case Study 1)", "=" * 40]
        for f, v in self.profile.as_dict().items():
            lines.append(f"  {f:15s}: {v:.2f}")
        lines.append("-" * 40)
        lines.append(f"  violated functions: {list(self.violations)}")
        lines.append(f"  severity score:     {self.severity:.2f}")
        return "\n".join(lines)


def evaluate_slavery() -> SlaveryDiagnosis:
    """Evaluate slavery against the six candidate moral functions."""
    profile = MoralFunctionProfile.from_dict(
        {
            "cooperation": 0.1,
            "conflict": 0.1,
            "distribution": 0.1,
            "care": 0.2,
            "information": 0.1,
            "sustainability": 0.3,
        }
    )
    threshold = 0.3
    violations = {
        f.value: profile[f]
        for f in MoralFunction
        if profile[f] < threshold
    }
    severity = (
        sum(threshold - v for v in violations.values())
        / len(MoralFunction)
    )
    return SlaveryDiagnosis(
        profile=profile,
        violations=violations,
        severity=float(severity),
    )
