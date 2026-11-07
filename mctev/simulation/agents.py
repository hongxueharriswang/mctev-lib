"""
Agent types for the Three Societies public goods simulation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List

import numpy as np

from mctev.core.cultural_params import CULTURAL_TYPES, CulturalParameters


class AgentType(Enum):
    UNIVERSALIST = "universalist"
    COLLECTIVIST = "collectivist"
    INDIVIDUALIST = "individualist"
    SELF_REGARDING = "self_regarding"


@dataclass
class Agent:
    """A public goods game agent."""

    agent_id: int
    agent_type: AgentType
    params: CulturalParameters
    belief: float = 0.5
    last_contribution: float = 0.0
    payoff_history: List[float] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        agent_id: int,
        agent_type: AgentType,
        belief: float = 0.5,
    ) -> "Agent":
        params = CULTURAL_TYPES[agent_type.value]
        return cls(
            agent_id=agent_id,
            agent_type=agent_type,
            params=params,
            belief=belief,
        )

    def best_contribution(
        self,
        endowment: float,
        group_size: int,
        return_rate: float,
        others_mean: float,
        harm_threshold: float = 0.3,
    ) -> float:
        """Choose contribution to maximize moral utility."""
        best_c = 0.0
        best_score = -np.inf
        for c in np.linspace(0.0, endowment, 41):
            group_avg = (
                (group_size - 1) * others_mean + c
            ) / group_size
            public_gain = return_rate * group_avg
            own_payoff = (endowment - c) + public_gain
            u_coop = own_payoff / endowment - 1.0
            u_fair = -abs(c - others_mean) / endowment
            u_harm = -max(0.0, harm_threshold - group_avg / endowment)

            score = (
                self.params["cooperation"] * u_coop
                + self.params["distribution"] * u_fair
                + self.params["care"] * u_harm
            )

            if score > best_score:
                best_score = score
                best_c = c
        return float(best_c)

    def update_belief(
        self, observed_mean: float, alpha: float = 0.1
    ) -> None:
        self.belief = (1 - alpha) * self.belief + alpha * observed_mean
