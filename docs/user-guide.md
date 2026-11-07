# mctev-lib User Guide

**A comprehensive guide to the Multi-Level Computational Theory of Ethics library**

Version 0.1.0

---

## Table of Contents

**Part I — Getting Started**
1. [Introduction](#1-introduction)
2. [What MCTEV Is and Is Not](#2-what-mctev-is-and-is-not)
3. [Installation and Setup](#3-installation-and-setup)
4. [Your First MCTEV Program](#4-your-first-mctev-program)

**Part II — Conceptual Foundation**
5. [The Three-Level Architecture](#5-the-three-level-architecture)
6. [The Six Candidate Universal Moral Functions](#6-the-six-candidate-universal-moral-functions)
7. [Cultural Parameters and the Level-1/Level-2 Distinction](#7-cultural-parameters-and-the-level-1level-2-distinction)
8. [The Feasible Moral Region and Viability](#8-the-feasible-moral-region-and-viability)
9. [Human Flourishing and the Persistence-Flourishing Distinction](#9-human-flourishing-and-the-persistence-flourishing-distinction)

**Part III — Tutorial: Building an Ethical System**
10. [Tutorial 1: Judging a Situation](#10-tutorial-1-judging-a-situation)
11. [Tutorial 2: Constructing a Cultural Parameter Configuration](#11-tutorial-2-constructing-a-cultural-parameter-configuration)
12. [Tutorial 3: Computing the Viability Kernel](#12-tutorial-3-computing-the-viability-kernel)
13. [Tutorial 4: Assessing Flourishing](#13-tutorial-4-assessing-flourishing)
14. [Tutorial 5: Evaluating the Constraint Violation Theorem](#14-tutorial-5-evaluating-the-constraint-violation-theorem)
15. [Tutorial 6: Running the Three Societies Simulation](#15-tutorial-6-running-the-three-societies-simulation)
16. [Tutorial 7: Analyzing a Case Study](#16-tutorial-7-analyzing-a-case-study)

**Part IV — Cookbook**
17. [Recipe: Diagnose Any Moral System](#17-recipe-diagnose-any-moral-system)
18. [Recipe: Compare Two Cultural Configurations](#18-recipe-compare-two-cultural-configurations)
19. [Recipe: Design a Cross-Cultural AI Policy](#19-recipe-design-a-cross-cultural-ai-policy)
20. [Recipe: Quantify Moral Convergence](#20-recipe-quantify-moral-convergence)
21. [Recipe: Extend the Library with New Functions](#21-recipe-extend-the-library-with-new-functions)

**Part V — Reference**
22. [Complete API Reference](#22-complete-api-reference)
23. [Common Pitfalls and Troubleshooting](#23-common-pitfalls-and-troubleshooting)
24. [Design Decisions and Rationale](#24-design-decisions-and-rationale)

**Part VI — Advanced Topics**
25. [Integration with COH/GISMOL](#25-integration-with-cohgismol)
26. [Numerical Considerations](#26-numerical-considerations)
27. [Performance and Scaling](#27-performance-and-scaling)

**Part VII — Appendices**
28. [Theoretical Foundations: Key Equations](#28-theoretical-foundations-key-equations)
29. [Glossary](#29-glossary)
30. [References](#30-references)

---

# Part I — Getting Started

## 1. Introduction

`mctev-lib` is the reference implementation of the **Multi-Level Computational Theory of Ethics (MCTEV)** — a framework that reconciles two positions that have dominated moral philosophy for over a century:

- **Ethical relativism**: moral truth depends on culture or individual attitudes.
- **Ethical objectivism**: moral truth is independent of culture or attitudes.

MCTEV resolves this apparent contradiction by showing that both positions capture part of the truth: ethics is **hierarchically organized**, with universal functions at Level 1, cultural variation at Level 2, and situational judgments at Level 3. The library makes every claim in the theory executable, testable, and quantitatively evaluable.

The library supports four core capabilities:

1. **Representation**: model any moral system as a three-level structure.
2. **Reasoning**: compute situational judgments under constraints.
3. **Simulation**: run multi-agent models of moral dynamics.
4. **Analysis**: quantify convergence, divergence, viability, and collapse.

## 2. What MCTEV Is and Is Not

**What it is:**

- A **formal framework** for representing ethical systems.
- A **computational model** of how universal functions interact with cultural parameters.
- A **testable theory** whose predictions can be checked against simulation and, ultimately, empirical data.
- A **research program** that positions ethics as a computational science, methodologically aligned with (but not formally derived from) the COH/GISMOL agenda.

**What it is not:**

- A **complete theory** of all moral phenomena. The framework is a scaffold for further work.
- A **deductive engine** that mechanically resolves every moral disagreement. Level 1 *constrains* but does not *uniquely determine* outcomes.
- A **formally instantiated** COH 9-tuple. The relationship is methodological alignment and structural analogy.
- A **substitute for normative ethics**. It is a meta-theoretical framework, not a first-order moral theory.

Users should keep these boundaries in mind, especially when using the library to make claims about real-world ethical questions.

## 3. Installation and Setup

### 3.1 Requirements

| Component | Minimum version |
|-----------|-----------------|
| Python | 3.10 |
| NumPy | 1.24 |
| SciPy | 1.10 |
| Matplotlib | 3.7 |
| pandas | 2.0 |

### 3.2 Standard installation

```bash
git clone <repository-url> mctev-lib
cd mctev-lib
pip install -e .
```

### 3.3 Development installation

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

### 3.4 Verifying the installation

```python
import mctev
print(mctev.__version__)   # 0.1.0

from mctev.core.moral_functions import MoralFunction
print(list(MoralFunction))
```

### 3.5 Recommended environment

For interactive exploration, use JupyterLab or IPython:

```bash
pip install jupyterlab
jupyter lab
```

The library works equally well in scripts, notebooks, and as a dependency of larger projects.

## 4. Your First MCTEV Program

This complete program demonstrates the core capability: judging an action under a cultural configuration.

```python
"""first_mctev.py — a minimal MCTEV program."""

from mctev.core.moral_functions import MoralFunction, MoralUtilityLibrary
from mctev.core.cultural_params import CULTURAL_TYPES
from mctev.core.situational import Action, Situation, SituationalJudgment

# ---- Step 1: Define per-function utilities ----
# u_coop: higher contribution yields higher utility
# u_care: higher contribution costs more care (illustrative trade-off)
lib = MoralUtilityLibrary()
lib[MoralFunction.COOPERATION]            = lambda a, s: float(a.payload)
lib[MoralFunction.REPRODUCTION_CARE]      = lambda a, s: 1.0 - float(a.payload)

# ---- Step 2: Choose a cultural configuration ----
universalist = CULTURAL_TYPES["universalist"]

# ---- Step 3: Build the solver ----
solver = SituationalJudgment(utilities=lib)

# ---- Step 4: Evaluate a situation ----
actions = [Action("low", 0.2), Action("high", 0.8)]
situation = Situation("allocation decision")

best = solver.judge(situation, actions, universalist)
print(f"Universalist chooses: {best.name}")   # 'high'
```

**What just happened?**

1. We defined two candidate moral functions — cooperation and care — as simple utility callables.
2. We selected the `universalist` cultural parameter configuration, which weights both functions.
3. We built a `SituationalJudgment` solver that, given a situation and a set of actions, computes the weighted utility.
4. We evaluated the situation and obtained the highest-scoring action.

The `universalist` configuration weights cooperation more heavily than care, so it picks the action that maximizes cooperation. A `collectivist` configuration would weight care more heavily and might pick `low`.

You have now used Level 1 (`MoralFunction`), Level 2 (`CulturalParameters`), and Level 3 (`SituationalJudgment`). The rest of the guide expands each level in depth.

---

# Part II — Conceptual Foundation

## 5. The Three-Level Architecture

MCTEV's most distinctive feature is its three-level hierarchy.

```
                    ┌───────────────────────────────┐
                    │  LEVEL 1                      │
                    │  Candidate universal functions│
                    │  (constraints on viability)   │
                    └────────────┬──────────────────┘
                                 │
                    constraints propagate downward
                                 │
                                 ▼
                    ┌───────────────────────────────┐
                    │  LEVEL 2                      │
                    │  Cultural parameter vectors   │
                    │  (weights over functions)     │
                    └────────────┬──────────────────┘
                                 │
                    constraints propagate downward
                                 │
                                 ▼
                    ┌───────────────────────────────┐
                    │  LEVEL 3                      │
                    │  Situational judgments        │
                    │  (constrained optimization)   │
                    └────────────┬──────────────────┘
                                 │
                    adaptation propagates upward
                                 │
                                 ▼
                    (back to Levels 1 and 2)
```

**The Ethical Constraint Hierarchy Principle**: constraints propagate downward; adaptation propagates upward.

- **Downward**: Level 1 functions determine what counts as a viable culture; Level 2 cultures determine what counts as a legitimate judgment.
- **Upward**: Level 3 outcomes reveal whether Level 2 implementations are working; Level 2 implementations reveal whether Level 1 functions are being satisfied.

This is why the paper insists that Level 1 **constrains** but does not **uniquely determine** moral outcomes. Level 1 sets the terms of legitimate debate; Level 2 sets the specific resolutions; Level 3 applies those resolutions to cases.

## 6. The Six Candidate Universal Moral Functions

MCTEV identifies six candidate universal moral functions, each derived from a **functional problem** that any enduring society must solve:

| # | Functional problem | Moral function | Description |
|---|-------------------|----------------|-------------|
| \(P_1\) | Cooperation | \(f_{\text{coop}}\) | Reciprocal contribution to collective goods |
| \(P_2\) | Conflict management | \(f_{\text{conflict}}\) | Structured regulation of social conflict |
| \(P_3\) | Resource distribution | \(f_{\text{dist}}\) | Resource accessibility for all members |
| \(P_4\) | Reproduction and care | \(f_{\text{care}}\) | Care for the young and dependent |
| \(P_5\) | Knowledge transmission | \(f_{\text{info}}\) | Information integrity in transmission |
| \(P_6\) | Sustainability | \(f_{\text{sustain}}\) | Restraint in resource use |

**Why these six?** The Minimal Sufficiency Proposition (paper §6.2) argues they are:

- **Minimal**: removing any one causes social failure in the long run.
- **Sufficient**: additional problems (identity, religion, innovation, defense) are subsumed or derivative.

**Why "candidate"?** The mapping from functional problems to moral functions is not unique. A different researcher might propose different candidates. The library accommodates this by exposing functions as an extensible enumeration.

### 6.1 Accessing functions programmatically

```python
from mctev.core.moral_functions import (
    MoralFunction,
    MORAL_FUNCTION_ORDER,
    N_FUNCTIONS,
)

print(N_FUNCTIONS)               # 6
print([f.value for f in MORAL_FUNCTION_ORDER])
# ['cooperation', 'conflict', 'distribution', 'care', 'information', 'sustainability']

print(MoralFunction.COOPERATION.description)
# 'Reciprocal contribution to collective goods'
```

## 7. Cultural Parameters and the Level-1/Level-2 Distinction

The most important conceptual distinction in MCTEV: **Level 1 is universal, Level 2 is culturally variable**.

Level 2 cultures are represented as **weight vectors** over Level 1 functions. A culture does not choose *whether* to satisfy the function — any viable culture must satisfy all six — but *how much weight* to place on each.

### 7.1 The canonical cultural types

The library ships with four canonical configurations:

| Name | Emphasizes | Illustrative use |
|------|-----------|------------------|
| `universalist` | Balanced across all functions | Baseline for comparison |
| `collectivist` | Care and cooperation | Collectivist societies |
| `individualist` | Distribution and information | Liberal individualist societies |
| `self_regarding` | Only cooperation (degenerate) | Illustrative violating configuration |

**A crucial caveat**: the `self_regarding` type is not a real-world culture. It is a *degenerate* configuration used to illustrate constraint violation. Real cultures always place some weight on multiple functions.

### 7.2 Inspecting and creating parameters

```python
from mctev.core.cultural_params import (
    CulturalParameters,
    CULTURAL_TYPES,
    get_cultural_type,
)

# Retrieve a canonical type
collectivist = get_cultural_type("collectivist")
print(collectivist)
# CulturalParameters(name='collectivist',
#   cooperation=0.25, conflict=0.15, distribution=0.15,
#   care=0.30, information=0.10, sustainability=0.05)

# Inspect a specific weight
print(collectivist["care"])  # 0.30

# Create a custom type
my_culture = CulturalParameters.from_dict(
    {
        "cooperation": 0.15,
        "conflict": 0.20,
        "distribution": 0.10,
        "care": 0.35,
        "information": 0.10,
        "sustainability": 0.10,
    },
    name="custom_confucian",
)

# Normalize (weights sum to 1)
normalized = my_culture.normalized()

# Distance from a canonical type
print(f"Distance from collectivist: "
      f"{normalized.distance(collectivist):.3f}")
```

### 7.3 The Level-1/Level-2 distinction in practice

| Question | Level | Library concept |
|----------|-------|-----------------|
| Does this culture have care? | Level 2 question | `care` weight in `CulturalParameters` |
| Does care matter at all? | Level 1 question | Presence of `MoralFunction.REPRODUCTION_CARE` |
| How does this culture resolve a care-vs-autonomy dispute? | Level 3 question | `SituationalJudgment.judge` |

## 8. The Feasible Moral Region and Viability

Level 1 functions are not just labels. They define a **feasible region** \(\mathcal{R}\) — the set of social states from which some policy can keep the society viable forever.

$$
\mathcal{R} = \text{Viab}(\mathcal{V}, F)
= \left\{\mathbf{x}_0 \in \mathcal{V} :
\exists \pi \text{ s.t. } \mathbf{x}(t) \in \mathcal{V}
\text{ for all } t \geq 0 \right\}
$$

where:

- \(\mathbf{x}\) is a state vector of functional indicators (cooperation rate, trust, etc.)
- \(\mathcal{V}\) is the constraint set \(\{V_i(\mathbf{x}) \geq \tau_i\}\)
- \(F\) is the dynamics of social evolution

### 8.1 Components of the viability layer

| Component | Class | Purpose |
|-----------|-------|---------|
| Constraints | `ViabilityConstraints` | Define \(\{V_i(\mathbf{x}) \geq \tau_i\}\) |
| Dynamics | `Dynamics`, `LinearDynamics` | Define \(F(\mathbf{x}, \theta_c)\) |
| Kernel | `ViabilityKernel` | Approximate \(\mathcal{R}\) |

### 8.2 Defining constraints

```python
from mctev.viability.constraints import ViabilityConstraints
from mctev.core.moral_functions import MoralFunction
import numpy as np

constraints = ViabilityConstraints()

# Interpret state as [cooperation, conflict, distribution, care, info, sustain]
constraints[MoralFunction.COOPERATION] = (lambda x: x[0], 0.5)
constraints[MoralFunction.CONFLICT_MANAGEMENT] = (lambda x: x[1], 0.3)
constraints[MoralFunction.RESOURCE_DISTRIBUTION] = (lambda x: x[2], 0.4)

# Check satisfaction
x = np.array([0.8, 0.4, 0.2, 0.5, 0.5, 0.5])
print(constraints.is_satisfied(x))   # False (distribution violates)
print(constraints.violations(x))     # {RESOURCE_DISTRIBUTION: 0.2}
```

Or use the illustrative defaults:

```python
from mctev.viability.constraints import default_constraints

constraints = default_constraints()  # All thresholds = 0.3
```

### 8.3 Computing the viability kernel

```python
from mctev.viability.kernel import compute_viable_region
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.core.cultural_params import CULTURAL_TYPES

kernel = compute_viable_region(
    constraints=default_constraints(),
    dynamics=LinearDynamics(),
    params=CULTURAL_TYPES["universalist"],
    grid_size=6,
    horizon=200,
)

print(f"Viable fraction of grid: {kernel.fraction_viable():.2%}")
# Viable fraction of grid: 23.15%

# Check whether a specific state is in R
import numpy as np
state = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
print(kernel.contains(state))   # True
```

**Performance note**: grid-based kernel computation scales as \(\text{grid\_size}^6\). `grid_size=6` means \(6^6 = 46{,}656\) simulations of `horizon` steps each. For `grid_size=8`, that's \(262{,}144\) simulations. Adjust `grid_size` and `horizon` to match your resources.

## 9. Human Flourishing and the Persistence-Flourishing Distinction

The framework's answer to the **functionalist objection** ("what survives is not necessarily moral") is to distinguish persistence from flourishing.

- **Persistence** is a *necessary* condition: a moral system must be viable.
- **Flourishing** is the *evaluative* condition: a moral system must enable human thriving.

$$
\text{Morality}(\theta_c)
= \text{Persistence}(\theta_c) \wedge \text{Flourishing}(\theta_c)
$$

### 9.1 The five dimensions

| Dimension | Symbol | Meaning |
|-----------|--------|---------|
| Wellbeing | \(W\) | Health, material security, absence of pain |
| Psychological functioning | \(P\) | Positive affect, resilience, cognitive function |
| Agency | \(A\) | Capacity to set and pursue goals |
| Social connectedness | \(S\) | Quality of relationships, belonging |
| Meaning | \(M\) | Sense of purpose, coherence, contribution |

### 9.2 Assessing flourishing

```python
from mctev.flourishing.dimensions import (
    FlourishingProfile,
    FlourishingThresholds,
)

# A flourishing society
society = FlourishingProfile.from_dict(
    {"W": 0.7, "P": 0.6, "A": 0.6, "S": 0.8, "M": 0.6}
)
thresholds = FlourishingThresholds.default()   # All 0.5

print(thresholds.is_flourishing(society))   # True
print(thresholds.deficit(society))          # 0.0

# A society that persists but does not flourish
oppressive = FlourishingProfile.from_dict(
    {"W": 0.6, "P": 0.4, "A": 0.1, "S": 0.2, "M": 0.2}
)
print(thresholds.is_flourishing(oppressive))   # False
print(thresholds.deficit(oppressive))          # 0.9
```

### 9.3 The set relation

$$
\mathcal{F} = \{\mathbf{x} : H(\mathbf{x}) \geq \tau_H\}
\subseteq \mathcal{R}
$$

**Every flourishing state is feasible, but not every feasible state is flourishing.** A dictatorship can be viable (in \(\mathcal{R}\)) without flourishing (outside \(\mathcal{F}\)). This is the formal basis for MCTEV's moral criticism of oppressive regimes.

---

# Part III — Tutorial: Building an Ethical System

## 10. Tutorial 1: Judging a Situation

**Goal**: Given a situation, actions, and a cultural configuration, determine the best action.

### 10.1 Define the utility functions

A utility function takes an `Action` and a `Situation` and returns a scalar contribution to the corresponding Level-1 function.

```python
from mctev.core.moral_functions import MoralFunction, MoralUtilityLibrary

lib = MoralUtilityLibrary()

# Cooperation: more contribution → more cooperative utility
lib[MoralFunction.COOPERATION] = lambda a, s: float(a.payload)

# Care: more contribution → less care utility (trade-off)
lib[MoralFunction.REPRODUCTION_CARE] = lambda a, s: 1.0 - float(a.payload)

# Distribution: utility peaks at 0.5 contribution (moderate sharing)
lib[MoralFunction.RESOURCE_DISTRIBUTION] = (
    lambda a, s: 1.0 - abs(float(a.payload) - 0.5) * 2
)

# Conflict management: penalize extreme contributions
lib[MoralFunction.CONFLICT_MANAGEMENT] = (
    lambda a, s: 1.0 - abs(float(a.payload) - 0.5) * 2
)

# Information and sustainability: not applicable in this scenario
# (utilities default to 0, meaning they don't influence the choice)
```

### 10.2 Define the situation and actions

```python
from mctev.core.situational import Action, Situation

situation = Situation(
    name="resource allocation",
    context={"stakes": "high", "reversible": True},
)

actions = [
    Action("selfish",   payload=0.1),
    Action("moderate",  payload=0.5),
    Action("generous",  payload=0.9),
]
```

The `context` is passed to the utility functions and can be used to make utilities situation-dependent.

### 10.3 Apply constraints (optional)

Constraints enforce deontological rules that filter admissible actions *before* utility evaluation.

```python
def no_selfishness(situation, action):
    """Rule: never take less than 20% for the collective."""
    return float(action.payload) >= 0.2

from mctev.core.situational import SituationalJudgment

solver = SituationalJudgment(utilities=lib, constraints=no_selfishness)

print(solver.admissible_actions(actions, situation))
# [Action('moderate'), Action('generous')]
```

### 10.4 Compute the judgment for each culture

```python
from mctev.core.cultural_params import CULTURAL_TYPES

for name, params in CULTURAL_TYPES.items():
    best = solver.judge(situation, actions, params)
    ranking = solver.rank(situation, actions, params)
    print(f"\n{name:15s} → {best.name if best else None}")
    for score, action in ranking:
        print(f"    {score:+.3f}  {action.name}")
```

**Expected output** (approximately):

```
universalist    → moderate
    +0.61  moderate
    +0.55  generous

collectivist    → moderate
    +0.68  moderate
    +0.42  generous

individualist   → moderate
    +0.58  moderate
    +0.53  generous

self_regarding  → generous
    +0.90  generous
    +0.50  moderate
```

Notice that three of the four cultures pick `moderate`, but `self_regarding` picks `generous` because its weights are dominated by cooperation. This demonstrates how different Level-2 configurations produce different Level-3 judgments from the same Level-1 functions.

### 10.5 Using `MCTEVSystem`

For repeated evaluations, use the higher-level `MCTEVSystem`:

```python
from mctev.core.hierarchy import MCTEVSystem

system = MCTEVSystem.from_type(
    "universalist",
    utilities=lib,
    constraints=no_selfishness,
)

print(system.describe())
print(f"Viable: {system.is_viable()}")
print(system.judge(situation, actions))
```

## 11. Tutorial 2: Constructing a Cultural Parameter Configuration

**Goal**: Model a new cultural configuration that isn't in the canonical set.

### 11.1 Start from an existing type

```python
from mctev.core.cultural_params import (
    CulturalParameters,
    CULTURAL_TYPES,
)
import numpy as np

# Start from collectivist and increase care weight
collectivist = CULTURAL_TYPES["collectivist"]
base = collectivist.weights.copy()

# Increase care weight, decrease cooperation weight
base[0] -= 0.05   # cooperation
base[3] += 0.05   # care

custom = CulturalParameters(weights=base, name="care_emphasizing")
print(custom)
```

### 11.2 Normalize for interpretability

```python
normalized = custom.normalized()
print(f"Sum of weights: {normalized.weights.sum():.4f}")   # 1.0000
```

### 11.3 Validate against the viable region

```python
from mctev.core.cultural_params import CulturalParametersRegion

# Default region: all weights in [0, 1]
region = CulturalParametersRegion.default()
print(region.contains(normalized))   # True

# Custom viable region: each weight in [0.05, 0.35]
custom_region = CulturalParametersRegion(
    lower=np.full(6, 0.05),
    upper=np.full(6, 0.35),
)
print(custom_region.contains(normalized))   # Depends on configuration
```

### 11.4 Compare against the canonical set

```python
for name, canonical in CULTURAL_TYPES.items():
    d = normalized.distance(canonical)
    print(f"Distance from {name:15s}: {d:.3f}")
```

## 12. Tutorial 3: Computing the Viability Kernel

**Goal**: Determine which social states lie within the feasible moral region.

### 12.1 Configure the dynamics

```python
from mctev.viability.dynamics import LinearDynamics, NonlinearCouplingDynamics
import numpy as np

# Simple linear dynamics with logistic self-limitation
linear = LinearDynamics()

# Richer dynamics with inter-indicator coupling
coupled = NonlinearCouplingDynamics()

# Custom dynamics: your own function
class MyDynamics(LinearDynamics):
    def __call__(self, x, params):
        # Example: cooperation decays faster
        base = super().__call__(x, params)
        base[0] *= 0.8
        return base

custom_dyn = MyDynamics()
```

### 12.2 Run the kernel computation

```python
from mctev.viability.kernel import compute_viable_region
from mctev.viability.constraints import default_constraints
from mctev.core.cultural_params import CULTURAL_TYPES

kernel = compute_viable_region(
    constraints=default_constraints(),
    dynamics=linear,
    params=CULTURAL_TYPES["universalist"],
    grid_size=5,        # smaller for speed
    horizon=150,
)

print(f"Viable fraction: {kernel.fraction_viable():.2%}")
```

### 12.3 Compare kernels across cultures

```python
for name in ["universalist", "collectivist", "individualist", "self_regarding"]:
    k = compute_viable_region(
        constraints=default_constraints(),
        dynamics=linear,
        params=CULTURAL_TYPES[name],
        grid_size=5,
        horizon=150,
    )
    print(f"{name:15s}  viable_fraction = {k.fraction_viable():.2%}")
```

A high viable fraction means the culture has a large basin of attraction to viability; a low fraction means the culture is fragile.

### 12.4 Sample viable states

```python
import numpy as np

viable_states = kernel.sample_viable(n_samples=50, rng=np.random.default_rng(42))
print(viable_states.shape)   # (n, 6)
print(viable_states.mean(axis=0))   # Average viable state
```

## 13. Tutorial 4: Assessing Flourishing

**Goal**: Determine whether a society meets the flourishing thresholds.

### 13.1 Assemble a flourishing profile

```python
from mctev.flourishing.dimensions import (
    FlourishingProfile,
    FlourishingThresholds,
)

profile = FlourishingProfile.from_dict({
    "W": 0.75,  # Wellbeing
    "P": 0.65,  # Psychological functioning
    "A": 0.55,  # Agency
    "S": 0.70,  # Social connectedness
    "M": 0.60,  # Meaning
})
```

### 13.2 Apply thresholds

```python
thresholds = FlourishingThresholds.default()

print(f"Flourishing: {thresholds.is_flourishing(profile)}")
print(f"Deficit:     {thresholds.deficit(profile):.3f}")

# Custom thresholds: higher bar for meaning
custom_th = FlourishingThresholds.from_dict({
    "W": 0.5, "P": 0.5, "A": 0.5, "S": 0.5, "M": 0.8
})
print(f"Flourishing under custom thresholds: "
      f"{custom_th.is_flourishing(profile)}")
```

### 13.3 Diagnose which dimension is limiting

```python
import numpy as np

deficits = np.clip(thresholds.thresholds - profile.values, 0, None)
dims = ["W", "P", "A", "S", "M"]

for dim, deficit in zip(dims, deficits):
    if deficit > 0:
        print(f"{dim} is deficient by {deficit:.3f}")
```

## 14. Tutorial 5: Evaluating the Constraint Violation Theorem

**Goal**: Empirically verify that sustained constraint violations predict collapse.

### 14.1 Set up the analyzer

```python
from mctev.collapse.theorem import ConstraintViolationAnalyzer
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.core.cultural_params import CULTURAL_TYPES
import numpy as np

analyzer_viable = ConstraintViolationAnalyzer(
    constraints=default_constraints(),
    dynamics=LinearDynamics(),
    params=CULTURAL_TYPES["universalist"],
    noise_scale=0.05,
    rng=np.random.default_rng(1),
)

analyzer_violating = ConstraintViolationAnalyzer(
    constraints=default_constraints(),
    dynamics=LinearDynamics(),
    params=CULTURAL_TYPES["self_regarding"],
    noise_scale=0.05,
    rng=np.random.default_rng(2),
)
```

### 14.2 Simulate from viable initial states

```python
rng = np.random.default_rng(0)
x0_samples = rng.uniform(0.4, 0.8, size=(100, 6))   # Start in viable region

result_viable = analyzer_viable.simulate(x0_samples, horizon_steps=2000)
print(result_viable.summary())
```

Expected output:

```
ExitTimeResult(n=100, horizon=20.0, noise=0.05)
  mean exit time: ~18.5   ← most trajectories never exit
  censor rate: ~92%
  exponential fit: C=~1.0, λ=~0.01
```

### 14.3 Simulate from a violating culture

```python
result_violating = analyzer_violating.simulate(x0_samples, horizon_steps=2000)
print(result_violating.summary())
```

Expected output:

```
ExitTimeResult(n=100, horizon=20.0, noise=0.05)
  mean exit time: ~6.2
  censor rate: ~5%
  exponential fit: C=~1.0, λ=~0.18   ← substantial decay
```

### 14.4 Interpret the results

- **Viable culture**: high censor rate (~92%), meaning most trajectories never exit. Low decay rate \(\lambda\).
- **Violating culture**: low censor rate (~5%), meaning most trajectories exit quickly. High decay rate \(\lambda\).

The **decay rate** \(\lambda\) is the key empirical quantity. It measures how fast the survival function falls off. Higher \(\lambda\) means faster collapse. This is the empirical content of the Constraint Violation Theorem.

### 14.5 Plot survival curves

```python
from mctev.analysis.visualization import plot_survival_curves
import matplotlib.pyplot as plt

results = {"viable": result_viable, "violating": result_violating}
plot_survival_curves(results)
plt.savefig("survival_curves.png", dpi=150)
```

## 15. Tutorial 6: Running the Three Societies Simulation

**Goal**: Simulate how a public good evolves under different agent compositions.

### 15.1 Configure the simulation

```python
from mctev.simulation import (
    ThreeSocietiesConfig,
    run_three_societies,
)

config = ThreeSocietiesConfig(
    n_agents=30,
    n_rounds=200,
    return_rate=1.5,
    endowment=10.0,
    coop_threshold=0.2,    # normalized: mean_contribution / endowment
)
```

### 15.2 Run all three conditions

```python
dfs = {
    cond: run_three_societies(cond, config=config, seed=42)
    for cond in (1, 2, 3)
}

for cond, df in dfs.items():
    final_mean = df["mean_contribution"].iloc[-10:].mean()
    print(f"Condition {cond}: "
          f"final mean = {final_mean:.2f}, "
          f"collapsed = {df['collapsed'].iloc[-1]}")
```

### 15.3 Interpret the results

| Condition | Description | Expected outcome |
|-----------|-------------|------------------|
| 1 | All universalists | Sustained high cooperation |
| 2 | Equal U + C + I | Sustained but lower cooperation |
| 3 | 10% self-regarding introduced | Cooperation declines; collapse |

**Why this matters**: Condition 2 shows that *different cultural configurations can coexist productively*. This is the simulation's support for the claim that Level-2 variation is compatible with Level-1 constraint satisfaction.

### 15.4 Visualize

```python
from mctev.analysis.visualization import plot_three_societies
import matplotlib.pyplot as plt

plot_three_societies(dfs)
plt.savefig("three_societies.png", dpi=150)
```

## 16. Tutorial 7: Analyzing a Case Study

**Goal**: Use MCTEV to diagnose moral systems.

### 16.1 Case 1: Slavery (constraint violation)

```python
from mctev.cases.slavery import evaluate_slavery

diagnosis = evaluate_slavery()
print(diagnosis.summary())
```

Expected output:

```
Slavery diagnosis (MCTEV Case Study 1)
========================================
  cooperation    : 0.10
  conflict       : 0.10
  distribution   : 0.10
  care           : 0.20
  information    : 0.10
  sustainability : 0.30
----------------------------------------
  violated functions: ['cooperation', 'conflict', 'distribution',
                       'information']
  severity score:     0.13
```

**Interpretation**: slavery violates four of six Level-1 functions, producing a severity score of 0.13. Under the Constraint Violation Theorem, this predicts elevated collapse pressures — consistent with the historical abolition of slavery.

### 16.2 Case 2: Capital punishment (legitimate disagreement)

```python
from mctev.cases.capital_punishment import evaluate_capital_punishment

diagnosis = evaluate_capital_punishment()
print(diagnosis.summary())
```

Expected output:

```
Capital punishment diagnosis (MCTEV Case Study 2)
===================================================
Both positions implement the same Level-1 function:
  conflict (structured regulation of conflict)

Retentionist profile:
  cooperation    : 0.50
  conflict       : 0.80  ← high
  distribution   : 0.40
  care           : 0.30
  information    : 0.50
  sustainability : 0.50

Abolitionist profile:
  cooperation    : 0.50
  conflict       : 0.80  ← also high
  distribution   : 0.70
  care           : 0.80
  information    : 0.70
  sustainability : 0.50

Conclusion: Level 2 disagreement over Level 1 function.
```

**Interpretation**: both sides agree that conflict management matters. They disagree about how to implement it (proportionality vs. restorative justice). This is a Level-2 disagreement, not a Level-1 disagreement — hence legitimate moral pluralism.

### 16.3 Diagnosing your own system

```python
from mctev.core.moral_functions import MoralFunctionProfile

your_system = MoralFunctionProfile.from_dict({
    "cooperation": 0.6,
    "conflict": 0.4,
    "distribution": 0.5,
    "care": 0.7,
    "information": 0.5,
    "sustainability": 0.3,
})

threshold = 0.3
violations = {
    f.value: your_system[f]
    for f in your_system.__class__.__dict__.get("_fields", [])
    if False  # placeholder
}

# More direct:
from mctev.core.moral_functions import MoralFunction
violations = {
    f.value: your_system[f]
    for f in MoralFunction
    if your_system[f] < threshold
}
print(f"Violated functions: {list(violations)}")
```

---

# Part IV — Cookbook

## 17. Recipe: Diagnose Any Moral System

**Problem**: You have a proposed ethical system (or historical institution) and want to evaluate its compliance with Level-1 functions.

**Solution**:

```python
from mctev.core.moral_functions import MoralFunction, MoralFunctionProfile

def diagnose(profile_dict: dict, threshold: float = 0.3) -> dict:
    """Diagnose a moral system against the six candidate functions."""
    profile = MoralFunctionProfile.from_dict(profile_dict)
    violations = {
        f.value: profile[f]
        for f in MoralFunction
        if profile[f] < threshold
    }
    severity = sum(threshold - v for v in violations.values()) / len(MoralFunction)
    return {
        "profile": profile,
        "violations": violations,
        "severity": severity,
        "num_violations": len(violations),
    }

# Example
result = diagnose({
    "cooperation": 0.7,
    "conflict": 0.5,
    "distribution": 0.2,   # weak
    "care": 0.6,
    "information": 0.4,
    "sustainability": 0.1,  # very weak
})
print(f"Violations: {result['violations']}")
print(f"Severity:   {result['severity']:.3f}")
```

**When to use**: when you have a proposed moral institution, policy, or historical period to evaluate.

**Caveat**: this is a diagnostic aid, not a moral verdict. The candidate functions are *candidates*, and a low score on one may be justified by context.

## 18. Recipe: Compare Two Cultural Configurations

**Problem**: You want to quantify the difference between two cultures.

**Solution**:

```python
from mctev.core.cultural_params import CulturalParameters
from mctev.analysis.metrics import convergence_index, divergence_index
import numpy as np

def compare_cultures(a: CulturalParameters, b: CulturalParameters) -> dict:
    """Quantify the difference between two cultural parameter vectors."""
    return {
        "distance": a.distance(b),
        "cosine_similarity": convergence_index([a.weights, b.weights]),
        "divergence": divergence_index([a.weights, b.weights]),
        "per_dimension_diff": {
            f: (a[f] - b[f])
            for f in ["cooperation", "conflict", "distribution",
                      "care", "information", "sustainability"]
        },
    }

# Example
from mctev.core.cultural_params import CULTURAL_TYPES
diff = compare_cultures(
    CULTURAL_TYPES["universalist"],
    CULTURAL_TYPES["collectivist"],
)
print(f"Distance: {diff['distance']:.3f}")
print(f"Divergence: {diff['divergence']:.3f}")
```

**When to use**: for quantitative cross-cultural comparisons.

## 19. Recipe: Design a Cross-Cultural AI Policy

**Problem**: You are designing an AI system that must operate across multiple cultural contexts.

**Solution**: use the three-layer architecture.

```python
from mctev.core.moral_functions import MoralFunction, MoralUtilityLibrary
from mctev.core.situational import Action, Situation, SituationalJudgment
from mctev.core.cultural_params import CULTURAL_TYPES

def design_ai_policy(
    universal_constraints: callable,
    deployment_contexts: list,
    actions: list,
    utilities: MoralUtilityLibrary,
) -> dict:
    """
    Design a cross-cultural AI policy.

    1. Universal constraints (Level 1): hard rules that apply everywhere.
    2. Cultural parameters (Level 2): weights chosen per deployment context.
    3. Situational judgments (Level 3): context-sensitive action selection.
    """
    solver = SituationalJudgment(
        utilities=utilities,
        constraints=universal_constraints,
    )

    policy = {}
    for context_name, params in deployment_contexts:
        situation = Situation(name=context_name)
        best = solver.judge(situation, actions, params)
        policy[context_name] = best.name if best else "no_admissible_action"

    return policy

# Example
lib = MoralUtilityLibrary()
lib[MoralFunction.COOPERATION] = lambda a, s: float(a.payload)

constraints = lambda sit, act: float(act.payload) >= 0.2  # hard floor

deployments = [
    ("US", CULTURAL_TYPES["individualist"]),
    ("Japan", CULTURAL_TYPES["collectivist"]),
    ("EU", CULTURAL_TYPES["universalist"]),
]

policy = design_ai_policy(
    universal_constraints=constraints,
    deployment_contexts=deployments,
    actions=[Action("a1", 0.3), Action("a2", 0.6), Action("a3", 0.9)],
    utilities=lib,
)
print(policy)
```

**When to use**: designing globally-deployed AI, international policy, humanitarian intervention.

## 20. Recipe: Quantify Moral Convergence

**Problem**: You want to measure whether two cultures are becoming more or less similar over time.

**Solution**:

```python
from mctev.core.cultural_params import CulturalParameters
from mctev.analysis.metrics import convergence_index

def temporal_convergence(
    time_series_a: list,
    time_series_b: list,
) -> list:
    """Compute convergence index at each time step."""
    return [
        convergence_index([a.weights, b.weights])
        for a, b in zip(time_series_a, time_series_b)
    ]

# Example
series_west = [
    CulturalParameters(weights=np.array([0.3, 0.15, 0.25, 0.15, 0.1, 0.05])),
    CulturalParameters(weights=np.array([0.28, 0.15, 0.27, 0.15, 0.1, 0.05])),
    CulturalParameters(weights=np.array([0.26, 0.15, 0.29, 0.15, 0.1, 0.05])),
]
series_east = [
    CulturalParameters(weights=np.array([0.2, 0.2, 0.1, 0.35, 0.1, 0.05])),
    CulturalParameters(weights=np.array([0.22, 0.2, 0.12, 0.33, 0.1, 0.03])),
    CulturalParameters(weights=np.array([0.24, 0.18, 0.15, 0.30, 0.1, 0.03])),
]

convergence = temporal_convergence(series_west, series_east)
print([f"{c:.3f}" for c in convergence])
```

**When to use**: longitudinal analysis of cultural change.

## 21. Recipe: Extend the Library with New Functions

**Problem**: You believe a seventh Level-1 function is needed (e.g., "temporal justice").

**Solution**: extend the enum in place.

```python
# In a new file: my_extension.py
from mctev.core.moral_functions import MoralFunction
import enum

# Define an extended enum
class ExtendedMoralFunction(enum.Enum):
    # Base six
    COOPERATION = "cooperation"
    CONFLICT_MANAGEMENT = "conflict"
    RESOURCE_DISTRIBUTION = "distribution"
    REPRODUCTION_CARE = "care"
    KNOWLEDGE_TRANSMISSION = "information"
    SUSTAINABILITY = "sustainability"
    # New seventh
    TEMPORAL_JUSTICE = "temporal"
```

**Note**: The core library assumes `N_FUNCTIONS = 6`. Adding a new function requires overriding `MORAL_FUNCTION_ORDER` and `N_FUNCTIONS`, or filing a feature request. The design is deliberately extensible but not dynamically extensible at runtime.

**Better approach** for exploratory work: create a parallel module that imports the core six and adds your own.

---

# Part V — Reference

## 22. Complete API Reference

### 22.1 `mctev.core.moral_functions`

#### `class MoralFunction(Enum)`

Six candidate universal moral functions. Members: `COOPERATION`, `CONFLICT_MANAGEMENT`, `RESOURCE_DISTRIBUTION`, `REPRODUCTION_CARE`, `KNOWLEDGE_TRANSMISSION`, `SUSTAINABILITY`.

**Properties**: `.description → str`

#### `MORAL_FUNCTION_ORDER: List[MoralFunction]`

Canonical ordering for vectors and matrices.

#### `N_FUNCTIONS: int`

`= 6`

#### `class MoralFunctionProfile`

Frozen dataclass. Vector of contributions in \([0,1]^6\).

| Method | Description |
|--------|-------------|
| `__getitem__(f)` | Get entry for function `f` |
| `as_dict()` | Return dict keyed by function names |
| `dominance()` | Fraction of functions ≥ 0.5 |
| `to_array()` | Return numpy array |
| `from_dict(d)` | Build from dict |
| `from_array(arr)` | Build from array |
| `uniform(v)` | Build with all entries = `v` |
| `zeros()` | Build with all zeros |

**Raises**: `ValueError` if shape ≠ 6 or any entry outside \([0,1]\).

#### `class MoralUtilityLibrary`

Mutable dict of per-function utility callables.

| Method | Description |
|--------|-------------|
| `__setitem__(f, fn)` | Register a utility function |
| `__getitem__(f)` | Retrieve (returns 0-function if absent) |
| `evaluate(action, situation, weights)` | Weighted sum of utilities |

### 22.2 `mctev.core.cultural_params`

#### `class CulturalParameters`

Frozen dataclass. Weight vector \(\theta_c\).

**Constructor**: `CulturalParameters(weights: np.ndarray, name: str = "custom")`

| Method | Description |
|--------|-------------|
| `__getitem__(f)` | Get entry for function `f` |
| `normalized()` | Return unit-sum version |
| `distance(other)` | L2 distance |
| `to_dict()` | Dict of weights |
| `from_dict(d, name)` | Build from dict |
| `uniform(name)` | All weights = 1/6 |

#### `CULTURAL_TYPES: Dict[str, CulturalParameters]`

Canonical types: `universalist`, `collectivist`, `individualist`, `self_regarding`.

#### `get_cultural_type(name) → CulturalParameters`

Retrieve by name.

#### `class CulturalParametersRegion`

Frozen dataclass. Convex region in parameter space.

**Constructor**: `CulturalParametersRegion(lower, upper)`

| Method | Description |
|--------|-------------|
| `contains(params)` | Whether parameters lie in region |
| `default()` | All weights in [0, 1] |

### 22.3 `mctev.core.situational`

#### `class Action`

`Action(name: str, payload: Any = None)`. Hashable by `(name, id(payload))`.

#### `class Situation`

`Situation(name: str, context: dict = {})`.

#### `class SituationalJudgment`

| Method | Description |
|--------|-------------|
| `admissible_actions(actions, situation)` | Filter by constraints |
| `score(action, situation, params)` | Weighted utility |
| `judge(situation, actions, params)` | Best admissible action |
| `rank(situation, actions, params)` | Sorted list `(score, action)` |

**Constructor**: `SituationalJudgment(utilities: MoralUtilityLibrary, constraints: Optional[Callable] = None)`

### 22.4 `mctev.core.hierarchy`

#### `class MCTEVSystem`

| Method | Description |
|--------|-------------|
| `situational_layer()` | Build a `SituationalJudgment` |
| `judge(situation, actions)` | Delegate to situational layer |
| `is_viable()` | Check region membership |
| `from_type(type_name, utilities, ...)` | Convenience constructor |
| `describe()` | Human-readable summary |

### 22.5 `mctev.viability`

#### `class ViabilityConstraints`

| Method | Description |
|--------|-------------|
| `__setitem__(f, (fn, tau))` | Add constraint |
| `__getitem__(f)` | Get `(fn, tau)` |
| `values(x)` | Evaluate all |
| `violations(x)` | Dict of deficits |
| `is_satisfied(x)` | Boolean |
| `violation_score(x)` | Sum of deficits |

#### `default_constraints() → ViabilityConstraints`

All thresholds at 0.3.

#### `class LinearDynamics(Dynamics)`

`dx/dt = A·x + B·θ_c − c·x·(1−x)`. Constructor: `LinearDynamics(A=None, B=None, c=0.5)`.

#### `class NonlinearCouplingDynamics(Dynamics)`

Coupled dynamics with inter-indicator coupling.

#### `class ViabilityKernel`

Grid-based approximate viability kernel.

| Method | Description |
|--------|-------------|
| `build_grid()` | Build probe grid |
| `trajectory_stays_viable(x0)` | Boolean |
| `build()` | Compute mask |
| `contains(x)` | Boolean |
| `fraction_viable()` | Fraction of grid in $\mathcal{R}$ |
| `sample_viable(n, rng)` | Sample points in $\mathcal{R}$ |

#### `compute_viable_region(...) → ViabilityKernel`

Convenience constructor.

### 22.6 `mctev.flourishing.dimensions`

#### `class FlourishingProfile`

Frozen dataclass. Vector in \([0,1]^5\).

| Method | Description |
|--------|-------------|
| `__getitem__(key)` | Get dimension (one of W, P, A, S, M) |
| `as_dict()` | Dict keyed by full names |
| `from_dict(d)` | Build from dict |

#### `class FlourishingThresholds`

Frozen dataclass. Threshold vector.

| Method | Description |
|--------|-------------|
| `is_flourishing(profile)` | Boolean |
| `deficit(profile)` | Sum of deficits |
| `default()` | All thresholds = 0.5 |
| `from_dict(d)` | Build from dict |

### 22.7 `mctev.collapse.theorem`

#### `class ConstraintViolationAnalyzer`

| Method | Description |
|--------|-------------|
| `run_trial(x0, horizon_steps)` | Single trajectory |
| `simulate(x0_samples, horizon_steps)` | Many trajectories → `ExitTimeResult` |

**Constructor**: `ConstraintViolationAnalyzer(constraints, dynamics, params, noise_scale=0.02, dt=0.01, rng=None)`

#### `class ExitTimeResult`

| Method / Property | Description |
|-------------------|-------------|
| `censor_rate` | Fraction with no exit |
| `survival_function()` | (times, survival probs) |
| `fit_exponential()` | (C, λ) fit |
| `summary()` | Human-readable string |

#### `compare_viable_vs_violating(...) → dict`

Returns `{"viable": ExitTimeResult, "violating": ExitTimeResult}`.

### 22.8 `mctev.simulation`

#### `class AgentType(Enum)`

`UNIVERSALIST`, `COLLECTIVIST`, `INDIVIDUALIST`, `SELF_REGARDING`.

#### `class Agent`

Public goods game agent. Key methods: `best_contribution(...)`, `update_belief(...)`.

#### `class PublicGoodsGame`

`play_round() → dict` of round statistics.

#### `class ThreeSocietiesConfig`

Dataclass with simulation parameters.

#### `run_three_societies(condition, config=None, seed=0) → pd.DataFrame`

### 22.9 `mctev.cases`

#### `evaluate_slavery() → SlaveryDiagnosis`

#### `evaluate_capital_punishment() → CapitalPunishmentDiagnosis`

### 22.10 `mctev.analysis`

#### Metrics

- `convergence_index(profiles) → float`
- `divergence_index(profiles) → float`
- `cultural_distance_matrix(params) → np.ndarray`

#### Visualization

- `plot_three_societies(dfs) → Axes`
- `plot_survival_curves(results) → Axes`
- `plot_viability_grid(kernel) → Axes`
- `plot_flourishing_radar(profile, thresholds=None) → Axes`

## 23. Common Pitfalls and Troubleshooting

### 23.1 "Expected vector of length 6"

**Cause**: You passed a vector with the wrong number of entries to `MoralFunctionProfile` or `CulturalParameters`.

**Fix**: Ensure your array has shape `(6,)`. If your weights sum to something other than 1, call `.normalized()`.

### 23.2 "Unknown moral function: 'reciprocity'"

**Cause**: You used a string that doesn't match a `MoralFunction` value.

**Fix**: Use one of the six canonical function names: `cooperation`, `conflict`, `distribution`, `care`, `information`, `sustainability`.

### 23.3 Viability kernel takes too long

**Cause**: Grid size × grid size × 6 × horizon is expensive.

**Fix**: Reduce `grid_size` (use 4 or 5 for exploration), reduce `horizon`, or use `sample_viable()` instead of computing the full grid.

### 23.4 Constraint violation analysis gives `NaN` for λ

**Cause**: The survival function has too few nonzero points to fit.

**Fix**: Increase `horizon_steps`, reduce `noise_scale`, or use more trials.

### 23.5 `judge()` returns `None`

**Cause**: No admissible actions (all filtered out by constraints).

**Fix**: Check `solver.admissible_actions(...)`. If empty, either relax constraints or provide actions that satisfy them.

### 23.6 Cultural parameters don't sum to 1

**Cause**: `CulturalParameters` allows arbitrary non-negative weights.

**Fix**: Use `.normalized()` if you need unit-sum weights for interpretability. This isn't required for the weighted optimization to work.

### 23.7 `MCTEVSystem` disagrees with my manual calculation

**Cause**: Common mismatch sources:
- Different utility library ordering.
- Constraints altering the admissible set.
- Weight signs (must be non-negative).

**Fix**: Compare intermediate steps: `solver.admissible_actions(...)`, then `solver.score(a, s, params)` for each action.

## 24. Design Decisions and Rationale

### 24.1 Why `f_i ∈ ⋂ S_i`, not `f_i = ⋂ S_i`?

The paper uses `∈` (membership) rather than `=` (equality) to signal that the candidate function is **one of potentially several** features common to viable solutions. This preserves the non-uniqueness that the paper emphasizes. The library honors this by:
- Exposing functions as an `Enum` you can extend.
- Accepting arbitrary weight vectors.
- Not hard-coding specific function-to-problem mappings.

### 24.2 Why not formal COH instantiation?

The paper says MCTEV is "methodologically aligned with, but not formally derived from" COH/GISMOL. `MCTEVSystem` is not a COH 9-tuple. This is **deliberate**: claiming formal derivation would require a rigorous proof the paper doesn't provide. The library honors this boundary.

### 24.3 Why empirical evaluation of the theorem?

The Constraint Violation Theorem is stated as a **theorem sketch** — not a fully rigorous proof — in the paper. The library implements the **empirical evaluation**: simulating many trajectories to estimate the survival function and exponential decay rate. This mirrors the paper's epistemic status: a claim you can test, not a claim you can assume.

### 24.4 Why grid-based viability kernels?

Full viability kernel computation is computationally expensive (exponential in state dimension). Grid-based approximation is a principled compromise: it produces an **approximate** viability kernel whose resolution is tunable. The paper's framework allows this — the specific computational method is a design choice, not a theoretical commitment.

### 24.5 Why four canonical cultural types?

The paper's Three Societies simulation uses four types (U, C, I, S). The library ships with these as examples. Real cultures can be represented by any weight vector — the four are illustrative, not exhaustive.

---

# Part VI — Advanced Topics

## 25. Integration with COH/GISMOL

The library is **methodologically aligned with, but not formally derived from** the [COH/GISMOL](https://github.com/hongxueharriswang/gismol-lib) research program.

### 25.1 What MCTEV shares with COH

- **Hierarchical organization**: both decompose complex phenomena into levels.
- **Constraint propagation**: constraints flow downward, adaptation flows upward.
- **Adaptive dynamics**: both admit learning and evolution within constraints.

### 25.2 What MCTEV does not do

- It does **not** implement the COH 9-tuple formalism.
- It does **not** import theorems from COH.
- It does **not** claim to be a formal instantiation.

### 25.3 The Ethical Constraint Hierarchy Principle

$$
\text{constraints} \xrightarrow{\text{downward}} \text{implementations} \xrightarrow{\text{downward}} \text{judgments}
$$

$$
\text{adaptation} \xrightarrow{\text{upward}} \text{implementations} \xrightarrow{\text{upward}} \text{functions}
$$

The library enforces this structurally: `MCTEVSystem` passes `cultural_params` down to `SituationalJudgment`, and `Agent.update_belief` provides upward adaptation in the simulation.

### 25.4 Full formal instantiation (future work)

A full formal instantiation would require:
1. Mapping each COH component (C, A, M, N, E, I, T, G, D) to MCTEV's ethical domain.
2. Proving the instantiation reproduces MCTEV's predictions.
3. Showing the Constraint Violation Theorem is preserved.

This is identified as future research in the paper (§18.2).

## 26. Numerical Considerations

### 26.1 Numerical integration

`Dynamics.step` uses forward Euler: `x_{t+1} = x_t + dt * F(x_t, θ_c)`. This is stable for `dt < 2 / ||A||` when \(F\) is linear. For default `A = -0.1·I`, this is stable for `dt < 20`.

### 26.2 Noise scale

`ConstraintViolationAnalyzer.noise_scale` defaults to `0.02`. This is a compromise:
- Too small: no trajectories exit even under constraint violation.
- Too large: viable trajectories also exit.

Recommended values: `0.01` (deterministic-leaning), `0.05` (noisy), `0.1` (very noisy).

### 26.3 Grid resolution

`ViabilityKernel.grid_size` defaults to 8 (per dimension), giving \(8^6 = 262{,}144\) grid points. For faster exploration:
- `grid_size=4`: \(4096\) points
- `grid_size=5`: \(15{,}625\) points
- `grid_size=6`: \(46{,}656\) points
- `grid_size=8`: \(262{,}144\) points

The viable fraction estimate becomes more accurate but slower as `grid_size` increases.

### 26.4 Horizon

`ViabilityKernel.horizon` defaults to 500. This is the number of Euler steps per probe point. Larger values are more accurate for slow dynamics but slower.

## 27. Performance and Scaling

### 27.1 Bottlenecks

| Operation | Complexity | Dominant factor |
|-----------|-----------|-----------------|
| Kernel computation | \(O(g^6 \cdot h)\) | Grid size, horizon |
| Collapse analysis | \(O(n \cdot h)\) | Number of trials, horizon |
| Three Societies | \(O(n \cdot r \cdot a)\) | Agents × rounds × actions |
| Situational judgment | \(O(a)\) | Number of actions |

### 27.2 Optimization tips

1. **Reduce grid size** for exploration; use larger only for final results.
2. **Parallelize** kernel computations across grid cells using `multiprocessing` or joblib.
3. **Cache** kernel computations if computing for many parameter vectors; cache is not built-in, but easy to add.
4. **Reduce horizon** for preliminary runs; increase for publication-quality.

### 27.3 Parallelization example

```python
from concurrent.futures import ProcessPoolExecutor
from mctev.viability.kernel import ViabilityKernel
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.core.cultural_params import CULTURAL_TYPES
import numpy as np

def compute_for_culture(name):
    kernel = ViabilityKernel(
        constraints=default_constraints(),
        dynamics=LinearDynamics(),
        params=CULTURAL_TYPES[name],
        grid_size=5,
        horizon=150,
    )
    kernel.build()
    return name, kernel.fraction_viable()

with ProcessPoolExecutor() as pool:
    results = dict(pool.map(compute_for_culture, CULTURAL_TYPES.keys()))
print(results)
```

---

# Part VII — Appendices

## 28. Theoretical Foundations: Key Equations

### 28.1 Situational judgment

$$
j(s; \theta_c) = \arg\max_{a \in \mathcal{A}}
\sum_{f \in \mathcal{F}} \theta_{c,f} \, u_f(a, s)
\quad \text{subject to} \quad a \in \mathcal{C}(s)
$$

### 28.2 Viability kernel

$$
\mathcal{R} = \text{Viab}(\mathcal{V}, F)
= \left\{\mathbf{x}_0 \in \mathcal{V} :
\exists \pi \text{ s.t. } \mathbf{x}(t) \in \mathcal{V} \; \forall t \geq 0\right\}
$$

### 28.3 Flourishing

$$
\mathcal{F} = \{\mathbf{x} : H(\mathbf{x}) \geq \tau_H\}
\subseteq \mathcal{R}
$$

### 28.4 Morality

$$
\text{Morality}(\theta_c)
= \text{Persistence}(\theta_c) \wedge \text{Flourishing}(\theta_c)
$$

### 28.5 Constraint Violation Theorem (empirical form)

$$
\mathbb{P}(\tau_{\text{exit}} > T) \leq C e^{-\lambda T}
$$

### 28.6 Cultural distance

$$
d(\theta_a, \theta_b) = \|\theta_a - \theta_b\|_2
$$

### 28.7 Convergence index

$$
\text{CI}(\{\theta_i\})
= \frac{1}{\binom{n}{2}} \sum_{i < j}
\frac{\langle \theta_i, \theta_j \rangle}
{\|\theta_i\| \cdot \|\theta_j\|}
$$

## 29. Glossary

| Term | Definition |
|------|-----------|
| **Level 1** | Candidate universal moral functions; functional requirements any enduring society must solve |
| **Level 2** | Cultural implementations; weight vectors over Level 1 functions |
| **Level 3** | Situational judgments; constrained optimization given cultural parameters |
| **Candidate function** | A proposed universal function; not uniquely determined |
| **Feasible moral region** | The viability kernel \(\mathcal{R}\) of social dynamics |
| **Viability kernel** | Set of states from which some policy keeps the system viable forever |
| **Flourishing** | Five-dimensional vector \((W, P, A, S, M)\) above thresholds |
| **Persistence** | Viability of a moral system; necessary but not sufficient for morality |
| **Constraint Violation Theorem** | Empirical claim that sustained constraint violations predict collapse |
| **Cultural parameters** | Weight vector \(\theta_c\) over Level 1 functions |
| **Ethical Constraint Hierarchy Principle** | Constraints propagate downward, adaptation propagates upward |
| **COH** | Constrained Object Hierarchies; the framework MCTEV is aligned with |
| **GISMOL** | General Intelligent System Modelling Language; toolkit for COH |

## 30. References

### Primary sources

- **Wang, H. (2026).** *Toward a Computational Science of Ethics: A Multi-Level Theory of Ethical Variation and Universal Moral Principles.* (Main paper.)
- **Wang, H. (2025).** Constrained object hierarchies as a unified theoretical model for intelligence and intelligent systems. *Computers*, *14*, 478. [doi:10.3390/computers14110478](https://doi.org/10.3390/computers14110478)
- **Wang, H. (2026).** GISMOL: A general intelligent systems modelling language.

### Viability theory

- **Aubin, J.-P. (1991).** *Viability Theory.* Birkhäuser.
- **Freidlin, M. I., & Wentzell, A. D. (2012).** *Random Perturbations of Dynamical Systems* (3rd ed.). Springer.

### Moral psychology

- **Awad, E., et al. (2018).** The Moral Machine experiment. *Nature*, *563*(7729), 59–64.
- **Atari, M., et al. (2023).** Morality beyond the WEIRD. *Journal of Personality and Social Psychology*.
- **Doğruyol, B., et al. (2019).** The five-factor model of the moral foundations theory is stable across WEIRD and non-WEIRD cultures. *Personality and Individual Differences*, *151*, 109547.
- **Haidt, J. (2001).** The emotional dog and its rational tail. *Psychological Review*, *108*(4), 814–834.

### Computational ethics

- **Bond, A. H. (2026).** Geometric ethics: A computational foundation for objective morality via topological optimization. *Zenodo*.
- **He, W. (2026).** An LLM-based agent simulation approach to study moral evolution. *ACL Anthology*.
- **Tennant, E., Hailes, S., & Musolesi, M. (2025).** Dynamics of moral behavior in heterogeneous populations of learning agents. *AAAI/ACM AIES*.

### AI alignment

- **Bai, Y., et al. (2022).** Constitutional AI: Harmlessness from AI feedback. *arXiv:2212.08073*.
- **Ouyang, L., et al. (2022).** Training language models to follow instructions with human feedback. *NeurIPS*, *35*.

### Foundational philosophy

- **Sen, A. (1999).** *Development as Freedom.* Oxford University Press.
- **Nussbaum, M. C. (2011).** *Creating Capabilities.* Harvard University Press.
- **Skyrms, B. (1996).** *Evolution of the Social Contract.* Cambridge University Press.
- **Alexander, R. D. (1987).** *The Biology of Moral Systems.* Aldine de Gruyter.

### Empirical work informing the framework

- **Yang, Y., & Ma, Z. (2026).** The Moral Foundations Questionnaire-1 short-form judgment section fails structural validation: Evidence from a 21-nation psychometric evaluation. *Collabra: Psychology*, *12*(1), 162286.

---

## Documentation License

This user guide is released under the same MIT license as `mctev-lib`. Corrections, extensions, and worked examples are welcome as pull requests.

## Getting Help

- **Bugs and feature requests**: open an issue on the project repository.
- **Theoretical questions**: consult the primary paper first; the API section (§22) provides pointers to the relevant paper sections.
- **Integration with other libraries**: see §25 for the COH/GISMOL connection and §27 for scaling considerations.

---

*End of User Guide.*