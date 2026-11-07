"""
Case study 2: Capital punishment as legitimate Level-2 disagreement.
"""

from __future__ import annotations

from dataclasses import dataclass

from mctev.core.moral_functions import MoralFunctionProfile


@dataclass
class CapitalPunishmentDiagnosis:
    retentionist: MoralFunctionProfile
    abolitionist: MoralFunctionProfile
    agreed_function: str = "conflict"

    def summary(self) -> str:
        lines = [
            "Capital punishment diagnosis (MCTEV Case Study 2)",
            "=" * 55,
            "Both positions implement the same Level-1 function:",
            f"  {self.agreed_function} "
            "(structured regulation of conflict)",
            "",
            "Retentionist profile:",
        ]
        for k, v in self.retentionist.as_dict().items():
            lines.append(f"  {k:15s}: {v:.2f}")
        lines.append("")
        lines.append("Abolitionist profile:")
        for k, v in self.abolitionist.as_dict().items():
            lines.append(f"  {k:15s}: {v:.2f}")
        lines.append("")
        lines.append(
            "Conclusion: Level 2 disagreement over Level 1 function."
        )
        return "\n".join(lines)


def evaluate_capital_punishment() -> CapitalPunishmentDiagnosis:
    """Evaluate capital punishment under MCTEV."""
    retentionist = MoralFunctionProfile.from_dict(
        {
            "cooperation": 0.5,
            "conflict": 0.8,
            "distribution": 0.4,
            "care": 0.3,
            "information": 0.5,
            "sustainability": 0.5,
        }
    )
    abolitionist = MoralFunctionProfile.from_dict(
        {
            "cooperation": 0.5,
            "conflict": 0.8,
            "distribution": 0.7,
            "care": 0.8,
            "information": 0.7,
            "sustainability": 0.5,
        }
    )
    return CapitalPunishmentDiagnosis(
        retentionist=retentionist,
        abolitionist=abolitionist,
        agreed_function="conflict",
    )
