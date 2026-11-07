"""Compute and visualize the viability kernel."""

import matplotlib.pyplot as plt

from mctev.core.cultural_params import CULTURAL_TYPES
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.viability.kernel import compute_viable_region
from mctev.analysis.visualization import plot_viability_grid


def main() -> None:
    constraints = default_constraints()
    dynamics = LinearDynamics()
    params = CULTURAL_TYPES["universalist"]

    kernel = compute_viable_region(
        constraints=constraints,
        dynamics=dynamics,
        params=params,
        grid_size=6,
        horizon=200,
    )

    print(
        f"Fraction of probing grid viable: "
        f"{kernel.fraction_viable():.2%}"
    )

    fig = plt.figure(figsize=(6, 5))
    plot_viability_grid(kernel, axes=(0, 2))
    plt.savefig(
        "viability_kernel.png", dpi=150, bbox_inches="tight"
    )
    print("Saved viability_kernel.png")


if __name__ == "__main__":
    main()
