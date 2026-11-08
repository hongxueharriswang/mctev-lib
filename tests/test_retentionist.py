from mctev.retentionist.architecture import (
    RetentionistArchitecture, AbolitionistArchitecture,
)
from mctev.retentionist.conditions import check_R1


def test_R1_retentionist():
    a = RetentionistArchitecture(name="A_R")
    assert check_R1(a) is True


def test_R1_abolitionist():
    a = AbolitionistArchitecture(name="A_A")
    assert check_R1(a) is False