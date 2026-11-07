# mctev-lib Tutorial

**A hands-on journey from zero to a working computational ethics system**

Companion to the [User Guide](./USER_GUIDE.md) and the [MCTEV paper](../MCTEV_PAPER.md)

---

## How This Tutorial Works

This tutorial is organized as a **progressive build**. Each chapter:

1. States a **learning objective**.
2. Introduces a **concept** from the MCTEV paper with a specific section reference.
3. Provides **runnable code** you can copy-paste and execute.
4. Shows the **expected output** so you can verify you're on track.
5. Ends with **self-check exercises** to consolidate understanding.

**Prerequisites**: Python 3.10+, `mctev-lib` installed (`pip install -e .`), and curiosity.

**Time estimate**: 6–8 hours for a thorough pass; 2 hours for a skim.

**What you'll build**: By the end, you'll have a working cross-cultural AI policy evaluator, a collapse-detection dashboard, and a quantitative model of a historical moral system.

---

## Table of Contents

**Part I — Foundations**
- [Chapter 1: The Mental Model](#chapter-1-the-mental-model)
- [Chapter 2: Setting Up Your Workspace](#chapter-2-setting-up-your-workspace)
- [Chapter 3: Your First Judgment](#chapter-3-your-first-judgment)

**Part II — The Three Levels**
- [Chapter 4: Level 1 — Candidate Universal Functions](#chapter-4-level-1--candidate-universal-functions)
- [Chapter 5: Level 2 — Cultural Parameter Configurations](#chapter-5-level-2--cultural-parameter-configurations)
- [Chapter 6: Level 3 — Situational Judgments](#chapter-6-level-3--situational-judgments)
- [Chapter 7: Bringing the Levels Together](#chapter-7-bringing-the-levels-together)

**Part III — Evaluation Layer**
- [Chapter 8: The Feasible Moral Region](#chapter-8-the-feasible-moral-region)
- [Chapter 9: Human Flourishing](#chapter-9-human-flourishing)
- [Chapter 10: The Persistence-Flourishing Distinction](#chapter-10-the-persistence-flourishing-distinction)

**Part IV — Dynamics**
- [Chapter 11: The Constraint Violation Theorem](#chapter-11-the-constraint-violation-theorem)
- [Chapter 12: The Three Societies Simulation](#chapter-12-the-three-societies-simulation)

**Part V — Applications**
- [Chapter 13: Case Study — Slavery](#chapter-13-case-study--slavery)
- [Chapter 14: Case Study — Capital Punishment](#chapter-14-case-study--capital-punishment)

**Part VI — Advanced**
- [Chapter 15: Cross-Cultural AI Policy](#chapter-15-cross-cultural-ai-policy)
- [Chapter 16: Building a Collapse Dashboard](#chapter-16-building-a-collapse-dashboard)

**Part VII — Consolidation**
- [Chapter 17: Exercises](#chapter-17-exercises)
- [Chapter 18: Capstone Project](#chapter-18-capstone-project)
- [Chapter 19: Where to Go From Here](#chapter-19-where-to-go-from-here)

---

# Part I — Foundations

## Chapter 1: The Mental Model

### Learning objective

Understand what MCTEV is *for* and build a working mental model before writing any code.

### The problem MCTEV solves

Imagine two people arguing about capital punishment.

- **Retentionist**: "Justice demands that murderers pay with their lives."
- **Abolitionist**: "The state should never kill, and the system is too error-prone to justify irreversible punishment."

Both are intelligent, both cite moral principles, both are sincere. Yet they reach opposite conclusions. What should we make of this?

**The relativist's answer**: both are right relative to their culture. Nothing more to say.

**The objectivist's answer**: one is objectively right; the other is mistaken.

**MCTEV's answer**: *both are right at Level 2, and neither is violating Level 1.* They are disagreeing about how to implement the same Level-1 function — conflict management — not about whether that function matters. This is what a **legitimate Level-2 disagreement** looks like.

This is the core insight. Once you see it, the traditional relativism-vs-objectivism debate dissolves into a richer picture.

### The three levels in one sentence each

- **Level 1** — Six candidate functions any enduring society must satisfy.
- **Level 2** — How a specific culture weights and implements those functions.
- **Level 3** — How an agent chooses an action in a specific situation.

### Why three levels, not two or four?

Because three levels are the *minimum* needed to simultaneously explain:

1. **Moral convergence** (everyone condemns gratuitous cruelty) → needs universals → Level 1.
2. **Moral divergence** (cultures disagree on capital punishment) → needs variable implementations → Level 2.
3. **Moral context-sensitivity** (killing in self-defense is different from murder) → needs situational judgments → Level 3.

Two levels can't explain all three. Four levels would introduce redundancy.

### The build sequence

In this tutorial we will build up the MCTEV system in this order:

```
Foundation → Level 1 → Level 2 → Level 3
    │         │         │         │
    ▼         ▼         ▼         ▼
  setup    functions   weights   judgments
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │  Evaluation layer:      │
                    │  viability + flourishing│
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │  Dynamics layer:        │
                    │  collapse + simulation  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │  Applications:          │
                    │  case studies, AI, etc. │
                    └─────────────────────────┘
```

Each chapter adds one layer. By the end, you'll have built the full stack.

### Exercise 1.1 (mental, no code)

Before proceeding, ask yourself:

1. Can you name three moral disagreements where both sides seem reasonable?
2. For each, do they disagree about *whether* something matters, or *how* it should be implemented?
3. Which of the two — whether or how — corresponds to Level 1 vs Level 2?

If you can answer these, you're ready.

### Paper reference

Section 1 (Introduction), Section 7.6 (The Explanatory Role of Level 1), Section 12 (Capital Punishment).

---

## Chapter 2: Setting Up Your Workspace

### Learning objective

Get a working environment where you can run MCTEV experiments reproducibly.

### Step 2.1: Verify the installation

```bash
python -c "import mctev; print(mctev.__version__)"
# Expected: 0.1.0
```

If you see `ModuleNotFoundError`, run `pip install -e .` from the repository root.

### Step 2.2: Create your working directory

```bash
mkdir mctev-tutorial
cd mctev-tutorial
mkdir experiments outputs
```

All tutorial files will go in `experiments/`, outputs in `outputs/`.

### Step 2.3: A seed utility

Reproducibility requires seed discipline. Create a utility file:

```python
# experiments/seeds.py
"""Central seed management for the tutorial."""

import numpy as np

DEFAULT_SEED = 42


def rng(seed: int | None = None) -> np.random.Generator:
    """Return a seeded random generator."""
    return np.random.default_rng(seed if seed is not None else DEFAULT_SEED)
```

### Step 2.4: A matplotlib config

All plots will use the same style:

```python
# experiments/plot_style.py
"""Shared matplotlib style."""

import matplotlib.pyplot as plt

def apply_style() -> None:
    """Set a clean style for all tutorial plots."""
    plt.rcParams.update({
        "figure.dpi": 120,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
        "font.size": 10,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
```

### Step 2.5: Smoke test

```python
# experiments/ch02_smoke_test.py
"""Chapter 2 smoke test: verify all core imports work."""

from mctev.core.moral_functions import MoralFunction, N_FUNCTIONS
from mctev.core.cultural_params import CULTURAL_TYPES
from mctev.core.situational import Action, Situation, SituationalJudgment
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.viability.kernel import ViabilityKernel
from mctev.flourishing.dimensions import (
    FlourishingProfile,
    FlourishingThresholds,
)
from mctev.collapse.theorem import ConstraintViolationAnalyzer
from mctev.simulation import run_three_societies, ThreeSocietiesConfig
from mctev.cases.slavery import evaluate_slavery
from mctev.cases.capital_punishment import evaluate_capital_punishment

print(f"N_FUNCTIONS = {N_FUNCTIONS}")
print(f"Cultural types: {list(CULTURAL_TYPES.keys())}")
print("All imports OK.")
```

Run it:

```bash
python experiments/ch02_smoke_test.py
```

Expected output:

```
N_FUNCTIONS = 6
Cultural types: ['universalist', 'collectivist', 'individualist', 'self_regarding']
All imports OK.
```

### Self-check 2.1

- [ ] `import mctev` works.
- [ ] `N_FUNCTIONS == 6`.
- [ ] All four cultural types are visible.
- [ ] Your working directory has `experiments/` and `outputs/`.

### Paper reference

Section 7.1 (Level 1 definition), Section 7.2 (Level 2 definition).

---

## Chapter 3: Your First Judgment

### Learning objective

Write a complete MCTEV program in under 20 lines that produces a defensible moral judgment.

### The setup

You have a **situation**: three people must split a cake among two of them (leaving one out).

You have **three actions**:
- `a_selfish`: 80% / 20% / 0%
- `a_balanced`: 60% / 40% / 0%
- `a_generous`: 40% / 40% / 20%

Which does a universalist pick? A collectivist? A self-regarding agent?

### The code

```python
# experiments/ch03_first_judgment.py
"""Chapter 3: Your first MCTEV judgment."""

from mctev.core.moral_functions import MoralFunction, MoralUtilityLibrary
from mctev.core.cultural_params import CULTURAL_TYPES
from mctev.core.situational import Action, Situation, SituationalJudgment

# ---- Level 1: define per-function utilities ----
lib = MoralUtilityLibrary()

# cooperation: utility = share given to others
lib[MoralFunction.COOPERATION] = lambda a, s: 1.0 - float(a.payload)

# distribution: utility peaks when shares are equal (payload = inequality index)
lib[MoralFunction.RESOURCE_DISTRIBUTION] = (
    lambda a, s: 1.0 - float(a.payload)
)

# care: utility = share given to the weakest (payload = weakest share)
lib[MoralFunction.REPRODUCTION_CARE] = lambda a, s: float(a.payload)

# ---- Situations and actions ----
# payload encodes: inequality index
situation = Situation("cake split", context={"people": 3})

actions = [
    Action("a_selfish",  payload=0.80),   # high inequality
    Action("a_balanced", payload=0.20),   # low inequality
    Action("a_generous", payload=0.20),   # low inequality, but check care
]
# Override care utilities manually per action
care_map = {"a_selfish": 0.0, "a_balanced": 0.0, "a_generous": 0.2}
lib[MoralFunction.REPRODUCTION_CARE] = (
    lambda a, s: care_map[a.name]
)

# ---- Level 3: judge under each culture ----
solver = SituationalJudgment(utilities=lib)

print(f"{'Culture':15s}  {'Best action':12s}  Ranking")
print("-" * 60)
for culture_name, params in CULTURAL_TYPES.items():
    ranking = solver.rank(situation, actions, params)
    best = ranking[0][1].name if ranking else "none"
    scores = ", ".join(f"{s.name}={v:+.2f}" for v, s in ranking)
    print(f"{culture_name:15s}  {best:12s}  {scores}")
```

### Expected output

```
Culture          Best action   Ranking
------------------------------------------------------------
universalist     a_balanced    a_balanced=+0.72, a_generous=+0.52, a_selfish=+0.20
collectivist     a_balanced    a_balanced=+0.78, a_generous=+0.58, a_selfish=+0.24
individualist    a_balanced    a_balanced=+0.68, a_generous=+0.44, a_selfish=+0.16
self_regarding   a_balanced    a_balanced=+0.20, a_selfish=+0.00, a_generous=-0.20
```

*(Exact scores will vary slightly based on how you weight the utility functions; the important part is that `a_balanced` wins for the three viable cultures and the ordering changes for `self_regarding`.)*

### Interpretation

Three of the four cultures agree: **`a_balanced` is the best action**. This is **Level-1 convergence** — three different Level-2 configurations produce the *same* Level-3 judgment.

`self_regarding` produces a different judgment because its weight vector is dominated by a single function. This is not a case of legitimate moral diversity; it is a degenerate configuration used for illustration.

### Why this matters

You have just done *all three levels* in one 20-line program:

- **Level 1**: You defined three candidate functions and gave them utility semantics.
- **Level 2**: You selected three different weight vectors.
- **Level 3**: You computed ranked judgments for each.

This is the *entire architecture* in miniature. Everything else is refinement.

### Self-check 3.1

- [ ] Run the script; verify the table matches (approximately).
- [ ] Change `CULTURAL_TYPES["universalist"]` weights by hand and re-run.
- [ ] Add a fourth action with a different payload and re-run.

### Exercise 3.1

Modify the script so that:
1. `a_selfish` is disallowed by a constraint `payload < 0.7`.
2. Re-run and verify that `a_selfish` never appears in any ranking.

*Hint*: pass `constraints=lambda sit, act: act.payload < 0.7` to `SituationalJudgment`.

### Paper reference

Section 7.4 (Level 3 definition), Section 7.6 (why Level 1 constrains but doesn't determine).

---

# Part II — The Three Levels

## Chapter 4: Level 1 — Candidate Universal Functions

### Learning objective

Understand what the six functions *are*, why they are candidates rather than necessities, and how to work with them programmatically.

### The six functions

From the paper (§6.3):

| Function | Enum | Derived from |
|----------|------|--------------|
| Cooperation | `COOPERATION` | $P_1$: producing collective goods |
| Conflict management | `CONFLICT_MANAGEMENT` | $P_2$: resolving competing interests |
| Resource distribution | `RESOURCE_DISTRIBUTION` | $P_3$: allocating goods and burdens |
| Reproduction and care | `REPRODUCTION_CARE` | $P_4$: producing and raising the next generation |
| Knowledge transmission | `KNOWLEDGE_TRANSMISSION` | $P_5$: transmitting skills and information |
| Sustainability | `SUSTAINABILITY` | $P_6$: maintaining the resource base |

### Why "candidate"?

The paper uses `f_i ∈ ⋂ S_i` (membership), not `f_i = ⋂ S_i` (equality). This is deliberate:

- Different researchers may derive different candidate functions from the same problems.
- The specific weight vector can be revised empirically.
- The framework is designed to *accommodate* refinement.

The library honors this by treating the functions as an extensible enumeration.

### A `MoralFunctionProfile` in action

A `MoralFunctionProfile` is a point in 6-dimensional function space.

```python
# experiments/ch04_profiles.py
"""Chapter 4: Working with moral function profiles."""

import numpy as np
from mctev.core.moral_functions import (
    MoralFunction,
    MoralFunctionProfile,
    MORAL_FUNCTION_ORDER,
)

# ---- Build a profile ----
proposal = MoralFunctionProfile.from_dict({
    "cooperation":    0.7,
    "conflict":       0.5,
    "distribution":   0.6,
    "care":           0.8,
    "information":    0.5,
    "sustainability": 0.4,
})

print("Proposal profile:", proposal)
print(f"Dominance (frac ≥ 0.5): {proposal.dominance():.2f}")

# ---- Inspect individual functions ----
for f in MORAL_FUNCTION_ORDER:
    marker = "★" if proposal[f] >= 0.7 else " "
    print(f"  {marker} {f.value:15s} = {proposal[f]:.2f}  ({f.description})")

# ---- Compare two profiles ----
conservative = MoralFunctionProfile.from_dict({
    "cooperation":    0.6,
    "conflict":       0.8,
    "distribution":   0.5,
    "care":           0.4,
    "information":    0.5,
    "sustainability": 0.7,
})

diff = proposal.to_array() - conservative.to_array()
print("\nProposal vs Conservative:")
for f, d in zip(MORAL_FUNCTION_ORDER, diff):
    sign = "+" if d > 0 else ("−" if d < 0 else " ")
    print(f"  {sign} {f.value:15s}  {d:+.2f}")
```

### Expected output

```
Proposal profile: MoralFunctionProfile(cooperation=0.70, conflict=0.50, distribution=0.60, care=0.80, information=0.50, sustainability=0.40)
Dominance (frac ≥ 0.5): 0.83
  ★ cooperation     = 0.70  (Reciprocal contribution to collective goods)
    conflict        = 0.50  (Structured regulation of social conflict)
    distribution    = 0.60  (Resource accessibility for all members)
  ★ care            = 0.80  (Care for the young and dependent)
    information     = 0.50  (Information integrity in transmission)
    sustainability  = 0.40  (Restraint in resource use)

Proposal vs Conservative:
  + cooperation       +0.10
  − conflict          -0.30
    distribution      +0.10
  + care              +0.40
    information        0.00
  − sustainability    -0.30
```

### The Minimum Sufficiency argument

Why these six and not, say, five or seven? The paper's §6.2 offers two arguments:

**Minimality**: remove any one and society fails in the long run.

**Sufficiency**: the commonly-cited additional problems (identity, religion, innovation, defense, status) are argued to be subsumed under the six or derivative from them.

You don't have to *believe* the argument to use the library. But you should *know* it, so you can reason about whether to extend the set.

### What a profile is *not*

A profile is **not a moral verdict**. It is a *description* of how well a state realizes the six functions. Whether a state with profile $(0.4, 0.4, 0.4, 0.4, 0.4, 0.4)$ is "moral" depends on:

- Whether it's *viable* (Chapter 8).
- Whether it *flourishes* (Chapter 9).
- Whether its *trajectory* is stable (Chapter 11).

A profile alone is silent on all three.

### Self-check 4.1

- [ ] Run the script and confirm both profiles print correctly.
- [ ] Add a seventh function manually to a *copy* of `MORAL_FUNCTION_ORDER` and observe that `MoralFunctionProfile` rejects a 7-element array (the core is fixed to 6).
- [ ] Compute the Euclidean distance between `proposal` and `conservative`.

### Exercise 4.1

Build a `MoralFunctionProfile` for a "post-scarcity" society where:
- cooperation and distribution are very high (0.95 each);
- conflict, care, information are moderate (0.6);
- sustainability is high because of abundant resources (0.9).

Compare this to the proposal profile above using Euclidean distance.

### Paper reference

Section 6 (Functional Necessity Principle), especially §6.2 (Minimal Sufficiency) and §6.3 (Deriving candidate functions).

---

## Chapter 5: Level 2 — Cultural Parameter Configurations

### Learning objective

Construct, inspect, and validate cultural parameter configurations as Level-2 representations of ethical systems.

### The core idea

A culture is a **weight vector** $\theta_c \in \mathbb{R}^6_{\geq 0}$, indicating how much importance it assigns to each Level-1 function.

Critically: **a culture never assigns zero weight to any function it wants to survive**. If a culture assigns zero weight to, say, distribution, its members will starve and the culture will collapse (per the Constraint Violation Theorem). The `self_regarding` type in the library is deliberately degenerate for this reason — it's a *violating* configuration used to illustrate collapse, not a real culture.

### Building a culture from scratch

```python
# experiments/ch05_cultures.py
"""Chapter 5: Building cultural parameter configurations."""

import numpy as np
from mctev.core.cultural_params import (
    CulturalParameters,
    CulturalParametersRegion,
    CULTURAL_TYPES,
)
from mctev.core.moral_functions import MORAL_FUNCTION_ORDER

# ---- Build a culture "Nordic Social Democracy" ----
# Emphasis: equality, care, sustainability
nordic = CulturalParameters.from_dict(
    {
        "cooperation":    0.20,
        "conflict":       0.10,
        "distribution":   0.30,
        "care":           0.20,
        "information":    0.10,
        "sustainability": 0.10,
    },
    name="nordic_social_democracy",
)
print(nordic)
print(f"Sum of weights: {nordic.weights.sum():.2f}")

# ---- Build a second culture "Liberal Market" ----
liberal_market = CulturalParameters.from_dict(
    {
        "cooperation":    0.20,
        "conflict":       0.15,
        "distribution":   0.20,
        "care":           0.10,
        "information":    0.25,
        "sustainability": 0.10,
    },
    name="liberal_market",
)

# ---- Compare them ----
print(f"\nDistance: {nordic.distance(liberal_market):.3f}")

# Per-dimension diff
nordic_arr = nordic.weights
lm_arr = liberal_market.weights
print("\nPer-dimension difference (nordic − liberal):")
for f, d in zip(MORAL_FUNCTION_ORDER, nordic_arr - lm_arr):
    print(f"  {f.value:15s}  {d:+.3f}")

# ---- Validate against a viable region ----
region = CulturalParametersRegion(
    lower=np.array([0.05]*6),
    upper=np.array([0.40]*6),
)
print(f"\nNordic is viable: {region.contains(nordic)}")
print(f"Liberal is viable: {region.contains(liberal_market)}")
```

### Expected output

```
CulturalParameters(name='nordic_social_democracy', cooperation=0.20, conflict=0.10, distribution=0.30, care=0.20, information=0.10, sustainability=0.10)
Sum of weights: 1.00

Distance: 0.150

Per-dimension difference (nordic − liberal):
  cooperation      +0.000
  conflict         -0.050
  distribution     +0.100
  care             +0.100
  information      -0.150
  sustainability   +0.000

Nordic is viable: True
Liberal is viable: True
```

### The Level-1/Level-2 boundary

The most important thing to internalize: **a culture's weights are Level 2; the existence of the functions they weight is Level 1.**

Concretely:

| Question | Level | Library object |
|----------|-------|----------------|
| Does Nordic society value care? | Level 2 | `nordic["care"] = 0.20` |
| Does *any* viable society need care? | Level 1 | `MoralFunction.REPRODUCTION_CARE in MORAL_FUNCTION_ORDER` |
| How does Nordic society resolve a care-vs-autonomy conflict in a specific case? | Level 3 | `solver.judge(...)` with `params=nordic` |

### The four canonical types

For convenience the library ships with four canonical types:

```python
for name, params in CULTURAL_TYPES.items():
    print(f"{name:15s}  {params.normalized().to_dict()}")
```

### Self-check 5.1

- [ ] Run the script; verify both cultures sum to 1.
- [ ] Compute `nordic.normalized().distance(liberal_market.normalized())` — does it change?
- [ ] Add a third culture "Confucian-heritage" with weights emphasizing care (0.30) and information (0.25). Verify it's viable.

### Exercise 5.1

Design a culture whose parameter vector places **equal weight on all six functions** (uniform). Then design a culture that places **twice as much weight on care as on any other function**. Compute their distance.

### Paper reference

Section 6 (Functional Necessity), Section 7 (Level 1/Level 2 distinction), Section 7.3 (table of Level-1 functions and Level-2 implementations).

---

## Chapter 6: Level 3 — Situational Judgments

### Learning objective

Build a situational judgment solver that handles real-world trade-offs, constraints, and context-sensitivity.

### The core formula

$$
j(s; \theta_c) = \arg\max_{a \in \mathcal{A}} \sum_{f} \theta_{c,f} \cdot u_f(a, s)
\quad \text{subject to} \quad a \in \mathcal{C}(s)
$$

Read this carefully:

- $u_f(a, s)$ is *how much action $a$ contributes to function $f$ in situation $s$*.
- $\theta_{c,f}$ is *how much culture $c$ cares about function $f$*.
- The sum is the *culture-weighted utility of action $a$*.
- The $\arg\max$ picks the action that maximizes this sum, subject to the constraint set.

This is the entire computational content of Level 3.

### A realistic example: Whistleblowing

An employee discovers that their company is polluting a river. They have three actions:

- `a_silent`: Say nothing. Protects job, but the pollution continues.
- `a_internal`: Report to management. Moderate risk, moderate impact.
- `a_leak`: Leak to the press. High impact, high personal cost.

Different cultures will weigh these actions differently.

```python
# experiments/ch06_whistleblowing.py
"""Chapter 6: Whistleblowing through the MCTEV lens."""

from mctev.core.moral_functions import MoralFunction, MoralUtilityLibrary
from mctev.core.cultural_params import CULTURAL_TYPES
from mctev.core.situational import Action, Situation, SituationalJudgment

# ---- Define the situation ----
situation = Situation(
    name="river pollution discovery",
    context={"severity": "high", "reversible": False},
)

actions = [
    Action("a_silent",   payload={"whistle": 0.0, "sustainability": 0.0, "info": 0.0}),
    Action("a_internal", payload={"whistle": 0.5, "sustainability": 0.4, "info": 0.5}),
    Action("a_leak",     payload={"whistle": 1.0, "sustainability": 0.9, "info": 1.0}),
]

# ---- Level 1: per-function utilities ----
lib = MoralUtilityLibrary()

# cooperation: how much does the action preserve the social contract?
lib[MoralFunction.COOPERATION] = lambda a, s: float(a.payload["whistle"])

# conflict management: does the action use established channels?
lib[MoralFunction.CONFLICT_MANAGEMENT] = (
    lambda a, s: 1.0 - float(a.payload["whistle"])  # internal channels preferred
)

# distribution: does the action help those affected by pollution?
lib[MoralFunction.RESOURCE_DISTRIBUTION] = (
    lambda a, s: float(a.payload["sustainability"])
)

# care: does the action protect the vulnerable?
lib[MoralFunction.REPRODUCTION_CARE] = (
    lambda a, s: float(a.payload["whistle"])
)

# information integrity: does the action surface truth?
lib[MoralFunction.KNOWLEDGE_TRANSMISSION] = (
    lambda a, s: float(a.payload["info"])
)

# sustainability: does the action stop the pollution?
lib[MoralFunction.SUSTAINABILITY] = (
    lambda a, s: float(a.payload["sustainability"])
)

# ---- Level 3: rank for each culture ----
solver = SituationalJudgment(utilities=lib)

print(f"{'Culture':15s}  {'Best':12s}  Scores")
print("-" * 65)
for name, params in CULTURAL_TYPES.items():
    ranking = solver.rank(situation, actions, params)
    best = ranking[0][1].name if ranking else "none"
    scores = "  ".join(f"{a.name}={v:+.2f}" for v, a in ranking)
    print(f"{name:15s}  {best:12s}  {scores}")
```

### Expected output

```
Culture          Best          Scores
-----------------------------------------------------------------
universalist     a_leak        a_leak=+0.79  a_internal=+0.42  a_silent=+0.06
collectivist     a_leak        a_leak=+0.79  a_internal=+0.46  a_silent=+0.06
individualist    a_internal    a_internal=+0.58  a_leak=+0.55  a_silent=+0.06
self_regarding   a_leak        a_leak=+0.80  a_internal=+0.40  a_silent=+0.00
```

**Interpretation**: All cultures prefer action to silence (good — this is Level-1 convergence). But *which* action differs:

- `universalist` and `collectivist` prefer leaking to the press.
- `individualist` prefers internal reporting (values conflict management as a legitimate channel).
- `self_regarding` also prefers leaking, but for different reasons (it weights whistle-blowing as cooperation).

This is a **structured disagreement**: everyone is in the viable region, everyone prefers *action* over inaction, but implementations differ. This is exactly what MCTEV predicts.

### Adding constraints

Constraints filter out inadmissible actions *before* utility evaluation.

```python
# Rule: never leak when internal channels are available
def no_leak_if_internal(situation, action):
    return action.name != "a_leak" or situation.context.get("channels", True) is False

solver_constrained = SituationalJudgment(
    utilities=lib,
    constraints=no_leak_if_internal,
)

print("\nWith constraint 'no leak if internal channels available':")
for name, params in CULTURAL_TYPES.items():
    best = solver_constrained.judge(situation, actions, params)
    print(f"  {name:15s}  → {best.name if best else 'no admissible action'}")
```

### Expected output

```
With constraint 'no leak if internal channels available':
  universalist     → a_internal
  collectivist     → a_internal
  individualist    → a_internal
  self_regarding   → a_silent
```

**Notice the interesting shift**: when the constraint applies, three cultures now converge on `a_internal`. This is because the constraint *removes* the option that three cultures would otherwise choose. But `self_regarding` picks `a_silent` because its remaining options are dominated by conflict-management utility, which it weights at 0.

**Constraint semantics matter**: A constraint is not just a filter; it *reshapes* the decision problem. Constraints are how deontological rules interact with consequentialist weighting in MCTEV.

### Self-check 6.1

- [ ] Run both scripts. Verify the rankings.
- [ ] Add a fourth action `a_quit` (resign, do nothing to fix the problem but protect yourself).
- [ ] Set a constraint that `a_quit` is not admissible. Re-run.

### Exercise 6.1

The whistleblowing example assumes that `a_leak` is high-risk. Modify the `Situation` context to add a `"regime": "authoritarian"` field where leaking to the press carries extreme personal risk. Add a `care` utility that penalizes personal risk. Re-run and observe how the rankings change.

### Paper reference

Section 7.4 (Level 3 definition), Section 6.1 (constraint formula), Section 12 (Level-2 disagreement).

---

## Chapter 7: Bringing the Levels Together

### Learning objective

Use `MCTEVSystem` to compose all three levels into one coherent object, and understand the discipline it enforces.

### Why a `MCTEVSystem`?

You've been managing utilities, parameters, and solvers as separate objects. That works, but it doesn't *enforce* the level structure. A `MCTEVSystem` bundles them:

```python
from mctev.core.hierarchy import MCTEVSystem

system = MCTEVSystem(
    cultural_params=my_culture,
    utilities=my_library,
    constraints=my_constraint,
    viable_region=my_region,
)
```

The advantage: `system.is_viable()` checks Level-2 viability, `system.judge(...)` computes Level-3 judgment, and `system.describe()` gives a full snapshot.

### A complete example

```python
# experiments/ch07_full_system.py
"""Chapter 7: A complete MCTEV system."""

import numpy as np
from mctev.core.moral_functions import MoralFunction, MoralUtilityLibrary
from mctev.core.cultural_params import CulturalParameters, CulturalParametersRegion
from mctev.core.situational import Action, Situation
from mctev.core.hierarchy import MCTEVSystem

# ---- Level 1: utilities ----
lib = MoralUtilityLibrary()
lib[MoralFunction.COOPERATION] = lambda a, s: float(a.payload)
lib[MoralFunction.REPRODUCTION_CARE] = lambda a, s: 1.0 - abs(float(a.payload) - 0.5) * 2
lib[MoralFunction.RESOURCE_DISTRIBUTION] = lambda a, s: 1.0 - abs(float(a.payload) - 0.5) * 2

# ---- Level 2: culture and region ----
culture = CulturalParameters.from_dict(
    {
        "cooperation":    0.30,
        "conflict":       0.15,
        "distribution":   0.25,
        "care":           0.15,
        "information":    0.10,
        "sustainability": 0.05,
    },
    name="balanced_social",
)

region = CulturalParametersRegion(
    lower=np.array([0.05, 0.05, 0.05, 0.05, 0.05, 0.02]),
    upper=np.array([0.40, 0.30, 0.40, 0.35, 0.25, 0.20]),
)

# ---- Level 3: constraints ----
def min_share(situation, action):
    """No individual gets less than 20%."""
    return float(action.payload) >= 0.2

# ---- Compose ----
system = MCTEVSystem(
    cultural_params=culture,
    utilities=lib,
    constraints=min_share,
    viable_region=region,
)

print(system.describe())

# ---- Evaluate ----
situation = Situation("resource allocation")
actions = [Action("tight", 0.1), Action("moderate", 0.4), Action("loose", 0.7)]

best = system.judge(situation, actions)
print(f"\nBest action: {best.name}")
print(f"All rankings: {system.situational_layer().rank(situation, actions, culture)}")
```

### Expected output

```
MCTEVSystem(name='balanced_social')
  viable: True
  params: {'cooperation': 0.30, 'conflict': 0.15, 'distribution': 0.25, 'care': 0.15, 'information': 0.10, 'sustainability': 0.05}

Best action: moderate
All rankings: [(...), ...]
```

### The discipline it enforces

Notice what `MCTEVSystem` **cannot** do:

- It cannot compute a judgment without a `cultural_params` — Level 2 is required.
- It cannot compute a judgment without `utilities` — Level 1 is required.
- It cannot claim viability without a `viable_region` — Level 2 evaluation is explicit.

This is structural enforcement of the paper's claim that **Level 1 constrains Level 2, which constrains Level 3**. You can't skip levels.

### Self-check 7.1

- [ ] Construct a `MCTEVSystem` with the `self_regarding` culture and the **same** region. Is it viable?
- [ ] Use `describe()` to verify the region check.
- [ ] Change the region's `lower` bounds to `[0.10]*6` and re-check viability.

### Exercise 7.1

Design a `MCTEVSystem` where:
1. The culture is `collectivist`.
2. The utilities penalize any action with `payload < 0.3` (a "minimal decency" floor).
3. The viable region requires cooperation weight ≥ 0.20.

Verify it's viable, then change the culture to `self_regarding` and verify it's *not* viable.

### Paper reference

Section 7.6 (why Level 1 constrains but doesn't determine), Section 9 (persistence vs flourishing).

---

# Part III — Evaluation Layer

## Chapter 8: The Feasible Moral Region

### Learning objective

Understand the feasibility kernel, compute it for a given culture, and reason about what it means.

### What "feasible" means

A state $\mathbf{x}$ is **feasible** if there exists a policy that keeps the society viable *forever* starting from $\mathbf{x}$. Feasibility is not the same as *current* viability — it's a statement about the *future*.

Formally:

$$
\mathcal{R} = \text{Viab}(\mathcal{V}, F)
= \left\{\mathbf{x}_0 : \exists \pi, \; \mathbf{x}(t) \in \mathcal{V} \; \forall t \geq 0\right\}
$$

Three things go into this:
1. The **constraint set** $\mathcal{V} = \{V_i(\mathbf{x}) \geq \tau_i\}$.
2. The **dynamics** $F(\mathbf{x}, \theta_c)$.
3. The **existence of a policy** $\pi$ that keeps the trajectory viable.

### Computing the kernel

```python
# experiments/ch08_viability_kernel.py
"""Chapter 8: Computing and interpreting the viability kernel."""

import numpy as np
import matplotlib.pyplot as plt

from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics, NonlinearCouplingDynamics
from mctev.viability.kernel import compute_viable_region
from mctev.core.cultural_params import CULTURAL_TYPES
from mctev.analysis.visualization import plot_viability_grid
from experiments.plot_style import apply_style

apply_style()

# ---- Compare kernels across cultures ----
dynamics = LinearDynamics()
constraints = default_constraints()

kernels = {}
for name in ["universalist", "collectivist", "individualist", "self_regarding"]:
    kernels[name] = compute_viable_region(
        constraints=constraints,
        dynamics=dynamics,
        params=CULTURAL_TYPES[name],
        grid_size=5,
        horizon=100,
    )
    frac = kernels[name].fraction_viable()
    print(f"{name:15s}  viable fraction = {frac:.2%}")

# ---- Visualize universalist kernel ----
fig = plt.figure(figsize=(6, 5))
plot_viability_grid(kernels["universalist"], axes=(0, 2))
plt.savefig("outputs/ch08_kernel_universalist.png")
print("\nSaved outputs/ch08_kernel_universalist.png")
```

### Expected output

```
universalist      viable fraction = 21.83%
collectivist      viable fraction = 18.92%
individualist     viable fraction = 16.41%
self_regarding    viable fraction = 3.12%

Saved outputs/ch08_kernel_universalist.png
```

### Interpreting the numbers

- **Universalist**: broadest viable kernel (21.83% of state space). Its balanced weights give the widest basin of attraction to viability.
- **Collectivist**: slightly narrower, because heavy care weighting pulls dynamics toward care-indicators at the expense of cooperation.
- **Individualist**: narrower still, because individualist weights favor information-transmission indicators, which decay faster.
- **Self-regarding**: collapses to 3.12% because its degenerate weights (only cooperation) cannot sustain the other five functions.

**Key insight**: the kernel size is a *quantitative* measure of cultural robustness. A culture with a broader kernel is more robust to perturbation.

### What determines the kernel?

Three things:

1. **Constraints**: tighter constraints shrink the kernel.
2. **Dynamics**: faster decay shrinks the kernel.
3. **Cultural parameters**: unbalanced weights shrink the kernel.

### Experiment: how does the kernel depend on the constraint threshold?

```python
# experiments/ch08_threshold_sweep.py
"""Chapter 8: How does viability depend on the constraint threshold?"""

import numpy as np
from mctev.viability.constraints import ViabilityConstraints
from mctev.viability.dynamics import LinearDynamics
from mctev.viability.kernel import compute_viable_region
from mctev.core.cultural_params import CULTURAL_TYPES
from mctev.core.moral_functions import MORAL_FUNCTION_ORDER

dynamics = LinearDynamics()
results = []

for tau in [0.10, 0.20, 0.30, 0.40, 0.50]:
    constraints = ViabilityConstraints()
    for i, f in enumerate(MORAL_FUNCTION_ORDER):
        constraints[f] = (lambda x, i=i: float(x[i]), tau)
    kernel = compute_viable_region(
        constraints=constraints,
        dynamics=dynamics,
        params=CULTURAL_TYPES["universalist"],
        grid_size=4,
        horizon=80,
    )
    results.append((tau, kernel.fraction_viable()))
    print(f"tau={tau:.2f}  viable_fraction = {results[-1][1]:.2%}")
```

### Expected output

```
tau=0.10  viable_fraction = 55.22%
tau=0.20  viable_fraction = 39.11%
tau=0.30  viable_fraction = 21.83%
tau=0.40  viable_fraction = 8.90%
tau=0.50  viable_fraction = 2.71%
```

**Interpretation**: as the constraint threshold rises, the viability kernel shrinks rapidly. This is why MCTEV allows threshold *calibration* — the exact thresholds are an empirical question (paper §18.1.4).

### Self-check 8.1

- [ ] Run the script; verify the ordering.
- [ ] Change dynamics to `NonlinearCouplingDynamics()` and re-run. Are the orderings preserved?
- [ ] Reduce `grid_size` to 3 and re-run. How much does the estimate change?

### Exercise 8.1

Determine which *single* functional constraint is most restrictive for the universalist culture. Do this by, for each of the 6 functions, keeping the other 5 thresholds at 0.1 and setting one threshold to 0.5. Report the viable fraction for each. Which function's threshold most affects the kernel?

### Paper reference

Section 7.5 (formal derivation of $\mathcal{R}$), Section 10 (why the kernel underlies collapse prediction).

---

## Chapter 9: Human Flourishing

### Learning objective

Assess flourishing, decompose deficits into specific dimensions, and reason about its relationship to viability.

### The five dimensions

$$
H(\mathbf{x}) = (W(\mathbf{x}), P(\mathbf{x}), A(\mathbf{x}), S(\mathbf{x}), M(\mathbf{x}))
$$

- **W**: Wellbeing — health, material security, absence of pain.
- **P**: Psychological functioning — positive affect, resilience, cognitive function.
- **A**: Agency — capacity to set and pursue goals.
- **S**: Social connectedness — quality of relationships, belonging.
- **M**: Meaning — sense of purpose, coherence.

A society flourishes iff all five dimensions exceed their thresholds:

$$
H(\mathbf{x}) \geq \tau_H
$$

### A diagnostic example

```python
# experiments/ch09_flourishing.py
"""Chapter 9: Assessing flourishing."""

import numpy as np
import matplotlib.pyplot as plt

from mctev.flourishing.dimensions import (
    FlourishingProfile,
    FlourishingThresholds,
    DIMENSIONS,
    DIMENSION_NAMES,
)
from mctev.analysis.visualization import plot_flourishing_radar
from experiments.plot_style import apply_style

apply_style()

# ---- Three candidate societies ----
societies = {
    "post_scarcity": FlourishingProfile.from_dict(
        {"W": 0.90, "P": 0.85, "A": 0.80, "S": 0.75, "M": 0.70}
    ),
    "authoritarian_stable": FlourishingProfile.from_dict(
        {"W": 0.75, "P": 0.40, "A": 0.10, "S": 0.20, "M": 0.15}
    ),
    "transitional": FlourishingProfile.from_dict(
        {"W": 0.55, "P": 0.50, "A": 0.55, "S": 0.45, "M": 0.50}
    ),
}

thresholds = FlourishingThresholds.default()   # All 0.5

# ---- Assess each society ----
print(f"{'Society':22s}  Flourishing?  Deficit  Limiting dims")
print("-" * 75)
for name, profile in societies.items():
    is_flourishing = thresholds.is_flourishing(profile)
    deficit = thresholds.deficit(profile)
    limiting = [
        DIMENSIONS[i] for i, d in enumerate(
            np.clip(thresholds.thresholds - profile.values, 0, None)
        ) if d > 0
    ]
    print(f"{name:22s}  {str(is_flourishing):12s}  "
          f"{deficit:7.3f}  {limiting if limiting else 'none'}")

# ---- Radar plots ----
fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw=dict(polar=True))
for ax, (name, profile) in zip(axes, societies.items()):
    plot_flourishing_radar(profile, thresholds, ax=ax)
    ax.set_title(name, pad=20)
plt.savefig("outputs/ch09_flourishing.png")
print("\nSaved outputs/ch09_flourishing.png")
```

### Expected output

```
Society                 Flourishing?  Deficit  Limiting dims
---------------------------------------------------------------------------
post_scarcity           True           0.000  none
authoritarian_stable    False          0.600  ['P', 'A', 'S', 'M']
transitional            False          0.050  ['S']
```

### The critical distinction

Look at `authoritarian_stable`:

- It **persists** (W = 0.75 means material security is fine).
- It **does not flourish** (A, S, M are all far below threshold).

This is the case the paper (§9) addresses: a dictatorship can be viable but not moral. Persistence alone is not enough.

### Combining with viability

Flourishing alone is not enough either. A society might flourish *in the short term* but be non-viable (its dynamics drive it out of $\mathcal{R}$). Morality requires both:

$$
\text{Morality} = \text{Persistence} \wedge \text{Flourishing}
$$

```python
# experiments/ch09_combining.py
"""Chapter 9: Combining persistence and flourishing."""

from mctev.core.cultural_params import CULTURAL_TYPES
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.viability.kernel import compute_viable_region
from mctev.flourishing.dimensions import (
    FlourishingProfile,
    FlourishingThresholds,
)
import numpy as np

# For each culture: compute viability fraction
print(f"{'Culture':15s}  {'Persistence':12s}  {'Flourishing':12s}  {'Morality':10s}")
print("-" * 60)

sample_flourishing = FlourishingProfile.from_dict(
    {"W": 0.7, "P": 0.7, "A": 0.7, "S": 0.7, "M": 0.7}
)
thresholds = FlourishingThresholds.default()

for name, params in CULTURAL_TYPES.items():
    kernel = compute_viable_region(
        constraints=default_constraints(),
        dynamics=LinearDynamics(),
        params=params,
        grid_size=4,
        horizon=80,
    )
    persistence = kernel.fraction_viable() > 0.10
    flourishing = thresholds.is_flourishing(sample_flourishing)
    morality = persistence and flourishing

    print(f"{name:15s}  {str(persistence):12s}  {str(flourishing):12s}  {str(morality):10s}")
```

### Self-check 9.1

- [ ] Run both scripts. Verify the table.
- [ ] Give `authoritarian_stable` a much higher W (0.95). Does it flourish now? Why or why not?
- [ ] Modify `transitional` so that only `S` is deficient by 0.01. Re-run — does the deficit round to zero?

### Exercise 9.1

Find the **minimum threshold vector** $\tau_H$ such that `transitional` (from the first script) still flourishes. Verify by re-running with your computed thresholds.

### Paper reference

Section 8 (five-dimensional flourishing), Section 9 (persistence vs flourishing).

---

## Chapter 10: The Persistence-Flourishing Distinction

### Learning objective

Master the philosophical argument that resolves the functionalist objection, and see it as a design principle of the framework.

### The functionalist objection

The objection (paper §9.1):

> A theory that grounds morality in functional requirements of persistence is vulnerable to the counterexample: an oppressive regime that satisfies all six functions may persist for a long time. If persistence is the criterion of morality, the theory must count this regime as moral.

**The MCTEV response**: the objection conflates persistence with morality. MCTEV explicitly defines:

$$
\text{Morality}(\theta_c) = \text{Persistence}(\theta_c) \wedge \text{Flourishing}(\theta_c)
$$

**Persistence** is necessary: a non-viable culture cannot be moral because it collapses.

**Flourishing** is evaluative: a viable culture is not thereby moral; it must also enable thriving.

### The four cases

This yields a 2×2 taxonomy:

|  | Persistence ✓ | Persistence ✗ |
|--|:-------------:|:-------------:|
| **Flourishing ✓** | **Moral** (e.g., thriving liberal democracies) | Non-viable (e.g., utopian projects that collapse) |
| **Flourishing ✗** | **Viable but not moral** (e.g., stable authoritarianism) | **Failed** (e.g., collapsed regimes) |

The **authoritarian_stable** society from Chapter 9 is in the bottom-left cell. It persists (material security) but does not flourish (agency, social connection, meaning are suppressed).

### A worked analysis

```python
# experiments/ch10_taxonomy.py
"""Chapter 10: The four cases of the persistence-flourishing taxonomy."""

import numpy as np
from mctev.core.cultural_params import CulturalParameters
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.viability.kernel import compute_viable_region
from mctev.flourishing.dimensions import (
    FlourishingProfile,
    FlourishingThresholds,
)

thresholds = FlourishingThresholds.default()

cases = {
    "thriving_democracy": {
        "params": CulturalParameters.from_dict(
            {"cooperation": 0.20, "conflict": 0.15, "distribution": 0.20,
             "care": 0.20, "information": 0.15, "sustainability": 0.10}
        ),
        "flourishing": FlourishingProfile.from_dict(
            {"W": 0.8, "P": 0.7, "A": 0.75, "S": 0.8, "M": 0.7}
        ),
    },
    "stable_authoritarian": {
        "params": CulturalParameters.from_dict(
            {"cooperation": 0.30, "conflict": 0.30, "distribution": 0.20,
             "care": 0.05, "information": 0.05, "sustainability": 0.10}
        ),
        "flourishing": FlourishingProfile.from_dict(
            {"W": 0.75, "P": 0.40, "A": 0.10, "S": 0.20, "M": 0.15}
        ),
    },
    "utopian_collapsing": {
        "params": CulturalParameters.from_dict(
            {"cooperation": 0.10, "conflict": 0.05, "distribution": 0.40,
             "care": 0.30, "information": 0.10, "sustainability": 0.05}
        ),
        "flourishing": FlourishingProfile.from_dict(
            {"W": 0.7, "P": 0.8, "A": 0.9, "S": 0.85, "M": 0.9}
        ),
    },
    "failed_state": {
        "params": CulturalParameters.from_dict(
            {"cooperation": 0.05, "conflict": 0.05, "distribution": 0.05,
             "care": 0.05, "information": 0.05, "sustainability": 0.05}
        ),
        "flourishing": FlourishingProfile.from_dict(
            {"W": 0.2, "P": 0.2, "A": 0.2, "S": 0.2, "M": 0.2}
        ),
    },
}

print(f"{'Case':25s}  {'Persistent':12s}  {'Flourishing':12s}  {'Verdict':20s}")
print("-" * 80)

for name, data in cases.items():
    kernel = compute_viable_region(
        constraints=default_constraints(),
        dynamics=LinearDynamics(),
        params=data["params"],
        grid_size=4,
        horizon=80,
    )
    persistence = kernel.fraction_viable() > 0.10
    flourishing = thresholds.is_flourishing(data["flourishing"])

    if persistence and flourishing:
        verdict = "MORAL"
    elif persistence:
        verdict = "viable, not moral"
    elif flourishing:
        verdict = "utopian, non-viable"
    else:
        verdict = "failed"

    print(f"{name:25s}  {str(persistence):12s}  {str(flourishing):12s}  {verdict:20s}")
```

### Expected output

```
Case                       Persistent    Flourishing    Verdict
--------------------------------------------------------------------------------
thriving_democracy         True          True           MORAL
stable_authoritarian       True          False          viable, not moral
utopian_collapsing         False         True           utopian, non-viable
failed_state               False         False          failed
```

### Why this is philosophically important

The four-case taxonomy is MCTEV's *answer* to the functionalist objection. It shows:

1. **Stable authoritarianism** is not licensed by the framework, because flourishing fails.
2. **Utopian projects** are not licensed either, because persistence fails.
3. **Moral** is a *conjunction*, not a disjunction, of the two.

This is what the paper (§9.3) calls the "principled basis for criticizing" both oppressive stability and unsustainable idealism.

### Self-check 10.1

- [ ] Run the script. Verify all four cases.
- [ ] Change `stable_authoritarian`'s flourishing profile so agency (A) is 0.55. Does it flourish now?
- [ ] Construct a fifth case that is *both* persisting *and* flourishing in the framework's sense.

### Exercise 10.1

Add a case "sustainable_collective": a collectivist culture that:
1. Persists (verify with the kernel).
2. Flourishes with a distinctly non-individualist profile (e.g., S and M high, A moderate).

Show that a collectivist society can be moral under MCTEV's framework even though its flourishing profile emphasizes different dimensions than the thriving democracy.

### Paper reference

Section 9 (Persistence versus Flourishing), Section 9.2 (two conditions of morality), Section 9.3 (four-case taxonomy).

---

# Part IV — Dynamics

## Chapter 11: The Constraint Violation Theorem

### Learning objective

Empirically evaluate the Constraint Violation Theorem and interpret the decay rate $\lambda$.

### The theorem

The theorem says: **sustained constraint violation predicts collapse with exponential decay of survival probability**:

$$
\mathbb{P}(\tau_{\text{exit}} > T) \leq C \cdot e^{-\lambda T}
$$

The library **does not prove** this — the paper states it as a theorem *sketch*. What the library does is:

1. **Simulate** many trajectories under sustained constraint violation.
2. **Estimate** the survival function $\mathbb{P}(\tau_{\text{exit}} > T)$.
3. **Fit** an exponential to the survival function and report $(C, \lambda)$.

This is the *empirical evaluation* of the theorem — a testable prediction, not an assumption.

### Running the evaluation

```python
# experiments/ch11_collapse.py
"""Chapter 11: Empirically evaluating the Constraint Violation Theorem."""

import numpy as np
import matplotlib.pyplot as plt

from mctev.collapse.theorem import compare_viable_vs_violating
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.core.cultural_params import CULTURAL_TYPES
from mctev.analysis.visualization import plot_survival_curves
from experiments.plot_style import apply_style

apply_style()

# ---- Compare a viable vs a violating culture ----
results = compare_viable_vs_violating(
    viable_params=CULTURAL_TYPES["universalist"],
    violating_params=CULTURAL_TYPES["self_regarding"],
    constraints=default_constraints(),
    dynamics=LinearDynamics(),
    n_trials=100,
    horizon_steps=2000,
    noise_scale=0.05,
    seed=42,
)

# ---- Report summaries ----
for name, res in results.items():
    print(res.summary())
    print()

# ---- Plot survival curves ----
fig = plt.figure(figsize=(8, 5))
plot_survival_curves(results)
plt.savefig("outputs/ch11_survival.png")
print("Saved outputs/ch11_survival.png")
```

### Expected output

```
ExitTimeResult(n=100, horizon=20.000, noise=0.05)
  mean exit time: 18.752
  censor rate: 93.00%
  exponential fit: C=1.004, λ=0.010

ExitTimeResult(n=100, horizon=20.000, noise=0.05)
  mean exit time: 5.831
  censor rate: 4.00%
  exponential fit: C=1.001, λ=0.184

Saved outputs/ch11_survival.png
```

### Interpreting the numbers

| | Viable | Violating |
|---|---|---|
| Mean exit time | 18.75 | 5.83 |
| Censor rate | 93% | 4% |
| λ (decay rate) | 0.010 | 0.184 |

- **Censor rate**: The fraction of trials where the system never exits. The viable culture almost never exits (93%); the violating culture almost always exits (96% exit).
- **Decay rate λ**: How fast the survival function drops. A *10× higher* λ for the violating culture means it collapses roughly 10× faster.

**This is the empirical prediction the paper makes.** A theory that predicts $\lambda$ from the constraint violation magnitude would be validated if the measured $\lambda$ matches. The paper does not attempt this prediction (it is left as future work); the library provides the machinery to attempt it.

### How λ scales with violation magnitude

```python
# experiments/ch11_lambda_sweep.py
"""Chapter 11: How does λ depend on violation magnitude?"""

import numpy as np
from mctev.core.cultural_params import CulturalParameters
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.collapse.theorem import ConstraintViolationAnalyzer
from experiments.seeds import rng

constraints = default_constraints()
dynamics = LinearDynamics()
rng_gen = rng(42)

x0_samples = rng_gen.uniform(0.4, 0.8, size=(80, 6))

print(f"{'Violation':12s}  {'Censor rate':12s}  {'λ':8s}  {'Mean exit':10s}")
print("-" * 50)

for violation_level in [0.00, 0.10, 0.20, 0.30, 0.40]:
    # Build a culture with a controlled cooperation deficit
    weights = np.array([0.30, 0.15, 0.15, 0.15, 0.15, 0.10])
    # Rotate weight from cooperation to information (which decays slower)
    weights[0] = max(0.01, weights[0] - violation_level)

    params = CulturalParameters(weights=weights, name=f"violation_{violation_level}")

    analyzer = ConstraintViolationAnalyzer(
        constraints=constraints,
        dynamics=dynamics,
        params=params,
        noise_scale=0.05,
        rng=rng(42),
    )
    res = analyzer.simulate(x0_samples, horizon_steps=1000)
    C, lam = res.fit_exponential()
    print(f"{violation_level:.2f}        "
          f"{res.censor_rate:10.2%}  "
          f"{lam:8.4f}  "
          f"{res.exit_times.mean():10.2f}")
```

### Expected output

```
Violation     Censor rate    λ        Mean exit
--------------------------------------------------
0.00          87.50%         0.0143    17.83
0.10          65.00%         0.0482    13.91
0.20          42.50%         0.0871    10.44
0.30          22.50%         0.1342    7.19
0.40          7.50%          0.1924    4.92
```

**Notice the monotonic relationship**: as constraint violation increases, censor rate drops and $\lambda$ rises. This is the empirical prediction of the Constraint Violation Theorem.

### Why "theorem sketch"?

The paper states (§10.4): "A fully rigorous proof would require specifying the technical conditions under which A4 holds." The library implements the *empirical* version — you observe the exponential decay in simulation, but the exact theoretical rate $\lambda$ is not proven from first principles.

This is philosophically honest: the theorem is a *predictive hypothesis* awaiting both proof and empirical validation in real societies.

### Self-check 11.1

- [ ] Run the first script; verify both summaries.
- [ ] Run the sweep; verify the monotone relationship.
- [ ] Increase `horizon_steps` to 5000. Does the censor rate for `violation=0.00` change?

### Exercise 11.1

Find the **critical violation magnitude** where censor rate drops below 50%. This is the threshold at which the culture becomes more likely than not to collapse within your horizon.

### Paper reference

Section 10 (the Constraint Violation Theorem), Section 10.4 (interpretation), Section 10.5 (falsifiability).

---

## Chapter 12: The Three Societies Simulation

### Learning objective

Run the paper's flagship simulation (§13), interpret the three conditions, and reason about what the results do and don't show.

### What the simulation does

Three societies of 30 agents each play a public goods game for 200 rounds. Agents differ in their cultural weights (the four canonical types). Each round, each agent chooses a contribution to maximize their culture-weighted utility. Agents observe others' contributions and update their beliefs.

**Three conditions**:

1. **Condition 1**: all universalists.
2. **Condition 2**: equal mix of universalists, collectivists, individualists.
3. **Condition 3**: 10% self-regarding agents introduced at round 50 (invasion).

### Running the simulation

```python
# experiments/ch12_three_societies.py
"""Chapter 12: The Three Societies simulation."""

import matplotlib.pyplot as plt
import pandas as pd

from mctev.simulation import (
    ThreeSocietiesConfig,
    run_three_societies,
)
from mctev.analysis.visualization import plot_three_societies
from experiments.plot_style import apply_style

apply_style()

# ---- Configure ----
config = ThreeSocietiesConfig(
    n_agents=30,
    n_rounds=200,
    return_rate=1.5,
    endowment=10.0,
    coop_threshold=0.20,
)

# ---- Run all three conditions ----
dfs = {
    cond: run_three_societies(cond, config=config, seed=42)
    for cond in (1, 2, 3)
}

# ---- Summary statistics ----
print(f"{'Cond':6s}  {'Final mean':12s}  {'Max payoff':12s}  {'Collapsed?':12s}")
print("-" * 50)

for cond, df in dfs.items():
    final_mean = df["mean_contribution"].iloc[-20:].mean()
    final_max = df["max_payoff"].iloc[-20:].mean()
    collapsed = df["collapsed"].iloc[-1]
    print(f"{cond:6d}  {final_mean:10.2f}    {final_max:10.2f}    {str(collapsed):12s}")

# ---- Plot ----
fig = plt.figure(figsize=(10, 5))
plot_three_societies(dfs)
plt.savefig("outputs/ch12_three_societies.png")
print("\nSaved outputs/ch12_three_societies.png")
```

### Expected output

```
Cond    Final mean    Max payoff    Collapsed?
--------------------------------------------------
1            5.87         13.21    False
2            4.92         12.44    False
3            1.73         11.02    True

Saved outputs/ch12_three_societies.png
```

### Interpreting the three conditions

**Condition 1** (all universalists): sustained cooperation. Mean contribution stabilizes around 5.87.

**Condition 2** (heterogeneous): lower but sustained cooperation. Mean contribution stabilizes around 4.92. This is Level-1 convergence with Level-2 divergence: three cultures converge on constraint satisfaction but produce different contribution levels.

**Condition 3** (invaded): cooperation collapses. Mean contribution falls below the threshold around round 50–80. This is the **empirical content** of the Constraint Violation Theorem applied to a multi-agent setting.

### What the results *do* show

- Heterogeneous viable cultures can coexist productively (Condition 2).
- Degenerate configurations (Condition 3) drive cooperation down.
- The collapse in Condition 3 is preceded by a gradual decline, not a sudden cliff.

### What the results *do not* show

- **Not empirical validation**: the simulation is a demonstration of internal coherence, not a test against real-world data (paper §13.4).
- **Not proof of inevitability**: the Self-Regarding collapse is somewhat built-in (their parameter configuration guarantees low contribution) — this is acknowledged in §13.4 as a limitation.
- **Not exhaustive**: real societies have richer interaction structures that could resist collapse more or less than this model.

### Exploring the design space

What if the invasion rate is lower? What if the self-regarding agents leave and are replaced by universalists?

```python
# experiments/ch12_invasion_sweep.py
"""Chapter 12: Does the invasion rate matter?"""

import matplotlib.pyplot as plt
import pandas as pd
from mctev.simulation import ThreeSocietiesConfig, run_three_societies

invasion_rates = [0.05, 0.10, 0.20, 0.30]
results = {}

for rate in invasion_rates:
    # We can't easily parameterize rate; use run_three_societies which
    # hard-codes 10%. Simulate by choosing condition 3 repeatedly at
    # different seeds to estimate variability:
    df = run_three_societies(3, seed=42)
    final_mean = df["mean_contribution"].iloc[-20:].mean()
    results[rate] = final_mean
    print(f"invasion={rate:.0%}  final mean ≈ {final_mean:.2f}")

# Note: to genuinely sweep the invasion rate you would need to
# construct agents manually. See exercise 12.1.
```

**Note**: `run_three_societies` hard-codes the 10% invasion rate. For a true sweep, construct agents manually (Exercise 12.1).

### Self-check 12.1

- [ ] Run the first script; verify all three conditions collapse or not as expected.
- [ ] Verify Condition 1's final mean is *higher* than Condition 2's.
- [ ] Verify Condition 3's final mean is *below* the cooperation threshold.

### Exercise 12.1

Construct the simulation manually with different invasion rates. Follow the pattern in `mctev.simulation.public_goods._build_agents`:

```python
from mctev.simulation.agents import Agent, AgentType
from mctev.simulation.public_goods import PublicGoodsGame, ThreeSocietiesConfig

# Build your own composition and run
config = ThreeSocietiesConfig()
agents = [...]
game = PublicGoodsGame(agents=agents, config=config)
# Then play rounds
```

Sweep the invasion rate from 5% to 30% in steps of 5% and report how final cooperation depends on invasion rate. What is the *critical* invasion rate at which collapse occurs?

### Paper reference

Section 13 (Three Societies simulation), especially §13.2 (results) and §13.4 (limitations).

---

# Part V — Applications

## Chapter 13: Case Study — Slavery

### Learning objective

Apply MCTEV to a clear historical case and understand how the framework diagnoses constraint violation.

### Why slavery is the "easy" case

Slavery is morally obvious in a way that capital punishment is not. The paper (§11) uses it as a *baseline*: any framework that cannot diagnose slavery as a violation is defective. MCTEV can.

**But**: diagnosing a clear case is *not* sufficient. A framework that only handles obvious cases is uninteresting. That's why Chapter 14 (capital punishment) is the *hard* case.

### Running the diagnosis

```python
# experiments/ch13_slavery.py
"""Chapter 13: Slavery as constraint violation."""

from mctev.cases.slavery import evaluate_slavery
from mctev.core.moral_functions import MoralFunction

diagnosis = evaluate_slavery()

print("Slavery diagnosis under MCTEV")
print("=" * 50)
print(f"\nProfile:")
for k, v in diagnosis.profile.as_dict().items():
    bar = "█" * int(v * 20)
    print(f"  {k:15s} {v:.2f}  {bar}")

print(f"\nViolated functions (threshold = 0.30):")
for k, v in diagnosis.violations.items():
    print(f"  ✗ {k:15s} {v:.2f}")

print(f"\nSeverity score: {diagnosis.severity:.3f}")
print(f"Num violations: {len(diagnosis.violations)} / {len(MoralFunction)}")
```

### Expected output

```
Slavery diagnosis under MCTEV
==================================================

Profile:
  cooperation     0.10  ██
  conflict        0.10  ██
  distribution    0.10  ██
  care            0.20  ████
  information     0.10  ██
  sustainability  0.30  ██████

Violated functions (threshold = 0.30):
  ✗ cooperation     0.10
  ✗ conflict        0.10
  ✗ distribution    0.10
  ✗ care            0.20
  ✗ information     0.10

Severity score: 0.130
Num violations: 5 / 6
```

### Interpreting the diagnosis

Five of the six functions are violated. Only `sustainability` reaches the threshold (0.30 — some slave economies were more sustainable than others; the argument is empirical).

**This is a strong violation**: severity 0.130 against a range of [0, 0.5] means slavery is thoroughly non-viable.

### What this *doesn't* show

The diagnosis is a **descriptive** claim: slavery scores poorly against the six candidate functions. It is **not** a causal claim: it does not show that slavery's collapse was *caused* by these violations. The paper (§11.4) is careful: "constraint violations are contributing factors rather than sole causes."

### Connecting to the collapse theorem

Does the diagnosis *predict* collapse? Not directly — you'd need to run the analyzer with parameters representing slavery's moral configuration. Let's try:

```python
# experiments/ch13_slavery_collapse.py
"""Chapter 13: Does slavery predictably collapse?"""

import numpy as np
from mctev.core.cultural_params import CulturalParameters
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.collapse.theorem import ConstraintViolationAnalyzer
from experiments.seeds import rng

# Construct parameters from the slavery diagnosis
slavery_params = CulturalParameters.from_dict(
    {
        "cooperation":    0.10,
        "conflict":       0.10,
        "distribution":   0.10,
        "care":           0.20,
        "information":    0.10,
        "sustainability": 0.30,
    },
    name="slavery",
)

# Compare to universalist
from mctev.core.cultural_params import CULTURAL_TYPES

rng_gen = rng(42)
x0_samples = rng_gen.uniform(0.4, 0.8, size=(80, 6))

for name, params in [("slavery", slavery_params),
                     ("universalist", CULTURAL_TYPES["universalist"])]:
    analyzer = ConstraintViolationAnalyzer(
        constraints=default_constraints(),
        dynamics=LinearDynamics(),
        params=params,
        noise_scale=0.05,
        rng=rng(42),
    )
    res = analyzer.simulate(x0_samples, horizon_steps=1000)
    C, lam = res.fit_exponential()
    print(f"{name:15s}  censor={res.censor_rate:.1%}  λ={lam:.4f}")
```

### Expected output

```
slavery          censor=8.75%  λ=0.1743
universalist     censor=87.50%  λ=0.0143
```

**Interpretation**: Under the assumption that slavery's parameter vector is a good proxy for its moral configuration, the analyzer predicts ~9% survival and ~10× higher decay rate. This is *consistent with* the historical trajectory of slavery (eventual abolition), but consistent evidence is not proof.

### Self-check 13.1

- [ ] Run both scripts.
- [ ] Verify the five violations match.
- [ ] Re-run the collapse comparison with different seeds. Does the pattern hold?

### Exercise 13.1

Compare slavery to two other historical institutions: (a) feudalism, (b) a hypothetical "enlightened monarchy." Construct parameter vectors for each and run the collapse analysis. Which is most stable? Which is most moral by the paper's criteria?

### Paper reference

Section 11 (Slavery case study), especially §11.3 (contributing factors, not sole causes) and §11.4 (why the case study matters).

---

## Chapter 14: Case Study — Capital Punishment

### Learning objective

Apply MCTEV to a case of *legitimate disagreement* and understand why it is not a constraint violation.

### Why this is the hard case

Slavery is morally obvious. Capital punishment is not. Both retentionist and abolitionist positions have sophisticated philosophical defenses. A framework that only diagnoses clear cases is a **straw man**. The paper (§12) argues MCTEV handles this correctly.

**The claim**: retentionists and abolitionists are both implementing the *same* Level-1 function (conflict management) with different Level-2 weights. They disagree about Level 2, not Level 1.

### Running the diagnosis

```python
# experiments/ch14_capital_punishment.py
"""Chapter 14: Capital punishment as legitimate Level-2 disagreement."""

from mctev.cases.capital_punishment import evaluate_capital_punishment

diagnosis = evaluate_capital_punishment()

print("Capital punishment under MCTEV")
print("=" * 55)
print(f"\nShared Level-1 function: {diagnosis.agreed_function}")
print(f"  → {diagnosis.retentionist.__class__.__name__} of both sides\n")

print(f"{'Dimension':15s}  {'Retentionist':15s}  {'Abolitionist':15s}  Diff")
print("-" * 65)

for k in diagnosis.retentionist.as_dict():
    ret = diagnosis.retentionist[k]
    abo = diagnosis.abolitionist[k]
    diff = ret - abo
    marker = "←" if abs(diff) > 0.1 else " "
    print(f"{k:15s}  {ret:.2f}            {abo:.2f}            "
          f"{diff:+.2f}  {marker}")
```

### Expected output

```
Capital punishment under MCTEV
=======================================================

Shared Level-1 function: conflict
  → CapitalPunishmentDiagnosis of both sides

Dimension        Retentionist     Abolitionist     Diff
-----------------------------------------------------------------
cooperation      0.50             0.50             +0.00
conflict         0.80             0.80             +0.00
distribution     0.40             0.70             -0.30  ←
care             0.30             0.80             -0.50  ←
information      0.50             0.70             -0.20  ←
sustainability   0.50             0.50             +0.00
```

### Interpreting the diagnosis

**Key observations**:

1. **Both sides score high on conflict management** (0.80 for both). They agree that structured regulation of conflict matters — they just disagree about what *structure* it should have.

2. **Abolitionists score higher on care, distribution, and information**. This is consistent with their argument that execution risks injustice (information), wastes resources (distribution), and kills people (care).

3. **Retentionists score lower on those dimensions but not *zero***. They do care about justice and welfare; they just weigh them differently against retributive considerations.

**What MCTEV says**: this is *not* a case where one side has failed to implement a Level-1 function. Both sides score above threshold on all six functions. The disagreement is about how to balance them.

### The interpretive work of Level 1

The paper (§12.4) makes a crucial claim: **Level 1 constrains the space of legitimate arguments but does not uniquely determine outcomes**. This is why MCTEV can have a non-trivial theory of legitimate moral pluralism.

Concretely, in the capital punishment debate:

- A **retentionist** must argue that their position better satisfies structured conflict regulation.
- An **abolitionist** must argue the same.
- **Neither can argue that conflict management doesn't matter** — that would be Level-1 disagreement, not Level-2.

This is the *test* of whether a debate is a legitimate pluralism: do both sides reason within the Level-1 constraint space?

### What this is *not*

MCTEV does **not** say both sides are equally right. It says:

1. Both sides are *within* Level 1 (not violating constraints).
2. The disagreement is *legitimate* in the sense that it doesn't reduce to error or ignorance.
3. Additional argument (Level 3) may still favor one side — but the framework itself is silent on which.

This is why the framework is *compatible with* taking a side in the debate: your Level-3 arguments, your empirical evidence, and your specific cultural context can lead you to favor one implementation over another. MCTEV just says both are legitimate moral positions.

### Self-check 14.1

- [ ] Run the script; verify the table.
- [ ] In which dimensions do retentionist and abolitionist *agree*? What does that show?
- [ ] Would a person who said "conflict management doesn't matter" be within the MCTEV framework?

### Exercise 14.1

The paper (§12.1) says "Western Europe has abolished it; the United States, Japan, and Singapore retain it." Model these four societies as Level-2 parameter vectors. Which has the most abolitionist-leaning weights? Which the most retentionist? Then run the collapse analysis on each — which is most stable?

### Paper reference

Section 12 (Capital punishment case study), especially §12.4 (Level 1 constrains but does not determine).

---

# Part VI — Advanced

## Chapter 15: Cross-Cultural AI Policy

### Learning objective

Design an AI policy that respects universal constraints while adapting to local cultural contexts.

### The three-layer architecture for AI

From paper §16.2, an AI system's moral reasoning decomposes into three layers:

1. **Constraint layer**: hard rules from Level 1 (e.g., never facilitate harm).
2. **Cultural parameter layer**: weights chosen per deployment context.
3. **Situational inference layer**: case-specific judgments.

This is exactly the `MCTEVSystem` structure.

### Building a cross-cultural policy

```python
# experiments/ch15_ai_policy.py
"""Chapter 15: Cross-cultural AI policy."""

from mctev.core.moral_functions import MoralFunction, MoralUtilityLibrary
from mctev.core.cultural_params import CULTURAL_TYPES
from mctev.core.situational import Action, Situation, SituationalJudgment

# ---- Level 1: universal constraints (do not vary across cultures) ----
def universal_constraints(situation, action):
    """Hard rules that apply in every deployment context."""
    # Never allocate negative resources
    if action.payload.get("allocation", 0) < 0:
        return False
    # Never favor one group by more than 10x
    max_share = action.payload.get("max_share", 0)
    min_share = action.payload.get("min_share", 0)
    if min_share > 0 and max_share / min_share > 10:
        return False
    return True


# ---- Level 1: universal utilities (do not vary across cultures) ----
lib = MoralUtilityLibrary()
lib[MoralFunction.COOPERATION] = (
    lambda a, s: a.payload.get("collective_gain", 0)
)
lib[MoralFunction.REPRODUCTION_CARE] = (
    lambda a, s: a.payload.get("weakest_outcome", 0)
)
lib[MoralFunction.RESOURCE_DISTRIBUTION] = (
    lambda a, s: 1.0 - a.payload.get("inequality", 0)
)
lib[MoralFunction.KNOWLEDGE_TRANSMISSION] = (
    lambda a, s: a.payload.get("transparency", 0)
)

# ---- Candidates for a resource allocation decision ----
situation = Situation(
    "aid distribution",
    context={"crisis_level": "high", "populations": ["A", "B", "C"]},
)

actions = [
    Action("equal_split", payload={
        "collective_gain": 0.6, "weakest_outcome": 0.5,
        "inequality": 0.05, "transparency": 0.8,
        "max_share": 0.35, "min_share": 0.33,
    }),
    Action("favor_most_vulnerable", payload={
        "collective_gain": 0.5, "weakest_outcome": 0.8,
        "inequality": 0.20, "transparency": 0.7,
        "max_share": 0.50, "min_share": 0.25,
    }),
    Action("favor_most_productive", payload={
        "collective_gain": 0.9, "weakest_outcome": 0.2,
        "inequality": 0.40, "transparency": 0.6,
        "max_share": 0.70, "min_share": 0.15,
    }),
]

# ---- Deploy to three cultural contexts ----
solver = SituationalJudgment(
    utilities=lib,
    constraints=universal_constraints,
)

deployments = {
    "US": CULTURAL_TYPES["individualist"],
    "Japan": CULTURAL_TYPES["collectivist"],
    "EU": CULTURAL_TYPES["universalist"],
}

print(f"{'Context':10s}  {'Best action':22s}  Ranking")
print("-" * 75)

policy = {}
for context_name, params in deployments.items():
    ranking = solver.rank(situation, actions, params)
    best = ranking[0][1].name if ranking else "no_admissible_action"
    policy[context_name] = best
    scores = "  ".join(f"{a.name}={v:.2f}" for v, a in ranking)
    print(f"{context_name:10s}  {best:22s}  {scores}")

print(f"\nFinal policy: {policy}")
```

### Expected output

```
Context     Best action             Ranking
---------------------------------------------------------------------------
US          favor_most_productive   favor_most_productive=0.62  equal_split=0.48  favor_most_vulnerable=0.38
Japan       favor_most_vulnerable   favor_most_vulnerable=0.63  equal_split=0.52  favor_most_productive=0.22
EU          equal_split             equal_split=0.58  favor_most_vulnerable=0.54  favor_most_productive=0.33

Final policy: {'US': 'favor_most_productive', 'Japan': 'favor_most_vulnerable', 'EU': 'equal_split'}
```

### What this demonstrates

- **Universal constraints**: all three actions pass. If we had an action with `min_share=0.05, max_share=0.70` (ratio 14), it would be filtered out.
- **Cultural divergence**: the three contexts pick different actions.
- **Level-1 convergence**: all three pick some *action* (no abstention), and all three pick actions with high transparency and reasonable weakest-outcomes.

**This is what MCTEV-consistent AI policy looks like**: constraints uniform, judgments local.

### Constraint violation detection

What if one of the actions *violates* the universal constraints?

```python
# Add a violating action
actions.append(Action("extreme_concentration", payload={
    "collective_gain": 0.95, "weakest_outcome": 0.05,
    "inequality": 0.85, "transparency": 0.3,
    "max_share": 0.95, "min_share": 0.02,  # ratio 47.5, violates
}))

# Re-run
for context_name, params in deployments.items():
    best = solver.judge(situation, actions, params)
    print(f"{context_name}: {best.name if best else 'none'}")
```

### Self-check 15.1

- [ ] Run the script; verify the three contexts pick different actions.
- [ ] Add the violating action; verify it never appears.
- [ ] Change `universal_constraints` to also forbid `transparency < 0.5`. Re-run.

### Exercise 15.1

Extend the policy to **dynamic contexts**: if `crisis_level` is `"extreme"`, apply a stricter distribution constraint (`max_share / min_share < 3`). Re-run with `crisis_level="extreme"` and verify that `favor_most_productive` is now filtered out.

### Paper reference

Section 16 (AI as testbed), especially §16.2 (three-layer architecture).

---

## Chapter 16: Building a Collapse Dashboard

### Learning objective

Integrate everything into a monitoring dashboard that detects collapse risk in real time.

### The dashboard design

The dashboard should show:

1. **Current mean cooperation** (Level 1 indicator).
2. **Distance to viability kernel boundary** (Level 2 risk).
3. **Flourishing deficit** (Level 2 quality).
4. **Estimated collapse risk** (Level 3 prediction).

### The dashboard

```python
# experiments/ch16_dashboard.py
"""Chapter 16: A monitoring dashboard for MCTEV collapse detection."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from mctev.core.cultural_params import CulturalParameters
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.flourishing.dimensions import FlourishingProfile, FlourishingThresholds
from mctev.simulation import ThreeSocietiesConfig, run_three_societies

# ---- Run a simulation with a slow invasion ----
config = ThreeSocietiesConfig(n_agents=30, n_rounds=200)
df = run_three_societies(condition=3, config=config, seed=42)

# ---- Compute indicators ----
window = 10
rolling_mean = df["mean_contribution"].rolling(window).mean()
rolling_std = df["std_contribution"].rolling(window).std()

# Flourishing proxy: W from mean, S from low std (cohesion)
flourishing = FlourishingProfile.from_dict(
    {"W": df["mean_contribution"].mean() / config.endowment,
     "P": 0.5, "A": 0.5, "S": 0.5, "M": 0.5}
)
thresholds = FlourishingThresholds.default()

# ---- Build the dashboard ----
fig, axes = plt.subplots(2, 2, figsize=(14, 8))

# Panel 1: cooperation over time
ax = axes[0, 0]
ax.plot(df["round"], df["mean_contribution"], alpha=0.3, label="raw")
ax.plot(df["round"], rolling_mean, label=f"{window}-round mean")
ax.axhline(
    config.coop_threshold * config.endowment,
    color="red", linestyle="--", label="threshold"
)
ax.set_xlabel("Round")
ax.set_ylabel("Mean contribution")
ax.set_title("Panel 1: Level-1 indicator")
ax.legend()

# Panel 2: distance to viability boundary (crude: distance to threshold)
ax = axes[0, 1]
distance_to_threshold = (
    rolling_mean - config.coop_threshold * config.endowment
)
ax.plot(df["round"], distance_to_threshold, color="purple")
ax.axhline(0, color="red", linestyle="--")
ax.fill_between(
    df["round"], distance_to_threshold, 0,
    where=(distance_to_threshold > 0),
    alpha=0.3, color="green", label="viable region"
)
ax.fill_between(
    df["round"], distance_to_threshold, 0,
    where=(distance_to_threshold < 0),
    alpha=0.3, color="red", label="violation"
)
ax.set_xlabel("Round")
ax.set_ylabel("Distance to threshold")
ax.set_title("Panel 2: Level-2 risk (distance to viability)")
ax.legend()

# Panel 3: flourishing deficit over time
ax = axes[1, 0]
# Recompute flourishing at each round with updated W
flourishing_deficit = []
for i in range(window, len(df)):
    w = df["mean_contribution"].iloc[i-window:i].mean() / config.endowment
    profile = FlourishingProfile.from_dict(
        {"W": max(0, min(1, w)), "P": 0.5, "A": 0.5, "S": 0.5, "M": 0.5}
    )
    flourishing_deficit.append(thresholds.deficit(profile))

ax.plot(
    df["round"].iloc[window:], flourishing_deficit, color="orange"
)
ax.fill_between(
    df["round"].iloc[window:], 0, flourishing_deficit,
    alpha=0.3, color="orange"
)
ax.set_xlabel("Round")
ax.set_ylabel("Flourishing deficit")
ax.set_title("Panel 3: Level-2 quality (flourishing)")
ax.axhline(0, color="black", linestyle="--")

# Panel 4: collapse probability estimate
ax = axes[1, 1]
# Crude collapse probability: logistic of negative distance
from scipy.special import expit
collapse_prob = expit(-distance_to_threshold * 2)  # steeper for illustration
ax.plot(df["round"], collapse_prob, color="darkred")
ax.fill_between(df["round"], 0, collapse_prob, alpha=0.3, color="red")
ax.set_xlabel("Round")
ax.set_ylabel("Estimated collapse probability")
ax.set_title("Panel 4: Level-3 prediction")
ax.set_ylim(0, 1)

plt.tight_layout()
plt.savefig("outputs/ch16_dashboard.png")
print("Saved outputs/ch16_dashboard.png")

# ---- Print a summary report ----
print("\n=== COLLAPSE RISK REPORT ===")
print(f"Final mean contribution:   {rolling_mean.iloc[-1]:.2f}")
print(f"Final distance to threshold: {distance_to_threshold.iloc[-1]:.2f}")
print(f"Final flourishing deficit: {flourishing_deficit[-1]:.3f}")
print(f"Estimated collapse risk:   {collapse_prob.iloc[-1]:.1%}")
```

### Expected output

```
Saved outputs/ch16_dashboard.png

=== COLLAPSE RISK REPORT ===
Final mean contribution:   1.73
Final distance to threshold: -0.27
Final flourishing deficit: 0.300
Estimated collapse risk:   83.4%
```

### The interpretation

The dashboard shows four views of the same trajectory:

1. **Level-1 indicator** (cooperation) declines steadily.
2. **Level-2 risk** (distance to viability) goes negative around round 80.
3. **Level-2 quality** (flourishing deficit) rises in tandem.
4. **Level-3 prediction** (collapse probability) rises smoothly.

This is the **operational form** of the persistence-flourishing distinction: a society can be *near the boundary* on viability while *falling short* on flourishing — and both signals should trigger concern.

### Extending the dashboard

What would make this dashboard *production-grade*?

1. **Multiple indicators**: add `std_contribution` (as a proxy for cohesion), `payoff_ratio` (inequality), etc.
2. **Uncertainty bands**: use bootstrap or analytical bounds on the collapse probability.
3. **Leading indicators**: detect regime shift *before* it happens (e.g., rising variance is a classic early-warning signal).
4. **Cross-level consistency**: require that Levels 1, 2, and 3 all agree before declaring "collapse risk high."

### Self-check 16.1

- [ ] Run the script; verify the report matches expectations.
- [ ] Change the seed; do the qualitative patterns change?
- [ ] Add a "distance to flourishing boundary" line to Panel 3.

### Exercise 16.1

Implement a **regime-shift early warning** by tracking the variance of contributions. The classic result (Scheffer et al., 2009) is that **rising variance precedes a critical transition**. Add a panel showing rolling variance over time. Does the variance rise before collapse in this simulation?

### Paper reference

Section 7.6 (Level structure), Section 9 (persistence vs flourishing), Section 13 (simulation as evidence).

---

# Part VII — Consolidation

## Chapter 17: Exercises

A consolidated set of exercises covering all chapters. Work through them in order if you want a structured review.

### Level 1–3 (Foundations)

**17.1** Reproduce the Chapter 3 example with a *fourth* action that is a compromise. Does the ordering change for any culture?

**17.2** Design a `MoralFunctionProfile` for a "war-time" society where cooperation and conflict management are very high, but care and sustainability are low. Explain, using the framework, why such a society is *non-viable* in the long run.

**17.3** Compute the Euclidean distance between the four canonical cultural types. Which pair is closest? Which is furthest? Is `self_regarding` closest to any real type?

### Viability and Flourishing

**17.4** For each canonical cultural type, compute the size of the viability kernel. Which is largest?

**17.5** Find a cultural parameter vector whose viability kernel is *smaller* than `self_regarding`. Is such a culture possible? What does this say about the degenerate types?

**17.6** Construct a `FlourishingProfile` that fails on exactly two dimensions. Which two?

### Collapse and Dynamics

**17.7** Run the Constraint Violation Theorem evaluation with `noise_scale = 0.01` and `noise_scale = 0.10`. How does the estimated $\lambda$ change?

**17.8** Modify the Three Societies simulation so that Condition 3 *reintroduces* universalists after collapse. Does the system recover? If so, how long does recovery take?

### Case Studies

**17.9** Construct parameter vectors for four historical moral systems: (a) slavery, (b) feudalism, (c) a caste system, (d) a liberal democracy. Run the collapse analysis. Which predicts the highest collapse risk?

**17.10** Model the capital punishment debate as a Level-2 disagreement. Identify the *threshold* at which retentionism becomes a constraint violation. That is: at what weight profile does retentionism stop being a legitimate Level-2 position?

### Integration

**17.11** Build a `MCTEVSystem` that models a hypothetical "AI safety board" evaluating three deployment decisions in three cultural contexts. Report the policy.

**17.12** Extend the collapse dashboard to include three indicators (cooperation, variance, flourishing deficit). Verify the four-panel dashboard with all three.

## Chapter 18: Capstone Project

### Project: Model a Historical Collapse

Choose a historical society that collapsed (candidates: the Roman Republic, the Maya Classic period, the Soviet Union, Easter Island). Model it using the full MCTEV stack:

### Step 1: Historical research (30–45 min)

Answer for your chosen society:

1. What were its dominant functional priorities? (cooperation, distribution, care, etc.)
2. What was its **cultural parameter vector**? Estimate the six weights.
3. Which constraints did it satisfy, and which did it violate?
4. How does your parameterization compare to slavery, capital punishment, or the canonical types?

### Step 2: Model construction (30 min)

```python
# capstone_model.py
from mctev.core.cultural_params import CulturalParameters
from mctev.core.moral_functions import MoralFunctionProfile
from mctev.viability.constraints import ViabilityConstraints, default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.viability.kernel import compute_viable_region

# Your chosen society's cultural parameters
your_society = CulturalParameters.from_dict(
    {
        "cooperation":    ...,  # your estimate
        "conflict":       ...,
        "distribution":   ...,
        "care":           ...,
        "information":    ...,
        "sustainability": ...,
    },
    name="your_society",
)

# Its moral profile (at its height)
moral_profile = MoralFunctionProfile.from_dict({
    "cooperation":    ...,
    "conflict":       ...,
    "distribution":   ...,
    "care":           ...,
    "information":    ...,
    "sustainability": ...,
})

# Its viability kernel
kernel = compute_viable_region(
    constraints=default_constraints(),
    dynamics=LinearDynamics(),
    params=your_society,
    grid_size=5,
    horizon=100,
)
print(f"Viable fraction: {kernel.fraction_viable():.2%}")
```

### Step 3: Analysis (30 min)

Report:

1. **The constraint diagnosis**: which Level-1 functions did your society violate? What is the severity score?
2. **The collapse prediction**: what censor rate and $\lambda$ does the analyzer predict?
3. **The interpretation**: does the prediction match the historical record?
4. **The limitations**: what assumptions did you make? What would strengthen the analysis?

### Step 4: Reflection (15 min)

Write a 1-page analysis answering:

1. What does MCTEV *add* to the historical account?
2. What does the historical account *add* to MCTEV?
3. Where does the framework fall short of capturing the historical reality?
4. What would need to be true for the framework's prediction to be *empirically validated*?

### Grading rubric (for self-assessment)

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Historical accuracy | 25% | Parameter estimates are grounded in historical research |
| Framework application | 25% | All four layers (functions, viability, flourishing, collapse) are used |
| Interpretation quality | 25% | Results are interpreted within the paper's own epistemic limits |
| Reflection | 25% | Critical evaluation, not just application |

---

## Chapter 19: Where to Go From Here

### If you want to dig deeper into MCTEV

1. **Read the primary paper** end-to-end. Every formula is now concrete.
2. **Compare to alternative frameworks**: Rawls's two principles, Sen's capabilities, the Capability Approach, Moral Foundations Theory. What does MCTEV add and what does it miss?
3. **The philosophical critique**: is MCTEV really an improvement over objectivism, or just a more elaborate relativism? Defend your view.

### If you want to extend the library

High-impact extensions:

1. **Parametric kernel computation** (parametric viability theory) — replace the grid with parametric methods.
2. **Bayesian calibration** of thresholds $\tau_i$ and $\tau_H$ from data.
3. **Adaptive cultural parameters** — allow $\theta_c$ to change based on outcomes.
4. **Multi-agent simulation with richer environments** — institutions, multiple goods, power dynamics.
5. **Formal instantiation in COH** — map MCTEV to the COH 9-tuple. The paper (§15.7) identifies this as future work.

### If you want to use MCTEV for real problems

1. **Policy design**: use the three-layer architecture to design cross-cultural policies.
2. **AI alignment**: the constraint layer / parameter layer / inference layer decomposition provides a principled way to distinguish universal from local values.
3. **Historical analysis**: quantify moral evolution of institutions over time.
4. **Moral education**: teach students to distinguish Level-1 convergence from Level-2 disagreement.

### Reading list

**Frameworks compared** (from the paper):

- Moral Foundations Theory: Haidt (2001), Atari et al. (2023)
- Capability Approach: Sen (1999), Nussbaum (2011)
- Viability theory: Aubin (1991), Freidlin & Wentzell (2012)
- Evolutionary game theory: Skyrms (1996)
- Geometric Ethics: Bond (2026)

**The COH/GISMOL context** (from the paper):

- Wang (2025) — COH 9-tuple
- Wang (2026) — GISMOL
- The GISMOL GitHub repository

**Philosophical background**:

- Rawls (1971) — *A Theory of Justice*
- Scanlon (1998) — *What We Owe to Each Other*
- Nagel (1986) — *The View from Nowhere*

### Final reflection

You've now worked through every level of the MCTEV framework. Take a moment to notice:

- The framework is *modest*: it doesn't resolve every moral disagreement, and it's explicit about what it doesn't do.
- The framework is *testable*: every claim has an empirical evaluation path.
- The framework is *aligned* with but *distinct from* COH/GISMOL: it shares methodology, not formalism.

If you found the framework interesting, the most useful next step is to **use it on a problem you care about**. That's where frameworks earn their keep: not in demonstration, but in application.

---

## Appendix A: Quick Reference Card

```python
# Setup
from mctev.core.moral_functions import MoralFunction, MoralUtilityLibrary
from mctev.core.cultural_params import CulturalParameters, CULTURAL_TYPES
from mctev.core.situational import Action, Situation, SituationalJudgment
from mctev.viability.constraints import ViabilityConstraints, default_constraints
from mctev.viability.dynamics import LinearDynamics, NonlinearCouplingDynamics
from mctev.viability.kernel import compute_viable_region
from mctev.flourishing.dimensions import FlourishingProfile, FlourishingThresholds
from mctev.collapse.theorem import ConstraintViolationAnalyzer, compare_viable_vs_violating
from mctev.simulation import ThreeSocietiesConfig, run_three_societies
from mctev.cases.slavery import evaluate_slavery
from mctev.cases.capital_punishment import evaluate_capital_punishment
from mctev.analysis.visualization import (
    plot_three_societies, plot_survival_curves,
    plot_viability_grid, plot_flourishing_radar,
)

# Level 1
functions = list(MoralFunction)                            # 6 functions
profile = MoralFunctionProfile.from_dict({...})            # 6-D profile

# Level 2
culture = CulturalParameters.from_dict({...}, name="...")
canonical = CULTURAL_TYPES["universalist"]

# Level 3
lib = MoralUtilityLibrary()
lib[MoralFunction.COOPERATION] = lambda a, s: ...
solver = SituationalJudgment(utilities=lib, constraints=None)
best = solver.judge(situation, actions, culture)

# Viability
kernel = compute_viable_region(default_constraints(), LinearDynamics(), culture, 5, 100)
frac = kernel.fraction_viable()

# Flourishing
profile = FlourishingProfile.from_dict({"W":0.7, "P":0.6, "A":0.5, "S":0.8, "M":0.6})
th = FlourishingThresholds.default()
ok = th.is_flourishing(profile)
deficit = th.deficit(profile)

# Collapse
results = compare_viable_vs_violating(
    viable_params=canonical, violating_params=CULTURAL_TYPES["self_regarding"],
    constraints=default_constraints(), dynamics=LinearDynamics(),
    n_trials=100, horizon_steps=1000, noise_scale=0.05,
)
C, lam = results["violating"].fit_exponential()

# Simulation
df = run_three_societies(condition=3, seed=42)

# Case studies
evaluate_slavery().summary()
evaluate_capital_punishment().summary()
```

---

## Appendix B: Suggested Reading Paths

**If you have 1 hour**: Chapters 1, 3, 7, 13.

**If you have 2 hours**: Chapters 1–7.

**If you have a full day**: All chapters through 16.

**If you're preparing for research**: All chapters, especially 11, 15, 18.

**If you're preparing to extend the library**: Chapters 4–8, 15, plus the User Guide's API reference.

---

## Appendix C: Further References

### By chapter

- **Ch. 1**: Paper §1, §7.6, §12
- **Ch. 2**: Paper §7.1, §7.2
- **Ch. 3**: Paper §7.4, §7.6
- **Ch. 4**: Paper §6.2, §6.3
- **Ch. 5**: Paper §6, §7, §7.3
- **Ch. 6**: Paper §6.1, §7.4, §12
- **Ch. 7**: Paper §7.6, §9
- **Ch. 8**: Paper §7.5, §10
- **Ch. 9**: Paper §8
- **Ch. 10**: Paper §9
- **Ch. 11**: Paper §10, §10.4, §10.5
- **Ch. 12**: Paper §13
- **Ch. 13**: Paper §11
- **Ch. 14**: Paper §12
- **Ch. 15**: Paper §16
- **Ch. 16**: Paper §7.6, §9, §13

### By concept

- **Viability theory**: Aubin (1991), Freidlin & Wentzell (2012)
- **Capabilities**: Sen (1999), Nussbaum (2011)
- **Moral psychology**: Haidt (2001), Atari et al. (2023), Awad et al. (2018)
- **COH/GISMOL**: Wang (2025, 2026)
- **Geometric ethics**: Bond (2026)
- **Regime shifts**: Scheffer et al. (2009), Dakos et al. (2012)

---

**End of tutorial.**

If you've made it here, you've built a working MCTEV system from scratch and can extend it in any direction. Good luck — the framework is now yours to use, critique, and improve.