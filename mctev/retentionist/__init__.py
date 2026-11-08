"""
Retentionist and abolitionist architectures with conditions (R1)-(R3)
(manuscript Section 12.3).
"""

from mctev.retentionist.architecture import (
    Architecture, RetentionistArchitecture, AbolitionistArchitecture,
)
from mctev.retentionist.conditions import (
    check_R1, check_R2, check_R3, evaluate_test_situations,
)

__all__ = [
    "Architecture", "RetentionistArchitecture", "AbolitionistArchitecture",
    "check_R1", "check_R2", "check_R3", "evaluate_test_situations",
]