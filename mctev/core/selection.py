"""
Selection conventions ρ_c.

The judgment correspondence J(s; A, λ_c) is set-valued; the selection
function σ_{ρ_c} determines which maximizing action is realized. The
selection convention ρ_c parameterizes σ.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Optional

import numpy as np

from mctev.core.situational import Action, Situation


class SelectionConvention(Enum):
    """The five baseline selection conventions."""

    PRECEDENT = "precedent"
    MINIMUM_INTERVENTION = "minimum_intervention"
    STATUS_QUO = "status_quo"
    LEXICOGRAPHIC = "lexicographic"
    RANDOM = "random"


def select_action(
    convention: SelectionConvention,
    maximizers: List[Action],
    situation: Situation,
    previous_action: Optional[Action] = None,
    rng: Optional[np.random.Generator] = None,
    lexicographic_key: Optional[callable] = None,
) -> Action:
    """
    Apply the selection convention to the set of maximizing actions.

    Parameters
    ----------
    convention : SelectionConvention
    maximizers : List[Action]
        The set J(s; A, λ_c). Must be non-empty.
    situation : Situation
        Provides context for conventions that depend on the situation.
    previous_action : Optional[Action]
        Previous action in the sequence; used by PRECEDENT.
    rng : Optional[np.random.Generator]
        Random number generator; required for RANDOM.
    lexicographic_key : Optional[callable]
        Key function for LEXICOGRAPHIC.
    """
    if not maximizers:
        raise ValueError("maximizers must be non-empty")

    if convention is SelectionConvention.PRECEDENT:
        if previous_action is None:
            # Fall back to status-quo semantics
            return maximizers[0]
        # Choose the maximizer closest (by name) to the previous action
        return min(maximizers, key=lambda a: a.name == previous_action.name)

    if convention is SelectionConvention.STATUS_QUO:
        # Choose the maximizer whose name matches the current status quo
        status_quo = situation.context.get("status_quo")
        if status_quo is not None:
            for a in maximizers:
                if a.name == status_quo:
                    return a
        return maximizers[0]

    if convention is SelectionConvention.MINIMUM_INTERVENTION:
        # Choose the maximizer with the smallest payload magnitude
        def magnitude(a: Action) -> float:
            p = a.payload
            if isinstance(p, (int, float)):
                return abs(float(p))
            return 0.0
        return min(maximizers, key=magnitude)

    if convention is SelectionConvention.LEXICOGRAPHIC:
        if lexicographic_key is None:
            return maximizers[0]
        return min(maximizers, key=lexicographic_key)

    if convention is SelectionConvention.RANDOM:
        if rng is None:
            rng = np.random.default_rng(0)
        idx = int(rng.integers(0, len(maximizers)))
        return maximizers[idx]

    raise ValueError(f"Unknown selection convention: {convention}")