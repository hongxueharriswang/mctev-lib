"""
The Three Societies public goods simulation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from mctev.simulation.agents import Agent, AgentType


@dataclass
class ThreeSocietiesConfig:
    """Configuration for the Three Societies simulation."""

    n_agents: int = 30
    n_rounds: int = 200
    return_rate: float = 1.5
    endowment: float = 10.0
    learning_rate: float = 0.1

    coop_threshold: float = 0.2
    trust_threshold: float = 0.4
    equity_threshold: float = 3.0


@dataclass
class PublicGoodsGame:
    """A public goods game with heterogeneous agents."""

    agents: List[Agent]
    config: ThreeSocietiesConfig
    rng: np.random.Generator = field(
        default_factory=lambda: np.random.default_rng(0)
    )

    def play_round(self) -> Dict[str, float]:
        n = len(self.agents)
        contributions = []
        others_mean = (
            np.mean([a.belief for a in self.agents])
            * self.config.endowment
        )

        for agent in self.agents:
            c = agent.best_contribution(
                endowment=self.config.endowment,
                group_size=n,
                return_rate=self.config.return_rate,
                others_mean=others_mean,
            )
            agent.last_contribution = c
            contributions.append(c)

        contributions = np.array(contributions)
        total_contribution = contributions.sum()
        public_good = (
            self.config.return_rate * total_contribution / n
        )

        payoffs = (self.config.endowment - contributions) + public_good
        for agent, payoff in zip(self.agents, payoffs):
            agent.payoff_history.append(payoff)

        observed_mean = contributions.mean()
        for agent in self.agents:
            agent.update_belief(
                observed_mean, self.config.learning_rate
            )

        return {
            "mean_contribution": float(contributions.mean()),
            "std_contribution": float(contributions.std()),
            "max_payoff": float(payoffs.max()),
            "min_payoff": float(payoffs.min()),
            "payoff_ratio": float(
                payoffs.max() / max(payoffs.min(), 1e-9)
            ),
        }


def _build_agents(
    config: ThreeSocietiesConfig,
    composition: Dict[AgentType, float],
    rng: np.random.Generator,
) -> List[Agent]:
    agents: List[Agent] = []
    idx = 0
    for agent_type, fraction in composition.items():
        n = int(round(fraction * config.n_agents))
        for _ in range(n):
            belief = float(rng.uniform(0.3, 0.7))
            agents.append(Agent.create(idx, agent_type, belief))
            idx += 1
    while len(agents) < config.n_agents:
        agents.append(
            Agent.create(idx, AgentType.UNIVERSALIST, 0.5)
        )
        idx += 1
    return agents[: config.n_agents]


def run_three_societies(
    condition: int,
    config: Optional[ThreeSocietiesConfig] = None,
    seed: int = 0,
) -> pd.DataFrame:
    """Run the Three Societies simulation."""
    config = config or ThreeSocietiesConfig()
    rng = np.random.default_rng(seed)

    if condition == 1:
        composition = {AgentType.UNIVERSALIST: 1.0}
    elif condition == 2:
        composition = {
            AgentType.UNIVERSALIST: 1 / 3,
            AgentType.COLLECTIVIST: 1 / 3,
            AgentType.INDIVIDUALIST: 1 / 3,
        }
    elif condition == 3:
        composition = {
            AgentType.UNIVERSALIST: 0.3,
            AgentType.COLLECTIVIST: 0.3,
            AgentType.INDIVIDUALIST: 0.3,
            AgentType.SELF_REGARDING: 0.1,
        }
    else:
        raise ValueError(f"Unknown condition: {condition}")

    agents = _build_agents(config, composition, rng)
    game = PublicGoodsGame(agents=agents, config=config, rng=rng)

    records: List[Dict] = []
    for t in range(config.n_rounds):
        stats = game.play_round()
        stats["round"] = t
        stats["collapsed"] = (
            stats["mean_contribution"] / config.endowment
            < config.coop_threshold
        )
        records.append(stats)

    return pd.DataFrame(records)
