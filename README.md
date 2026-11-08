# mctev-lib

> **Reference implementation of the Multi-Level Computational Theory of Ethics (MCTEV), v0.2.0**

A Python library for formalizing, simulating, and empirically evaluating the three-level ethical architecture described in *"Toward a Computational Science of Ethics: A Multi-Level Computational Theory of Ethical Variation and Candidate Level 1 Moral Functions."*

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](CHANGELOG.md)

---

## Table of Contents

- [What's new in 0.2.0](#whats-new-in-020)
- [Overview](#overview)
- [Conceptual alignment with the manuscript](#conceptual-alignment-with-the-manuscript)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Core concepts](#core-concepts)
- [Module reference](#module-reference)
- [Examples](#examples)
- [Reproducing the paper's results](#reproducing-the-papers-results)
- [Migration from v0.1.0](#migration-from-v010)
- [Design commitments](#design-commitments)
- [Testing](#testing)
- [Citation](#citation)
- [License](#license)

---

## What's new in 0.2.0

v0.2.0 brings the library into alignment with the current manuscript. The formal structures below are now **first-class objects**:

| Manuscript refinement | Library module | Version |
|---|---|---|
| Three threshold families \(\boldsymbol{\tau}^V, \boldsymbol{\tau}^S, \boldsymbol{\tau}^H\) | `mctev.core.thresholds` | new |
| Full Level-2 configuration \(\lambda_c = (\theta_c, \boldsymbol{\tau}_c^V, \boldsymbol{\tau}_c^S, \boldsymbol{\tau}_c^H, \rho_c, M_c)\) | `mctev.core.configuration` | new |
| Selection convention \(\rho_c\) | `mctev.core.selection` | new |
| Measurement operator \(M_c\) with cross-context comparability | `mctev.core.measurement` | new |
| Qualifying condition \(Q_{-i}\) + proxy audit | `mctev.core.qualifying` | new |
| Boundary-Instability with index/outcome sets | `mctev.instability` | new (replaces `collapse`) |
| Retentionist conditions (R1)–(R3) | `mctev.retentionist` | new |
| Situation-dependent action sets \(\mathcal{A}(s)\) | `mctev.core.situational` | revised |
| Dispersion measures \(D_F, \ldots, D_J\) | `mctev.analysis.metrics` | revised |
| Set-specific survival \(q_{T,\mathcal{K}_{\text{out}}}^\pi\) | `mctev.instability.survival` | new |

**Backward compatibility is preserved** through deprecation shims (`CulturalParameters`, `collapse`, legacy import paths). Every breaking change is documented in [`CHANGELOG.md`](CHANGELOG.md) and [`MIGRATION.md`](MIGRATION.md).

---

## Overview

MCTEV formalizes ethics as a three-level computational system:

```
┌────────────────────────────────────────────────────────────────────┐
│  LEVEL 1 — Candidate Level 1 moral functions and architecture A    │
│  ────────────────────────────────────────────────────────────────  │
│  ℱ₁ = {f_coop, f_conflict, f_dist, f_care, f_info, f_sustain}      │
│  A = (ℱ₁, T_V^{L1}, T_S^{L1}, T_H^{L1}, C^{L1},                    │
│       S^{dom}, S^{req}, P_A, M_A, Q)                               │
│                                                                    │
│                     constrains                                     │
│                        ▼                                           │
│  LEVEL 2 — Cultural-institutional configuration λ_c               │
│  ────────────────────────────────────────────────────────────────  │
│  λ_c = (θ_c, τ^V, τ^S, τ^H, ρ_c, M_c)                              │
│       │    │    │    │    │    │                                   │
│       │    │    │    │    │    └─ measurement operator              │
│       │    │    │    │    └────── selection convention              │
│       │    │    │    └─────────── flourishing thresholds            │
│       │    │    └──────────────── safeguard thresholds              │
│       │    └───────────────────── dynamical viability thresholds    │
│       └────────────────────────── compensatory weights              │
│                                                                    │
│                     constrains                                     │
│                        ▼                                           │
│  LEVEL 3 — Situational judgment                                    │
│  ────────────────────────────────────────────────────────────────  │
│  J(s; A, λ_c) = argmax_{a ∈ A(s) ∩ C(s; A, τ^S)}                   │
│                 Σ_f θ_c,f · u_f(a, s)                              │
│                                                                    │
│  j(s; A, λ_c) = σ_{ρ_c}( J(s; A, λ_c), s )                         │
└────────────────────────────────────────────────────────────────────┘
```

The library supports:

- **Representation** of any moral system as a full \(\lambda_c\) configuration under a fixed architecture \(\mathfrak{A}\).
- **Reasoning** about specific situations under situation-dependent action sets \(\mathcal{A}(s)\).
- **Simulation** of moral dynamics (the Three Societies public-goods model).
- **Evaluation** of viability through the controlled viability kernel \(\mathcal{R}(\lambda_c; \Pi)\).
- **Boundary-Instability analysis** with distinct index-boundary and outcome-set designs.
- **Retentionist / abolitionist comparison** via conditions (R1)–(R3).
- **Dispersion quantification** across the eight type-appropriate measures \(D_F, \ldots, D_J\).

---

## Conceptual alignment with the manuscript

Every public class corresponds to a formal object in the paper. The table below maps the reader directly to the relevant section.

| Manuscript § | Formal object | Library class / function |
|---|---|---|
| §6.3.1 | \(S_i^{\text{viab}}\) (descriptive viability) | *conceptual; supplied by the user* |
| §6.3.2 | \(S_i^{\text{qual}}\), \(Q_{-i}\), proxy audit | `QualifyingCondition`, `QualifyingConditions`, `proxy_audit` |
| §7.1 | Threshold families \(\mathcal{T}_V^{L1}, \mathcal{T}_S^{L1}, \mathcal{T}_H^{L1}\) | `ViabilityThresholds`, `SafeguardThresholds`, `FlourishingThresholds` |
| §7.2 | Full configuration \(\lambda_c\) | `CulturalConfiguration` |
| §7.4 | Selection function \(\sigma_{\rho_c}\) | `SelectionConvention`, `select_action` |
| §7.5 | Controlled viability kernel \(\mathcal{R}(\lambda_c; \Pi)\) | `ViabilityKernel`, `compute_viable_region` |
| §8.2 | Measurement operator \(M_c\) | `MeasurementOperator`, `LinearMeasurement` |
| §8.2 | Cross-context comparability | `validate_cross_context_comparability` |
| §8.4 | Flourishing region \(\mathcal{F}(\lambda_c)\) | `FlourishingProfile` |
| §9.2 | Witness argument, stabilization time | *conceptual; see `FlourishingProfile`* |
| §10.4 | Set-specific survival \(q_{T,\mathcal{K}_{\text{out}}}^\pi\) | `set_specific_survival` |
| §10.6 | Three designs (indicator, kernel-to-exit, kernel-retention) | `build_three_designs`, `BoundaryInstabilityAnalyzer` |
| §10.6 | Index boundary \(\partial\mathcal{K}_{\text{index}}\) | `IndicatorSafeSet`, `KernelSafeSet` |
| §12.3 | Retentionist conditions (R1)–(R3) | `check_R1`, `check_R2`, `check_R3`, `anti_triviality_filter` |
| §14 | Dispersion measures \(D_F,\ldots,D_J\) | `mctev.analysis.metrics` |

---

## Installation

### From GitHub (v0.2.0)

```bash
git clone https://github.com/hongxueharriswang/mctev-lib.git
cd mctev-lib
python -m venv .mctev-venv
source .mctev-venv/bin/activate
pip install -e .
```

### Development install

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

### Requirements

- Python ≥ 3.10
- NumPy ≥ 1.24
- SciPy ≥ 1.10
- Matplotlib ≥ 3.7
- pandas ≥ 2.0

---

## Quick start

### Example 1: Level-3 judgment with a full configuration

```python
from mctev.core.configuration import default_configuration
from mctev.core.moral_functions import MoralFunction, MoralUtilityLibrary
from mctev.core.selection import SelectionConvention
from mctev.core.situational import Action, Situation, SituationalJudgment

# Define per-function utilities
lib = MoralUtilityLibrary()
lib[MoralFunction.COOPERATION] = lambda a, s: float(a.payload)
lib[MoralFunction.REPRODUCTION_CARE] = lambda a, s: 1.0 - float(a.payload)

# Build a full configuration λ_c
config = default_configuration(
    name="universalist",
    weights=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05],
    viability_value=0.30,
    safeguard_values={"error_rate": 0.05},
    flourishing_value=0.50,
    selection=SelectionConvention.STATUS_QUO,
)

# Judge under the full configuration
solver = SituationalJudgment(utilities=lib)
best = solver.judge(
    Situation("allocation", {"status_quo": "moderate"}),
    [Action("selfish", 0.2), Action("moderate", 0.5), Action("generous", 0.8)],
    config,
)
print(best.name)  # respects ρ_c = STATUS_QUO
```

### Example 2: Boundary-Instability with the three designs

```python
import numpy as np
from mctev.core.configuration import default_configuration
from mctev.core.moral_functions import MoralFunction
from mctev.viability.constraints import default_constraints
from mctev.viability.dynamics import LinearDynamics
from mctev.viability.kernel import compute_viable_region
from mctev.instability.analyzer import build_three_designs

config = default_configuration(name="universalist")
constraints = default_constraints()
dynamics = LinearDynamics()

kernel = compute_viable_region(
    constraints=constraints, dynamics=dynamics,
    configuration=config, grid_size=5, horizon=150,
)

designs = build_three_designs(
    dynamics=dynamics, configuration=config,
    viability_constraints=constraints, viability_kernel=kernel,
    function=MoralFunction.COOPERATION,
)

for name, analyzer in designs.items():
    print(f"\n=== {name} ===")
    result = analyzer.design_B(
        boundary_point=np.full(6, 0.32),
        inward_distances=[0.02, 0.05, 0.10, 0.20],
        horizon_steps=300, n_trials=20,
    )
    print(result.summary())
```

### Example 3: Retentionist conditions (R1)–(R3)

```python
from mctev.cases.capital_punishment import evaluate_capital_punishment

diag = evaluate_capital_punishment()
print(diag.summary())
# R1 (retentionist non-exclusion): True
# R1 (abolitionist non-exclusion): False
# R2 (weak non-vacuity):           True
# R3 (strong non-vacuity):         False
```

---

## Core concepts

### The full configuration \(\lambda_c\)

The **only** Level-2 object in v0.2.0 is `CulturalConfiguration`. It carries all six components:

```python
from mctev.core.configuration import CulturalConfiguration, default_configuration
from mctev.core.thresholds import (
    ViabilityThresholds, SafeguardThresholds, FlourishingThresholds,
)
from mctev.core.selection import SelectionConvention
from mctev.core.measurement import LinearMeasurement
import numpy as np

config = CulturalConfiguration(
    weights=np.array([0.30, 0.20, 0.20, 0.15, 0.10, 0.05]),
    viability_thresholds=ViabilityThresholds.uniform(0.30),
    safeguard_thresholds=SafeguardThresholds.from_dict({"error_rate": 0.05}),
    flourishing_thresholds=FlourishingThresholds.uniform(0.50),
    selection_convention=SelectionConvention.STATUS_QUO,
    measurement_operator=LinearMeasurement(to_core=lambda x: x[:5]),
    name="universalist",
)
```

The weights must lie in the probability simplex \(\Delta^5\); `__post_init__` enforces this.

### Three threshold families (do not conflate them)

```python
# τ^V — dynamical viability: state-level constraint V(λ_c)
viability = ViabilityThresholds.from_dict({"cooperation": 0.4, "care": 0.3})

# τ^S — safeguard: action-level constraint C(s; A, τ^S)
safeguard = SafeguardThresholds.from_dict({"error_rate": 0.05, "disparity": 0.10})

# τ^H — flourishing: membership in F(λ_c)
flourishing = FlourishingThresholds.from_dict({"W": 0.5, "P": 0.5, "A": 0.6})
```

These are **not interchangeable**. Each acts on a different object:

| Family | Acts on | Example |
|---|---|---|
| \(\boldsymbol{\tau}^V\) | States | Minimum cooperation rate for societal viability |
| \(\boldsymbol{\tau}^S\) | Actions | Wrongful-conviction rate threshold in a capital case |
| \(\boldsymbol{\tau}^H\) | States | Minimum agency for flourishing |

### Selection conventions \(\rho_c\)

Five built-in conventions resolve ties among maximizers:

```python
from mctev.core.selection import SelectionConvention, select_action

# Supported conventions:
#   PRECEDENT           — choose closest to previous action
#   MINIMUM_INTERVENTION — choose smallest-payload maximizer
#   STATUS_QUO          — choose the status-quo action if it maximizes
#   LEXICOGRAPHIC       — choose by a declared secondary key
#   RANDOM              — uniform among maximizers (seeded)
```

### Qualifying conditions \(Q_{-i}\)

The qualifying condition \(Q_{-i}\) excludes the target function \(f_i\) and must satisfy the **definitional-independence** requirement:

```python
from mctev.core.moral_functions import MoralFunction
from mctev.core.qualifying import (
    QualifyingConditions, MemberInclusiveViability, proxy_audit,
)
import numpy as np

conditions = QualifyingConditions()
conditions[MoralFunction.RESOURCE_DISTRIBUTION] = MemberInclusiveViability(
    target_function=MoralFunction.RESOURCE_DISTRIBUTION,
    welfare_index=lambda x: np.array([x[0], x[3]]),
    minimum_member_welfare=0.3,
)

# Run the proxy audit
report = proxy_audit(conditions, MoralFunction.RESOURCE_DISTRIBUTION)
print(report.summary())  # PASS or FAIL
```

### Boundary-Instability: index boundary vs outcome set

The key distinction of Section 10.6: the set whose **boundary** indexes proximity need not be the set whose **survival** is evaluated.

```python
from mctev.instability.safe_sets import IndicatorSafeSet, KernelSafeSet
from mctev.instability.analyzer import BoundaryInstabilityAnalyzer

# Design 1: index = V_i, outcome = V
analyzer_1 = BoundaryInstabilityAnalyzer(
    dynamics=dyn, configuration=config,
    index_set=IndicatorSafeSet(...),  # V_i(λ_c)
    outcome_set=viability_set,        # V(λ_c)
)

# Design 2: index = R, outcome = V (kernel-to-viability-exit)
analyzer_2 = BoundaryInstabilityAnalyzer(
    dynamics=dyn, configuration=config,
    index_set=KernelSafeSet(kernel=kernel),  # R(λ_c; Π)
    outcome_set=viability_set,                # V(λ_c)
)

# Design 3: index = R, outcome = R (kernel-retention; reported separately)
analyzer_3 = BoundaryInstabilityAnalyzer(
    dynamics=dyn, configuration=config,
    index_set=KernelSafeSet(kernel=kernel),
    outcome_set=KernelSafeSet(kernel=kernel),
)
```

### Retentionist conditions (R1)–(R3)

```python
from mctev.retentionist.architecture import (
    RetentionistArchitecture, AbolitionistArchitecture,
)
from mctev.retentionist.conditions import (
    check_R1, check_R2, check_R3, anti_triviality_filter,
)

A_R = RetentionistArchitecture(name="A_R", constraint_predicate=...)
A_A = AbolitionistArchitecture(name="A_A", constraint_predicate=...)

# R1: architectural non-exclusion
assert check_R1(A_R) is True
assert check_R1(A_A) is False

# R2/R3 require test situations and an action generator
test_sits = anti_triviality_filter(raw_test_situations)
R2 = check_R2(A_R, configs, test_sits, action_gen)
R3 = check_R3(A_R, configs, test_sits, action_gen)
```

---

## Module reference

### `mctev.core`

| Module | Public API |
|---|---|
| `moral_functions` | `MoralFunction`, `MoralFunctionProfile`, `MoralUtilityLibrary`, `MORAL_FUNCTION_ORDER`, `N_FUNCTIONS` |
| `thresholds` | `ViabilityThresholds`, `SafeguardThresholds`, `FlourishingThresholds`, `ThresholdFamilies` |
| `configuration` | `CulturalConfiguration`, `default_configuration` |
| `selection` | `SelectionConvention`, `select_action` |
| `measurement` | `MeasurementOperator`, `LinearMeasurement`, `validate_cross_context_comparability` |
| `qualifying` | `QualifyingCondition`, `MemberInclusiveViability`, `MinimumFlourishing`, `QualifyingConditions`, `proxy_audit` |
| `situational` | `Situation`, `Action`, `SituationalJudgment`, `ConstraintPredicate`, `ActionGenerator` |
| `hierarchy` | `MCTEVSystem` |
| `cultural_params` | *(deprecated shim)* `CulturalParameters`, `CULTURAL_TYPES` |

### `mctev.viability`

| Module | Public API |
|---|---|
| `constraints` | `ViabilityConstraints`, `default_constraints` |
| `dynamics` | `Dynamics`, `LinearDynamics`, `NonlinearCouplingDynamics` |
| `kernel` | `ViabilityKernel`, `compute_viable_region` |

### `mctev.instability` *(replaces `mctev.collapse`)*

| Module | Public API |
|---|---|
| `safe_sets` | `SafeSet`, `IndicatorSafeSet`, `KernelSafeSet` |
| `survival` | `set_specific_survival` |
| `analyzer` | `BoundaryInstabilityAnalyzer`, `InstabilityResult`, `build_three_designs`, `THREE_DESIGNS` |

### `mctev.retentionist`

| Module | Public API |
|---|---|
| `architecture` | `Architecture`, `RetentionistArchitecture`, `AbolitionistArchitecture` |
| `conditions` | `check_R1`, `check_R2`, `check_R3`, `CapitalActionSet`, `evaluate_test_situations`, `anti_triviality_filter` |

### `mctev.flourishing`

| Module | Public API |
|---|---|
| `dimensions` | `FlourishingProfile`, `FlourishingDimension`, `DIMENSIONS` |

*(Note: `FlourishingThresholds` now lives in `mctev.core.thresholds`; the legacy import from `mctev.flourishing.dimensions` continues to work but is deprecated.)*

### `mctev.analysis`

| Module | Public API |
|---|---|
| `metrics` | `dispersion_function_recognition` (\(D_F\)), `dispersion_weights` (\(D_\theta\)), `dispersion_viability_thresholds` (\(D_{\tau^V}\)), `dispersion_safeguard_thresholds` (\(D_{\tau^S}\)), `dispersion_flourishing_thresholds` (\(D_{\tau^H}\)), `dispersion_selection_conventions` (\(D_\rho\)), `dispersion_measurement_operators` (\(D_M\)), `dispersion_judgments` (\(D_J\)), `full_dispersion_vector`, `aitchison_distance` |
| `visualization` | `plot_three_societies`, `plot_survival_curves`, `plot_viability_grid`, `plot_flourishing_radar`, `plot_index_outcome_designs` |

### `mctev.simulation`

| Module | Public API |
|---|---|
| `agents` | `Agent`, `AgentType` |
| `public_goods` | `PublicGoodsGame`, `ThreeSocietiesConfig`, `run_three_societies` |

### `mctev.cases`

| Module | Public API |
|---|---|
| `slavery` | `evaluate_slavery`, `SlaveryDiagnosis` |
| `capital_punishment` | `evaluate_capital_punishment`, `CapitalPunishmentDiagnosis` |

### `mctev.collapse` *(deprecated shim)*

Redirects to `mctev.instability` with a `DeprecationWarning`. The legacy names `ConstraintViolationAnalyzer` and `ExitTimeResult` are aliased to `BoundaryInstabilityAnalyzer` and `InstabilityResult` respectively.

---

## Examples

All examples are executable scripts in `examples/`.

| Script | Reproduces |
|---|---|
| `demo_three_societies.py` | Section 13 — Three Societies simulation |
| `demo_viability_kernel.py` | Section 7.5 — controlled viability kernel |
| `demo_flourishing.py` | Section 8 — measurement operator and flourishing |
| `demo_boundary_instability.py` | Section 10.4–10.6 — Boundary-Instability |
| `demo_index_outcome_designs.py` | Section 10.6 — three designs |
| `demo_capital_punishment.py` | Section 12.3 — retentionist conditions |
| `demo_case_studies.py` | Sections 11–12 — combined case studies |

Run any example:

```bash
python examples/demo_index_outcome_designs.py
```

---

## Reproducing the paper's results

| Paper section | Script | Key output |
|---|---|---|
| §7.5 — Controlled viability kernel | `demo_viability_kernel.py` | Kernel fraction-viable |
| §8 — Flourishing measurement | `demo_flourishing.py` | Flourishing profile and radar plot |
| §10.4 — Set-specific survival | `demo_boundary_instability.py` | \(q_{T,\mathcal{K}_{\text{out}}}^\pi\) curves |
| §10.6 — Three designs | `demo_index_outcome_designs.py` | \(\Delta_\epsilon^{\mathcal{K}_{\text{index}} \to \mathcal{K}_{\text{out}}}\) for each design |
| §12.3 — (R1)–(R3) | `demo_capital_punishment.py` | Retentionist condition report |
| §13 — Three Societies | `demo_three_societies.py` | Cooperation over time |

> **Note on the simulation.** The Three Societies simulation is a **hybrid proxy utility model** (Supplement S9), not a full MCTEV implementation. Results are illustrative pending archival reproduction from the finalized implementation.

---

## Migration from v0.1.0

v0.2.0 is a **substantial revision**. Full migration guide in [`MIGRATION.md`](MIGRATION.md). Key changes:

| v0.1.0 | v0.2.0 |
|---|---|
| `CulturalParameters` (θ_c only) | `CulturalConfiguration` (full λ_c) |
| Single `ViabilityConstraints` for state + action | `ViabilityConstraints` (τ^V) + `SafeguardThresholds` (τ^S) |
| `FlourishingThresholds` in `mctev.flourishing.dimensions` | `FlourishingThresholds` in `mctev.core.thresholds` |
| `ConstraintViolationAnalyzer` | `BoundaryInstabilityAnalyzer` |
| `compare_viable_vs_violating` | `BoundaryInstabilityAnalyzer.design_B` + `build_three_designs` |
| Implicit tie-breaking | `SelectionConvention` (ρ_c) |

**All v0.1.0 public APIs remain importable** through deprecation shims. Existing code continues to work; the shims emit `DeprecationWarning` and will be removed in v1.0.0.

### Minimal migration

```python
# v0.1.0
from mctev.core.cultural_params import CULTURAL_TYPES
params = CULTURAL_TYPES["universalist"]
best = solver.judge(situation, actions, params)

# v0.2.0
from mctev.core.configuration import default_configuration
config = default_configuration(
    name="universalist",
    weights=[0.30, 0.20, 0.20, 0.15, 0.10, 0.05],
)
best = solver.judge(situation, actions, config)
```

---

## Design commitments

The library embodies three epistemic commitments from the manuscript:

### 1. Candidate, not dogma

The six Level 1 functions are exposed as an **explicitly extensible enumeration**. The epistemic tier of each function (strict universal, robust regularity, weak regularity) is **not yet established** and is not pre-assigned. Extending the set of functions is a source-level operation that requires re-running the test suite.

### 2. Alignment, not derivation

The library is **methodologically aligned with** — but **not formally derived from** — the COH/GISMOL research program. `MCTEVSystem` is MCTEV's own composition; it is not a specialization of the COH 9-tuple.

### 3. Simulation-based evaluation, not proof

The Boundary-Instability Hypothesis is a **research hypothesis and testing protocol**, not a proved theorem. `BoundaryInstabilityAnalyzer` implements the empirical evaluation; it does not prove the hypothesis.

### 4. Three threshold families are not interchangeable

The manuscript's separation of \(\boldsymbol{\tau}^V\), \(\boldsymbol{\tau}^S\), and \(\boldsymbol{\tau}^H\) is enforced at the type level. The library prevents accidental conflation by requiring distinct classes for each family.

---

## Testing

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

The test suite covers:

- **Threshold families** (`test_thresholds.py`): shape, dictionary roundtrip, override behavior
- **Full configuration** (`test_configuration.py`): simplex normalization, field presence
- **Selection conventions** (`test_selection.py`): status-quo, random, empty-maximizer error
- **Measurement operators** (`test_measurement.py`): linear measurement, cross-context validation
- **Qualifying conditions** (`test_qualifying.py`): proxy audit flags and passes
- **Boundary-Instability** (`test_instability.py`): three-design registry, safe sets, design shape
- **Retentionist conditions** (`test_retentionist.py`): R1 for retentionist and abolitionist
- **Metrics** (`test_metrics.py`): identity checks for each dispersion measure

---

## Citation

If you use `mctev-lib` in academic work, please cite both the paper and the library:

### Paper

```bibtex
@article{wang2026mctev,
  title   = {Toward a Computational Science of Ethics: A Multi-Level
             Computational Theory of Ethical Variation and Candidate
             Level 1 Moral Functions},
  author  = {Wang, Harris},
  year    = {2026},
  note    = {Manuscript in preparation}
}
```

### Library

```bibtex
@software{wang2026mctevlib,
  title   = {mctev-lib: Reference implementation of the Multi-Level
             Computational Theory of Ethics},
  author  = {Wang, Harris},
  version = {0.2.0},
  year    = {2026},
  url     = {https://github.com/hongxueharriswang/mctev-lib},
  license = {MIT}
}
```

### Sibling research program

```bibtex
@article{wang2025coh,
  title   = {Constrained Object Hierarchies as a Unified Theoretical Model
             for Intelligence and Intelligent Systems},
  author  = {Wang, Harris},
  journal = {Computers},
  volume  = {14},
  pages   = {478},
  year    = {2025},
  doi     = {10.3390/computers14110478}
}
```

---

## License

MIT License. See [`LICENSE`](LICENSE) for details.

---

## Acknowledgments

The MCTEV framework is methodologically aligned with the [COH/GISMOL](https://github.com/hongxueharriswang/gismol-lib) research program on hierarchical computational explanations of complex systems. The **Ethical Constraint Hierarchy Principle** — *constraints propagate downward, adaptation propagates upward* — captures the shared mechanism between the two frameworks.

---

**mctev-lib v0.2.0** · Built for reproducibility, falsifiability, and extension.

**Status**: The library implements the computational infrastructure for the MCTEV framework. It does not itself constitute an empirical validation of the framework, nor does it report results for the model architecture specified in the paper's Section 13. A DOI-minted archival release is planned before claims of archival reproducibility are made.