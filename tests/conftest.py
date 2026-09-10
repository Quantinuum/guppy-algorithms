"""Conftest file for test parameterization with fixture."""

import pytest
from pytest_lazy_fixtures import lf as lazy_fixture
from typing import Any

import sys

from guppylang_internals.diagnostic import DiagnosticsRenderer
from guppylang_internals.engine import DEF_STORE
from guppylang_internals.error import GuppyError


def pytest_exception_interact(
        node: pytest.Item,
        call: pytest.CallInfo[Any],
        report: pytest.CollectReport|pytest.TestReport
    )->None:
    """Insert guppy compiler errors into test errors."""
    if call.excinfo is not None:
        exc = call.excinfo.value
        if isinstance(exc, GuppyError):
            _render_guppy_error(exc)


def _render_guppy_error(err: GuppyError) -> None:
    sys.stderr.write("\n")
    renderer = DiagnosticsRenderer(DEF_STORE.sources)
    renderer.render_diagnostic(err.error)
    sys.stderr.write("\n".join(renderer.buffer))
    sys.stderr.write("\n\nGuppy compilation failed due to 1 previous error\n")


###### ZIXY OPERATOR FIXTURES ######

import zixy.qubit.pauli as zqp


# 1-qubit hermitian (real) operators
@pytest.fixture()
def ham_1q_posreal_0() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str("(0.1, X0), (0.4, Y0)")


@pytest.fixture()
def ham_1q_posreal_1() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str("(0.3, Y0), (0.2, X0)")


@pytest.fixture()
def ham_1q_posreal_2() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str("(0.5, Z0), (0.1, X0)")


@pytest.fixture()
def ham_1q_posreal_3() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str("(0.5, Y0), (0.1, Z0)")


@pytest.fixture()
def ham_1q_posreal_4() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str("(0.3, I0), (0.2, X0)")


@pytest.fixture()
def ham_1q_posreal_5() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str("(0.5, I0), (0.1, X0)")


@pytest.fixture()
def ham_1q_posreal_6() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str("(0.5, Y0), (0.1, I0)")


@pytest.fixture()
def ham_1q_negreal_0() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str("(-0.1, X0), (-0.4, Z0)")


# 1-qubit non-hermitian (imaginary) operators
@pytest.fixture()
def ham_1q_posimaginary_0() -> zqp.ComplexTermSum:
    return zqp.ComplexTermSum.from_str("(0.1j, X0), (0.4j, Y0)")


@pytest.fixture()
def ham_1q_negimaginary_1() -> zqp.ComplexTermSum:
    return zqp.ComplexTermSum.from_str("(-0.3j, Y0), (-0.2j, X0)")


# 2-qubit hermitian (real) operators
@pytest.fixture()
def ham_2q_posreal_0() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str("(0.5, Z0 X1), (0.1, X0 Z1)")


@pytest.fixture()
def ham_2q_posreal_1() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str("(0.3, Y0 Z1), (0.2, X0 X1)")


@pytest.fixture()
def ham_2q_posreal_2() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str("(0.5, Y0 Y1), (0.1, X0 Z1)")


@pytest.fixture()
def ham_2q_posreal_3() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str("(0.5, I0), (0.1, X0 Z1)")


@pytest.fixture()
def ham_2q_posreal_4() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str("(0.5, I0), (0.1, X0 Z1)")


@pytest.fixture()
def ham_2q_negreal_0() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str("(-0.5, Z0 X1), (-0.1, X0 Z1)")


@pytest.fixture()
def ham_2q_negreal_1() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str("(-0.3, Y0 Z1), (-0.2, X0 X1)")


# 2-qubit non-hermitian
@pytest.fixture()
def ham_2q_posimaginary_0() -> zqp.ComplexTermSum:
    return zqp.ComplexTermSum.from_str("(0.5j, Z0 X1), (0.1j, X0 Z1)")


@pytest.fixture()
def ham_2q_posimaginary_1() -> zqp.ComplexTermSum:
    return zqp.ComplexTermSum.from_str("(0.3j, Y0 Z1), (0.2j, X0 X1)")


@pytest.fixture()
def ham_2q_negimaginary_0() -> zqp.ComplexTermSum:
    return zqp.ComplexTermSum.from_str("(-0.5j, Z0 X1), (-0.1j, X0 Z1)")


@pytest.fixture()
def ham_2q_negimaginary_1() -> zqp.ComplexTermSum:
    return zqp.ComplexTermSum.from_str("(-0.3j, Y0 Z1), (-0.2j, X0 X1)")


@pytest.fixture()
def ham_2q_mixed_0() -> zqp.ComplexTermSum:
    return zqp.ComplexTermSum.from_str("(0.7, Z0 X1), (-0.9j, X0 Z1)")


@pytest.fixture()
def ham_2q_mixed_1() -> zqp.ComplexTermSum:
    return zqp.ComplexTermSum.from_str("(0.7, Y0 Z1), (-0.8j, X0 X1)")


# 3-qubit hermitian (real) operators
@pytest.fixture()
def ham_3q_posreal_0() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str(
        "(0.5, Z0 X1 Y2), (0.1, X0 Z1 Z2), (0.2, Y0 Y1 X2), (0.3, X0 X1 Y2)"
    )


@pytest.fixture()
def ham_3q_posreal_1() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str(
        "(0.5, Y0 Z1 X2), (0.1, X0 X1 Z2), (0.2, Y0 Y1 Y2), (0.3, X0 Z1 X2)"
    )


@pytest.fixture()
def ham_3q_negreal_0() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str(
        "(-0.5, Z0 X1 Y2), (-0.1, X0 Z1 Z2), (-0.2, Y0 Y1 X2), (-0.3, X0 X1 Y2)"
    )


@pytest.fixture()
def ham_3q_negreal_1() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str(
        "(-0.5, Y0 Z1 X2), (-0.1, X0 X1 Z2), (-0.2, Y0 Y1 Y2), (-0.3, X0 Z1 X2)"
    )


# 3-qubit non-hermitian
@pytest.fixture()
def ham_3q_posimaginary_0() -> zqp.ComplexTermSum:
    return zqp.ComplexTermSum.from_str(
        "(0.5j, Z0 X1 Y2), (0.1j, X0 Z1 Z2), (0.2j, Y0 Y1 X2), (0.3j, X0 X1 Y2)"
    )


@pytest.fixture()
def ham_3q_posimaginary_1() -> zqp.ComplexTermSum:
    return zqp.ComplexTermSum.from_str(
        "(0.5j, Y0 Z1 X2), (0.1j, X0 X1 Z2), (0.2j, Y0 Y1 Y2), (0.3j, X0 Z1 X2)"
    )


@pytest.fixture()
def ham_3q_negimaginary_0() -> zqp.ComplexTermSum:
    return zqp.ComplexTermSum.from_str(
        "(-0.5j, Z0 X1 Y2), (-0.1j, X0 Z1 Z2), (-0.2j, Y0 Y1 X2), (-0.3j, X0 X1 Y2)"
    )


@pytest.fixture()
def ham_3q_negimaginary_1() -> zqp.ComplexTermSum:
    return zqp.ComplexTermSum.from_str(
        "(-0.5j, Y0 Z1 X2), (-0.1j, X0 X1 Z2), (-0.2j, Y0 Y1 Y2), (-0.3j, X0 Z1 X2)"
    )


@pytest.fixture()
def ham_3q_mixed_0() -> zqp.ComplexTermSum:
    return zqp.ComplexTermSum.from_str(
        "(0.5, Z0 X1 Y2), (0.1, X0 Z1 Z2), (0.7j, Y0 Y1 X2), (-0.6j, X0 X1 Y2)"
    )


@pytest.fixture()
def ham_commuting_comp_basis_example_0() -> tuple[zqp.RealTermSum, float]:
    """Small commuting Hamiltonian diagonal in the computational basis."""
    return zqp.RealTermSum.from_str("(0.5, Z0), (0.25, Z1), (0.25, Z0 Z1)"), -1.5


@pytest.fixture()
def ham_commuting_comp_basis_example_1() -> tuple[zqp.RealTermSum, float]:
    """Small commuting Hamiltonian diagonal in the computational basis."""
    return zqp.RealTermSum.from_str("(0.4, Z0), (-0.2, Z1), (0.1, Z0 Z1)"), 0.8


@pytest.fixture()
def ham_commuting_comp_basis_example_2() -> tuple[zqp.RealTermSum, float]:
    """Three-qubit commuting Hamiltonian diagonal in the computational basis."""
    return (
        zqp.RealTermSum.from_str(
            "(0.5, Z0), (-0.25, Z1), (0.125, Z2), (0.25, Z0 Z1), (-0.125, Z1 Z2)"
        ),
        -1.5,
    )


@pytest.fixture()
def ham_noncommuting_example_0() -> tuple[zqp.RealTermSum, float]:
    """Notebook noncommuting Hamiltonian paired with its example timestep."""
    return (
        zqp.RealTermSum.from_str("(0.6708203932499369, X0), (-1.3416407864998738, Z0)"),
        1.0,
    )


@pytest.fixture()
def ham_1q_mixedreal_0(
    ham_noncommuting_example_0: tuple[zqp.RealTermSum, float],
) -> zqp.RealTermSum:
    """One-qubit Hermitian Hamiltonian with mixed-sign coefficients."""
    return ham_noncommuting_example_0[0]


@pytest.fixture()
def ham_2q_mixedreal_0(
    ham_commuting_comp_basis_example_1: tuple[zqp.RealTermSum, float],
) -> zqp.RealTermSum:
    """Two-qubit Hermitian Hamiltonian with mixed-sign coefficients."""
    return ham_commuting_comp_basis_example_1[0]


@pytest.fixture()
def ham_noncommuting_example_1(
    ham_1q_posreal_2: zqp.RealTermSum,
) -> tuple[zqp.RealTermSum, float]:
    """One-qubit noncommuting Hamiltonian paired with a representative timestep."""
    return ham_1q_posreal_2, 0.3


@pytest.fixture()
def ham_noncommuting_example_2(
    ham_3q_posreal_0: zqp.RealTermSum,
) -> tuple[zqp.RealTermSum, float]:
    """Three-qubit noncommuting Hamiltonian paired with a representative timestep."""
    return ham_3q_posreal_0, 0.2


@pytest.fixture(
    params=[
        lazy_fixture("ham_commuting_comp_basis_example_0"),
        lazy_fixture("ham_commuting_comp_basis_example_1"),
        lazy_fixture("ham_commuting_comp_basis_example_2"),
    ]
)
def ham_commuting_comp_basis_fixture(
    request: Any,
) -> tuple[zqp.RealTermSum, float]:
    """Small commuting Hamiltonians diagonal in the computational basis."""
    return request.param


@pytest.fixture(
    params=[
        lazy_fixture("ham_noncommuting_example_0"),
        lazy_fixture("ham_noncommuting_example_1"),
        lazy_fixture("ham_noncommuting_example_2"),
    ]
)
def ham_noncommuting_fixture(request: Any) -> tuple[zqp.RealTermSum, float]:
    """Small noncommuting Hamiltonians paired with example timesteps."""
    return request.param


# Parameterized zixy operator fixtures mirroring the pytket ones
@pytest.fixture(
    params=[
        lazy_fixture("ham_1q_posreal_0"),
        lazy_fixture("ham_1q_posreal_1"),
        lazy_fixture("ham_1q_posreal_2"),
        lazy_fixture("ham_1q_posreal_3"),
        lazy_fixture("ham_1q_posreal_4"),
        lazy_fixture("ham_1q_posreal_5"),
        lazy_fixture("ham_1q_posreal_6"),
        lazy_fixture("ham_1q_negreal_0"),
        lazy_fixture("ham_2q_posreal_0"),
        lazy_fixture("ham_2q_posreal_1"),
        lazy_fixture("ham_2q_posreal_2"),
        lazy_fixture("ham_2q_posreal_3"),
        lazy_fixture("ham_2q_posreal_4"),
        lazy_fixture("ham_2q_negreal_0"),
        lazy_fixture("ham_2q_negreal_1"),
        lazy_fixture("ham_3q_posreal_0"),
        lazy_fixture("ham_3q_posreal_1"),
        lazy_fixture("ham_3q_negreal_0"),
        lazy_fixture("ham_3q_negreal_1"),
    ]
)
def op_hermitian_fixture(request: Any) -> zqp.RealTermSum:
    """Rupauli: parameterized hermitian operators."""
    return request.param


@pytest.fixture(
    params=[
        lazy_fixture("ham_1q_posimaginary_0"),
        lazy_fixture("ham_1q_negimaginary_1"),
        lazy_fixture("ham_2q_posimaginary_0"),
        lazy_fixture("ham_2q_posimaginary_1"),
        lazy_fixture("ham_2q_negimaginary_0"),
        lazy_fixture("ham_2q_negimaginary_1"),
        lazy_fixture("ham_2q_mixed_0"),
        lazy_fixture("ham_2q_mixed_1"),
        lazy_fixture("ham_3q_posimaginary_0"),
        lazy_fixture("ham_3q_posimaginary_1"),
        lazy_fixture("ham_3q_negimaginary_0"),
        lazy_fixture("ham_3q_negimaginary_1"),
        lazy_fixture("ham_3q_mixed_0"),
    ]
)
def op_nonhermitian_fixture(request: Any) -> zqp.ComplexTermSum:
    """Rupauli: parameterized nonhermitian operators."""
    return request.param


@pytest.fixture(
    params=[
        lazy_fixture("op_hermitian_fixture"),
        lazy_fixture("op_nonhermitian_fixture"),
    ]
)
def op_fixture(request: Any) -> Any:
    """Rupauli: parameterized operators (hermitian and nonhermitian)."""
    return request.param


@pytest.fixture()
def ham_h2_sto3g_jw() -> zqp.RealTermSum:
    return zqp.RealTermSum.from_str(
        "(-0.05962058276034765, I0), (0.1757594291831968, Z0), (0.17575942918319679, Z1), (0.17001546439603182, Z0 Z1), "
        "(0.044917169890753894, X0 Y1 Y2 X3), (-0.044917169890753894, X0 X1 Y2 Y3), (-0.044917169890753894, Y0 Y1 X2 X3), "
        "(0.044917169890753894, Y0 X1 X2 Y3), (-0.23667117678035537, Z2), (0.12222714936261826, Z0 Z2), (0.16714431925337217, Z1 Z2), "
        "(-0.23667117678035543, Z3), (0.16714431925337217, Z0 Z3), (0.12222714936261826, Z1 Z3), (0.1757033833190701, Z2 Z3)"
    )
