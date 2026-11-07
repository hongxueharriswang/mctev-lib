"""
mctev-lib — Multi-Level Computational Theory of Ethics
======================================================

Reference implementation of the MCTEV framework:

    Level 1: Candidate universal moral functions
    Level 2: Cultural parameter configurations
    Level 3: Situational judgments

Key components:
    - viability: Feasible moral region as viability kernel
    - flourishing: Five-dimensional flourishing construct
    - collapse: Constraint Violation Theorem (empirical)
    - simulation: Three Societies public goods model
    - cases: Slavery and capital punishment case studies
"""

from mctev.core.moral_functions import MoralFunction, MoralFunctionProfile
from mctev.core.cultural_params import CulturalParameters, CULTURAL_TYPES
from mctev.core.situational import SituationalJudgment, Situation, Action
from mctev.core.hierarchy import MCTEVSystem
from mctev.viability.constraints import ViabilityConstraints
from mctev.viability.dynamics import LinearDynamics, Dynamics
from mctev.viability.kernel import ViabilityKernel
from mctev.flourishing.dimensions import (
    FlourishingProfile,
    FlourishingThresholds,
)
from mctev.collapse.theorem import ConstraintViolationAnalyzer

__version__ = "0.1.0"
__all__ = [
    "MoralFunction",
    "MoralFunctionProfile",
    "CulturalParameters",
    "CULTURAL_TYPES",
    "SituationalJudgment",
    "Situation",
    "Action",
    "MCTEVSystem",
    "ViabilityConstraints",
    "LinearDynamics",
    "Dynamics",
    "ViabilityKernel",
    "FlourishingProfile",
    "FlourishingThresholds",
    "ConstraintViolationAnalyzer",
]
