# mctev-lib User Guide

**Comprehensive reference for the Multi-Level Computational Theory of Ethics library (v0.2.0)**

Companion to the [Tutorial](./TUTORIAL.md), [Migration Guide](./MIGRATION.md), and the [MCTEV paper](../MCTEV_PAPER.md).

---

## Table of Contents

**Part I — Getting Started**
1. [Introduction](#1-introduction)
2. [What MCTEV Is and Is Not](#2-what-mctev-is-and-is-not)
3. [Installation](#3-installation)
4. [Your First MCTEV Program](#4-your-first-mctev-program)

**Part II — Conceptual Foundation**
5. [The Three-Level Architecture](#5-the-three-level-architecture)
6. [The Six Candidate Level 1 Functions](#6-the-six-candidate-level-1-functions)
7. [The Three Threshold Families](#7-the-three-threshold-families)
8. [The Full Level-2 Configuration λ_c](#8-the-full-level-2-configuration-λ_c)
9. [The Controlled Viability Region and Flourishing](#9-the-controlled-viability-region-and-flourishing)

**Part III — Working with the Library**
10. [Building Configurations](#10-building-configurations)
11. [Judging Situations](#11-judging-situations)
12. [Computing Viability Kernels](#12-computing-viability-kernels)
13. [Measuring Flourishing](#13-measuring-flourishing)
14. [Boundary-Instability Analysis](#14-boundary-instability-analysis)
15. [Retentionist Conditions](#15-retentionist-conditions)
16. [Qualifying Conditions and the Proxy Audit](#16-qualifying-conditions-and-the-proxy-audit)
17. [Dispersion Measures](#17-dispersion-measures)

**Part IV — Reference**
18. [Complete API Reference](#18-complete-api-reference)
19. [Common Pitfalls and Troubleshooting](#19-common-pitfalls-and-troubleshooting)
20. [Design Commitments and Rationale](#20-design-commitments-and-rationale)

**Part V — Advanced Topics**
21. [Integration with COH/GISMOL](#21-integration-with-cohgismol)
22. [Numerical Considerations](#22-numerical-considerations)
23. [Performance and Scaling](#23-performance-and-scaling)

**Part VI — Appendices**
24. [Theoretical Foundations](#24-theoretical-foundations)
25. [Glossary](#25-glossary)
26. [References](#26-references)

---

# Part I — Getting Started

## 1. Introduction

`mctev-lib` is the reference implementation of the **Multi-Level Computational Theory of Ethics (MCTEV)** — a framework that reconciles ethical relativism and ethical objectivism by decomposing ethics into three hierarchically organized levels.

The library supports four core capabilities:

1. **Representation**: model any moral system as a three-level structure with a full Level-2 configuration.
2. **Reasoning**: compute situational judgments with situation-dependent action sets, safeguard constraints, and explicit tie-breaking.
3. **Simulation**: run multi-agent models of moral dynamics.
4. **Analysis**: quantify convergence, divergence, viability, flourishing, boundary instability, and dispersion across eight type-appropriate measures.

The v0.2.0 release brings the library into alignment with the current manuscript. The most significant change is that **Level 2 is now six components, not one**:

$$
\lambda_c = (\theta_c, \boldsymbol{\tau}_c^V, \boldsymbol{\tau}_c^S, \boldsymbol{\tau}_c^H, \rho_c, M_c)
$$

Every component acts on a **different object**, and the library enforces the distinction at the type level.

## 2. What MCTEV Is and Is Not

**What it is:**

- A **formal framework** for representing ethical systems as hierarchically organized computational objects.
- A **computational model** of how universal functions, cultural parameters, and situational judgments interact.
- A **testable theory** whose predictions can be checked against simulation and, ultimately, empirical data.
- A **research program** positioning ethics as a computational science, methodologically aligned with (but not formally derived from) the COH/GISMOL agenda.

**What it is not:**

- A **complete theory** of all moral phenomena. The framework is a scaffold for further work.
- A **deductive engine** that mechanically resolves every moral disagreement. Level 1 *constrains* but does not *uniquely determine* outcomes.
- A **formally instantiated** COH 9-tuple. The relationship is methodological alignment and structural analogy.
- A **substitute for normative ethics**. It is a meta-theoretical framework, not a first-order moral theory.
- An **empirically validated** theory. The library implements the computational infrastructure; it does not itself constitute empirical evaluation.

Users should keep these boundaries in mind, especially when using the library to make claims about real-world ethical questions.

## 3. Installation

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
git clone https://github.com/hongxueharriswang/mctev-lib.git
cd mctev-lib
python -m venv .mctev-venv
source .mctev-venv/bin/activate
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
print(mctev.__version__)   # 0.2.0

from mctev.core.moral_functions import MoralFunction
print(list(MoralFunction))

from mctev.core.thresholds import (
    ViabilityThresholds, SafeguardThresholds, FlourishingThresholds,
)
print("Three threshold families OK.")
```

### 3.5 Recommended environment

For interactive exploration, use JupyterLab or IPython:

```bash
pip install jupyterlab
jupyter lab
```

## 4. Your First MCTEV Program

This complete program demonstrates the core capability: building a full Level-2 configuration λ_c and using it to judge a situation.

```python
"""first_mctev.py — a minimal MCTEV v0.2.0 program."""

from mctev.core.configuration import default_configuration
from mctev.core.moral_functions import MoralFunction, MoralUtilityLibrary
from mctev.core.selection import SelectionConvention
from mctev.core.situational import Action, Situation, SituationalJudgment

# ---- Step 1: Define per-function utilities ----
lib = MoralUtilityLibrary()
lib[MoralFunction.COOPERATION] = lambda a, s: float(a.payload)
lib[MoralFunction.REPRODUCTION_CARE] = lambda a, s: 1.0 - float(a.payload)

# ---- Step 2: Build a FULL configuration λ_c (all six components) ----
config = default_configuration(
    name="universalist",
    weights=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05],
    viability_value=0.30,
    safeguard_values={"error_rate": 0.05},
    flourishing_value=0.50,
    selection=SelectionConvention.STATUS_QUO,
)

# ---- Step 3: Build the Level-3 solver ----
solver = SituationalJudgment(utilities=lib)

# ---- Step 4: Judge ----
best = solver.judge(
    Situation("allocation decision"),
    [Action("low", 0.2), Action("high", 0.8)],
    config,
)
print(f"Universalist chooses: {best.name}")
```

**What just happened?**

1. We defined two candidate moral functions — cooperation and care — as utility callables.
2. We built a **full Level-2 configuration** λ_c with all six components: weights, three threshold families, selection convention, and measurement operator.
3. We built a `SituationalJudgment` solver.
4. We evaluated the situation under the full configuration.

You have now used Levels 1, 2, and 3.

---

# Part II — Conceptual Foundation

## 5. The Three-Level Architecture

```
                    ┌───────────────────────────────────────────┐
                    │  LEVEL 1                                  │
                    │  Candidate Level 1 moral functions        │
                    │  + Architecture 𝔄                         │
                    └─────────────┬─────────────────────────────┘
                                  │
                       constrains (downward)
                                  │
                                  ▼
                    ┌───────────────────────────────────────────┐
                    │  LEVEL 2                                  │
                    │  Cultural-institutional configuration λ_c │
                    │  = (θ, τ^V, τ^S, τ^H, ρ, M)                │
                    └─────────────┬─────────────────────────────┘
                                  │
                       constrains (downward)
                                  │
                                  ▼
                    ┌───────────────────────────────────────────┐
                    │  LEVEL 3                                  │
                    │  Situational judgments j(s; 𝔄, λ_c)       │
                    └───────────────────────────────────────────┘
```

**The Ethical Constraint Hierarchy Principle**: constraints propagate downward; adaptation propagates upward.

- **Downward**: Level 1 functions and architecture constrain what counts as a viable Level-2 configuration; Level 2 configurations constrain what counts as a legitimate Level-3 judgment.
- **Upward**: Level 3 outcomes reveal whether Level 2 configurations are working; Level 2 configurations reveal whether Level 1 functions are being satisfied.

This is why Level 1 **constrains** but does not **uniquely determine** moral outcomes.

## 6. The Six Candidate Level 1 Functions

MCTEV identifies six candidate Level 1 functions, each derived from a **functional problem** that any enduring society must solve:

| # | Functional problem | Library value | Description |
|---|---|---|---|
| \(P_1\) | Cooperation | `cooperation` | Reciprocal contribution to collective goods |
| \(P_2\) | Conflict management | `conflict` | Structured regulation of social conflict |
| \(P_3\) | Resource distribution | `distribution` | Resource accessibility for all members |
| \(P_4\) | Reproduction and care | `care` | Care for the young and dependent |
| \(P_5\) | Knowledge transmission | `information` | Information integrity in transmission |
| \(P_6\) | Sustainability | `sustainability` | Restraint in resource use |

**Why "candidate"?** The mapping from functional problems to functions is not unique. The library exposes them as a fixed enum but documents them as **candidates whose epistemic tier (strict universal, robust regularity, weak regularity) is not yet established**.

### 6.1 Accessing the functions

```python
from mctev.core.moral_functions import (
    MoralFunction,
    MORAL_FUNCTION_ORDER,
    N_FUNCTIONS,
)

print(N_FUNCTIONS)   # 6
print([f.value for f in MORAL_FUNCTION_ORDER])
# ['cooperation', 'conflict', 'distribution', 'care', 'information', 'sustainability']

print(MoralFunction.COOPERATION.description)
# 'Reciprocal contribution to collective goods'
```

### 6.2 Working with profiles

A `MoralFunctionProfile` is a point in 6-D function space:

```python
from mctev.core.moral_functions import MoralFunctionProfile

profile = MoralFunctionProfile.from_dict({
    "cooperation": 0.7,
    "care":        0.8,
    "distribution": 0.6,
})
print(profile)
print(f"Dominance (frac ≥ 0.5): {profile.dominance():.2f}")
```

## 7. The Three Threshold Families

This is the **most important conceptual distinction in v0.2.0**. The manuscript (Section 7.1) separates three families of thresholds because they govern three distinct objects.

### 7.1 The three families

| Family | Symbol | Acts on | Example |
|---|---|---|---|
| **Dynamical viability** | \(\boldsymbol{\tau}^V\) | Society-level state viability \(\mathcal{V}(\lambda_c)\) | Minimum cooperation rate; maximum violence rate |
| **Safeguard** | \(\boldsymbol{\tau}^S\) | Action admissibility \(\mathcal{C}(s; \mathfrak{A}, \boldsymbol{\tau}^S)\) | Wrongful-conviction rate threshold; procedural-integrity index |
| **Flourishing** | \(\boldsymbol{\tau}^H\) | Membership in \(\mathcal{F}(\lambda_c)\) | Minimum agency; minimum social connectedness |

### 7.2 Why they are not interchangeable

Consider the **wrongful-conviction rate threshold** `error_rate = 0.05`:

- It is a **safeguard** \(\tau^S\). It gates whether the *action* "execute" is admissible in *a specific case*.
- It is **not** a viability threshold \(\tau^V\). A society is not unviable because its error rate is high; only the *action* is inadmissible.
- It is **not** a flourishing threshold \(\tau^H\). Flourishing doesn't require anything about error rates.

**If you use the same threshold class for all three, you will systematically misclassify.**

### 7.3 Building each family

```python
from mctev.core.thresholds import (
    ViabilityThresholds, SafeguardThresholds, FlourishingThresholds,
    ThresholdFamilies,
)

# ---- τ^V — dynamical viability thresholds ----
tau_V = ViabilityThresholds.from_dict({
    "cooperation":    0.40,
    "conflict":       0.30,
    "distribution":   0.35,
    "care":           0.30,
    "information":    0.30,
    "sustainability": 0.25,
})

# ---- τ^S — safeguard thresholds ----
tau_S = SafeguardThresholds.from_dict({
    "error_rate":  0.05,
    "disparity":   0.10,
    "consistency": 0.80,
})

# ---- τ^H — flourishing thresholds ----
tau_H = FlourishingThresholds.from_dict({
    "W": 0.50, "P": 0.50, "A": 0.60, "S": 0.50, "M": 0.50,
})

# ---- Container ----
families = ThresholdFamilies(
    viability=tau_V, safeguard=tau_S, flourishing=tau_H,
)
```

### 7.4 Type-level enforcement

The library enforces the distinction at the type level. Attempting to pass `SafeguardThresholds` where `ViabilityThresholds` is expected raises a `TypeError`:

```python
from mctev.core.configuration import CulturalConfiguration

# This will fail at construction:
try:
    CulturalConfiguration(
        weights=[0.2]*5,
        viability_thresholds=tau_S,  # wrong type!
        safeguard_thresholds=tau_S,
        flourishing_thresholds=tau_H,
        selection_convention=..., measurement_operator=...,
    )
except TypeError as e:
    print(f"Correctly rejected: {e}")
```

## 8. The Full Level-2 Configuration λ_c

### 8.1 The six components

$$
\lambda_c = (\theta_c, \boldsymbol{\tau}_c^V, \boldsymbol{\tau}_c^S, \boldsymbol{\tau}_c^H, \rho_c, M_c)
$$

| Component | Class | Acts on |
|---|---|---|
| \(\theta_c \in \Delta^5\) | `weights` (in `CulturalConfiguration`) | Balancing the six functions |
| \(\boldsymbol{\tau}^V\) | `ViabilityThresholds` | State viability \(\mathcal{V}(\lambda_c)\) |
| \(\boldsymbol{\tau}^S\) | `SafeguardThresholds` | Action admissibility \(\mathcal{C}(s; \mathfrak{A}, \boldsymbol{\tau}^S)\) |
| \(\boldsymbol{\tau}^H\) | `FlourishingThresholds` | Flourishing region \(\mathcal{F}(\lambda_c)\) |
| \(\rho_c\) | `SelectionConvention` | Tie-breaking among maximizers |
| \(M_c\) | `MeasurementOperator` | Mapping states to observed flourishing |

### 8.2 Building a configuration

```python
import numpy as np
from mctev.core.configuration import CulturalConfiguration, default_configuration
from mctev.core.thresholds import (
    ViabilityThresholds, SafeguardThresholds, FlourishingThresholds,
)
from mctev.core.selection import SelectionConvention
from mctev.core.measurement import LinearMeasurement

config = CulturalConfiguration(
    weights=np.array([0.30, 0.20, 0.20, 0.15, 0.10, 0.05]),
    viability_thresholds=ViabilityThresholds.uniform(0.30),
    safeguard_thresholds=SafeguardThresholds.from_dict({
        "error_rate": 0.05,
        "disparity":  0.10,
    }),
    flourishing_thresholds=FlourishingThresholds.uniform(0.50),
    selection_convention=SelectionConvention.STATUS_QUO,
    measurement_operator=LinearMeasurement(to_core=lambda x: np.asarray(x)[:5]),
    name="universalist",
)
```

### 8.3 Simplex normalization

The weights must lie in the probability simplex:

$$
\theta_c \in \Delta^5 = \left\{\theta \in \mathbb{R}_{\geq 0}^6 : \sum_f \theta_f = 1\right\}
$$

`CulturalConfiguration.__post_init__` enforces this:

```python
try:
    CulturalConfiguration(
        weights=np.array([1.0]*6),  # sums to 6
        ...
    )
except ValueError as e:
    print(f"Rejected: {e}")
# Rejected: Weights must sum to 1 (simplex normalization); got sum = 6.0
```

**Why simplex?** The Level-3 objective is invariant under positive rescaling of \(\theta_c\): only relative weights matter. The simplex restriction is a Level-2 identifiability condition.

### 8.4 The convenience constructor

`default_configuration` fills sensible defaults:

```python
config2 = default_configuration(
    name="collectivist",
    weights=[0.25, 0.15, 0.15, 0.30, 0.10, 0.05],
    selection=SelectionConvention.PRECEDENT,
)
```

### 8.5 Serialization

```python
config.to_dict()
# {
#   "name": "universalist",
#   "weights": {...},
#   "viability_thresholds": {...},
#   "safeguard_thresholds": {...},
#   "flourishing_thresholds": {...},
#   "selection_convention": "status_quo",
#   "measurement_operator": "LinearMeasurement"
# }
```

### 8.6 Backward compatibility (deprecated)

The v0.1.0 `CulturalParameters` class (which held only \(\theta_c\)) is retained as a deprecated shim:

```python
from mctev.core.cultural_params import CulturalParameters

params = CulturalParameters(weights=[0.3, 0.2, 0.2, 0.15, 0.1, 0.05])
# DeprecationWarning: CulturalParameters is deprecated;
# use CulturalConfiguration or default_configuration instead.
```

The shim returns an object that behaves as a `CulturalConfiguration` with default thresholds, status-quo selection, and identity measurement. This preserves v0.1.0 code paths but should be migrated.

## 9. The Controlled Viability Region and Flourishing

### 9.1 The controlled viability region

The **controlled viability region** is the set:

$$
\mathcal{R}(\lambda_c; \Pi) = \left\{\mathbf{x}_0 \in \mathcal{V}(\lambda_c) : \exists \pi \in \Pi \text{ s.t. } \mathbf{x}^{\pi}(t) \in \mathcal{V}(\lambda_c) \; \forall t \geq 0\right\}
$$

where \(\mathcal{V}(\lambda_c)\) is defined by the **dynamical viability thresholds \(\tau^V\)**.

**Important terminology.** This is a *controlled viability kernel* — one component of moral assessment, not the whole of it. Safeguards, flourishing, and rights are handled through separate objects.

### 9.2 The three flourishing notions

| Notion | Formula | Meaning |
|---|---|---|
| Instantaneous | \(\mathcal{F}(\lambda_c)\) | Currently meets flourishing thresholds |
| Viable current | \(\mathcal{F}(\lambda_c) \cap \mathcal{R}(\lambda_c; \Pi)\) | Currently flourishing and recoverably viable |
| Sustainable | \(\mathcal{R}_{\mathcal{F}}(\lambda_c; \Pi) = \mathrm{Viab}_\Pi(\mathcal{F} \cap \mathcal{V}; F_{\lambda_c})\) | Some policy maintains flourishing-and-viability indefinitely |

These are nested when both kernels share dynamics, policy class, and configuration.

### 9.3 The objectivity safeguard

Because \(\boldsymbol{\tau}_c^H \in \mathcal{T}_H^{L1}\) and \(M_c \in \mathcal{M}_{\mathfrak{A}}\), a cultural context cannot:

- Select thresholds outside the admissible range.
- Adopt a measurement operator that reverses within-context ordering.

This preserves flourishing as a basis for cross-cultural criticism.

---

# Part III — Working with the Library

## 10. Building Configurations

### 10.1 From canonical types

The library does not ship with pre-built configurations beyond `default_configuration`; but you can build a canonical set easily:

```python
CANONICAL = {
    "universalist":   default_configuration(
        name="universalist",
        weights=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05],
    ),
    "collectivist":   default_configuration(
        name="collectivist",
        weights=[0.25, 0.15, 0.15, 0.30, 0.10, 0.05],
    ),
    "individualist":  default_configuration(
        name="individualist",
        weights=[0.20, 0.15, 0.20, 0.10, 0.20, 0.15],
    ),
    "self_regarding": default_configuration(
        name="self_regarding",
        weights=[1.00, 0.00, 0.00, 0.00, 0.00, 0.00],
    ),
}
```

### 10.2 From a starting configuration

To modify an existing configuration:

```python
from mctev.core.thresholds import SafeguardThresholds

# Increase the error-rate safeguard
new_safeguards = config.safeguard_thresholds.with_overrides(error_rate=0.001)

new_config = CulturalConfiguration(
    weights=config.weights,
    viability_thresholds=config.viability_thresholds,
    safeguard_thresholds=new_safeguards,
    flourishing_thresholds=config.flourishing_thresholds,
    selection_convention=config.selection_convention,
    measurement_operator=config.measurement_operator,
    name="strict_retentionist",
)
```

## 11. Judging Situations

### 11.1 The judgment pipeline

Given a situation \(s\), a configuration \(\lambda_c\), and a set of actions \(\mathcal{A}(s)\):

1. **Build A(s)** — situation-dependent action set (user-supplied).
2. **Filter by C(s; A, τ^S)** — via `constraints` predicate.
3. **Compute J(s; A, λ_c)** — set of maximizers via `correspondence()`.
4. **Apply σ_{ρ_c}** — resolve ties via `judge()`.

### 11.2 The three methods

```python
from mctev.core.situational import SituationalJudgment, Action, Situation

solver = SituationalJudgment(utilities=lib, constraints=None)
situation = Situation("test")
actions = [Action("a", 0.3), Action("b", 0.7)]

# 1. Filter by constraints
admissible = solver.admissible_actions(actions, situation, config)

# 2. Compute correspondence (set of maximizers)
J = solver.correspondence(situation, actions, config)

# 3. Apply selection
selected = solver.judge(situation, actions, config)

# Or get the full ranking
ranking = solver.rank(situation, actions, config)
for score, action in ranking:
    print(f"{score:+.3f}  {action.name}")
```

### 11.3 Selection conventions

Five conventions are supported:

```python
from mctev.core.selection import SelectionConvention, select_action

# STATUS_QUO — choose the status-quo action if it maximizes
situation = Situation("s", {"status_quo": "b"})
chosen = select_action(
    SelectionConvention.STATUS_QUO,
    [Action("a"), Action("b")],
    situation,
)  # → 'b'

# PRECEDENT — choose closest to previous action
chosen = select_action(
    SelectionConvention.PRECEDENT,
    [Action("a"), Action("b"), Action("c")],
    situation,
    previous_action=Action("c"),
)  # → 'c'

# MINIMUM_INTERVENTION — choose smallest payload
chosen = select_action(
    SelectionConvention.MINIMUM_INTERVENTION,
    [Action("a", 0.5), Action("b", 0.1)],
    situation,
)  # → 'b'

# LEXICOGRAPHIC — choose by a secondary key
chosen = select_action(
    SelectionConvention.LEXICOGRAPHIC,
    [Action("b"), Action("a")],
    situation,
    lexicographic_key=lambda a: a.name,
)  # → 'a'

# RANDOM — uniform among maximizers
import numpy as np
chosen = select_action(
    SelectionConvention.RANDOM,
    [Action("a"), Action("b"), Action("c")],
    situation,
    rng=np.random.default_rng(42),
)
```

### 11.4 Constraints that read τ^S

The constraint predicate receives `(situation, action, configuration)`, so it can inspect the safeguard thresholds:

```python
def safeguard_constraint(situation, action, config):
    """Gate 'execute' on the error-rate safeguard."""
    if action.name != "execute":
        return True
    tau_error = config.safeguard_thresholds.get("error_rate", 0.05)
    observed = situation.context.get("observed_error_rate", 0.0)
    return observed <= tau_error

solver = SituationalJudgment(utilities=lib, constraints=safeguard_constraint)
```

### 11.5 Situation-dependent action sets

The library does not enforce a fixed action set. You build \(\mathcal{A}(s)\) however you like:

```python
def action_generator(situation):
    budget = situation.context.get("budget", 10)
    return [
        Action("small",  0.2 * budget),
        Action("medium", 0.5 * budget),
        Action("large",  0.8 * budget),
    ]

situation = Situation("alloc", {"budget": 100})
actions = action_generator(situation)
best = solver.judge(situation, actions, config)
```

## 12. Computing Viability Kernels

### 12.1 Basic usage

```python
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.viability.kernel import compute_viable_region

constraints = default_constraints(thresholds=config.viability_thresholds)
dynamics = LinearDynamics()

kernel = compute_viable_region(
    constraints=constraints,
    dynamics=dynamics,
    configuration=config,
    grid_size=5,
    horizon=100,
)
print(f"Viable fraction: {kernel.fraction_viable():.2%}")
```

### 12.2 Custom dynamics

```python
from mctev.viability.dynamics import NonlinearCouplingDynamics
dynamics = NonlinearCouplingDynamics()
kernel = compute_viable_region(..., dynamics=dynamics, ...)
```

### 12.3 Kernel membership

```python
import numpy as np
state = np.full(6, 0.5)
in_kernel = kernel.contains(state)
print(f"State in kernel: {in_kernel}")
```

### 12.4 Comparing configurations

```python
for name, cfg in CANONICAL.items():
    cons = default_constraints(thresholds=cfg.viability_thresholds)
    k = compute_viable_region(
        constraints=cons, dynamics=LinearDynamics(),
        configuration=cfg, grid_size=4, horizon=80,
    )
    print(f"{name:15s}  viable fraction = {k.fraction_viable():.2%}")
```

**Note**: Only \(\tau^V\) affects the viability kernel. Changing \(\tau^S\) or \(\tau^H\) does not change it. This is the correct behavior — the kernel is defined by state viability alone.

## 13. Measuring Flourishing

### 13.1 Building a measurement operator

```python
import numpy as np
from mctev.core.measurement import LinearMeasurement, MeasurementOperator

# Identity measurement
identity = LinearMeasurement(to_core=lambda x: np.asarray(x)[:5])

# Culturally specific measurement (monotone transform on agency)
agency_boost = LinearMeasurement(
    to_core=lambda x: np.asarray(x)[:5],
    monotone_transforms={2: lambda v: v ** 0.7},
)

# With noise
noisy = LinearMeasurement(
    to_core=lambda x: np.asarray(x)[:5],
    noise_std=0.05,
    rng=np.random.default_rng(42),
)
```

### 13.2 Validating a measurement operator

The library provides `within_context_monotone`:

```python
ok = identity.within_context_monotone(
    x_lower=np.full(6, 0.3),
    x_higher=np.full(6, 0.7),
    dimension=0,
    n_samples=100,
)
print(f"Within-context monotone: {ok}")
```

### 13.3 Cross-context comparability

```python
from mctev.core.measurement import validate_cross_context_comparability

# Without anchors or linking — not comparable
report = validate_cross_context_comparability(identity, agency_boost)
print(report)
# {'comparable': False, 'mechanism': 'unavailable'}

# With anchor states
anchors = [np.full(6, 0.5), np.full(6, 0.7)]
report = validate_cross_context_comparability(
    identity, agency_boost, anchor_states=anchors,
)
print(report)
# {'comparable': True/False, 'mechanism': 'anchors', 'mean_discrepancy': ...}
```

### 13.4 Computing a flourishing profile

```python
from mctev.flourishing.dimensions import FlourishingProfile

state = np.array([0.55, 0.55, 0.65, 0.55, 0.55, 0.5])
profile = FlourishingProfile.from_measurement(
    state, config.measurement_operator,
)
print(profile)
# FlourishingProfile(W=0.55, P=0.55, A=0.76, S=0.55, M=0.55)

# Check against τ^H
meets = profile.meets(config.flourishing_thresholds)
print(f"Meets τ^H: {meets}")
```

## 14. Boundary-Instability Analysis

### 14.1 The index/outcome distinction

The Boundary-Instability Hypothesis distinguishes:

- **Index boundary** \(\partial\mathcal{K}_{\text{index}}\) — the set whose proximity is measured.
- **Outcome set** \(\mathcal{K}_{\text{out}}\) — the set whose survival is evaluated.

These need not coincide.

### 14.2 The three designs

```python
from mctev.instability.analyzer import build_three_designs

designs = build_three_designs(
    dynamics=dynamics,
    configuration=config,
    viability_constraints=constraints,
    viability_kernel=kernel,
    function=MoralFunction.COOPERATION,
)

# Three designs:
#   indicator_specific       — index = V_i,    outcome = V
#   kernel_to_viability_exit — index = R,      outcome = V
#   kernel_retention         — index = R,      outcome = R
```

### 14.3 Running Design B

```python
import numpy as np

boundary_point = np.full(6, 0.32)  # just inside V
inward_distances = [0.02, 0.05, 0.10, 0.20]

for name, analyzer in designs.items():
    result = analyzer.design_B(
        boundary_point=boundary_point,
        inward_distances=inward_distances,
        horizon_steps=300,
        n_trials=20,
    )
    print(result.summary())
```

The result reports:

- `inward_distances`: the ε values.
- `survival_probabilities`: \(q_{T, \mathcal{K}_{\text{out}}}^\pi\) at each ε.
- `delta_epsilon()`: the outermost Δ_ε.

### 14.4 Building custom safe sets

```python
from mctev.instability.safe_sets import SafeSet

class MySafeSet(SafeSet):
    def __init__(self, predicate):
        self.predicate = predicate
    def contains(self, x):
        return self.predicate(x)
    def signed_distance(self, x):
        return 1.0 if self.contains(x) else -1.0

custom_set = MySafeSet(lambda x: x[0] > 0.5)
```

### 14.5 Set-specific survival

```python
from mctev.instability.survival import set_specific_survival

# q_{T, V}^π(x0)
survived = set_specific_survival(
    x0=np.full(6, 0.4),
    outcome_set=my_set,
    dynamics=dynamics,
    configuration=config,
    horizon_steps=300,
    noise_scale=0.02,
)
```

## 15. Retentionist Conditions

### 15.1 The three conditions

The manuscript (Section 12.3) distinguishes:

- **(R1) Architectural non-exclusion**: the architecture contains no categorical prohibition of capital punishment.
- **(R2) Weak configuration-specific non-vacuity**: some configuration admits a capital action in some test situation.
- **(R3) Strong configuration-specific non-vacuity**: every configuration admits a capital action in some test situation.

### 15.2 Checking R1

```python
from mctev.retentionist.architecture import (
    RetentionistArchitecture, AbolitionistArchitecture,
)
from mctev.retentionist.conditions import check_R1

A_R = RetentionistArchitecture(name="A_R", constraint_predicate=my_constraint)
A_A = AbolitionistArchitecture(name="A_A", constraint_predicate=my_constraint)

assert check_R1(A_R) is True   # retentionist doesn't exclude categorically
assert check_R1(A_A) is False  # abolitionist excludes categorically
```

### 15.3 Checking R2 and R3

```python
from mctev.retentionist.conditions import (
    check_R2, check_R3, CapitalActionSet, evaluate_test_situations,
    anti_triviality_filter,
)

# Define test situations and action generator
test_situations = [Situation("murder", {"severity": "high"})]
def action_gen(s):
    actions = [Action("life", 0.5), Action("acquit", 0.0)]
    if s.context.get("severity") == "high":
        actions.append(Action("execute", 1.0))
    return actions

# R2: weak non-vacuity
R2 = check_R2(A_R, [config], test_situations, action_gen,
              capital_set=CapitalActionSet(), judgment=solver)
print(f"R2: {R2}")

# R3: strong non-vacuity
R3 = check_R3(A_R, [config, config_strict], test_situations, action_gen,
              capital_set=CapitalActionSet(), judgment=solver)
print(f"R3: {R3}")
```

### 15.4 Anti-triviality filter

The test situations must pass anti-triviality conditions:

```python
filtered = anti_triviality_filter(
    raw_test_situations,
    is_factually_coherent=lambda s: True,
    in_jurisdiction=lambda s: True,
    is_feasible=lambda s: True,
    is_artificial=lambda s: False,
)
```

## 16. Qualifying Conditions and the Proxy Audit

### 16.1 The problem

When \(S_i^{\text{qual}}\) is used to derive \(f_i\), the qualifying condition \(Q_{-i}\) must not contain \(f_i\) or any proxy that presupposes \(f_i\). Mere non-equivalence is insufficient.

### 16.2 Building a qualifying condition

```python
import numpy as np
from mctev.core.moral_functions import MoralFunction
from mctev.core.qualifying import (
    QualifyingConditions, MemberInclusiveViability, proxy_audit,
)

condition = MemberInclusiveViability(
    target_function=MoralFunction.RESOURCE_DISTRIBUTION,
    welfare_index=lambda x: np.array([x[0], x[3]]),  # cooperation + care
    minimum_member_welfare=0.3,
)
condition._inputs = ["cooperation_indicator", "care_indicator"]

conditions = QualifyingConditions()
conditions[MoralFunction.RESOURCE_DISTRIBUTION] = condition

# Run the audit
report = proxy_audit(conditions, MoralFunction.RESOURCE_DISTRIBUTION)
print(report.summary())
# Proxy audit [PASS] for target f = distribution
```

### 16.3 When the audit fails

```python
# A condition that secretly presupposes distribution
suspect = MemberInclusiveViability(
    target_function=MoralFunction.RESOURCE_DISTRIBUTION,
    welfare_index=lambda x: np.array([x[2]]),  # distribution!
)
suspect._inputs = ["gini_coefficient"]  # a proxy for distribution

conditions[MoralFunction.RESOURCE_DISTRIBUTION] = suspect
report = proxy_audit(conditions, MoralFunction.RESOURCE_DISTRIBUTION)
print(report.summary())
# Proxy audit [FAIL] for target f = distribution
#   flagged proxies: ['gini_coefficient']
```

The library flags common proxies (see `_COMMON_PROXY_NAMES` in `qualifying.py`). The audit is heuristic — full definitional independence may require human judgment.

### 16.4 Beyond the library check

The proxy audit catches:

- Direct mentions of the target function value name (e.g., `"cooperation"`).
- Common proxy names (`"gini_coefficient"`, `"reciprocity_index"`, etc.).

It does not catch:

- Semantic proxies that are not in the common list.
- Proxies hidden inside measurement operators.
- Indirect dependence through other functions.

For full independence, inspect `Q_{-i}`'s `constitutive_inputs()`, its measurement operators, and its threshold rules manually.

## 17. Dispersion Measures

### 17.1 The eight measures

| Measure | What it captures | Function |
|---|---|---|
| \(D_F\) | Function recognition | `dispersion_function_recognition` |
| \(D_\theta\) | Simplex weights | `dispersion_weights` |
| \(D_{\tau^V}\) | Viability thresholds | `dispersion_viability_thresholds` |
| \(D_{\tau^S}\) | Safeguard thresholds | `dispersion_safeguard_thresholds` |
| \(D_{\tau^H}\) | Flourishing thresholds | `dispersion_flourishing_thresholds` |
| \(D_\rho\) | Selection conventions | `dispersion_selection_conventions` |
| \(D_M\) | Measurement operators | `dispersion_measurement_operators` |
| \(D_J\) | Judgments | `dispersion_judgments` |

### 17.2 Computing weights dispersion

```python
from mctev.analysis.metrics import dispersion_weights

configs = list(CANONICAL.values())
d_theta = dispersion_weights([c.weights for c in configs])
print(f"D_θ: {d_theta:.4f}")
```

By default, `dispersion_weights` uses **Aitchison distance** (the natural metric for compositional data). Pass `metric="js"` for Jensen-Shannon divergence.

### 17.3 Computing threshold dispersions

```python
from mctev.analysis.metrics import (
    dispersion_viability_thresholds,
    dispersion_safeguard_thresholds,
    dispersion_flourishing_thresholds,
)

print(f"D_τ^V: {dispersion_viability_thresholds(configs):.4f}")
print(f"D_τ^S: {dispersion_safeguard_thresholds(configs):.4f}")
print(f"D_τ^H: {dispersion_flourishing_thresholds(configs):.4f}")
```

### 17.4 Computing D_ρ on a shared benchmark

\(D_\rho\) requires a **shared benchmark**: both conventions must be applied to the **same maximizer sets**, with all other components held fixed.

```python
from mctev.analysis.metrics import dispersion_selection_conventions
from mctev.core.situational import Action, Situation

# Shared benchmark: same maximizers for all situations
benchmark_situations = [
    Situation(f"s{i}", {"status_quo": "b"}) for i in range(5)
]
benchmark_maximizers = [
    [Action("a"), Action("b"), Action("c")] for _ in range(5)
]

d_rho = dispersion_selection_conventions(
    configs, benchmark_situations, benchmark_maximizers,
)
print(f"D_ρ: {d_rho:.4f}")
```

### 17.5 The full dispersion vector

```python
from mctev.analysis.metrics import full_dispersion_vector

full = full_dispersion_vector(
    configs=configs,
    recognized_sets=[[MoralFunction.COOPERATION, MoralFunction.CARE]] * 3,
    anchor_states=[np.full(6, 0.5)],
    benchmark={
        "situations": benchmark_situations,
        "maximizers": benchmark_maximizers,
        "judgment_lists": [["a"]*5, ["b"]*5, ["c"]*5],
    },
)
for k, v in full.items():
    print(f"{k:12s}: {v:.4f}")
```

### 17.6 The MCTEV convergence prediction

The manuscript predicts:

$$
D_F < D_\theta, \; D_{\tau^V}, \; D_{\tau^S}, \; D_{\tau^H}, \; D_\rho, \; D_M, \; D_J
$$

Verify this on your data:

```python
if "D_F" in full:
    others = [full[k] for k in full if k != "D_F"]
    holds = full["D_F"] < min(others)
    print(f"Convergence prediction holds: {holds}")
```

**Robustness**: per Section 14, each pairwise comparison must be tested across defensible normalizations. The library does not choose a normalization for you.

---

# Part IV — Reference

## 18. Complete API Reference

### 18.1 `mctev.core.moral_functions`

#### `class MoralFunction(Enum)`

Members: `COOPERATION`, `CONFLICT_MANAGEMENT`, `RESOURCE_DISTRIBUTION`, `REPRODUCTION_CARE`, `KNOWLEDGE_TRANSMISSION`, `SUSTAINABILITY`.

**Property**: `.description → str`

#### `MORAL_FUNCTION_ORDER: List[MoralFunction]`

Canonical ordering.

#### `N_FUNCTIONS: int`

`= 6`

#### `class MoralFunctionProfile`

| Method | Description |
|---|---|
| `__getitem__(f)` | Get entry |
| `as_dict()` | Return dict |
| `dominance()` | Fraction ≥ 0.5 |
| `to_array()` | Numpy array |
| `from_dict(d)` | Build from dict |
| `from_array(arr)` | Build from array |
| `uniform(v)` | All entries = `v` |
| `zeros()` | All zeros |

#### `class MoralUtilityLibrary`

| Method | Description |
|---|---|
| `__setitem__(f, fn)` | Register utility |
| `__getitem__(f)` | Retrieve (0-function if absent) |
| `evaluate(action, situation, weights)` | Weighted sum |

### 18.2 `mctev.core.thresholds`

#### `class ViabilityThresholds`

| Method | Description |
|---|---|
| `__getitem__(f)` | Access by MoralFunction |
| `as_dict()` | Return dict |
| `uniform(v)` | All entries = `v` |
| `from_dict(d)` | Build from dict |
| `from_array(arr)` | Build from array |

#### `class SafeguardThresholds`

| Method | Description |
|---|---|
| `__getitem__(name)` | Access by name |
| `get(name, default)` | Retrieve with default |
| `as_dict()` | Dict of values |
| `from_dict(d)` | Build from dict |
| `with_overrides(**kw)` | Return new with overrides |

#### `class FlourishingThresholds`

| Method | Description |
|---|---|
| `__getitem__(dim)` | Access by dimension (W/P/A/S/M) |
| `as_dict()` | Dict of values |
| `uniform(v)` | All entries = `v` |
| `from_dict(d)` | Build from dict |

#### `class ThresholdFamilies`

Container for all three families.

### 18.3 `mctev.core.configuration`

#### `class CulturalConfiguration`

| Method | Description |
|---|---|
| `__getitem__(f)` | Weight for function |
| `to_dict()` | Full serialization |

**Constructor**: `CulturalConfiguration(weights, viability_thresholds, safeguard_thresholds, flourishing_thresholds, selection_convention, measurement_operator, name="custom")`

**Raises**: `ValueError` if weights are not in the simplex.

#### `default_configuration(...) → CulturalConfiguration`

Convenience constructor.

### 18.4 `mctev.core.selection`

#### `class SelectionConvention(Enum)`

Members: `PRECEDENT`, `MINIMUM_INTERVENTION`, `STATUS_QUO`, `LEXICOGRAPHIC`, `RANDOM`.

#### `select_action(convention, maximizers, situation, previous_action=None, rng=None, lexicographic_key=None) → Action`

### 18.5 `mctev.core.measurement`

#### `class MeasurementOperator(ABC)`

Abstract base with `measure(x)` and `within_context_monotone(...)`.

#### `class LinearMeasurement(MeasurementOperator)`

Baseline additive model.

#### `validate_cross_context_comparability(a, b, anchor_states=None, linking_map=None, tolerance=0.05) → dict`

### 18.6 `mctev.core.qualifying`

#### `class QualifyingCondition(ABC)`

Abstract base with `__call__`, `description()`, `constitutive_inputs()`.

#### `class MemberInclusiveViability(QualifyingCondition)`

Concrete example.

#### `class MinimumFlourishing(QualifyingCondition)`

Concrete example.

#### `class QualifyingConditions`

Container with `__getitem__`, `__setitem__`, `score`.

#### `proxy_audit(conditions, target) → ProxyAuditReport`

#### `class ProxyAuditReport`

Has `definitionally_independent`, `flagged_proxies`, `summary()`.

### 18.7 `mctev.core.situational`

#### `class Situation`

`Situation(name, context={})`

#### `class Action`

`Action(name, payload=None)`

#### `class SituationalJudgment`

**Constructor**: `SituationalJudgment(utilities, constraints=None)`

| Method | Description |
|---|---|
| `admissible_actions(actions, situation, config)` | Filter by C |
| `score(action, situation, config)` | Weighted utility |
| `correspondence(situation, actions, config)` | J(s) — set of maximizers |
| `judge(situation, actions, config, ...)` | j(s) — single action |
| `rank(situation, actions, config)` | Sorted list |

### 18.8 `mctev.core.hierarchy`

#### `class MCTEVSystem`

**Constructor**: `MCTEVSystem(configuration, utilities, constraints=None)`

| Method | Description |
|---|---|
| `situational_layer()` | Return SituationalJudgment |
| `judge(situation, actions, previous_action=None)` | Delegate to layer |
| `describe()` | Summary |

### 18.9 `mctev.viability`

#### `class ViabilityConstraints`

**Constructor**: `ViabilityConstraints(viability_fns={}, thresholds=ViabilityThresholds.uniform(0.3))`

| Method | Description |
|---|---|
| `__setitem__(f, fn)` | Add indicator |
| `__getitem__(f)` | Get indicator fn |
| `values(x)` | Evaluate all |
| `violations(x)` | Dict of deficits |
| `is_satisfied(x)` | Boolean |
| `violation_score(x)` | Sum of deficits |
| `with_thresholds(thresholds)` | Return new |

#### `default_constraints(thresholds=None) → ViabilityConstraints`

#### `class Dynamics(ABC)` and `class LinearDynamics(Dynamics)`

#### `class ViabilityKernel`

**Constructor**: `ViabilityKernel(constraints, dynamics, configuration, horizon=500, dt=0.01, grid_size=8)`

| Method | Description |
|---|---|
| `build()` | Compute mask |
| `contains(x)` | Boolean |
| `fraction_viable()` | Fraction in kernel |

#### `compute_viable_region(...) → ViabilityKernel`

### 18.10 `mctev.instability`

#### `class SafeSet(ABC)`

Abstract base with `contains(x)`, `signed_distance(x)`, `boundary_normal(x)`.

#### `class IndicatorSafeSet(SafeSet)`

**Constructor**: `IndicatorSafeSet(indicator_fn, threshold, function)`

#### `class KernelSafeSet(SafeSet)`

**Constructor**: `KernelSafeSet(kernel)`

#### `set_specific_survival(x0, outcome_set, dynamics, configuration, horizon_steps=1000, dt=0.01, noise_scale=0.02, policy=None, rng=None) → float`

#### `class BoundaryInstabilityAnalyzer`

**Constructor**: `BoundaryInstabilityAnalyzer(dynamics, configuration, index_set, outcome_set, noise_scale=0.02, dt=0.01, rng=None)`

| Method | Description |
|---|---|
| `design_B(boundary_point, inward_distances, horizon_steps, n_trials)` | Run Design B |

#### `class InstabilityResult`

Has `inward_distances`, `survival_probabilities`, `delta_epsilon()`, `summary()`.

#### `build_three_designs(dynamics, configuration, viability_constraints, viability_kernel, function=COOPERATION) → dict`

### 18.11 `mctev.retentionist`

#### `class Architecture(ABC)`

Base class with `name`, `categorical_prohibitions`, `constraint_predicate`.

#### `class RetentionistArchitecture(Architecture)`

No categorical prohibitions.

#### `class AbolitionistArchitecture(Architecture)`

Categorically prohibits "capital_punishment".

#### `check_R1(architecture) → bool`

#### `check_R2(architecture, configurations, test_situations, action_generator, **kwargs) → bool`

#### `check_R3(...) → bool`

#### `class CapitalActionSet`

**Constructor**: `CapitalActionSet(action_names=None)`

| Method | Description |
|---|---|
| `select(actions)` | Filter to capital actions |
| `contains(action)` | Boolean |

#### `evaluate_test_situations(architecture, configuration, test_situations, action_generator, ...) → dict`

#### `anti_triviality_filter(test_situations, is_factually_coherent=..., in_jurisdiction=..., is_feasible=..., is_artificial=...) → List[Situation]`

### 18.12 `mctev.flourishing.dimensions`

#### `class FlourishingProfile`

**Constructor**: `FlourishingProfile(values)`

| Method | Description |
|---|---|
| `__getitem__(dim)` | Access W/P/A/S/M |
| `from_measurement(x, operator)` | Build via M_c |
| `from_dict(d)` | Build from dict |
| `meets(thresholds)` | Boolean |

### 18.13 `mctev.analysis.metrics`

| Function | Measure |
|---|---|
| `dispersion_function_recognition(recognized_sets)` | \(D_F\) |
| `dispersion_weights(weight_vectors, metric="aitchison")` | \(D_\theta\) |
| `dispersion_viability_thresholds(configs)` | \(D_{\tau^V}\) |
| `dispersion_safeguard_thresholds(configs)` | \(D_{\tau^S}\) |
| `dispersion_flourishing_thresholds(configs)` | \(D_{\tau^H}\) |
| `dispersion_selection_conventions(configs, situations, maximizers)` | \(D_\rho\) |
| `dispersion_measurement_operators(configs, anchor_states)` | \(D_M\) |
| `dispersion_judgments(judgment_lists)` | \(D_J\) |
| `full_dispersion_vector(...)` | All |
| `aitchison_distance(w1, w2)` | Aitchison metric |

### 18.14 `mctev.simulation`

| Symbol | Description |
|---|---|
| `AgentType` | Enum: UNIVERSALIST, COLLECTIVIST, INDIVIDUALIST, SELF_REGARDING |
| `Agent` | Public-goods agent |
| `PublicGoodsGame` | Orchestrator |
| `ThreeSocietiesConfig` | Configuration |
| `run_three_societies(...)` | Returns `pd.DataFrame` |

**Note**: The simulation is a **hybrid proxy** utility model, not a full MCTEV implementation. See the paper's Supplement S9.

### 18.15 `mctev.cases`

| Function | Returns |
|---|---|
| `evaluate_slavery()` | `SlaveryDiagnosis` with proxy audit |
| `evaluate_capital_punishment()` | `CapitalPunishmentDiagnosis` with (R1)–(R3) |

### 18.16 `mctev.collapse` (deprecated)

Redirects to `mctev.instability` with a `DeprecationWarning`. Legacy aliases:
- `ConstraintViolationAnalyzer = BoundaryInstabilityAnalyzer`
- `ExitTimeResult = InstabilityResult`

## 19. Common Pitfalls and Troubleshooting

### 19.1 "Weights must sum to 1"

**Cause**: You passed weights that don't sum to 1.

**Fix**: Normalize before constructing:

```python
weights = np.array([...])
config = default_configuration(weights=weights)  # auto-normalizes
# Or explicitly:
weights = weights / weights.sum()
```

### 19.2 "Expected vector of length 6, got (5,)"

**Cause**: You tried to build a `ViabilityThresholds` from a 5-dimensional vector.

**Fix**: `ViabilityThresholds` has 6 entries (one per candidate function). `FlourishingThresholds` has 5 entries (one per flourishing dimension).

### 19.3 "Rejected: ValueError: Weights must be non-negative"

**Cause**: You passed negative weights.

**Fix**: Weight vectors must be in $\mathbb{R}_{\geq 0}^6$.

### 19.4 `judge()` returns `None`

**Cause**: No admissible actions (all filtered by constraints).

**Fix**: Check `admissible_actions(...)`. If empty, either relax constraints or provide actions that satisfy them.

### 19.5 Kernel computation takes too long

**Cause**: `grid_size**6 * horizon` is expensive.

**Fix**: Reduce `grid_size` to 4 or 5, or reduce `horizon`.

### 19.6 "TypeError: ... does not match ViabilityThresholds"

**Cause**: You passed a threshold family in the wrong slot (e.g., `SafeguardThresholds` in `viability_thresholds`).

**Fix**: This is intentional. Use the correct class for each slot.

### 19.7 Design B Δ_ε is negative

**Cause**: Possible reasons:
- The diffusion is too large; the trajectory exits regardless of proximity.
- The boundary point is not on ∂K_index.
- The inward distances are too small to matter.

**Fix**: Verify that `boundary_point` is close to the boundary via `safe_set.signed_distance(boundary_point) ≈ 0`. Increase `inward_distances`. Reduce `noise_scale`.

### 19.8 The convergence prediction `D_F < others` fails

**Cause**: Possible reasons:
- The recognized sets are very different across contexts (D_F is high).
- Some other dispersion measure is artificially low.

**Fix**: Verify your recognized sets. Check that D_θ, D_τ^V etc. are computed with sufficient data (at least 2 configurations).

## 20. Design Commitments and Rationale

### 20.1 Candidate, not dogma

The six Level 1 functions are exposed as an `Enum` with an explicit `MORAL_FUNCTION_ORDER`. The library does not assign each function to an epistemic tier (strict universal, robust regularity, weak regularity). That is a research target, not a library default.

### 20.2 Alignment, not derivation

The library is **methodologically aligned with** — but not formally derived from — the COH/GISMOL research program. `MCTEVSystem` is MCTEV's own composition; it is not a specialization of the COH 9-tuple.

### 20.3 Simulation-based evaluation, not proof

`BoundaryInstabilityAnalyzer` implements the **empirical evaluation** of the Boundary-Instability Hypothesis. It does not prove the hypothesis. The hypothesis is a research hypothesis and testing protocol.

### 20.4 Three threshold families are not interchangeable

Enforced by class types. Every class that holds thresholds holds exactly one family.

### 20.5 Simplex normalization is required

Enforced in `CulturalConfiguration.__post_init__`.

### 20.6 Proxy audit is heuristic

The proxy audit uses a common-proxy list. It catches the obvious cases but not all semantic circularity. Full independence may require human inspection.

### 20.7 Index/outcome distinction is explicit

`BoundaryInstabilityAnalyzer` takes separate `index_set` and `outcome_set` arguments. You cannot accidentally conflate them.

### 20.8 Retentionist conditions are explicit

The three conditions (R1)–(R3) are separately checkable. The library does not choose which condition is "correct"; that is a specification decision.

---

# Part V — Advanced Topics

## 21. Integration with COH/GISMOL

The library is **methodologically aligned with** the [COH/GISMOL](https://github.com/hongxueharriswang/gismol-lib) research program but is not a formal instantiation of the COH 9-tuple.

### 21.1 What MCTEV shares with COH

- **Hierarchical organization**: both decompose complex phenomena into levels.
- **Constraint propagation**: constraints flow downward, adaptation flows upward.
- **Adaptive dynamics**: both admit learning and evolution within constraints.

### 21.2 What MCTEV does not do

- Does **not** implement the COH 9-tuple formalism.
- Does **not** import theorems from COH.
- Does **not** claim formal instantiation.

### 21.3 The Ethical Constraint Hierarchy Principle

$$
\text{constraints} \xrightarrow{\text{downward}} \text{implementations} \xrightarrow{\text{downward}} \text{judgments}
$$

$$
\text{adaptation} \xrightarrow{\text{upward}} \text{implementations} \xrightarrow{\text{upward}} \text{functions}
$$

The library enforces this structurally: `MCTEVSystem` passes `configuration` down to `SituationalJudgment`, and `Agent.update_belief` provides upward adaptation in the simulation.

### 21.4 Full formal instantiation (future work)

A full formal instantiation would require:

1. Mapping each COH component to MCTEV's ethical domain.
2. Proving the instantiation reproduces MCTEV's predictions.
3. Showing the Boundary-Instability Hypothesis is preserved.

This is identified as future research in the paper (§18.3).

## 22. Numerical Considerations

### 22.1 Numerical integration

`Dynamics.step` uses forward Euler: `x_{t+1} = x_t + dt * F(x_t, config)`. This is stable for `dt < 2 / ||A||` when F is linear.

### 22.2 Noise scale

`set_specific_survival` and `BoundaryInstabilityAnalyzer.design_B` accept `noise_scale`. Recommended values:
- `0.01` — nearly deterministic.
- `0.02` — default.
- `0.05` — noisy.
- `0.10` — very noisy.

### 22.3 Grid resolution

`ViabilityKernel.grid_size` defaults to 8. For exploration:
- `4` → 4096 points.
- `5` → 15625 points.
- `6` → 46656 points.
- `8` → 262144 points.

### 22.4 Horizon

`ViabilityKernel.horizon` defaults to 500 Euler steps. Increase for slow dynamics, decrease for exploration.

## 23. Performance and Scaling

### 23.1 Bottlenecks

| Operation | Complexity |
|---|---|
| Kernel computation | \(O(g^6 \cdot h)\) |
| Boundary-Instability | \(O(n \cdot h)\) |
| Three Societies | \(O(n \cdot r \cdot a)\) |
| Judgment | \(O(a)\) |

### 23.2 Optimization tips

1. **Reduce grid size** for exploration.
2. **Parallelize** kernel computation across cells (use `multiprocessing`).
3. **Cache** kernel computations when varying only τ^S or τ^H (they don't change the kernel).
4. **Reduce horizon** for preliminary runs.

### 23.3 Parallelization example

```python
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from mctev.core.configuration import default_configuration
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.viability.kernel import compute_viable_region

def compute_for_config(name):
    cfg = default_configuration(
        name=name,
        weights=np.random.dirichlet(np.ones(6)),
    )
    kernel = compute_viable_region(
        constraints=default_constraints(thresholds=cfg.viability_thresholds),
        dynamics=LinearDynamics(),
        configuration=cfg,
        grid_size=4, horizon=80,
    )
    return name, kernel.fraction_viable()

with ProcessPoolExecutor() as pool:
    results = dict(pool.map(compute_for_config, [f"c{i}" for i in range(20)]))
print(results)
```

---

# Part VI — Appendices

## 24. Theoretical Foundations

### 24.1 Level-3 judgment

$$
j(s; \mathfrak{A}, \lambda_c) = \sigma_{\rho_c}\left(\operatorname*{arg\,max}_{a \in \mathcal{A}(s) \cap \mathcal{C}(s; \mathfrak{A}, \boldsymbol{\tau}_c^S)} \sum_f \theta_{c,f} u_f(a,s), \; s\right)
$$

### 24.2 Controlled viability kernel

$$
\mathcal{R}(\lambda_c; \Pi) = \left\{\mathbf{x}_0 \in \mathcal{V}(\lambda_c) : \exists \pi \in \Pi \text{ s.t. } \mathbf{x}^\pi(t) \in \mathcal{V}(\lambda_c) \; \forall t \geq 0\right\}
$$

### 24.3 Flourishing region

$$
\mathcal{F}(\lambda_c) = \{\mathbf{x} : \widehat{H}_c(\mathbf{x}) \geq \boldsymbol{\tau}_c^H\}
$$

### 24.4 Sustainable flourishing kernel

$$
\mathcal{R}_{\mathcal{F}}(\lambda_c; \Pi) = \mathrm{Viab}_\Pi(\mathcal{F}(\lambda_c) \cap \mathcal{V}(\lambda_c); F_{\lambda_c})
$$

### 24.5 Morality

$$
\mathrm{Morality}(\lambda_c) = \mathrm{Persistence}(\lambda_c) \wedge \mathrm{SustainableFlourishing}(\lambda_c)
$$

### 24.6 Set-specific survival

$$
q_{T,\mathcal{K}_{\text{out}}}^\pi(\mathbf{x}) = \mathbb{P}_\mathbf{x}^\pi\left[\mathbf{X}_t \in \mathcal{K}_{\text{out}} \;\forall t \in [0,T]\right]
$$

### 24.7 Design B estimand

$$
\Delta_\epsilon^{\mathcal{K}_{\text{index}}\to\mathcal{K}_{\text{out}}} = q_{T,\mathcal{K}_{\text{out}}}^\pi(\mathbf{x}_b - \epsilon_2 n_{\mathcal{K}_{\text{index}}}) - q_{T,\mathcal{K}_{\text{out}}}^\pi(\mathbf{x}_b - \epsilon_1 n_{\mathcal{K}_{\text{index}}})
$$

## 25. Glossary

| Term | Definition |
|---|---|
| **Level 1** | Candidate Level 1 moral functions and the architecture \(\mathfrak{A}\) |
| **Level 2** | Cultural-institutional configuration \(\lambda_c = (\theta, \tau^V, \tau^S, \tau^H, \rho, M)\) |
| **Level 3** | Situational judgment \(j(s; \mathfrak{A}, \lambda_c)\) |
| **Architecture** \(\mathfrak{A}\) | Bundle of function set, threshold domains, constraints, situation domains, selection class, measurement class, and qualifying conditions |
| **Configuration** \(\lambda_c\) | Concrete instantiation of Level 2 under a fixed architecture |
| **\(\tau^V\)** | Dynamical viability thresholds — define \(\mathcal{V}(\lambda_c)\) |
| **\(\tau^S\)** | Safeguard thresholds — define \(\mathcal{C}(s; \mathfrak{A}, \tau^S)\) |
| **\(\tau^H\)** | Flourishing thresholds — define \(\mathcal{F}(\lambda_c)\) |
| **\(\rho_c\)** | Selection convention — resolves ties among maximizers |
| **\(M_c\)** | Measurement operator — maps states to observed flourishing |
| **\(Q_{-i}\)** | Qualifying condition for deriving \(f_i\) — excludes \(f_i\) |
| **Proxy audit** | Heuristic check that \(Q_{-i}\) doesn't contain proxies for \(f_i\) |
| **\(\mathcal{R}(\lambda_c; \Pi)\)** | Controlled viability region — one component of moral assessment |
| **\(\mathcal{R}_{\mathcal{F}}\)** | Sustainable flourishing kernel |
| **\(\mathcal{K}_{\text{index}}\)** | Index boundary set — whose proximity is measured |
| **\(\mathcal{K}_{\text{out}}\)** | Outcome set — whose survival is evaluated |
| **(R1)–(R3)** | Retentionist conditions — architectural non-exclusion, weak non-vacuity, strong non-vacuity |
| **COH** | Constrained Object Hierarchies — the framework MCTEV is aligned with |
| **GISMOL** | General Intelligent System Modelling Language — toolkit for COH |

## 26. References

### Primary sources

- **Wang, H. (2026).** *Toward a Computational Science of Ethics: A Multi-Level Computational Theory of Ethical Variation and Candidate Level 1 Moral Functions.* (Main paper.)
- **Wang, H. (2025).** Constrained object hierarchies as a unified theoretical model for intelligence and intelligent systems. *Computers*, *14*, 478.

### Viability theory

- **Aubin, J.-P. (1991).** *Viability Theory.* Birkhäuser.
- **Blanchini, F. (1999).** Set invariance in control. *Automatica*, *35*(11), 1747–1767.
- **Freidlin, M. I., & Wentzell, A. D. (2012).** *Random Perturbations of Dynamical Systems* (3rd ed.). Springer.
- **Mitchell, I. M., Bayen, A. M., & Tomlin, C. J. (2005).** A time-dependent Hamilton-Jacobi formulation of reachable sets. *IEEE TAC*, *50*(7), 947–957.
- **Abate, A., et al. (2008).** Probabilistic reachability and safety. *Automatica*, *44*(11), 2724–2734.

### Moral psychology

- **Awad, E., et al. (2018).** The Moral Machine experiment. *Nature*, *563*, 59–64.
- **Atari, M., et al. (2023).** Morality beyond the WEIRD. *JPSP*, *125*(6), 1157–1188.
- **Doğruyol, B., et al. (2019).** The five-factor model of the moral foundations theory. *Personality and Individual Differences*, *151*, 109547.
- **Haidt, J., & Graham, J. (2007).** When morality opposes justice. *Social Justice Research*, *20*(1), 98–116.

### Flourishing

- **VanderWeele, T. J. (2017).** On the promotion of human flourishing. *PNAS*, *114*(31), 8148–8156.
- **OECD (2020).** *How's Life? 2020.* OECD Publishing.
- **Sen, A. (1999).** *Development as Freedom.* Oxford University Press.
- **Nussbaum, M. C. (2011).** *Creating Capabilities.* Harvard University Press.

### Functionalist sociology

- **Durkheim, É. (1893/1984).** *The Division of Labour in Society.* Macmillan.
- **Parsons, T. (1951).** *The Social System.* Free Press.
- **Ostrom, E. (1990).** *Governing the Commons.* Cambridge University Press.
- **Holling, C. S. (1973).** Resilience and stability of ecological systems. *Annual Review of Ecology and Systematics*, *4*, 1–23.
- **Folke, C. (2006).** Resilience. *Global Environmental Change*, *16*(3), 253–267.
- **Boyd, R., & Richerson, P. J. (1985).** *Culture and the Evolutionary Process.* University of Chicago Press.
- **Henrich, J. (2004).** Cultural group selection. *JEBO*, *53*(1), 3–35.

### Computational ethics

- **Tennant, E., Hailes, S., & Musolesi, M. (2024).** Dynamics of moral behavior in heterogeneous populations of learning agents. *AIES*, *7*(1), 1444–1454.

### AI alignment

- **Bai, Y., et al. (2022).** Constitutional AI: Harmlessness from AI feedback. arXiv:2212.08073.
- **Ouyang, L., et al. (2022).** Training language models to follow instructions with human feedback. *NeurIPS*, *35*, 27730–27744.

### Philosophical background

- **Rawls, J. (1971).** *A Theory of Justice.* Harvard University Press.
- **Nozick, R. (1974).** *Anarchy, State, and Utopia.* Basic Books.
- **Skyrms, B. (1996).** *Evolution of the Social Contract.* Cambridge University Press.

---

## Documentation License

This user guide is released under the same MIT license as `mctev-lib`.

## Getting Help

- **Bugs and feature requests**: open an issue on the [project repository](https://github.com/hongxueharriswang/mctev-lib).
- **Theoretical questions**: consult the primary paper first; §18 points to the relevant paper sections.
- **Migration from v0.1.0**: see [`MIGRATION.md`](./MIGRATION.md).
- **Interactive learning**: see [`TUTORIAL.md`](./TUTORIAL.md).

---

**End of User Guide.**