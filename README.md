# mctev-lib

> **Reference implementation of the Multi-Level Computational Theory of Ethics (MCTEV)**

A Python library for formalizing, simulating, and empirically evaluating the three-level architecture of ethics proposed in *"Toward a Computational Science of Ethics: A Multi-Level Theory of Ethical Variation and Universal Moral Principles."*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Conceptual Architecture](#conceptual-architecture)
- [Module Reference](#module-reference)
- [Examples](#examples)
- [Reproducing Paper Results](#reproducing-paper-results)
- [Design Principles](#design-principles)
- [Testing](#testing)
- [Citation](#citation)
- [License](#license)

---

## Overview

The **Multi-Level Computational Theory of Ethics (MCTEV)** proposes that moral phenomena are organized across three interconnected levels:

| Level | Concept | Formal object | Library module |
|-------|---------|---------------|----------------|
| **Level 1** | Candidate universal moral functions | Constraint set $\mathcal{V}$, viability kernel $\mathcal{R}$ | `mctev.core.moral_functions`, `mctev.viability` |
| **Level 2** | Cultural parameter configurations | Weight vector $\theta_c \in \Theta_{\text{viable}}$ | `mctev.core.cultural_params` |
| **Level 3** | Situational judgments | Constrained optimization $j(s; \theta_c)$ | `mctev.core.situational` |

The library operationalizes the paper's central claims:

1. **Functional universals**: Six candidate moral functions derived from the functional problems any enduring society must solve.
2. **Feasible moral region**: The viability kernel of social dynamics — the set of states from which some policy can keep a society viable forever.
3. **Measurable flourishing**: A five-dimensional construct $H = (W, P, A, S, M)$ with componentwise thresholds.
4. **Constraint Violation Theorem (empirical)**: Sustained violations of viability constraints predict exponential survival decay.
5. **Two case studies**: Slavery (constraint violation and collapse pressures) and capital punishment (legitimate Level-2 disagreement over Level-1 functions).

The framework is **methodologically aligned with, but not formally derived from** the [COH/GISMOL](https://github.com/hongxueharriswang/gismol-lib) research program on hierarchical computational explanations of complex systems.

---

## Installation

### From a local copy

```bash
git clone <repository-url> mctev-lib
cd mctev-lib
pip install -e .
```

### With development dependencies

```bash
pip install -e ".[dev]"
```

### Requirements

- Python ≥ 3.10
- NumPy ≥ 1.24
- SciPy ≥ 1.10
- Matplotlib ≥ 3.7
- pandas ≥ 2.0

---

## Quick Start

### Judging a situation under a cultural configuration

```python
from mctev.core.moral_functions import MoralFunction, MoralUtilityLibrary
from mctev.core.cultural_params import CULTURAL_TYPES
from mctev.core.situational import Action, Situation, SituationalJudgment

# Define per-function utilities
lib = MoralUtilityLibrary()
lib[MoralFunction.COOPERATION] = lambda a, s: float(a.payload)
lib[MoralFunction.REPRODUCTION_CARE] = lambda a, s: 1.0 - float(a.payload)

# Pick a cultural parameter configuration
params = CULTURAL_TYPES["universalist"]

# Build the Level-3 solver and evaluate
solver = SituationalJudgment(utilities=lib)
actions = [Action("low", 0.2), Action("high", 0.8)]
best = solver.judge(Situation("test"), actions, params)

print(best.name)  # 'high' for a universalist
```

### Diagnosing a moral system

```python
from mctev.cases.slavery import evaluate_slavery
from mctev.cases.capital_punishment import evaluate_capital_punishment

print(evaluate_slavery().summary())
print()
print(evaluate_capital_punishment().summary())
```

### Running the Three Societies simulation

```python
from mctev.simulation import ThreeSocietiesConfig, run_three_societies

config = ThreeSocietiesConfig(n_agents=30, n_rounds=200)
df = run_three_societies(condition=3, config=config, seed=42)

print(df.tail())
print("Collapsed:", df["collapsed"].iloc[-1])
```

### Evaluating the Constraint Violation Theorem empirically

```python
from mctev.core.cultural_params import CULTURAL_TYPES
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.collapse.theorem import compare_viable_vs_violating

results = compare_viable_vs_violating(
    viable_params=CULTURAL_TYPES["universalist"],
    violating_params=CULTURAL_TYPES["self_regarding"],
    constraints=default_constraints(),
    dynamics=LinearDynamics(),
    n_trials=100,
    horizon_steps=2000,
)

print(results["viable"].summary())
print(results["violating"].summary())
```

---

## Conceptual Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  LEVEL 1:  Candidate Universal Moral Functions                  │
│  ─────────────────────────────────────────────────────────────  │
│  f_coop    f_conflict    f_dist    f_care    f_info    f_sustain│
│      │         │            │          │         │         │    │
│      └─────────┴────────────┴──────────┴─────────┴─────────┘    │
│                              │                                  │
│                     define feasible region R (viability kernel) │
│                              │  ← constraints propagate down    │
│                              ▼                                  │
│  LEVEL 2:  Cultural Parameter Configurations  θ_c ∈ Θ_viable    │
│  ─────────────────────────────────────────────────────────────  │
│  universalist  collectivist  individualist  self_regarding      │
│                              │                                  │
│                     constrain situational judgment              │
│                              │  ← adaptation propagates up      │
│                              ▼                                  │
│  LEVEL 3:  Situational Judgments  j(s; θ_c)                     │
│  ─────────────────────────────────────────────────────────────  │
│  argmax_a Σ_f θ_{c,f} · u_f(a, s)   subject to  a ∈ C(s)        │
└─────────────────────────────────────────────────────────────────┘
```

The **Ethical Constraint Hierarchy Principle** — *constraints propagate downward, adaptation propagates upward* — is the mechanism the framework shares with COH/GISMOL, though MCTEV is not a formal instantiation of the COH 9-tuple.

---

## Module Reference

### `mctev.core`

The three-level heart of the library.

#### `mctev.core.moral_functions`

| Symbol | Description |
|--------|-------------|
| `MoralFunction` | Enum of the six candidate universal moral functions |
| `MORAL_FUNCTION_ORDER` | Canonical list ordering for vectors and matrices |
| `N_FUNCTIONS` | Constant `= 6` |
| `MoralFunctionProfile` | Frozen dataclass; vector of contributions in $[0,1]^6$ |
| `MoralUtilityLibrary` | Library of per-function utility callables $u_f(a, s)$ |

```python
from mctev.core.moral_functions import MoralFunction, MoralFunctionProfile

profile = MoralFunctionProfile.from_dict({"cooperation": 0.9, "care": 0.7})
print(profile.dominance())  # fraction of functions above 0.5
```

#### `mctev.core.cultural_params`

| Symbol | Description |
|--------|-------------|
| `CulturalParameters` | Weight vector $\theta_c$ over the six functions |
| `CULTURAL_TYPES` | Dictionary of canonical types |
| `CulturalParametersRegion` | Convex region in parameter space |
| `get_cultural_type(name)` | Retrieve a canonical type by name |

Available canonical types:

- `universalist` — balanced across all six functions
- `collectivist` — emphasizes care and cooperation
- `individualist` — emphasizes distribution and information
- `self_regarding` — degenerate: prioritizes only cooperation (illustrative)

#### `mctev.core.situational`

| Symbol | Description |
|--------|-------------|
| `Action` | Named action with optional payload |
| `Situation` | Named situation with context dictionary |
| `SituationalJudgment` | Solver implementing $j(s;\theta_c)$ |

```python
solver = SituationalJudgment(utilities=lib)
ranking = solver.rank(situation, actions, params)
for score, action in ranking:
    print(f"{score:+.3f}  {action.name}")
```

#### `mctev.core.hierarchy`

| Symbol | Description |
|--------|-------------|
| `MCTEVSystem` | Combines all three levels in one object |

```python
from mctev.core.hierarchy import MCTEVSystem

system = MCTEVSystem.from_type("universalist", utilities=lib)
print(system.is_viable())
print(system.judge(Situation("s"), actions))
```

---

### `mctev.viability`

Feasible moral region $\mathcal{R} = \text{Viab}(\mathcal{V}, F)$.

#### `mctev.viability.constraints`

| Symbol | Description |
|--------|-------------|
| `ViabilityConstraints` | Container for $\{V_i(\mathbf{x}) \ge \tau_i\}$ |
| `default_constraints()` | Illustrative constraints with $\tau_i = 0.3$ |

```python
from mctev.viability.constraints import default_constraints
import numpy as np

constraints = default_constraints()
constraints.is_satisfied(np.array([0.5]*6))    # True
constraints.violations(np.array([0.1]*6))      # dict of deficits
```

#### `mctev.viability.dynamics`

| Symbol | Description |
|--------|-------------|
| `Dynamics` | Abstract base class |
| `LinearDynamics` | $\dot x = Ax + B\theta_c - c \cdot x(1-x)$ |
| `NonlinearCouplingDynamics` | Coupled indicator dynamics |

#### `mctev.viability.kernel`

| Symbol | Description |
|--------|-------------|
| `ViabilityKernel` | Grid-based approximation of $\mathcal{R}$ |
| `compute_viable_region(...)` | Convenience constructor |

```python
from mctev.viability.kernel import compute_viable_region
from mctev.core.cultural_params import CULTURAL_TYPES
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics

kernel = compute_viable_region(
    constraints=default_constraints(),
    dynamics=LinearDynamics(),
    params=CULTURAL_TYPES["universalist"],
    grid_size=6,
    horizon=200,
)
print(f"Viable fraction: {kernel.fraction_viable():.2%}")
```

---

### `mctev.flourishing`

Five-dimensional flourishing construct with componentwise thresholds.

| Symbol | Description |
|--------|-------------|
| `FlourishingProfile` | Vector $H = (W,P,A,S,M) \in [0,1]^5$ |
| `FlourishingThresholds` | Threshold vector $\tau_H$ |
| `DIMENSIONS` | `["W","P","A","S","M"]` |
| `DIMENSION_NAMES` | Human-readable dimension names |

```python
from mctev.flourishing.dimensions import (
    FlourishingProfile, FlourishingThresholds
)

p = FlourishingProfile.from_dict({"W": 0.7, "P": 0.6, "A": 0.5, "S": 0.8, "M": 0.6})
th = FlourishingThresholds.default()
print(th.is_flourishing(p))   # True
print(th.deficit(p))          # 0.0
```

---

### `mctev.collapse`

Empirical evaluation of the Constraint Violation Theorem.

| Symbol | Description |
|--------|-------------|
| `ConstraintViolationAnalyzer` | Run many noisy trajectories |
| `ExitTimeResult` | Survival function, exponential fit |
| `compare_viable_vs_violating(...)` | Side-by-side comparison helper |

```python
result = analyzer.simulate(x0_samples, horizon_steps=2000)
print(result.summary())
# ExitTimeResult(...)
#   mean exit time: 4.317
#   censor rate: 12.00%
#   exponential fit: C=1.021, λ=0.184
```

---

### `mctev.simulation`

The Three Societies public goods simulation from Section 13.

| Symbol | Description |
|--------|-------------|
| `AgentType` | `UNIVERSALIST`, `COLLECTIVIST`, `INDIVIDUALIST`, `SELF_REGARDING` |
| `Agent` | Individual public goods player |
| `PublicGoodsGame` | Game orchestrator |
| `ThreeSocietiesConfig` | Configuration dataclass |
| `run_three_societies(...)` | Returns a `pandas.DataFrame` |

Conditions:
- **1** — homogeneous viable (all universalists)
- **2** — heterogeneous viable (equal mix of U, C, I)
- **3** — invasion by self-regarding agents

---

### `mctev.cases`

Two worked case studies from the paper.

| Symbol | Description |
|--------|-------------|
| `evaluate_slavery()` | Returns a `SlaveryDiagnosis` |
| `evaluate_capital_punishment()` | Returns a `CapitalPunishmentDiagnosis` |

---

### `mctev.analysis`

Metrics and visualization.

| Symbol | Description |
|--------|-------------|
| `convergence_index(profiles)` | Mean pairwise cosine similarity |
| `divergence_index(profiles)` | `1 − convergence_index` |
| `cultural_distance_matrix(params)` | Pairwise L2 distance matrix |
| `plot_three_societies(dfs)` | Multi-condition line plot |
| `plot_survival_curves(results)` | Survival curves from collapse analysis |
| `plot_viability_grid(kernel)` | 2-D marginalized viability mask |
| `plot_flourishing_radar(profile)` | Five-axis radar chart |

---

### `mctev.utils`

Small math helpers: `normalize`, `safe_divide`, `cosine_similarity`.

---

## Examples

All examples are executable scripts in `examples/`.

| Script | Reproduces |
|--------|------------|
| `demo_three_societies.py` | Section 13 — convergence/divergence simulation |
| `demo_viability_kernel.py` | Section 7.5 — feasible region as viability kernel |
| `demo_flourishing.py` | Section 8 — five-dimensional flourishing |
| `demo_collapse.py` | Section 10 — Constraint Violation Theorem |
| `demo_case_studies.py` | Sections 11–12 — slavery + capital punishment |

Run any example:

```bash
python examples/demo_case_studies.py
```

---

## Reproducing Paper Results

| Paper concept | Library call | Expected output |
|---------------|--------------|-----------------|
| Section 6 — candidate functions | `MoralFunction` enum | Six functions with descriptions |
| Section 7 — Level-1/Level-2 distinction | `MORAL_FUNCTION_ORDER` vs. `CULTURAL_TYPES` | 6 functions, 4 canonical cultures |
| Section 8 — flourishing thresholds | `FlourishingThresholds.default()` | $\tau_H = (0.5, 0.5, 0.5, 0.5, 0.5)$ |
| Section 9 — persistence ∧ flourishing | `MCTEVSystem.is_viable()` + `FlourishingThresholds.is_flourishing()` | Both must return `True` |
| Section 10 — Constraint Violation Theorem | `compare_viable_vs_violating(...)` | Viable config: flat survival ≈ 1.0; violating config: exponential decay |
| Section 11 — slavery | `evaluate_slavery().summary()` | 5 violated functions, severity ≈ 0.15 |
| Section 12 — capital punishment | `evaluate_capital_punishment().summary()` | Both profiles score high on `conflict` |
| Section 13 — Three Societies | `run_three_societies(3)` | Mean contribution falls below threshold near round ~50–80 |

> **Note on empirical status.** The library implements the *empirical evaluation* of the Constraint Violation Theorem via simulation. Fully rigorous proofs under stated assumptions (compactness, smoothness, positive feedback, noise) would require additional mathematical work; the theorem remains a *sketch* in the paper and an *empirical estimate* in the library.

---

## Design Principles

### 1. Candidate, not uniquely determined universals

The six moral functions are exposed as an `Enum` with an explicit `MORAL_FUNCTION_ORDER` list. Every class that accepts a moral function profile (`MoralFunctionProfile`, `CulturalParameters`, `MoralFunctionProfile.from_dict`) accepts **arbitrary weights**. This mirrors the paper's `f_i ∈ ⋂ S_i` (not `=`): the functions are candidates, not unique necessities.

### 2. Methodological alignment with COH/GISMOL, not formal instantiation

`MCTEVSystem` is **not** a COH 9-tuple. It exposes fields `cultural_params`, `utilities`, `constraints`, `viable_region` — MCTEV's own structure. The Constraint Violation Theorem is MCTEV's own result; it is **analogous to** COH's stability results, not derived from them.

### 3. Falsifiable claims

Every quantitative claim is surfaced as a checkable return value:

- `ConstraintViolationAnalyzer.fit_exponential()` returns `(C, λ)`, which can be compared against predicted decay.
- `ViabilityKernel.fraction_viable()` returns a scalar measurable against ground truth.
- `SlaveryDiagnosis.severity` returns a scalar summary of constraint violation.

### 4. Level separation

The three levels are strictly separated by module boundary:

- `mctev.core.moral_functions` does **not** import from `mctev.core.cultural_params`
- `mctev.core.cultural_params` does **not** import from `mctev.core.situational`
- `mctev.core.situational` takes cultural parameters as an input, not as a constructor default

This enforces the paper's claim that Level 1 is not reducible to Level 2, nor Level 2 to Level 3.

---

## Testing

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

The test suite covers:

- `MoralFunctionProfile` bounds and round-tripping
- `CulturalParameters` normalization and canonical types
- `SituationalJudgment` with and without deontological constraints
- `FlourishingProfile` threshold logic
- Both case study diagnoses

---

## Extending the Library

### Adding a new candidate moral function

Because the framework treats functions as **candidates**, adding a seventh function is a purely additive change:

```python
# 1. Extend the enum in mctev/core/moral_functions.py
class MoralFunction(Enum):
    ...
    TEMPORAL_JUSTICE = "temporal"

# 2. Add to MORAL_FUNCTION_ORDER
MORAL_FUNCTION_ORDER = [..., MoralFunction.TEMPORAL_JUSTICE]

# 3. Update N_FUNCTIONS automatically (it's len(MORAL_FUNCTION_ORDER))
```

Subsequent code (profiles, parameters, viability vectors) adapts to the new dimensionality automatically.

### Adding a new cultural type

```python
from mctev.core.cultural_params import CulturalParameters, CULTURAL_TYPES
import numpy as np

CULTURAL_TYPES["confucian"] = CulturalParameters(
    weights=np.array([0.15, 0.20, 0.10, 0.35, 0.10, 0.10]),
    name="confucian",
)
```

### Adding a new dynamics model

```python
from mctev.viability.dynamics import Dynamics
import numpy as np

class MyDynamics(Dynamics):
    def __call__(self, x, params):
        return -0.1 * x + params.weights  # example
```

Any `Dynamics` subclass can be passed to `ViabilityKernel`, `ConstraintViolationAnalyzer`, and `compute_viable_region`.

---

## Citation

If you use `mctev-lib` in academic work, please cite:

```bibtex
@article{wang2026mctev,
  title   = {Toward a Computational Science of Ethics: A Multi-Level
             Theory of Ethical Variation and Universal Moral Principles},
  author  = {Wang, Harris},
  year    = {2026},
  note    = {Reference implementation: \texttt{mctev-lib}}
}
```

For the sibling research program on hierarchical computational explanations of complex systems, see:

```bibtex
@article{wang2025coh,
  title   = {Constrained Object Hierarchies as a Unified Theoretical Model
             for Intelligence and Intelligent Systems},
  author  = {Wang, Harris},
  journal = {Computers},
  volume  = {14},
  pages   = {478},
  year    = {2025}
}
```

---

## License

MIT License. See `LICENSE` for details.

---

## Acknowledgments

The MCTEV framework is methodologically aligned with the [COH/GISMOL](https://github.com/hongxueharriswang/gismol-lib) research program on hierarchical computational explanations of complex systems. The Ethical Constraint Hierarchy Principle — *constraints propagate downward, adaptation propagates upward* — captures the shared mechanism between the two frameworks.

---

**MCTEV-Lib v0.1.0** · Built for reproducibility, falsifiability, and extension.