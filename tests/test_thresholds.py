import numpy as np
import pytest

from mctev.core.thresholds import (
    ViabilityThresholds, SafeguardThresholds, FlourishingThresholds,
    ThresholdFamilies,
)


def test_viability_thresholds_shape():
    with pytest.raises(ValueError):
        ViabilityThresholds(values=np.zeros(5))


def test_viability_thresholds_dict_roundtrip():
    t = ViabilityThresholds.from_dict({"cooperation": 0.4, "care": 0.5})
    assert t["cooperation"] == pytest.approx(0.4)
    assert t["care"] == pytest.approx(0.5)


def test_safeguard_thresholds_with_overrides():
    t = SafeguardThresholds.from_dict({"error_rate": 0.1})
    t2 = t.with_overrides(error_rate=0.05)
    assert t2["error_rate"] == pytest.approx(0.05)
    assert t["error_rate"] == pytest.approx(0.1)  # unchanged


def test_flourishing_thresholds_shape():
    with pytest.raises(ValueError):
        FlourishingThresholds(values=np.zeros(4))


def test_threshold_families_container():
    fam = ThresholdFamilies(
        viability=ViabilityThresholds.uniform(0.3),
        safeguard=SafeguardThresholds.from_dict({"error_rate": 0.05}),
        flourishing=FlourishingThresholds.uniform(0.5),
    )
    d = fam.as_dict()
    assert "viability" in d and "safeguard" in d and "flourishing" in d