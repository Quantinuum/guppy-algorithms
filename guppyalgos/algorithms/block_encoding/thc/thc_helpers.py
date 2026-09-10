"""Classical preprocessing helpers for THC circuit construction."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from guppyalgos.utils import float_to_fixed_point, int_to_bits


@dataclass(frozen=True)
class THCParameters:
    r"""Classical parameters appearing in the factorized THC Hamiltonian.

    Args:
        one_body_coefficients: The :math:`t_k` coefficients.
        two_body_coefficients: Symmetric :math:`\zeta_{\mu\nu}` coefficient matrix.
        one_body_rotations: Full-turn neighboring-Givens angles defining
            :math:`V_k`.
        two_body_rotations: Full-turn neighboring-Givens angles defining
            :math:`U_\mu`.

    """

    one_body_coefficients: NDArray[np.float64]
    two_body_coefficients: NDArray[np.float64]
    one_body_rotations: NDArray[np.float64]
    two_body_rotations: NDArray[np.float64]


@dataclass(frozen=True)
class THCPreparedTerm:
    """One term in the unified THC alias-sampling table.

    Args:
        mu: Index of the first orbital transformation.
        nu: Index of the second orbital transformation for a two-body term, or
            ``None`` for a one-body term.
        coefficient: Signed coefficient prepared by the LCU construction.

    """

    mu: int
    nu: int | None
    coefficient: float

    @property
    def is_one_body(self) -> bool:
        """Whether this entry represents a one-body term."""
        return self.nu is None


def generate_thc_parameters(
    n_orbitals: int,
    thc_rank: int,
    *,
    seed: int = 7,
) -> THCParameters:
    """Generate deterministic example coefficients and orbital rotations.

    The generated arrays have the shapes required by the BLISS-THC expression.
    This helper is intended for examples and compilation studies; production
    applications should construct :class:`THCParameters` from chemistry data.
    """
    rng = np.random.default_rng(seed)
    one_body_coefficients = rng.choice([-1.0, 1.0], n_orbitals) * rng.uniform(
        0.5, 1.5, n_orbitals
    )
    upper_two_body = np.zeros((thc_rank, thc_rank), dtype=np.float64)
    for nu in range(thc_rank):
        for mu in range(nu + 1):
            upper_two_body[mu, nu] = rng.choice([-1.0, 1.0]) * rng.uniform(0.5, 1.5)
    two_body_coefficients = upper_two_body + np.triu(upper_two_body, 1).T
    one_body_rotations = rng.random((n_orbitals, n_orbitals - 1))
    two_body_rotations = rng.random((thc_rank, n_orbitals - 1))
    return THCParameters(
        one_body_coefficients,
        two_body_coefficients,
        one_body_rotations,
        two_body_rotations,
    )


def build_thc_alias_terms(parameters: THCParameters) -> list[THCPreparedTerm]:
    r"""Build the unified term table consumed by alias-sampling PREPARE.

    Two-body terms cover the upper triangle ``mu <= nu``. Their off-diagonal
    weights are :math:`\zeta_{\mu\nu}`, while diagonal weights are
    :math:`\zeta_{\mu\mu}/4`. One-body terms have ``nu=None`` and weights
    :math:`-t_\mu`.

    The paper's fixed-width quantum encoding can be pictured as appending an
    extra column ``nu = M`` to the two-body coefficient matrix and placing the
    one-body terms in that column. This user-facing table represents that extra
    column with ``nu=None``; :func:`build_select_data` introduces the integer
    sentinel ``M`` only when producing the QROM data.
    """
    terms = [
        THCPreparedTerm(
            mu,
            nu,
            float(
                parameters.two_body_coefficients[mu, nu] / (4.0 if mu == nu else 1.0)
            ),
        )
        for nu in range(parameters.two_body_coefficients.shape[0])
        for mu in range(nu + 1)
    ]
    terms.extend(
        THCPreparedTerm(mu, None, float(-coefficient))
        for mu, coefficient in enumerate(parameters.one_body_coefficients)
    )
    return terms


def encode_givens_rotations(
    rotations: NDArray[np.float64],
    precision_bits: int,
    n_indices: int,
) -> list[list[list[bool]]]:
    """Encode supplied Givens angles without padding to ``n_indices`` rows.

    Raises:
        ValueError: If the supplied rotation rows do not fit in the declared
            index space.

    """
    if len(rotations) > n_indices:
        raise ValueError("Givens rotation rows do not fit in the index register.")

    return [
        [float_to_fixed_point(float(angle), precision_bits) for angle in row]
        for row in rotations
    ]


def encode_combined_givens_rotations(
    two_body_rotations: NDArray[np.float64],
    one_body_rotations: NDArray[np.float64],
    precision_bits: int,
    n_index_qubits: int,
) -> list[list[list[bool]]]:
    """Encode the combined rotation QROM addressed by little-endian ``[mu, c]``.

    The one-body flag ``c`` is the most-significant address bit. Consequently,
    two-body rows occupy addresses ``mu`` and one-body rows occupy addresses
    ``2**n_index_qubits + mu``. Unused two-body addresses between the physical THC
    rank and the start of the one-body block are filled with zero angles.

    Args:
        two_body_rotations: Givens angles defining each two-body ``U_mu``.
        one_body_rotations: Givens angles defining each one-body ``V_mu``.
        precision_bits: Number of bits used to encode each angle.
        n_index_qubits: Width of the ``mu`` register before appending ``c``.

    """
    if two_body_rotations.shape[1:] != one_body_rotations.shape[1:]:
        raise ValueError("One- and two-body rotations must have the same row width.")

    one_body_offset = 2**n_index_qubits
    if len(two_body_rotations) > one_body_offset:
        raise ValueError("Two-body rotations do not fit in the mu index register.")
    if len(one_body_rotations) > one_body_offset:
        raise ValueError("One-body rotations do not fit in the mu index register.")

    two_body_data = encode_givens_rotations(
        two_body_rotations,
        precision_bits,
        one_body_offset,
    )
    one_body_data = encode_givens_rotations(
        one_body_rotations,
        precision_bits,
        one_body_offset,
    )
    unused_two_body_rows = one_body_offset - len(two_body_data)
    unused_data = [
        [[False] * precision_bits for _ in range(two_body_rotations.shape[1])]
        for _ in range(unused_two_body_rows)
    ]
    return [
        *two_body_data,
        *unused_data,
        *one_body_data,
    ]


def build_select_data(
    terms: list[THCPreparedTerm],
    n_index_qubits: int,
    one_body_sentinel: int,
) -> list[list[bool]]:
    """Encode ``(mu, nu, one-body, sign)`` for each flat alias index.

    A one-body entry has no mathematical ``nu`` index. For the fixed-width
    register layout used by ``SelectTHCCntrl``, it is encoded in the conceptual
    extra
    column ``nu = one_body_sentinel``.
    """
    return [
        [
            *int_to_bits(term.mu, n_index_qubits),
            *int_to_bits(
                one_body_sentinel if term.nu is None else term.nu,
                n_index_qubits,
            ),
            term.is_one_body,
            term.coefficient < 0.0,
        ]
        for term in terms
    ]


def validate_thc_parameters(parameters: THCParameters) -> tuple[int, int]:
    """Validate the array shapes and return ``(n_modes, thc_rank)``."""
    n_modes = len(parameters.one_body_coefficients)
    if n_modes < 2:
        raise ValueError("THC LCU construction requires at least two orbitals.")

    if parameters.two_body_coefficients.ndim != 2:
        raise ValueError("two_body_coefficients must be a square matrix.")
    thc_rank, second_rank = parameters.two_body_coefficients.shape
    if thc_rank == 0 or second_rank != thc_rank:
        raise ValueError("two_body_coefficients must be a non-empty square matrix.")
    if parameters.one_body_rotations.shape != (n_modes, n_modes - 1):
        raise ValueError("one_body_rotations must have shape (n_modes, n_modes - 1).")
    if parameters.two_body_rotations.shape != (thc_rank, n_modes - 1):
        raise ValueError("two_body_rotations must have shape (thc_rank, n_modes - 1).")
    return n_modes, thc_rank
