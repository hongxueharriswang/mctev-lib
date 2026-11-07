"""
Matplotlib-based visualization helpers.
"""

from __future__ import annotations

from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_three_societies(
    dfs: dict,
    ax=None,
):
    """Plot mean contribution over rounds for each condition."""
    ax = ax or plt.gca()
    for condition, df in dfs.items():
        ax.plot(
            df["round"],
            df["mean_contribution"],
            label=f"Condition {condition}",
        )
    ax.set_xlabel("Round")
    ax.set_ylabel("Mean contribution")
    ax.set_title("Three Societies: mean contribution by condition")
    ax.legend()
    return ax


def plot_survival_curves(
    results: dict,
    ax=None,
):
    """Plot survival functions S(T)."""
    ax = ax or plt.gca()
    for name, res in results.items():
        T, S = res.survival_function()
        ax.plot(T, S, label=name)
    ax.set_xlabel("Time T")
    ax.set_ylabel("P(τ_exit > T)")
    ax.set_title("Survival curves: Constraint Violation Theorem")
    ax.legend()
    return ax


def plot_viability_grid(
    kernel,
    axes: tuple = (0, 2),
    ax=None,
):
    """Plot the viability kernel marginalized over two dimensions."""
    ax = ax or plt.gca()
    if kernel._mask is None:
        kernel.build()
    mask = kernel._mask.reshape((kernel.grid_size,) * 6)
    keep = set(axes)
    other = [i for i in range(6) if i not in keep]
    marg = mask.max(axis=tuple(other))
    im = ax.imshow(
        marg.T,
        origin="lower",
        extent=[0, 1, 0, 1],
        cmap="viridis",
        aspect="auto",
    )
    ax.set_xlabel(f"State dimension {axes[0]}")
    ax.set_ylabel(f"State dimension {axes[1]}")
    ax.set_title("Viability kernel (marginalized)")
    plt.colorbar(im, ax=ax, label="viable indicator")
    return ax


def plot_flourishing_radar(
    profile,
    thresholds=None,
    ax=None,
):
    """Radar plot of a flourishing profile."""
    dims = ["W", "P", "A", "S", "M"]
    angles = np.linspace(
        0, 2 * np.pi, len(dims), endpoint=False
    ).tolist()
    values = [profile[d] for d in dims]
    values += values[:1]
    angles += angles[:1]

    ax = ax or plt.subplot(111, polar=True)
    ax.plot(angles, values, label="profile")
    ax.fill(angles, values, alpha=0.25)
    if thresholds is not None:
        th = [thresholds.thresholds[i] for i in range(5)]
        th += th[:1]
        ax.plot(angles, th, "--", label="thresholds")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dims)
    ax.set_title("Flourishing profile")
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    return ax
