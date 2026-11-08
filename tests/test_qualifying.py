import numpy as np

from mctev.core.moral_functions import MoralFunction
from mctev.core.qualifying import (
    QualifyingConditions, MemberInclusiveViability, proxy_audit,
)


def test_proxy_audit_flags_common_proxy():
    condition = MemberInclusiveViability(
        target_function=MoralFunction.RESOURCE_DISTRIBUTION,
        welfare_index=lambda x: np.array([x[0], x[3]]),
    )
    # Manually mark a common proxy for distribution as an input
    condition._inputs = ["gini_coefficient"]

    qc = QualifyingConditions()
    qc[MoralFunction.RESOURCE_DISTRIBUTION] = condition
    report = proxy_audit(qc, MoralFunction.RESOURCE_DISTRIBUTION)
    assert report.definitionally_independent is False
    assert "gini_coefficient" in report.flagged_proxies


def test_proxy_audit_passes_without_proxy():
    condition = MemberInclusiveViability(
        target_function=MoralFunction.RESOURCE_DISTRIBUTION,
        welfare_index=lambda x: np.array([x[0]]),
    )
    condition._inputs = ["cooperation_indicator"]
    qc = QualifyingConditions()
    qc[MoralFunction.RESOURCE_DISTRIBUTION] = condition
    report = proxy_audit(qc, MoralFunction.RESOURCE_DISTRIBUTION)
    assert report.definitionally_independent is True