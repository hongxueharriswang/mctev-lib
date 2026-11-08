"""
Run the three designs of Section 10.6:

    (1) indicator_specific       — index=V_i, outcome=V
    (2) kernel_to_viability_exit — index=R,   outcome=V
    (3) kernel_retention         — index=R,   outcome=R
"""

import numpy as np
import matplotlib.pyplot as plt

from mctev.core.configuration import default_configuration
from mctev.core.moral_functions import MoralFunction
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.viability.kernel import compute_viable_region
from mctev.instability.analyzer import build_three_designs
from mctev.analysis.visualization import plot_index_outcome_designs


def main():
    config = default_configuration(name="universalist")
    constraints = default_constraints()
    dynamics = LinearDynamics()

    kernel = compute_viable_region(
        constraints=constraints, dynamics=dynamics,
        configuration=config, grid_size=5, horizon=150,
    )

    designs = build_three_designs(
        dynamics=dynamics,
        configuration=config,
        viability_constraints=constraints,
        viability_kernel=kernel,
        function=MoralFunction.COOPERATION,
    )

    results = {}
    boundary_point = np.full(6, 0.32)  # just inside V
    for name, analyzer in designs.items():
        print(f"\n=== Design: {name} ===")
        res = analyzer.design_B(
            boundary_point=boundary_point,
            inward_distances=[0.02, 0.05, 0.10, 0.20],
            horizon_steps=300,
            n_trials=20,
        )
        print(res.summary())
        results[name] = res

    fig = plt.figure(figsize=(8, 5))
    plot_index_outcome_designs(results)
    plt.savefig("index_outcome_designs.png", dpi=150, bbox_inches="tight")
    print("\nSaved index_outcome_designs.png")


if __name__ == "__main__":
    main()