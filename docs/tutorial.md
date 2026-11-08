# mctev-lib v0.2.0 — Comprehensive Tutorial

**A hands-on journey from zero to a complete computational ethics system under the revised MCTEV framework**

Companion to the [User Guide](./USER_GUIDE.md), the [Migration Guide](./MIGRATION.md), and the [MCTEV paper](../MCTEV_PAPER.md).

---

## How This Tutorial Works

Each chapter:

1. States a **learning objective** tied to a specific manuscript section.
2. Introduces a **concept** from the paper with the section reference.
3. Provides **runnable code** you can copy-paste.
4. Shows the **expected output** so you can verify.
5. Ends with **self-check exercises**.

**Prerequisites**: Python 3.10+, `mctev-lib` 0.2.0 installed (`pip install -e .`).

**Time estimate**: 8–10 hours for a thorough pass.

**What you'll build**: A working cross-cultural AI policy evaluator, a Boundary-Instability dashboard with the three designs of Section 10.6, a retentionist/abolitionist comparison tool, and a dispersion report across eight measures.

---

## What's New Relative to the v0.1.0 Tutorial

If you completed the earlier tutorial, the key changes are:

| Concept | v0.1.0 tutorial | v0.2.0 tutorial |
|---|---|---|
| Level-2 object | `CulturalParameters` (θ only) | `CulturalConfiguration` (full λ_c) |
| Thresholds | Single `ViabilityConstraints` | Three families `τ^V, τ^S, τ^H` |
| Tie-breaking | Implicit | `SelectionConvention` (ρ_c) |
| Flourishing | Direct values | Measured via `M_c` |
| Collapse analysis | `ConstraintViolationAnalyzer` | `BoundaryInstabilityAnalyzer` with index/outcome sets |
| Capital punishment | Single profile | Retentionist conditions (R1)–(R3) |
| Qualifying conditions | Not present | `Q_{-i}` + proxy audit |
| Dispersion | 2 measures | 8 measures |

Chapters that assume the older library are marked **`[UPDATED]`**.

---

## Table of Contents

**Part I — Foundations**
- [Chapter 1: The Mental Model](#chapter-1-the-mental-model)
- [Chapter 2: Setup and Workspace](#chapter-2-setup-and-workspace)
- [Chapter 3: Your First Full-Configuration Judgment](#chapter-3-your-first-full-configuration-judgment)

**Part II — The Three Levels**
- [Chapter 4: Level 1 — Candidate Functions and Architectures](#chapter-4-level-1--candidate-functions-and-architectures)
- [Chapter 5: Level 2a — Three Threshold Families](#chapter-5-level-2a--three-threshold-families)
- [Chapter 6: Level 2b — The Full Configuration λ_c](#chapter-6-level-2b--the-full-configuration-λ_c)
- [Chapter 7: Level 2c — Selection Conventions and Measurement Operators](#chapter-7-level-2c--selection-conventions-and-measurement-operators)
- [Chapter 8: Level 3 — Situational Judgments with A(s)](#chapter-8-level-3--situational-judgments-with-as)

**Part III — Evaluation Layer**
- [Chapter 9: The Controlled Viability Region](#chapter-9-the-controlled-viability-region)
- [Chapter 10: Flourishing Measurement](#chapter-10-flourishing-measurement)
- [Chapter 11: Viable Current vs Sustainable Flourishing](#chapter-11-viable-current-vs-sustainable-flourishing)

**Part IV — Dynamics**
- [Chapter 12: Boundary-Instability — the Index/Outcome Distinction](#chapter-12-boundary-instability--the-indexoutcome-distinction)
- [Chapter 13: The Three Designs of Section 10.6](#chapter-13-the-three-designs-of-section-106)
- [Chapter 14: Retentionist Conditions (R1)–(R3)](#chapter-14-retentionist-conditions-r1r3)

**Part V — Applications**
- [Chapter 15: Qualifying Conditions and the Proxy Audit](#chapter-15-qualifying-conditions-and-the-proxy-audit)
- [Chapter 16: The Slavery Case Study](#chapter-16-the-slavery-case-study)
- [Chapter 17: The Capital Punishment Case Study](#chapter-17-the-capital-punishment-case-study)

**Part VI — Dispersion Analysis**
- [Chapter 18: Eight Dispersion Measures](#chapter-18-eight-dispersion-measures)

**Part VII — Consolidation**
- [Chapter 19: Exercises](#chapter-19-exercises)
- [Chapter 20: Capstone Project](#chapter-20-capstone-project)
- [Chapter 21: Where to Go From Here](#chapter-21-where-to-go-from-here)

---

# Part I — Foundations

## Chapter 1: The Mental Model

### Learning objective

Build a working mental model of the **full Level-2 configuration** λ_c that will anchor every subsequent chapter.

### The three-level architecture (unchanged)

```
Level 1:  Candidate Level 1 moral functions and architecture A
                    ↓  (constraints propagate downward)
Level 2:  Cultural-institutional configuration λ_c
                    ↓  (constraints propagate downward)
Level 3:  Situational judgments j(s; A, λ_c)
```

### What changed in v0.2.0: Level 2 is now six components, not one

In the earlier manuscript, Level 2 was just θ_c (function weights). In the **current manuscript** (Section 7.2), Level 2 is:

$$
\lambda_c = (\theta_c, \boldsymbol{\tau}_c^V, \boldsymbol{\tau}_c^S, \boldsymbol{\tau}_c^H, \rho_c, M_c)
$$

Each component acts on a **different object**:

| Component | Symbol | Acts on | Wrong example |
|---|---|---|---|
| Function weights | θ_c | Balancing the six candidate functions | Using θ_c to set a wrongful-conviction threshold |
| Viability thresholds | τ^V | Society-level state viability V(λ_c) | Using τ^V to gate a specific action |
| Safeguard thresholds | τ^S | Action admissibility C(s; A, τ^S) | Using τ^S to define societal cooperation viability |
| Flourishing thresholds | τ^H | Membership in F(λ_c) | Using τ^H as a wrongdoing threshold |
| Selection convention | ρ_c | Resolving ties among maximizers | Confusing with weights (both are policy choices, but at different levels) |
| Measurement operator | M_c | Mapping states to observed flourishing indicators | Using M_c to define what flourishing *is* |

**The most important lesson of this tutorial**: **do not conflate these six**. Every chapter will hammer this point.

### The full picture at a glance

```
┌─────────────────────────────────────────────────────────────────┐
│  LEVEL 1  (A = (ℱ₁, T_V^{L1}, T_S^{L1}, T_H^{L1}, C^{L1},       │
│              S^{dom}, S^{req}, P_A, M_A, Q))                     │
└─────────────────────────────────────────────────────────────────┘
                          │ constrains
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  LEVEL 2  (λ_c = (θ_c, τ^V, τ^S, τ^H, ρ_c, M_c))                │
│                                                                  │
│    θ_c ∈ Δ⁵        ← weights                                    │
│    τ^V             ← dynamical viability thresholds              │
│    τ^S             ← safeguard thresholds                        │
│    τ^H             ← flourishing thresholds                      │
│    ρ_c             ← selection convention                        │
│    M_c             ← measurement operator                        │
└─────────────────────────────────────────────────────────────────┘
                          │ constrains
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│  LEVEL 3  (j(s; A, λ_c) = σ_{ρ_c}(J(s; A, λ_c), s))              │
│                                                                  │
│    J(s; A, λ_c) = argmax over A(s) ∩ C(s; A, τ^S) of            │
│                    Σ_f θ_{c,f} · u_f(a, s)                       │
└─────────────────────────────────────────────────────────────────┘
```

### Why three threshold families?

A concrete example from the manuscript (§12.2):

- **Wrongful-conviction rate threshold** is a **safeguard** τ^S. It gates whether *the action* "execute" is admissible in *a specific case*.
- **Minimum cooperation rate** is a **dynamical viability** τ^V. It gates whether *a state of the world* is viable.
- **Minimum agency** is a **flourishing** τ^H. It gates whether *a state of the world* counts as flourishing.

If you use the same threshold class for all three, you will systematically:
- Classify societies as unviable when their *procedural safeguards* are strict.
- Call executions admissible when societal *cooperation* is high.
- Confuse flourishing with thriving.

The library makes this mistake **impossible** at the type level.

### Self-check 1

Before continuing:
- [ ] Can you name all six components of λ_c?
- [ ] For each, can you name a different object it governs?
- [ ] Why is "using θ_c to gate actions" a category error?

### Paper reference

Section 7.1 (architecture), Section 7.2 (configuration), Section 7.4 (Level 3).

---

## Chapter 2: Setup and Workspace

### Learning objective

A reproducible working directory with smoke tests.

### Step 2.1: Verify installation

```bash
python -c "import mctev; print(mctev.__version__)"
# Expected: 0.2.0
```

### Step 2.2: Directory structure

```bash
mkdir mctev-tutorial
cd mctev-tutorial
mkdir experiments outputs
```

### Step 2.3: Smoke test

```python
# experiments/ch02_smoke_test.py
"""Verify all v0.2.0 imports work."""

from mctev import (
    # Core
    MoralFunction, MoralFunctionProfile, MoralUtilityLibrary,
    MORAL_FUNCTION_ORDER, N_FUNCTIONS,
    # Thresholds
    ViabilityThresholds, SafeguardThresholds, FlourishingThresholds,
    ThresholdFamilies,
    # Configuration
    CulturalConfiguration,
    # Selection / measurement
    SelectionConvention, MeasurementOperator, LinearMeasurement,
    # Qualifying
    QualifyingConditions, QualifyingCondition,
    # Situational
    Situation, Action, SituationalJudgment, ConstraintPredicate,
    # Hierarchy
    MCTEVSystem,
    # Viability
    ViabilityConstraints, LinearDynamics, Dynamics,
    ViabilityKernel, compute_viable_region,
    # Instability
    SafeSet, IndicatorSafeSet, KernelSafeSet,
    BoundaryInstabilityAnalyzer, InstabilityResult,
    set_specific_survival,
    # Flourishing
    FlourishingProfile, FlourishingDimension,
    # Retentionist
    Architecture, RetentionistArchitecture, AbolitionistArchitecture,
    check_R1, check_R2, check_R3,
)

print(f"mctev version: 0.2.0")
print(f"N_FUNCTIONS = {N_FUNCTIONS}")
print(f"Selection conventions: {[c.value for c in SelectionConvention]}")
print("All v0.2.0 imports OK.")
```

Run:

```bash
python experiments/ch02_smoke_test.py
```

Expected output:

```
mctev version: 0.2.0
N_FUNCTIONS = 6
Selection conventions: ['precedent', 'minimum_intervention', 'status_quo', 'lexicographic', 'random']
All v0.2.0 imports OK.
```

### Self-check 2

- [ ] `mctev.__version__ == "0.2.0"`
- [ ] All imports succeed
- [ ] Five selection conventions visible

### Paper reference

Sections 7.1, 7.2, 7.4.

---

## Chapter 3: Your First Full-Configuration Judgment

### Learning objective

Build a complete λ_c and use it to judge a situation.

### The setup

A three-person cake division with three candidate actions:

- `a_selfish`: 80 / 20 / 0
- `a_balanced`: 60 / 40 / 0
- `a_generous`: 40 / 40 / 20

We want to know how a **universalist** configuration decides.

### The code

```python
# experiments/ch03_first_judgment.py
"""Chapter 3: A full-configuration judgment."""

import numpy as np

from mctev.core.moral_functions import MoralFunction, MoralUtilityLibrary
from mctev.core.configuration import default_configuration
from mctev.core.selection import SelectionConvention
from mctev.core.situational import Action, Situation, SituationalJudgment

# ---- Step 1: define per-function utilities ----
lib = MoralUtilityLibrary()
# cooperation: utility = share given to others
lib[MoralFunction.COOPERATION] = lambda a, s: 1.0 - float(a.payload)
# distribution: utility peaks when shares are equal
lib[MoralFunction.RESOURCE_DISTRIBUTION] = (
    lambda a, s: 1.0 - float(a.payload)
)
# care: utility = weakest share (payload encodes inequality, so penalize high payload)
care_map = {"a_selfish": 0.0, "a_balanced": 0.0, "a_generous": 0.2}
lib[MoralFunction.REPRODUCTION_CARE] = lambda a, s: care_map[a.name]

# ---- Step 2: build a full configuration λ_c ----
config = default_configuration(
    name="universalist",
    weights=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05],
    viability_value=0.30,
    safeguard_values={"error_rate": 0.05},
    flourishing_value=0.50,
    selection=SelectionConvention.STATUS_QUO,
)
print(config)
# CulturalConfiguration(name='universalist', weights=[0.3, 0.2, 0.2, 0.15, 0.1, 0.05], ρ=status_quo)

# ---- Step 3: define the situation and actions ----
situation = Situation("cake split", {"people": 3})
actions = [
    Action("a_selfish",  payload=0.80),
    Action("a_balanced", payload=0.20),
    Action("a_generous", payload=0.20),
]

# ---- Step 4: judge ----
solver = SituationalJudgment(utilities=lib)

# The correspondence J(s; A, λ_c)
J = solver.correspondence(situation, actions, config)
print(f"Correspondence: {[a.name for a in J]}")
# ['a_balanced', 'a_generous']

# The selection j(s; A, λ_c) = σ_{ρ_c}(J)
best = solver.judge(situation, actions, config)
print(f"Selected action: {best.name}")
# 'a_balanced' (status-quo fallback)

# Full ranking
for score, action in solver.rank(situation, actions, config):
    print(f"  {score:+.3f}  {action.name}")
#  +0.72  a_balanced
#  +0.52  a_generous
#  +0.20  a_selfish
```

### What just happened

1. **Level 1**: You defined three candidate functions and utilities.
2. **Level 2**: You built a **full configuration** λ_c with all six components — not just θ_c.
3. **Level 3**: You computed the correspondence J (set of maximizers), then applied the selection function σ_{ρ_c} to get a single action.

### Self-check 3

- [ ] Run the script; verify `a_balanced` is selected.
- [ ] Change `selection=SelectionConvention.LEXICOGRAPHIC` with `lexicographic_key=lambda a: a.name`. Does the output change?
- [ ] Change the weights and re-run. Does the correspondence change?

### Exercise 3.1

Modify the script so that `a_selfish` is disallowed by a safeguard `payload < 0.7`. Pass a constraint predicate to `SituationalJudgment` that reads `config.safeguard_thresholds`. Verify that `a_selfish` never appears in the correspondence.

### Paper reference

Sections 7.2, 7.4.

---

# Part II — The Three Levels

## Chapter 4: Level 1 — Candidate Functions and Architectures

### Learning objective

Understand the six candidate functions and the **architecture object** \(\mathfrak{A}\) they belong to.

### The six functions

(Unchanged from v0.1.0.)

```python
# experiments/ch04_functions.py
from mctev.core.moral_functions import (
    MoralFunction, MORAL_FUNCTION_ORDER, N_FUNCTIONS,
)

for f in MORAL_FUNCTION_ORDER:
    print(f"{f.value:15s}  {f.description}")
```

### The architecture object \(\mathfrak{A}\) (conceptual)

In the manuscript, \(\mathfrak{A}\) bundles the six functions with:

- three threshold **domains** \(T_V^{L1}, T_S^{L1}, T_H^{L1}\) (not the thresholds themselves)
- the non-compensatory constraints \(C^{L1}\)
- the situation domain \(S^{dom}\) and required-coverage domain \(S^{req}\)
- the admissible selection-convention class \(P_A\)
- the admissible measurement-operator class \(M_A\)
- the qualifying conditions \(Q = (Q_{-1}, \ldots, Q_{-6})\)

The library does not expose \(\mathfrak{A}\) as a single class because most users work with **one** architecture at a time. The architecture's components are distributed across:

| \(\mathfrak{A}\) component | Where it lives in the library |
|---|---|
| \(\mathcal{F}_1\) | `MoralFunction` enum (fixed) |
| \(T_V^{L1}, T_S^{L1}, T_H^{L1}\) | Validated in `CulturalConfiguration.__post_init__` |
| \(C^{L1}\) | The `constraint_predicate` you supply to `SituationalJudgment` |
| \(S^{dom}, S^{req}\) | Implicit in the situations you pass |
| \(P_A\) | `SelectionConvention` enum (fixed) |
| \(M_A\) | Validated by `MeasurementOperator` subclasses |
| \(Q\) | `QualifyingConditions` object |

When you need to compare architectures explicitly (Chapter 14), the `RetentionistArchitecture` and `AbolitionistArchitecture` classes capture \(C^{L1}\).

### Self-check 4

- [ ] Run the script.
- [ ] Explain why \(T_V^{L1}\) is a **domain** (set of admissible values), not a specific value.

### Paper reference

Section 6 (functions), Section 7.1 (architecture).

---

## Chapter 5: Level 2a — Three Threshold Families

### Learning objective

Build each of the three threshold families and understand why they are not interchangeable.

### The three families

```python
# experiments/ch05_three_families.py
from mctev.core.thresholds import (
    ViabilityThresholds, SafeguardThresholds, FlourishingThresholds,
    ThresholdFamilies,
)
from mctev.core.moral_functions import MoralFunction

# ---- τ^V — dynamical viability thresholds ----
tau_V = ViabilityThresholds.from_dict({
    "cooperation":    0.40,
    "conflict":       0.30,
    "distribution":   0.35,
    "care":           0.30,
    "information":    0.30,
    "sustainability": 0.25,
})
print("τ^V (dynamical viability):", tau_V.as_dict())

# ---- τ^S — safeguard thresholds ----
tau_S = SafeguardThresholds.from_dict({
    "error_rate":  0.05,   # wrongful-conviction rate threshold
    "disparity":   0.10,   # discrimination threshold
    "consistency": 0.80,   # non-arbitrariness threshold
})
print("τ^S (safeguard):", tau_S.as_dict())

# ---- τ^H — flourishing thresholds ----
tau_H = FlourishingThresholds.from_dict({
    "W": 0.50,
    "P": 0.50,
    "A": 0.60,   # agency is set higher
    "S": 0.50,
    "M": 0.50,
})
print("τ^H (flourishing):", tau_H.as_dict())

# ---- Container ----
families = ThresholdFamilies(
    viability=tau_V, safeguard=tau_S, flourishing=tau_H,
)
print("\nAll three families:")
for family, values in families.as_dict().items():
    print(f"  {family}: {values}")
```

### Why the families are structurally distinct

Consider the **wrongful-conviction rate threshold** `error_rate = 0.05`.

- It is a **safeguard** τ^S. It gates whether the *action* "execute" is admissible in *a specific case*.
- It is **not** a viability threshold τ^V. A society is not unviable because its error rate is high; only the *action* is inadmissible.
- It is **not** a flourishing threshold τ^H. Flourishing doesn't require anything about error rates; those depend on the *institution's* procedural reliability, not on the state's flourishing.

If you used `error_rate = 0.05` as a **viability** threshold, you would be claiming that a society becomes non-viable when its error rate exceeds 5%. That is a category error.

The library enforces the distinction by using three different classes. You cannot accidentally pass `SafeguardThresholds` where `ViabilityThresholds` is expected.

### Self-check 5

- [ ] Run the script; verify all three families print correctly.
- [ ] Try `ViabilityThresholds.from_dict({"error_rate": 0.05})` — this should fail because `error_rate` is not a `MoralFunction`.
- [ ] Try to construct a `CulturalConfiguration` that puts `SafeguardThresholds` in the `viability_thresholds` slot — this should fail at construction.

### Exercise 5.1

Design a `SafeguardThresholds` with three safeguards: `error_rate`, `disparity`, `procedural_integrity`. Then design a `ViabilityThresholds` with all six functions set at 0.3. Verify that the two objects cannot be swapped in a `CulturalConfiguration` (they'll raise a `TypeError`).

### Paper reference

Section 7.1.

---

## Chapter 6: Level 2b — The Full Configuration λ_c

### Learning objective

Build and validate a `CulturalConfiguration` with all six components.

### The full construction

```python
# experiments/ch06_full_config.py
import numpy as np

from mctev.core.configuration import CulturalConfiguration, default_configuration
from mctev.core.thresholds import (
    ViabilityThresholds, SafeguardThresholds, FlourishingThresholds,
)
from mctev.core.selection import SelectionConvention
from mctev.core.measurement import LinearMeasurement

# ---- Explicit construction ----
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
print(config)
print()
print("Full configuration as dict:")
import json
print(json.dumps(config.to_dict(), indent=2))
```

Expected output:

```
CulturalConfiguration(name='universalist', weights=[0.3, 0.2, 0.2, 0.15, 0.1, 0.05], ρ=status_quo)

Full configuration as dict:
{
  "name": "universalist",
  "weights": {
    "cooperation": 0.3,
    "conflict": 0.2,
    "distribution": 0.2,
    "care": 0.15,
    "information": 0.1,
    "sustainability": 0.05
  },
  "viability_thresholds": {...},
  "safeguard_thresholds": {"error_rate": 0.05, "disparity": 0.1},
  "flourishing_thresholds": {...},
  "selection_convention": "status_quo",
  "measurement_operator": "LinearMeasurement"
}
```

### Simplex validation

`CulturalConfiguration` enforces the **simplex normalization** condition from the manuscript (Section 7.2):

```python
# weights must sum to 1
try:
    bad = CulturalConfiguration(
        weights=np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0]),  # sums to 6
        ...
    )
except ValueError as e:
    print(f"Rejected: {e}")
# Rejected: Weights must sum to 1 (simplex normalization); got sum = 6.0
```

### The convenience constructor

`default_configuration` fills sensible defaults:

```python
config2 = default_configuration(
    name="collectivist",
    weights=[0.25, 0.15, 0.15, 0.30, 0.10, 0.05],
    selection=SelectionConvention.PRECEDENT,
)
print(config2)
```

### Self-check 6

- [ ] Run the script; verify the dict output.
- [ ] Change `weights` to a non-normalized vector; verify the error message.
- [ ] Add a `safeguard_values` argument with two safeguards; verify both appear in the dict.

### Exercise 6.1

Construct two configurations:
1. `strict_retentionist`: `safeguard_values={"error_rate": 0.001}`
2. `permissive_retentionist`: `safeguard_values={"error_rate": 0.20}`

Show that the two configurations differ **only** in the safeguard threshold, not in weights, viability thresholds, or flourishing thresholds. This is the "configuration-specific non-vacuity" scenario of Section 12.3.

### Paper reference

Section 7.2.

---

## Chapter 7: Level 2c — Selection Conventions and Measurement Operators

### Learning objective

Master the two "policy-like" components of λ_c.

### Selection conventions ρ_c

The judgment correspondence J(s; A, λ_c) may have multiple maximizers. The **selection convention ρ_c** resolves ties.

```python
# experiments/ch07_selection.py
from mctev.core.selection import SelectionConvention, select_action
from mctev.core.situational import Action, Situation

# Five maximizers (a tie)
maximizers = [Action("a"), Action("b"), Action("c")]
situation = Situation("tie-break", {"status_quo": "b"})

# Convention 1: status_quo — choose the status-quo action if it maximizes
chosen = select_action(
    convention=SelectionConvention.STATUS_QUO,
    maximizers=maximizers, situation=situation,
)
print(f"STATUS_QUO: {chosen.name}")  # 'b'

# Convention 2: precedent — choose closest to previous
chosen = select_action(
    convention=SelectionConvention.PRECEDENT,
    maximizers=maximizers, situation=situation,
    previous_action=Action("c"),
)
print(f"PRECEDENT: {chosen.name}")  # 'c'

# Convention 3: minimum_intervention — choose smallest payload
payload_actions = [
    Action("a", 0.5), Action("b", 0.1), Action("c", 0.9),
]
chosen = select_action(
    convention=SelectionConvention.MINIMUM_INTERVENTION,
    maximizers=payload_actions, situation=situation,
)
print(f"MINIMUM_INTERVENTION: {chosen.name}")  # 'b'

# Convention 4: lexicographic
chosen = select_action(
    convention=SelectionConvention.LEXICOGRAPHIC,
    maximizers=maximizers, situation=situation,
    lexicographic_key=lambda a: a.name,
)
print(f"LEXICOGRAPHIC: {chosen.name}")  # 'a'

# Convention 5: random
import numpy as np
rng = np.random.default_rng(42)
chosen = select_action(
    convention=SelectionConvention.RANDOM,
    maximizers=maximizers, situation=situation, rng=rng,
)
print(f"RANDOM: {chosen.name}")  # varies with seed
```

**Why ρ_c is separate from θ_c**: two cultures could share the same weights but differ in how they break ties. The selection convention is a **separate policy choice** at Level 2. It is not a moral weight; it is a **procedural commitment**.

### Measurement operators M_c

The measurement operator maps a state x to observed flourishing indicators Ĥ_c(x). It is the Level-2 component that operationalizes flourishing.

```python
# experiments/ch07_measurement.py
import numpy as np
from mctev.core.measurement import (
    LinearMeasurement, validate_cross_context_comparability,
)

# Identity measurement
identity = LinearMeasurement(to_core=lambda x: np.asarray(x)[:5])
state = np.array([0.7, 0.6, 0.55, 0.8, 0.65, 0.5])
print(f"Identity measurement: {identity.measure(state)}")

# Nonlinear measurement (monotone transform on agency)
agency_boosted = LinearMeasurement(
    to_core=lambda x: np.asarray(x)[:5],
    monotone_transforms={2: lambda v: v ** 0.7},  # agency more generous
)
print(f"Agency-boosted: {agency_boosted.measure(state)}")

# Cross-context comparability check (Section 8.2)
# Without anchors/linking, they are NOT comparable
report = validate_cross_context_comparability(identity, agency_boosted)
print(f"Without anchors: {report}")
# {'comparable': False, 'mechanism': 'unavailable'}

# With anchor states, they may be comparable
anchors = [np.array([0.5]*6), np.array([0.7]*6)]
report = validate_cross_context_comparability(
    identity, agency_boosted, anchor_states=anchors,
)
print(f"With anchors: {report}")
# {'comparable': True/False, 'mechanism': 'anchors', 'mean_discrepancy': ...}
```

**Why M_c matters**: In the manuscript (§8.2), a cultural context **cannot** lower its flourishing thresholds below the architecture's admissible range, nor can it select a measurement operator that reverses the ordering of states. Without the validity checks, a context could game the flourishing classification by choosing a biased measurement operator.

### Self-check 7

- [ ] Run both scripts.
- [ ] Verify that `STATUS_QUO` picks `b` when `status_quo="b"`.
- [ ] Verify that without anchors, cross-context comparability is `"unavailable"`.

### Exercise 7.1

Design a `MeasurementOperator` subclass that: (a) applies a monotone transform on all five dimensions, (b) adds Gaussian noise with `noise_std=0.05`. Test its within-context monotonicity using `operator.within_context_monotone`.

### Paper reference

Sections 7.4 (selection), 8.2 (measurement).

---

## Chapter 8: Level 3 — Situational Judgments with A(s)

### Learning objective

Use **situation-dependent action sets** and understand the full judgment pipeline.

### What changed since v0.1.0

In v0.1.0, `SituationalJudgment` accepted a static list of `Action`s. In v0.2.0, the action set is **situation-dependent**: \(\mathcal{A}(s)\), not \(\mathcal{A}\).

The library supports this by letting you pass **any iterable of actions** — you build \(\mathcal{A}(s)\) from the situation as you like.

```python
# experiments/ch08_dynamic_actions.py
from mctev.core.configuration import default_configuration
from mctev.core.moral_functions import MoralFunction, MoralUtilityLibrary
from mctev.core.situational import Action, Situation, SituationalJudgment


def action_generator(situation: Situation):
    """Build A(s) from the situation context."""
    budget = situation.context.get("budget", 10)
    return [
        Action("small",  0.2 * budget),
        Action("medium", 0.5 * budget),
        Action("large",  0.8 * budget),
    ]


lib = MoralUtilityLibrary()
lib[MoralFunction.COOPERATION] = lambda a, s: float(a.payload) / 10.0

config = default_configuration(
    name="universalist",
    weights=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05],
)

solver = SituationalJudgment(utilities=lib)

for budget in [10, 100]:
    situation = Situation("alloc", {"budget": budget})
    actions = action_generator(situation)
    print(f"\nBudget {budget}: A(s) = {[a.name for a in actions]}")
    best = solver.judge(situation, actions, config)
    print(f"Selected: {best.name}")
```

### The full pipeline (formally)

For each situation s:

1. **Build A(s)** — situation-dependent action set.
2. **Filter by C(s; A, τ^S)** — apply safeguard constraints (from `config.safeguard_thresholds`).
3. **Compute J(s; A, λ_c)** — argmax over A(s) ∩ C(s; A, τ^S) of Σ_f θ_{c,f} · u_f(a, s).
4. **Apply σ_{ρ_c}** — resolve ties via the selection convention.

Each step corresponds to a method:

```python
# 1. A(s) built by user
actions = action_generator(situation)

# 2. C(s; A, τ^S) applied
admissible = solver.admissible_actions(actions, situation, config)

# 3. J(s; A, λ_c) — full correspondence
J = solver.correspondence(situation, actions, config)

# 4. σ_{ρ_c}(J) — final action
selected = solver.judge(situation, actions, config)
```

### Constraints that read τ^S

The constraint predicate should **inspect config.safeguard_thresholds**:

```python
def make_safeguard_constraint(situation, action, config):
    """Example: gate 'execute' on the error-rate safeguard."""
    if action.name != "execute":
        return True
    tau_error = config.safeguard_thresholds.get("error_rate", 0.05)
    observed_error = situation.context.get("observed_error_rate", 0.0)
    return observed_error <= tau_error


solver_with_constraints = SituationalJudgment(
    utilities=lib, constraints=make_safeguard_constraint,
)
```

The constraint predicate receives **(situation, action, configuration)**. This gives it access to τ^S while keeping τ^V and τ^H out of the action-level decision (they act on state viability and flourishing, not on actions).

### Self-check 8

- [ ] Run the script; verify that A(s) scales with budget.
- [ ] Add a safeguard constraint that filters on `error_rate`; verify that only admissible actions are considered.

### Exercise 8.1

Write an `action_generator` that returns different actions for different `situation.context["role"]` values (e.g., "doctor", "administrator", "patient"). Show that the correspondence J changes across roles even when the configuration λ_c and utilities are held fixed. This demonstrates Level-3 situational variation.

### Paper reference

Sections 7.4.

---

# Part III — Evaluation Layer

## Chapter 9: The Controlled Viability Region

### Learning objective

Compute the controlled viability kernel \(\mathcal{R}(\lambda_c; \Pi)\) using the viability thresholds τ^V.

### The setup

```python
# experiments/ch09_viability_kernel.py
import numpy as np
from mctev.core.configuration import default_configuration
from mctev.core.thresholds import ViabilityThresholds
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.viability.kernel import compute_viable_region

# Configuration with τ^V
config = default_configuration(name="universalist")
print(f"τ^V: {config.viability_thresholds.as_dict()}")

# Constraints use τ^V
constraints = default_constraints(thresholds=config.viability_thresholds)

# Dynamics
dynamics = LinearDynamics()

# Kernel computation
kernel = compute_viable_region(
    constraints=constraints,
    dynamics=dynamics,
    configuration=config,
    grid_size=5,
    horizon=100,
)
print(f"Fraction viable: {kernel.fraction_viable():.2%}")
# Fraction viable: ~15-25% depending on random seed
```

### Naming: "controlled viability region"

The set \(\mathcal{R}(\lambda_c; \Pi)\) is a **controlled viability kernel**, not "the set of morally permissible states." The manuscript (§7.5) renamed this section accordingly. It is:

- **Relative** to τ^V (state viability).
- **Relative** to Π (stationary feedback-policy class).
- **Not** the whole of moral assessment (safeguards, flourishing, rights are handled separately).

### Comparing configurations

```python
# experiments/ch09_compare.py
from mctev.core.configuration import default_configuration
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.viability.kernel import compute_viable_region

# Two configurations with different τ^V
configs = {
    "strict": default_configuration(
        name="strict", viability_value=0.50,
    ),
    "lenient": default_configuration(
        name="lenient", viability_value=0.20,
    ),
}

dynamics = LinearDynamics()

print(f"{'Config':10s}  {'τ^V (uniform)':15s}  {'Viable fraction':15s}")
print("-" * 45)
for name, config in configs.items():
    constraints = default_constraints(thresholds=config.viability_thresholds)
    kernel = compute_viable_region(
        constraints=constraints, dynamics=dynamics,
        configuration=config, grid_size=4, horizon=80,
    )
    print(
        f"{name:10s}  "
        f"{config.viability_thresholds.values[0]:.2f}            "
        f"{kernel.fraction_viable():.2%}"
    )
```

### Self-check 9

- [ ] Run the script; verify the viable fraction.
- [ ] Change `τ^V` from 0.30 to 0.50; does the viable fraction shrink?
- [ ] Explain why a **stricter** τ^V produces a **smaller** kernel.

### Exercise 9.1

Determine which single function's τ^V is most restrictive. Set five of the six functions to `τ^V = 0.1` and vary the sixth from 0.1 to 0.7. Report the viable fraction at each level. Which function shrinks the kernel fastest?

### Paper reference

Section 7.5.

---

## Chapter 10: Flourishing Measurement

### Learning objective

Build a culturally specific measurement operator \(M_c\) and use it with τ^H.

### The measurement pipeline

```python
# experiments/ch10_flourishing.py
import numpy as np
from mctev.core.configuration import default_configuration
from mctev.core.measurement import LinearMeasurement
from mctev.flourishing.dimensions import FlourishingProfile

# Build a culturally specific measurement operator
agency_boost = LinearMeasurement(
    to_core=lambda x: np.asarray(x)[:5],
    monotone_transforms={2: lambda v: v ** 0.7},  # boost agency
)
config = default_configuration(
    name="agency_emphasizing",
    flourishing_value=0.50,
    measurement=agency_boost,
)

# Compute flourishing profile for a state
state = np.array([0.55, 0.55, 0.65, 0.55, 0.55, 0.5])
profile = FlourishingProfile.from_measurement(
    state, config.measurement_operator,
)
print(f"Observed flourishing: {profile}")
# FlourishingProfile(W=0.55, P=0.55, A=0.76, S=0.55, M=0.55)  ← agency boosted

# Check against τ^H
meets = profile.meets(config.flourishing_thresholds)
print(f"Meets τ^H: {meets}")
```

### The objectivity safeguard

A cultural context cannot lower its thresholds below the architecture's admissible range, nor use an invalid measurement operator. The library enforces:

1. **Threshold values** are validated in `FlourishingThresholds.__post_init__` (shape `(5,)`, no bound on values but you should set them per the architecture).
2. **Measurement operators** must implement `within_context_monotone`, which checks that E[Ĥ_d(x_higher)] > E[Ĥ_d(x_lower)].
3. **Cross-context comparability** is explicitly unavailable without anchors or linking maps.

### Self-check 10

- [ ] Run the script; verify that agency is boosted.
- [ ] Change the transform to `lambda v: v ** 0.3` (more boosting). Does the profile change?
- [ ] Try `within_context_monotone` for a valid and an invalid operator.

### Exercise 10.1

Design two measurement operators:
1. `identity`: leaves indicators unchanged.
2. `discriminatory`: adds `+0.2` to all dimensions for states with `x[0] > 0.5` (i.e., boosts flourishing for high-cooperation states).

Show that the second operator **violates within-context monotonicity** if the boost is conditioned on an indicator that isn't a monotone function of the core dimensions. Use `operator.within_context_monotone` to detect this.

### Paper reference

Sections 8.1–8.4.

---

## Chapter 11: Viable Current vs Sustainable Flourishing

### Learning objective

Distinguish the three flourishing notions:
- **Instantaneous**: \(x \in \mathcal{F}(\lambda_c)\)
- **Viable current**: \(x \in \mathcal{F}(\lambda_c) \cap \mathcal{R}(\lambda_c; \Pi)\)
- **Sustainable**: \(x \in \mathcal{R}_\mathcal{F}(\lambda_c; \Pi) = \mathrm{Viab}_\Pi(\mathcal{F}(\lambda_c) \cap \mathcal{V}(\lambda_c); F_{\lambda_c})\)

### The three notions at a glance

```python
# experiments/ch11_three_flourishing.py
import numpy as np
from mctev.core.configuration import default_configuration
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.viability.kernel import compute_viable_region
from mctev.flourishing.dimensions import FlourishingProfile

config = default_configuration(name="universalist")
constraints = default_constraints(thresholds=config.viability_thresholds)
dynamics = LinearDynamics()

# R — the controlled viability region
R_kernel = compute_viable_region(
    constraints=constraints, dynamics=dynamics,
    configuration=config, grid_size=4, horizon=80,
)

# Instantaneous flourishing for one state
state = np.array([0.6, 0.6, 0.6, 0.6, 0.6, 0.5])
profile = FlourishingProfile.from_measurement(
    state, config.measurement_operator,
)
instantaneous = profile.meets(config.flourishing_thresholds)

# Viable current: instantaneous AND in R
viable_current = instantaneous and R_kernel.contains(state)

print(f"State: {state}")
print(f"  Instantaneous flourishing: {instantaneous}")
print(f"  In R (viable region):      {R_kernel.contains(state)}")
print(f"  Viable current flourishing: {viable_current}")

# The distinction matters:
# A state can be flourishing NOW but not viably current.
# Viable current flourishing does NOT guarantee sustained flourishing.
```

### Why the distinction matters

A society can be:

| State | Instantaneous F | In R (viable)? | Sustained? |
|---|---|---|---|
| Thriving democracy | ✓ | ✓ | ✓ |
| Transiently flourishing (about to collapse) | ✓ | ✗ | ✗ |
| Stable but oppressive | ✗ | ✓ | ✗ |
| Failed | ✗ | ✗ | ✗ |

The distinction is what allows MCTEV to criticize **both** unsustainable prosperity **and** stable authoritarianism (§9).

### Self-check 11

- [ ] Run the script; verify both checks.
- [ ] Try states with different profiles; find one that is instantaneous-flourishing but not in R.
- [ ] Explain the four-case taxonomy in your own words.

### Paper reference

Sections 8.5–8.7, 9.

---

# Part IV — Dynamics

## Chapter 12: Boundary-Instability — the Index/Outcome Distinction

### Learning objective

Understand the crucial distinction between the **index boundary** (whose proximity is measured) and the **outcome set** (whose survival is evaluated).

### The crucial distinction

The manuscript (§10.6) requires:

$$
\Delta_\epsilon^{\mathcal{K}_{\text{index}} \to \mathcal{K}_{\text{out}}} = q_{T, \mathcal{K}_{\text{out}}}^\pi(\mathbf{x}_b - \epsilon_2 n) - q_{T, \mathcal{K}_{\text{out}}}^\pi(\mathbf{x}_b - \epsilon_1 n)
$$

**Two different sets**:

- \(\mathcal{K}_{\text{index}}\) — the set whose **boundary** is used to define inward displacement.
- \(\mathcal{K}_{\text{out}}\) — the set whose **survival** is evaluated.

These need not coincide.

### Set-specific survival

```python
# experiments/ch12_survival.py
import numpy as np
from mctev.core.configuration import default_configuration
from mctev.viability.constraints import default_constraints, ViabilityConstraints
from mctev.viability.dynamics import LinearDynamics
from mctev.instability.safe_sets import SafeSet
from mctev.instability.survival import set_specific_survival


class ViabilitySet(SafeSet):
    """The viability set V(λ_c)."""
    def __init__(self, constraints):
        self.constraints = constraints
    def contains(self, x):
        return self.constraints.is_satisfied(x)
    def signed_distance(self, x):
        return -self.constraints.violation_score(x)


config = default_configuration(name="universalist")
constraints = default_constraints(thresholds=config.viability_thresholds)
dynamics = LinearDynamics()

outcome_set = ViabilitySet(constraints)
x0 = np.full(6, 0.4)

# q_{T, V}^π(x0)
survived = set_specific_survival(
    x0=x0,
    outcome_set=outcome_set,
    dynamics=dynamics,
    configuration=config,
    horizon_steps=300,
    noise_scale=0.02,
)
print(f"Survived V for horizon: {survived}")
```

### Two different "safe sets"

The library provides two concrete `SafeSet` subclasses:

```python
from mctev.instability.safe_sets import IndicatorSafeSet, KernelSafeSet

# V_i(λ_c) — indicator-specific safe set
indicator_set = IndicatorSafeSet(
    indicator_fn=constraints.viability_fns[MoralFunction.COOPERATION],
    threshold=config.viability_thresholds[MoralFunction.COOPERATION],
    function=MoralFunction.COOPERATION,
)

# R(λ_c; Π) — controlled viability kernel
kernel_set = KernelSafeSet(kernel=R_kernel)

# These are DIFFERENT sets.
# Being deep inside R does not imply being deep inside V_i, and vice versa.
```

### Self-check 12

- [ ] Run the script.
- [ ] Explain in your own words why "being far from ∂R" is not equivalent to "being far from ∂V".

### Paper reference

Sections 10.3–10.6.

---

## Chapter 13: The Three Designs of Section 10.6

### Learning objective

Run all three designs:
1. **Indicator-specific**: index = V_i, outcome = V
2. **Kernel-to-viability-exit**: index = R, outcome = V
3. **Kernel-retention**: index = R, outcome = R

### The three designs

```python
# experiments/ch13_three_designs.py
import numpy as np
import matplotlib.pyplot as plt

from mctev.core.configuration import default_configuration
from mctev.core.moral_functions import MoralFunction
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.viability.kernel import compute_viable_region
from mctev.instability.analyzer import (
    build_three_designs, THREE_DESIGNS,
)

config = default_configuration(name="universalist")
constraints = default_constraints(thresholds=config.viability_thresholds)
dynamics = LinearDynamics()

kernel = compute_viable_region(
    constraints=constraints, dynamics=dynamics,
    configuration=config, grid_size=5, horizon=100,
)

designs = build_three_designs(
    dynamics=dynamics, configuration=config,
    viability_constraints=constraints, viability_kernel=kernel,
    function=MoralFunction.COOPERATION,
)

boundary_point = np.full(6, 0.32)
inward_distances = [0.02, 0.05, 0.10, 0.20]

results = {}
for name, analyzer in designs.items():
    print(f"\n=== {name} ===")
    print(f"  {THREE_DESIGNS[name]['description']}")
    res = analyzer.design_B(
        boundary_point=boundary_point,
        inward_distances=inward_distances,
        horizon_steps=200, n_trials=20,
    )
    print(res.summary())
    results[name] = res
```

### Interpreting the results

- **Design 1** (indicator-specific): proximity to V_i boundary predicts exit from V. This is the most direct test.
- **Design 2** (kernel-to-viability-exit): proximity to ∂R predicts exit from V. **The directional hypothesis requires additional assumptions** because R ⊂ V — you can leave R while remaining in V.
- **Design 3** (kernel-retention): proximity to ∂R predicts exit from R. This probes the **internal geometry** of the kernel. It is **excluded from Prediction 5** in the manuscript, because it answers a different question.

### Self-check 13

- [ ] Run the script; verify all three designs produce results.
- [ ] Compare Δ_ε across designs. Which is largest? Does that match your intuition?
- [ ] Explain why Design 3 answers a different question from Prediction 5.

### Exercise 13.1

Modify the script to hold the **index boundary** fixed (always R) but vary the **outcome set** between V and R. Show that Δ_ε differs. This demonstrates the outcome-set dependence of the estimand.

### Paper reference

Section 10.6.

---

## Chapter 14: Retentionist Conditions (R1)–(R3)

### Learning objective

Implement the three retentionist conditions from the manuscript.

### The three conditions

```python
# experiments/ch14_retentionist.py
import numpy as np
from mctev.core.configuration import default_configuration
from mctev.core.situational import Action, Situation
from mctev.retentionist.architecture import (
    RetentionistArchitecture, AbolitionistArchitecture,
)
from mctev.retentionist.conditions import (
    check_R1, check_R2, check_R3,
    CapitalActionSet, evaluate_test_situations, anti_triviality_filter,
)


# ---- Constraint predicate (with error-rate safeguard) ----
def constraint(situation, action, config):
    if action.name != "execute":
        return True
    if situation.context.get("severity") != "high":
        return False
    tau_error = config.safeguard_thresholds.get("error_rate", 0.05)
    return situation.context.get("observed_error_rate", 0.01) <= tau_error


# ---- Architectures ----
A_R = RetentionistArchitecture(name="A_R", constraint_predicate=constraint)
A_A = AbolitionistArchitecture(name="A_A", constraint_predicate=constraint)

# ---- R1: architectural non-exclusion ----
print(f"R1 for A_R: {check_R1(A_R)}")  # True
print(f"R1 for A_A: {check_R1(A_A)}")  # False

# ---- Test situations + actions ----
test_situations = [
    Situation("murder", {"severity": "high", "observed_error_rate": 0.01}),
    Situation("theft",  {"severity": "low",  "observed_error_rate": 0.01}),
]

def action_generator(situation):
    actions = [
        Action("life_imprisonment", 0.5),
        Action("acquittal", 0.0),
    ]
    if situation.context.get("severity") == "high":
        actions.append(Action("execute", 1.0))
    return actions

capital_set = CapitalActionSet()

# ---- R2: weak configuration-specific non-vacuity ----
config_permissive = default_configuration(
    name="permissive", safeguard_values={"error_rate": 0.05},
)
config_strict = default_configuration(
    name="strict", safeguard_values={"error_rate": 0.001},
)

R2 = check_R2(
    A_R, [config_permissive, config_strict], test_situations, action_generator,
    capital_set=capital_set, judgment=SituationalJudgment(
        utilities=MoralUtilityLibrary(), constraints=constraint,
    ),
)
print(f"R2 (weak non-vacuity): {R2}")  # True (permissive admits execute)

# ---- R3: strong configuration-specific non-vacuity ----
R3 = check_R3(
    A_R, [config_permissive, config_strict], test_situations, action_generator,
    capital_set=capital_set, judgment=SituationalJudgment(
        utilities=MoralUtilityLibrary(), constraints=constraint,
    ),
)
print(f"R3 (strong non-vacuity): {R3}")  # False (strict admits no execution)

# ---- Anti-triviality filter ----
filtered = anti_triviality_filter(
    test_situations,
    is_factually_coherent=lambda s: s.context.get("severity") in {"high", "low"},
    in_jurisdiction=lambda s: True,
    is_feasible=lambda s: s.context.get("observed_error_rate", 0) >= 0,
    is_artificial=lambda s: False,
)
print(f"Test situations passing filter: {len(filtered)}")
```

### The interpretive point

- **R1** says the **architecture** does not exclude execution categorically.
- **R2** says **some** configuration admits execution in **some** test situation.
- **R3** says **every** configuration admits execution in **some** test situation.

The manuscript (§12.3) states that **R1 + R2** is the natural requirement for a genuinely retentionist **architecture**. A configuration that fails to admit execution—even within a retentionist-permissive architecture—is **abolitionist in implementation**.

### Self-check 14

- [ ] Run the script; verify R1 for retentionist is True, R1 for abolitionist is False.
- [ ] Verify R2 is True (because permissive admits execution).
- [ ] Verify R3 is False (because strict does not).
- [ ] Explain what "abolitionist in implementation" means for `config_strict`.

### Exercise 14.1

Add a third configuration `moderate` with `error_rate=0.02`. Does the addition change R2? R3? Report the outcomes.

### Paper reference

Section 12.3.

---

# Part V — Applications

## Chapter 15: Qualifying Conditions and the Proxy Audit

### Learning objective

Build qualifying conditions \(Q_{-i}\) and run the **proxy audit** for non-circularity.

### The problem the proxy audit solves

The manuscript (§6.3.2) requires that when \(S_i^{\text{qual}}\) is used to derive or evaluate candidate function \(f_i\), the qualifying condition \(Q_{-i}\) must **not** contain \(f_i\) or any proxy that presupposes \(f_i\). Mere non-equivalence is insufficient.

### Building a qualifying condition

```python
# experiments/ch15_qualifying.py
import numpy as np
from mctev.core.moral_functions import MoralFunction
from mctev.core.qualifying import (
    QualifyingConditions, MemberInclusiveViability, proxy_audit,
)

# Example: member-inclusive viability, excluding distribution
member_inclusive = MemberInclusiveViability(
    target_function=MoralFunction.RESOURCE_DISTRIBUTION,
    welfare_index=lambda x: np.array([x[0], x[3]]),  # coop + care
    minimum_member_welfare=0.3,
)
member_inclusive._inputs = ["cooperation_indicator", "care_indicator"]

conditions = QualifyingConditions()
conditions[MoralFunction.RESOURCE_DISTRIBUTION] = member_inclusive

# Proxy audit
report = proxy_audit(conditions, MoralFunction.RESOURCE_DISTRIBUTION)
print(report.summary())
# Proxy audit [PASS] for target f = distribution
#   condition: member-inclusive welfare on non-distribution dimensions >= 0.3
#   constitutive inputs: ['cooperation_indicator', 'care_indicator']
```

### When the audit fails

```python
# A qualifying condition that secretly contains f_dist
suspect = MemberInclusiveViability(
    target_function=MoralFunction.RESOURCE_DISTRIBUTION,
    welfare_index=lambda x: np.array([x[2]]),  # distribution!
)
suspect._inputs = ["gini_coefficient"]  # a proxy for distribution

conditions[MoralFunction.RESOURCE_DISTRIBUTION] = suspect
report = proxy_audit(conditions, MoralFunction.RESOURCE_DISTRIBUTION)
print(report.summary())
# Proxy audit [FAIL] for target f = distribution
#   ...
#   flagged proxies: ['gini_coefficient']
```

The library flags `gini_coefficient` as a **common proxy** for distribution. The audit does not catch every circularity (semantic proxies require human judgment), but it catches the common cases.

### Self-check 15

- [ ] Run the script; verify PASS then FAIL.
- [ ] Add a qualifying condition that includes "reciprocity_index" and audit for `COOPERATION`. Does it FAIL?
- [ ] Explain why mere non-equivalence is insufficient to prevent circularity.

### Exercise 15.1

Design a qualifying condition for \(f_{\text{coop}}\) that satisfies the proxy audit. It must exclude both the function itself and any common proxy (e.g., `reciprocity_index`, `public_goods_contribution`). Use the audit to verify.

### Paper reference

Sections 6.3.2, Supplement S12.

---

## Chapter 16: The Slavery Case Study

### Learning objective

Run the slavery diagnosis with the **descriptive/qualified distinction** and **proxy audit**.

### What changed since v0.1.0

The slavery diagnosis now distinguishes:

1. **Descriptive profile** (S^viab): how slavery scores on the six functions.
2. **Qualifying condition** Q_{-dist}: the condition used to evaluate the distribution function.
3. **Proxy audit**: verifies that Q_{-dist} does not itself presuppose distribution.

### The script

```python
# experiments/ch16_slavery.py
from mctev.cases.slavery import evaluate_slavery

diag = evaluate_slavery()
print(diag.summary())
```

Expected output:

```
Slavery diagnosis (MCTEV v0.2.0)
=============================================
Descriptive profile (S^viab):
  cooperation    : 0.10
  conflict       : 0.10
  distribution   : 0.10
  care           : 0.20
  information    : 0.10
  sustainability : 0.30
---------------------------------------------
Descriptive violations: ['cooperation', 'conflict', 'distribution', 'care', 'information']
Descriptive severity:   0.130
Qualifying condition: member-inclusive welfare on non-distribution dimensions >= 0.3
Proxy audit:
  Proxy audit [PASS] for target f = distribution
  ...
```

### The interpretive caution

The slavery diagnosis is **descriptive**, not causal. It does not claim that slavery collapsed **because** it violated these functions. Per §11:

> Moral wrongness and empirical instability are distinct questions.

The diagnosis reports the **profile**, not the **causal explanation**. The **flourishing** classification of slavery depends on the independently justified architecture and calibrated measurements.

### Self-check 16

- [ ] Run the script; verify 5 violations.
- [ ] Change `SlaveryMemberInclusive._inputs` to include `"gini_coefficient"`; does the proxy audit fail?
- [ ] Explain the difference between "descriptive profile" and "causal explanation".

### Exercise 16.1

Add a second qualifying condition `Q_{-care}` for slavery using the flourishing indicators W, P, S, M. Verify it passes the proxy audit (it should not include care-specific proxies).

### Paper reference

Section 11.

---

## Chapter 17: The Capital Punishment Case Study

### Learning objective

Run the capital punishment diagnosis with the **retentionist conditions (R1)–(R3)**.

### The script

```python
# experiments/ch17_capital.py
from mctev.cases.capital_punishment import evaluate_capital_punishment

diag = evaluate_capital_punishment()
print(diag.summary())
```

Expected output:

```
Capital punishment diagnosis (MCTEV v0.2.0)
=======================================================
R1 (retentionist non-exclusion): True
R1 (abolitionist non-exclusion): False
R2 (weak non-vacuity):           True
R3 (strong non-vacuity):         False
Test situations passing filter:  3
```

### The interpretation

- **R1** for retentionist: True. The retentionist architecture contains **no categorical prohibition** of execution.
- **R1** for abolitionist: False. The abolitionist architecture categorically prohibits execution.
- **R2**: True. **Some** configuration admits execution in **some** test situation.
- **R3**: False. **Not every** configuration admits execution. A "strict" configuration (with `error_rate = 0.001`) does not. This configuration is **abolitionist in implementation** within the retentionist-permissive architecture.

### The meta-level point

The capital punishment case study's contribution is **not** that MCTEV resolves the debate. It is that MCTEV **makes the choice explicit**:

- Architecture A_R: retentionist-conditional
- Architecture A_A: abolitionist-categorical

The choice between them is a **meta-level choice about the constraint architecture**, not an ordinary Level-2 parameter choice. MCTEV frames the choice; it does not adjudicate.

### Self-check 17

- [ ] Run the script; verify all four conditions print.
- [ ] Change the `_make_constraint_predicate` in `capital_punishment.py` to be more permissive; does R3 become True?
- [ ] Explain what "abolitionist in implementation" means.

### Exercise 17.1

Add a third architecture `A_weak_retentionist` that prohibits execution in low-severity cases but allows it in high-severity cases. Compute R1, R2, R3 for this new architecture. Compare to A_R.

### Paper reference

Section 12.

---

# Part VI — Dispersion Analysis

## Chapter 18: Eight Dispersion Measures

### Learning objective

Quantify cross-context dispersion using the eight type-appropriate measures from Section 14.

### The eight measures

```python
# experiments/ch18_dispersion.py
import numpy as np
from mctev.core.configuration import default_configuration
from mctev.core.moral_functions import MoralFunction
from mctev.core.selection import SelectionConvention
from mctev.core.measurement import LinearMeasurement
from mctev.analysis.metrics import (
    dispersion_function_recognition,
    dispersion_weights,
    dispersion_viability_thresholds,
    dispersion_safeguard_thresholds,
    dispersion_flourishing_thresholds,
    dispersion_selection_conventions,
    dispersion_measurement_operators,
    dispersion_judgments,
    full_dispersion_vector,
)

# Build three configurations (contexts)
configs = [
    default_configuration(
        name="universalist",
        weights=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05],
        viability_value=0.30,
        safeguard_values={"error_rate": 0.05},
        selection=SelectionConvention.STATUS_QUO,
    ),
    default_configuration(
        name="collectivist",
        weights=[0.25, 0.15, 0.15, 0.30, 0.10, 0.05],
        viability_value=0.35,
        safeguard_values={"error_rate": 0.03},
        selection=SelectionConvention.PRECEDENT,
    ),
    default_configuration(
        name="individualist",
        weights=[0.20, 0.15, 0.20, 0.10, 0.20, 0.15],
        viability_value=0.25,
        safeguard_values={"error_rate": 0.10},
        selection=SelectionConvention.LEXICOGRAPHIC,
    ),
]

# Compute each measure individually
print(f"D_θ    (weights, Aitchison):       {dispersion_weights([c.weights for c in configs]):.4f}")
print(f"D_τ^V  (viability thresholds):     {dispersion_viability_thresholds(configs):.4f}")
print(f"D_τ^S  (safeguard thresholds):     {dispersion_safeguard_thresholds(configs):.4f}")
print(f"D_τ^H  (flourishing thresholds):   {dispersion_flourishing_thresholds(configs):.4f}")

# D_F requires recognized function sets
recognized = [
    [MoralFunction.COOPERATION, MoralFunction.CARE],
    [MoralFunction.COOPERATION, MoralFunction.CARE],
    [MoralFunction.COOPERATION],  # individualist recognizes fewer
]
print(f"D_F    (function recognition):     {dispersion_function_recognition(recognized):.4f}")

# D_M requires anchor states
anchors = [np.array([0.5]*6), np.array([0.7]*6)]
print(f"D_M    (measurement operators):    {dispersion_measurement_operators(configs, anchors):.4f}")

# D_ρ requires a shared benchmark
benchmark = {
    "situations": [
        __import__("mctev.core.situational", fromlist=["Situation"]).Situation(
            f"s{i}", {"status_quo": "b"}
        )
        for i in range(5)
    ],
    "maximizers": [
        [
            __import__("mctev.core.situational", fromlist=["Action"]).Action("a"),
            __import__("mctev.core.situational", fromlist=["Action"]).Action("b"),
            __import__("mctev.core.situational", fromlist=["Action"]).Action("c"),
        ]
        for _ in range(5)
    ],
}
print(f"D_ρ    (selection conventions):    {dispersion_selection_conventions(configs, benchmark['situations'], benchmark['maximizers']):.4f}")

# D_J requires judgment lists
judgment_lists = [
    ["a", "b", "a", "b", "a"],
    ["b", "b", "a", "a", "a"],
    ["c", "b", "c", "b", "a"],
]
print(f"D_J    (judgments):                {dispersion_judgments(judgment_lists):.4f}")

# Full vector
print("\nFull dispersion vector:")
full = full_dispersion_vector(
    configs=configs, recognized_sets=recognized,
    anchor_states=anchors, benchmark={**benchmark, "judgment_lists": judgment_lists},
)
for k, v in full.items():
    print(f"  {k:12s}: {v:.4f}")
```

### The MCTEV convergence prediction

The manuscript (§14) predicts:

$$
D_F < D_\theta, \; D_{\tau^V}, \; D_{\tau^S}, \; D_{\tau^H}, \; D_\rho, \; D_M, \; D_J
$$

That is: **function recognition should vary less than any Level-2 component**.

```python
# Check the prediction against the computed values
predicted_order = full["D_F"] < min(
    full["D_theta"], full["D_tau_V"], full["D_tau_S"],
    full["D_tau_H"], full["D_rho"],
)
print(f"\nMCTEV convergence prediction holds: {predicted_order}")
```

### The robustness requirement

The manuscript also requires (§14):

> Each pairwise comparison must be tested for robustness across defensible normalizations.

Different normalizations can change the ordering. The library does not choose a normalization for you; it provides the raw measures, and you choose the normalization that is defensible for your application.

### Self-check 18

- [ ] Run the script; verify all eight measures compute.
- [ ] Which measure is largest? Which is smallest?
- [ ] Verify the MCTEV convergence prediction (`D_F` < others) holds in your example.

### Exercise 18.1

Add a fourth configuration `self_regarding` with `weights=[1.0, 0, 0, 0, 0, 0]`. Recompute all eight measures. Does the MCTEV convergence prediction still hold? Which measure changes most?

### Paper reference

Section 14.

---

# Part VII — Consolidation

## Chapter 19: Exercises

A consolidated set of exercises covering all chapters.

### Level 1–2 (Foundations)

**19.1** Construct a `CulturalConfiguration` with non-uniform `flourishing_thresholds` (e.g., agency at 0.7, others at 0.5). Verify it passes validation.

**19.2** Show that a configuration with `weights` summing to 1.5 is rejected. Then show that `weights / 1.5` is accepted.

**19.3** For each of the five `SelectionConvention` values, construct a scenario where that convention picks a different action than the others. Report the five choices.

### Level 3 (Situational judgments)

**19.4** Write an `action_generator` that returns different actions based on `situation.context["role"]`. Show that `situation.context` changes the correspondence J.

**19.5** Write a constraint predicate that reads `config.safeguard_thresholds.get("error_rate")`. Show that changing only `safeguard_thresholds["error_rate"]` changes which actions are admissible.

### Viability and flourishing

**19.6** For each of the three threshold families, construct a configuration where the family is set very strict vs. very lenient. Show that the viable fraction depends only on τ^V, not on τ^S or τ^H.

**19.7** Construct two measurement operators that agree on average but disagree on ordering. Use `within_context_monotone` to detect the disagreement.

### Boundary-Instability

**19.8** Run all three designs with the same boundary point and same inward distances. Report the three Δ_ε values. Which is largest?

**19.9** Show that Design 3 (kernel-retention) has a different Δ_ε than Design 2 (kernel-to-viability-exit), even when the index boundary is the same (R). Explain why.

### Retentionist

**19.10** Design three architectures: A_R (retentionist-permissive), A_moderate (execution only for terrorism), A_A (abolitionist-categorical). Compute R1, R2, R3 for each.

### Qualifying conditions

**19.11** Design a qualifying condition for `f_coop` that passes the proxy audit. Verify with `proxy_audit`.

**19.12** Design one that fails the proxy audit. Show the flagged proxy.

### Dispersion

**19.13** Compute all eight measures for two configurations that differ **only** in `weights`. Which measures are zero? Which are non-zero?

**19.14** Verify the MCTEV convergence prediction (`D_F < others`) holds for your example. If it doesn't, explain why.

## Chapter 20: Capstone Project

### Project: Model a historical collapse

Choose a historical society that collapsed (Roman Republic, Maya Classic, Soviet Union, Easter Island).

### Step 1: Research (30–45 min)

For your society:

1. What were its **functional priorities**? Estimate the six weights.
2. What were its **viability thresholds** τ^V? Which functions were near the boundary?
3. What were its **safeguard thresholds** τ^S? Which procedures were strong/weak?
4. What were its **flourishing thresholds** τ^H? What was the measurement operator?
5. What was its **selection convention** ρ_c?

### Step 2: Model construction (30 min)

```python
# capstone_model.py
import numpy as np
from mctev.core.configuration import CulturalConfiguration
from mctev.core.thresholds import (
    ViabilityThresholds, SafeguardThresholds, FlourishingThresholds,
)
from mctev.core.selection import SelectionConvention
from mctev.core.measurement import LinearMeasurement

your_society = CulturalConfiguration(
    weights=np.array([...]),
    viability_thresholds=ViabilityThresholds.from_dict({...}),
    safeguard_thresholds=SafeguardThresholds.from_dict({...}),
    flourishing_thresholds=FlourishingThresholds.from_dict({...}),
    selection_convention=SelectionConvention.PRECEDENT,
    measurement_operator=LinearMeasurement(to_core=lambda x: x[:5]),
    name="your_society",
)
```

### Step 3: Analysis (45 min)

Report:

1. **Controlled viability kernel**: viable fraction.
2. **Boundary-Instability (all three designs)**: which is most predictive?
3. **Flourishing classification**: instantaneous, viable-current, sustainable?
4. **Dispersion**: which components differ most from the universalist baseline?

### Step 4: Reflection (15 min)

Answer:

1. What does MCTEV add to the historical account?
2. Where does the framework fall short?
3. What would need to be true for the framework's prediction to be validated?

### Grading rubric (self-assessment)

| Criterion | Weight |
|---|---|
| Historical accuracy | 25% |
| Framework application (all three levels + dynamics) | 25% |
| Interpretation quality (within epistemic limits) | 25% |
| Reflection (critical evaluation) | 25% |

## Chapter 21: Where to Go From Here

### If you want to extend the library

High-impact extensions:

1. **Bayesian calibration** of τ^V, τ^S, τ^H from data.
2. **Adaptive upward mechanism** implementing the full λ_c update.
3. **Full COH instantiation** of MCTEV.
4. **Multi-agent simulation with adaptive cultural transmission** (not just payoff-biased).
5. **Conformance test suite** for the Section 13 simulation.

### If you want to extend the framework

1. **Meta-level criteria** for choosing between architectures (A_R vs. A_A).
2. **Cross-context scale-linking maps** for M_c.
3. **Empirical calibration** of Q_{-i} conditions.
4. **Non-payoff-biased transmission** in the simulation.

### If you want to use MCTEV for real problems

1. **Policy design**: the three-layer architecture for cross-cultural policy.
2. **AI alignment**: the constraint/parameter/inference layer decomposition.
3. **Historical analysis**: quantify moral evolution over time.
4. **Moral education**: teach Level-1 vs. Level-2 reasoning.

### Final thought

You have now walked through every major revision in v0.2.0. The key insight that emerged from the manuscript's evolution is:

> **Moral disagreement can be localized.** Level-1 disagreement (about which functions matter) is different from Level-2 disagreement (about weights, thresholds, selection, or measurement) is different from Level-3 disagreement (about a specific case). The library now supports you in distinguishing these three.

That is the framework's most useful contribution. Use it well.

---

**End of Tutorial.**

If you have completed this tutorial, you have a working understanding of every formal object in the current manuscript. The remaining challenge is **application**: use the framework on a problem you care about. That is where frameworks earn their keep.