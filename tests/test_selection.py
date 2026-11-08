import pytest
from mctev.core.selection import SelectionConvention, select_action
from mctev.core.situational import Action, Situation


def test_status_quo_selects_matching_action():
    sit = Situation("s", {"status_quo": "b"})
    ms = [Action("a"), Action("b")]
    chosen = select_action(
        SelectionConvention.STATUS_QUO, ms, sit,
    )
    assert chosen.name == "b"


def test_random_selects_from_maximizers():
    sit = Situation("s")
    ms = [Action("a"), Action("b"), Action("c")]
    import numpy as np
    rng = np.random.default_rng(42)
    for _ in range(10):
        chosen = select_action(SelectionConvention.RANDOM, ms, sit, rng=rng)
        assert chosen.name in {"a", "b", "c"}


def test_empty_maximizers_raises():
    with pytest.raises(ValueError):
        select_action(SelectionConvention.STATUS_QUO, [], Situation("s"))