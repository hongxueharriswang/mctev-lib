import numpy as np

from mctev.core.measurement import (
    LinearMeasurement, validate_cross_context_comparability,
)


def test_linear_measurement_identity():
    op = LinearMeasurement(to_core=lambda x: np.asarray(x)[:5])
    out = op.measure(np.array([0.5]*6))
    assert out.shape == (5,)
    assert np.allclose(out, 0.5)


def test_cross_context_without_anchors_or_linking_is_incomparable():
    op = LinearMeasurement(to_core=lambda x: np.asarray(x)[:5])
    report = validate_cross_context_comparability(op, op)
    assert report["comparable"] is False
    assert report["mechanism"] == "unavailable"


def test_cross_context_with_anchors():
    op = LinearMeasurement(to_core=lambda x: np.asarray(x)[:5])
    anchor = [np.array([0.5]*6)]
    report = validate_cross_context_comparability(
        op, op, anchor_states=anchor,
    )
    assert report["mechanism"] == "anchors"
    assert report["comparable"] is True