"""
Capital-punishment case study, revised for (R1)-(R3).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List

from mctev.core.configuration import CulturalConfiguration, default_configuration
from mctev.core.moral_functions import MoralFunctionProfile
from mctev.core.situational import Action, Situation
from mctev.retentionist.architecture import (
    RetentionistArchitecture, AbolitionistArchitecture,
)
from mctev.retentionist.conditions import (
    CapitalActionSet, check_R1, check_R2, check_R3,
    anti_triviality_filter, evaluate_test_situations,
)


@dataclass
class CapitalPunishmentDiagnosis:
    retentionist_profile: MoralFunctionProfile
    abolitionist_profile: MoralFunctionProfile
    agreed_function: str = "conflict"
    R1_retentionist: bool = False
    R1_abolitionist: bool = False
    R2: bool = False
    R3: bool = False
    test_situations_passed: int = 0

    def summary(self) -> str:
        lines = [
            "Capital punishment diagnosis (MCTEV v0.2.0)",
            "=" * 55,
            f"R1 (retentionist non-exclusion): {self.R1_retentionist}",
            f"R1 (abolitionist non-exclusion): {self.R1_abolitionist}",
            f"R2 (weak non-vacuity):           {self.R2}",
            f"R3 (strong non-vacuity):         {self.R3}",
            f"Test situations passing filter:  {self.test_situations_passed}",
        ]
        return "\n".join(lines)


def _make_test_situations() -> List[Situation]:
    """Illustrative test situations."""
    return [
        Situation("first_degree_murder", {"severity": "high"}),
        Situation("terrorism", {"severity": "high"}),
        Situation("treason", {"severity": "high"}),
    ]


def _make_action_generator(severity_threshold: str = "high") -> Callable:
    """Illustrative action generator: high severity → capital available."""
    def generate(situation: Situation) -> List[Action]:
        sev = situation.context.get("severity", "low")
        actions = [
            Action("life_imprisonment", 0.5),
            Action("acquittal", 0.0),
        ]
        if sev == severity_threshold:
            actions.append(Action("execute", 1.0))
        return actions
    return generate


def _make_constraint_predicate(config: CulturalConfiguration) -> Callable:
    """
    Illustrative C(s; A, τ^S): 'execute' is admissible iff
    (a) situation severity is high, and
    (b) the informational-reliability safeguard is above threshold.
    """
    def predicate(situation: Situation, action: Action, cfg) -> bool:
        if action.name != "execute":
            return True
        if situation.context.get("severity") != "high":
            return False
        tau_error = cfg.safeguard_thresholds.get("error_rate", 0.1)
        observed_error = situation.context.get("observed_error_rate", 0.01)
        return observed_error <= tau_error
    return predicate


def evaluate_capital_punishment() -> CapitalPunishmentDiagnosis:
    """Run the retentionist/abolitionist comparison with (R1)-(R3)."""

    # Baseline configurations for the two architectures
    config = default_configuration(
        name="baseline",
        safeguard_values={"error_rate": 0.05},
        selection=__import__(
            "mctev.core.selection", fromlist=["SelectionConvention"]
        ).SelectionConvention.STATUS_QUO,
    )
    config_strict = default_configuration(
        name="strict",
        safeguard_values={"error_rate": 0.001},
        selection=config.selection_convention,
    )

    # Test situations with anti-triviality filter
    raw_tests = _make_test_situations()
    test_situations = anti_triviality_filter(raw_tests)

    # Architectures
    constraint = _make_constraint_predicate(config)
    A_R = RetentionistArchitecture(
        name="A_R", constraint_predicate=constraint,
    )
    A_A = AbolitionistArchitecture(
        name="A_A", constraint_predicate=constraint,
    )

    # Action generator
    action_gen = _make_action_generator()

    # R1
    R1_R = check_R1(A_R)
    R1_A = check_R1(A_A)

    # R2 / R3
    configs = [config, config_strict]
    capital_set = CapitalActionSet()
    R2 = check_R2(
        A_R, configs, test_situations, action_gen, capital_set=capital_set
    )
    R3 = check_R3(
        A_R, configs, test_situations, action_gen, capital_set=capital_set
    )

    # Sample diagnostic profiles
    retentionist_profile = MoralFunctionProfile.from_dict({
        "cooperation": 0.5, "conflict": 0.8, "distribution": 0.4,
        "care": 0.3, "information": 0.5, "sustainability": 0.5,
    })
    abolitionist_profile = MoralFunctionProfile.from_dict({
        "cooperation": 0.5, "conflict": 0.8, "distribution": 0.7,
        "care": 0.8, "information": 0.7, "sustainability": 0.5,
    })

    return CapitalPunishmentDiagnosis(
        retentionist_profile=retentionist_profile,
        abolitionist_profile=abolitionist_profile,
        agreed_function="conflict",
        R1_retentionist=R1_R,
        R1_abolitionist=R1_A,
        R2=R2,
        R3=R3,
        test_situations_passed=len(test_situations),
    )