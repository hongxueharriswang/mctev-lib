import numpy as np
import pytest

from mctev.core.moral_functions import MoralFunction
from mctev.analysis.metrics import (
    dispersion_function_recognition,
    aitchison_distance,
    dispersion_weights,
    dispersion_thresholds,
    dispersion_judgments,
)


def test_dispersion_function_recognition_identical():
    s = [MoralFunction.COOPERATION, MoralFunction.CARE]
    assert dispersion_function_recognition([s, s]) == 0.0


def test_aitchison_distance_identity():
    w = np.array([0.2]*5)
    assert aitchison_distance(w, w) == pytest.approx(0.0, abs=1e-6)


def test_dispersion_weights_identity():
    w = np.array([0.2]*5)
    assert dispersion_weights([w, w]) == pytest.approx(0.0, abs=1e-6)


def test_dispersion_thresholds_identity():
    v = np.array([0.5]*5)
    assert dispersion_thresholds([v, v]) == pytest.approx(0.0, abs=1e-6)


def test_dispersion_judgments_identical():
    assert dispersion_judgments([["a", "b"], ["a", "b"]]) == 0.0