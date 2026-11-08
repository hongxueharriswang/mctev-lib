"""
mctev-lib — Multi-Level Computational Theory of Ethics (v0.2.0)

Reference implementation aligned with the current manuscript:

    λ_c = (θ_c, τ^V, τ^S, τ^H, ρ_c, M_c)

Key components:
    - core.thresholds: three threshold families
    - core.configuration: full Level-2 cultural configuration λ_c
    - core.selection: selection conventions ρ_c
    - core.measurement: measurement operators M_c
    - core.qualifying: Q_{-i} and the proxy audit
    - core.situational: situation-dependent A(s)
    - instability: Boundary-Instability Hypothesis with index/outcome sets
    - retentionist: retentionist conditions (R1)-(R3)
"""

from mctev.core.moral_functions import (
    MoralFunction, MoralFunctionProfile, MoralUtilityLibrary,
    MORAL_FUNCTION_ORDER, N_FUNCTIONS,
)
from mctev.core.thresholds import (
    ViabilityThresholds, SafeguardThresholds, FlourishingThresholds,
    ThresholdFamilies,
)
from mctev.core.configuration import CulturalConfiguration
from mctev.core.selection import SelectionConvention
from mctev.core.measurement import MeasurementOperator, LinearMeasurement
from mctev.core.qualifying import QualifyingConditions, QualifyingCondition
from mctev.core.situational import (
    Situation, Action, SituationalJudgment, ConstraintPredicate,
)
from mctev.core.hierarchy import MCTEVSystem
from mctev.viability.constraints import ViabilityConstraints
from mctev.viability.dynamics import LinearDynamics, Dynamics
from mctev.viability.kernel import ViabilityKernel, compute_viable_region
from mctev.instability.safe_sets import (
    SafeSet, IndicatorSafeSet, KernelSafeSet,
)
from mctev.instability.analyzer import (
    BoundaryInstabilityAnalyzer, InstabilityResult,
)
from mctev.instability.survival import set_specific_survival
from mctev.flourishing.dimensions import (
    FlourishingProfile, FlourishingDimension,
)
from mctev.retentionist.architecture import (
    RetentionistArchitecture, AbolitionistArchitecture, Architecture,
)
from mctev.retentionist.conditions import check_R1, check_R2, check_R3

__version__ = "0.2.0"

__all__ = [
    # Core
    "MoralFunction", "MoralFunctionProfile", "MoralUtilityLibrary",
    "MORAL_FUNCTION_ORDER", "N_FUNCTIONS",
    # Thresholds
    "ViabilityThresholds", "SafeguardThresholds", "FlourishingThresholds",
    "ThresholdFamilies",
    # Configuration
    "CulturalConfiguration",
    # Selection / measurement
    "SelectionConvention", "MeasurementOperator", "LinearMeasurement",
    # Qualifying
    "QualifyingConditions", "QualifyingCondition",
    # Situational
    "Situation", "Action", "SituationalJudgment", "ConstraintPredicate",
    # Hierarchy
    "MCTEVSystem",
    # Viability
    "ViabilityConstraints", "LinearDynamics", "Dynamics",
    "ViabilityKernel", "compute_viable_region",
    # Instability
    "SafeSet", "IndicatorSafeSet", "KernelSafeSet",
    "BoundaryInstabilityAnalyzer", "InstabilityResult",
    "set_specific_survival",
    # Flourishing
    "FlourishingProfile", "FlourishingDimension",
    # Retentionist
    "Architecture", "RetentionistArchitecture", "AbolitionistArchitecture",
    "check_R1", "check_R2", "check_R3",
]