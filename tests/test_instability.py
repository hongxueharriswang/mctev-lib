import numpy as np

from mctev.core.configuration import default_configuration
from mctev.core.moral_functions import MoralFunction
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.viability.kernel import compute_viable_region
from mctev.instability.analyzer import (
    build_three_designs, THREE_DESIGNS,
)
from mctev.instability.safe_sets import (
    IndicatorSafeSet, KernelSafeSet,
)


def _build():
    cfg = default_configuration()
    cons = default_constraints()
    dyn = LinearDynamics()
    k = compute_viable_region(
        constraints=cons, dynamics=dyn, configuration=cfg,
        grid_size=4, horizon=100,
    )
    return cfg, cons, dyn, k


def test_three_designs_registered():
    assert set(THREE_DESIGNS.keys()) == {
        "indicator_specific", "kernel_to_viability_exit", "kernel_retention",
    }


def test_indicator_safe_set():
    fn = lambda x: float(x[0])
    safe = IndicatorSafeSet(
        indicator_fn=fn, threshold=0.3, function=MoralFunction.COOPERATION,
    )
    assert safe.contains(np.array([0.5]*6))
    assert not safe.contains(np.array([0.1]*6))


def test_design_B_shape():
    cfg, cons, dyn, k = _build()
    designs = build_three_designs(
        dynamics=dyn, configuration=cfg,
        viability_constraints=cons, viability_kernel=k,
        function=MoralFunction.COOPERATION,
    )
    res = designs["indicator_specific"].design_B(
        boundary_point=np.full(6, 0.32),
        inward_distances=[0.02, 0.05],
        horizon_steps=50, n_trials=5,
    )
    assert len(res.inward_distances) == 2
    assert len(res.survival_probabilities) == 2