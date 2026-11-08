# Changelog

## [0.2.0] — 2026-11-07

### Added

- **Three threshold families**: `ViabilityThresholds` (τ^V), `SafeguardThresholds` (τ^S), `FlourishingThresholds` (τ^H), and a `ThresholdFamilies` container, per manuscript Section 7.1.
- **Full configuration**: `CulturalConfiguration` with the full λ_c = (θ_c, τ^V, τ^S, τ^H, ρ_c, M_c), per Section 7.2.
- **Selection conventions**: `SelectionConvention` enum and `select_action` function implementing PRECEDENT, MINIMUM_INTERVENTION, STATUS_QUO, LEXICOGRAPHIC, and RANDOM (Section 7.4).
- **Measurement operators**: `MeasurementOperator` ABC and `LinearMeasurement` baseline; `validate_cross_context_comparability` helper (Section 8.2).
- **Qualifying conditions**: `QualifyingCondition` ABC, `MemberInclusiveViability`, `MinimumFlourishing`, `QualifyingConditions`, and the `proxy_audit` diagnostic (Section 6.3, Supplement S12).
- **Boundary-Instability module** (`mctev.instability`) replacing the `collapse` module:
  - `SafeSet`, `IndicatorSafeSet`, `KernelSafeSet` (Section 10.6 index boundaries);
  - `set_specific_survival` implementing q_{T,K_out}^π (Section 10.4);
  - `BoundaryInstabilityAnalyzer` with `design_B` and `build_three_designs` for the three distinguishable designs of Section 10.6.
- **Retentionist module** (`mctev.retentionist`) with `Architecture`, `RetentionistArchitecture`, `AbolitionistArchitecture`, `check_R1`, `check_R2`, `check_R3`, `CapitalActionSet`, `evaluate_test_situations`, and `anti_triviality_filter` (Section 12.3).
- **Expanded dispersion measures** in `mctev.analysis.metrics`: `D_F`, `D_θ` (Aitchison primary, JS secondary), `D_{τ^V}`, `D_{τ^S}`, `D_{τ^H}`, `D_ρ` (shared-benchmark), `D_M`, `D_J`, and `full_dispersion_vector` (Section 14).
- **Example scripts**: `demo_index_outcome_designs.py`, `demo_capital_punishment.py`.
- **Tests**: `test_thresholds.py`, `test_configuration.py`, `test_selection.py`, `test_measurement.py`, `test_qualifying.py`, `test_instability.py`, `test_retentionist.py`, `test_metrics.py`.

### Changed

- **Breaking**: `CulturalConfiguration` replaces `CulturalParameters` as the primary Level-2 object. The old class is retained as a deprecated shim.
- **Breaking**: `SituationalJudgment.judge()` now takes a `CulturalConfiguration` (which carries the selection convention ρ_c) and threads the safeguard thresholds τ^S into the constraint predicate.
- **Breaking**: `ViabilityKernel` and `compute_viable_region` now take a `CulturalConfiguration` (which carries τ^V).
- **Breaking**: `FlourishingThresholds` moved from `mctev.flourishing.dimensions` to `mctev.core.thresholds`; the old import path still works but is deprecated.
- The `collapse` module is deprecated; all its content is re-exported from `instability` with a warning. `ConstraintViolationAnalyzer` is aliased to `BoundaryInstabilityAnalyzer` but no longer reflects the manuscript's terminology.

### Deprecated

- `CulturalParameters` → `CulturalConfiguration` / `default_configuration`.
- `mctev.collapse` module → `mctev.instability`.
- `FlourishingThresholds` imported from `mctev.flourishing.dimensions` → from `mctev.core.thresholds`.

### Removed

- Nothing. All v0.1.0 public APIs remain importable (some via deprecation shims).

## [0.1.0] — 2026-11-06

- Initial release. See MIGRATION.md for a summary of how v0.1.0 maps to v0.2.0.