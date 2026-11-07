"""Run the Three Societies simulation and plot results."""

import matplotlib.pyplot as plt

from mctev.simulation import ThreeSocietiesConfig, run_three_societies
from mctev.analysis.visualization import plot_three_societies


def main() -> None:
    config = ThreeSocietiesConfig(n_agents=30, n_rounds=200)

    dfs = {
        cond: run_three_societies(cond, config=config, seed=42)
        for cond in (1, 2, 3)
    }

    for cond, df in dfs.items():
        collapsed = df["collapsed"].iloc[-1]
        mean_c = (
            df["mean_contribution"].iloc[-20:].mean()
            / config.endowment
        )
        print(
            f"Condition {cond}: final collapsed={collapsed}, "
            f"late mean={mean_c:.2f}"
        )

    plot_three_societies(dfs)
    plt.savefig(
        "three_societies.png", dpi=150, bbox_inches="tight"
    )
    print("Saved three_societies.png")


if __name__ == "__main__":
    main()
