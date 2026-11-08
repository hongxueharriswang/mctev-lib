import numpy as np
import pytest

from mctev.core.configuration import (
    CulturalConfiguration, default_configuration,
)
from mctev.core.thresholds import (
    ViabilityThresholds, SafeguardThresholds, FlourishingThresholds,
)
from mctev.core.selection import SelectionConvention
from mctev.core.measurement import LinearMeasurement
from mctev.core.moral_functions import N_FUNCTIONS


def test_default_configuration_weights_sum_to_one():
    cfg = default_configuration()
    assert np.isclose(cfg.weights.sum(), 1.0)


def test_configuration_rejects_unnormalized_weights():
    with pytest.raises(ValueError):
        CulturalConfiguration(
            weights=np.full(N_FUNCTIONS, 2.0),
            viability_thresholds=ViabilityThresholds.uniform(),
            safeguard_thresholds=SafeguardThresholds(),
            flourishing_thresholds=FlourishingThresholds.uniform(),
            selection_convention=SelectionConvention.STATUS_QUO,
            measurement_operator=LinearMeasurement(to_core=lambda x: x[:5]),
        )


def test_configuration_fields_present():
    cfg = default_configuration(name="test")
    assert cfg.name == "test"
    assert cfg.viability_thresholds is not None
    assert cfg.safeguard_thresholds is not None
    assert cfg.flourishing_thresholds is not None
    assert cfg.selection_convention is SelectionConvention.STATUS_QUO