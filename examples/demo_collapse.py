"""Demonstrate the Constraint Violation Theorem empirically."""

import matplotlib.pyplot as plt

from mctev.core.cultural_params import CULTURAL_TYPES
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.collapse.theorem import compare_viable_vs_violating
from mctev.analysis.visualization import plot_survival_curves


def main() -> None:
    constraints = default_constraints()
    dynamics = LinearDynamics()

    results = compare_viable_vs_violating(
        viable_params=CULTURAL_TYPES["universalist"],
        violating_params=CULTURAL_TYPES["self_regarding"],
        constraints=constraints,
        dynamics=dynamics,
        n_trials=100,
        horizon_steps=2000,
        noise_scale=0.05,
    )

    for name, res in results.items():
        print(res.summary())
        print()

    plot_survival_curves(results)
    plt.savefig(
        "survival_curves.png", dpi=150, bbox_inches="tight"
    )
    print("Saved survival_curves.png")


if __name__ == "__main__":
    main()
