"""
Retentionist conditions (R1)-(R3) and the anti-triviality test.

Implements manuscript Section 12.3:

    (R1) Architectural non-exclusion: A_R contains no categorical
         prohibition of capital punishment in C^{L1}.
    (R2) Weak configuration-specific non-vacuity: ∃ config, ∃ test
         situation where a capital action is admissible.
    (R3) Strong configuration-specific non-vacuity: ∀ admissible config,
         ∃ test situation where a capital action is admissible.

The `evaluate_test_situations` helper also applies the anti-triviality
conditions from the manuscript.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, List

from mctev.core.configuration import CulturalConfiguration
from mctev.core.situational import Action, Situation, SituationalJudgment
from mctev.retentionist.architecture import (
    Architecture, RetentionistArchitecture,
)


def check_R1(architecture: Architecture) -> bool:
    """Architectural non-exclusion: no categorical prohibition of capital."""
    return not architecture.excludes_categorically("capital_punishment")


@dataclass
class CapitalActionSet:
    """The set A_cap(s) ⊆ A(s) of capital-punishment actions."""

    action_names: List[str] = None

    def __post_init__(self) -> None:
        if self.action_names is None:
            self.action_names = [
                "execute", "capital_sentence", "death_penalty",
            ]

    def select(
        self, actions: Iterable[Action]
    ) -> List[Action]:
        return [
            a for a in actions if a.name in self.action_names
        ]

    def contains(self, action: Action) -> bool:
        return action.name in self.action_names


def _capital_actions_admissible(
    situation: Situation,
    actions: List[Action],
    configuration: CulturalConfiguration,
    architecture: Architecture,
    capital_set: CapitalActionSet,
    judgment: SituationalJudgment,
) -> List[Action]:
    """The subset A_cap(s) ∩ C(s; A, τ^S)."""
    cap = capital_set.select(actions)
    return judgment.admissible_actions(cap, situation, configuration)


def evaluate_test_situations(
    architecture: Architecture,
    configuration: CulturalConfiguration,
    test_situations: List[Situation],
    action_generator: Callable[[Situation], List[Action]],
    capital_set: CapitalActionSet = None,
    judgment: SituationalJudgment = None,
) -> dict:
    """
    Evaluate a set of test situations against the architecture.

    Returns a dict with per-situation results plus the boolean
    outcomes for (R2) and (R3) evaluation.
    """
    from mctev.core.moral_functions import MoralUtilityLibrary

    capital_set = capital_set or CapitalActionSet()
    judgment = judgment or SituationalJudgment(
        utilities=MoralUtilityLibrary(),
        constraints=architecture.constraint_predicate,
    )

    results = []
    any_admissible = False
    for s in test_situations:
        actions = action_generator(s)
        cap_admissible = _capital_actions_admissible(
            situation=s,
            actions=actions,
            configuration=configuration,
            architecture=architecture,
            capital_set=capital_set,
            judgment=judgment,
        )
        admissible = len(cap_admissible) > 0
        any_admissible = any_admissible or admissible
        results.append({
            "situation": s.name,
            "capital_actions_admissible": admissible,
            "admissible_capital_action_names": [a.name for a in cap_admissible],
        })
    return {
        "per_situation": results,
        "any_capital_admissible": any_admissible,
    }


def check_R2(
    architecture: Architecture,
    configurations: List[CulturalConfiguration],
    test_situations: List[Situation],
    action_generator: Callable[[Situation], List[Action]],
    **kwargs,
) -> bool:
    """
    Weak configuration-specific non-vacuity: some (config, situation) admits
    a capital action.
    """
    for config in configurations:
        report = evaluate_test_situations(
            architecture, config, test_situations, action_generator, **kwargs
        )
        if report["any_capital_admissible"]:
            return True
    return False


def check_R3(
    architecture: Architecture,
    configurations: List[CulturalConfiguration],
    test_situations: List[Situation],
    action_generator: Callable[[Situation], List[Action]],
    **kwargs,
) -> bool:
    """
    Strong configuration-specific non-vacuity: every config admits a
    capital action in some test situation.
    """
    for config in configurations:
        report = evaluate_test_situations(
            architecture, config, test_situations, action_generator, **kwargs
        )
        if not report["any_capital_admissible"]:
            return False
    return True


def anti_triviality_filter(
    test_situations: List[Situation],
    is_factually_coherent: Callable[[Situation], bool] = lambda s: True,
    in_jurisdiction: Callable[[Situation], bool] = lambda s: True,
    is_feasible: Callable[[Situation], bool] = lambda s: True,
    is_artificial: Callable[[Situation], bool] = lambda s: False,
) -> List[Situation]:
    """
    Apply the four anti-triviality conditions from the manuscript.
    Returns the subset of test situations that pass all four filters.
    """
    return [
        s for s in test_situations
        if is_factually_coherent(s)
        and in_jurisdiction(s)
        and is_feasible(s)
        and not is_artificial(s)
    ]