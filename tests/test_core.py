"""Basic unit tests for mctev-lib."""

import numpy as np
import pytest

from mctev.core.moral_functions import (
    MoralFunction,
    MoralFunctionProfile,
    MoralUtilityLibrary,
)
from mctev.core.cultural_params import CULTURAL_TYPES, CulturalParameters
from mctev.core.situational import Action, Situation, SituationalJudgment
from mctev.flourishing.dimensions import (
    FlourishingProfile,
    FlourishingThresholds,
)
from mctev.cases.slavery import evaluate_slavery
from mctev.cases.capital_punishment import (
    evaluate_capital_punishment,
)


def test_moral_function_profile_bounds():
    with pytest.raises(ValueError):
        MoralFunctionProfile(
            values=np.array([1.2, 0, 0, 0, 0, 0])
        )
    with pytest.raises(ValueError):
        MoralFunctionProfile(values=np.array([0, 0, 0, 0, 0]))


def test_moral_function_profile_roundtrip():
    d = {"cooperation": 0.8, "care": 0.9}
    p = MoralFunctionProfile.from_dict(d)
    out = p.as_dict()
    assert out["cooperation"] == pytest.approx(0.8)
    assert out["care"] == pytest.approx(0.9)


def test_cultural_params_normalization():
    p = CulturalParameters(weights=np.ones(6), name="test")
    n = p.normalized()
    assert np.isclose(n.weights.sum(), 1.0)


def test_cultural_types_present():
    for k in (
        "universalist",
        "collectivist",
        "individualist",
        "self_regarding",
    ):
        assert k in CULTURAL_TYPES


def test_situational_judgment_basic():
    lib = MoralUtilityLibrary()
    lib[MoralFunction.COOPERATION] = lambda a, s: float(a.payload)
    lib[MoralFunction.REPRODUCTION_CARE] = (
        lambda a, s: 1.0 - float(a.payload)
    )

    params = CulturalParameters.from_dict(
        {"cooperation": 1.0, "care": 0.0}
    )
    sit = Situation(name="test")
    actions = [
        Action("low", payload=0.2),
        Action("high", payload=0.8),
    ]
    solver = SituationalJudgment(utilities=lib)
    best = solver.judge(sit, actions, params)
    assert best.name == "high"


def test_flourishing():
    p = FlourishingProfile.from_dict(
        {"W": 0.7, "P": 0.7, "A": 0.7, "S": 0.7, "M": 0.7}
    )
    th = FlourishingThresholds.default()
    assert th.is_flourishing(p)


def test_slavery_diagnosis():
    d = evaluate_slavery()
    assert len(d.violations) >= 4
    assert d.severity > 0


def test_capital_punishment_diagnosis():
    d = evaluate_capital_punishment()
    assert (
        d.retentionist[MoralFunction.CONFLICT_MANAGEMENT] > 0.5
    )
    assert (
        d.abolitionist[MoralFunction.CONFLICT_MANAGEMENT] > 0.5
    )
