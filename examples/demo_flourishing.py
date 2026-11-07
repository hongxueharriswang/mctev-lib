"""Demonstrate the flourishing construct."""

import matplotlib.pyplot as plt

from mctev.flourishing.dimensions import (
    FlourishingProfile,
    FlourishingThresholds,
)
from mctev.analysis.visualization import plot_flourishing_radar


def main() -> None:
    flourishing = FlourishingProfile.from_dict(
        {"W": 0.7, "P": 0.6, "A": 0.5, "S": 0.8, "M": 0.6}
    )
    thresholds = FlourishingThresholds.default()

    print("Flourishing profile:", flourishing)
    print("Is flourishing?", thresholds.is_flourishing(flourishing))
    print("Deficit:", thresholds.deficit(flourishing))

    plot_flourishing_radar(flourishing, thresholds)
    plt.savefig("flourishing.png", dpi=150, bbox_inches="tight")
    print("Saved flourishing.png")


if __name__ == "__main__":
    main()
