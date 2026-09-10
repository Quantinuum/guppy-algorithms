"""Tests for classical THC preprocessing helpers."""

import numpy as np
import pytest

from guppyalgos.algorithms.block_encoding.thc import (
    THCParameters,
    THCPreparedTerm,
    build_select_data,
    build_thc_alias_terms,
    encode_combined_givens_rotations,
    encode_givens_rotations,
)
from guppyalgos.utils import bits_to_int


def test_build_thc_alias_terms_uses_none_for_one_body_nu() -> None:
    """Represent one-body terms without exposing the QROM sentinel as an index."""
    parameters = THCParameters(
        one_body_coefficients=np.array([0.75, -0.25, 1.5]),
        two_body_coefficients=np.array(
            [
                [0.8, 0.1, -0.2],
                [0.1, -0.4, 0.3],
                [-0.2, 0.3, 1.2],
            ]
        ),
        one_body_rotations=np.array([[0.0, 0.125], [0.25, 0.375], [0.5, 0.625]]),
        two_body_rotations=np.array([[0.125, 0.25], [0.375, 0.5], [0.625, 0.75]]),
    )

    assert build_thc_alias_terms(parameters) == [
        THCPreparedTerm(0, 0, 0.2),
        THCPreparedTerm(0, 1, 0.1),
        THCPreparedTerm(1, 1, -0.1),
        THCPreparedTerm(0, 2, -0.2),
        THCPreparedTerm(1, 2, 0.3),
        THCPreparedTerm(2, 2, 0.3),
        THCPreparedTerm(0, None, -0.75),
        THCPreparedTerm(1, None, 0.25),
        THCPreparedTerm(2, None, -1.5),
    ]


def test_build_select_data_encodes_one_body_extra_column() -> None:
    """Insert the one-body sentinel only when encoding the flat QROM table."""
    terms = [
        THCPreparedTerm(2, 4, -0.5),
        THCPreparedTerm(5, None, 0.5),
        THCPreparedTerm(0, 3, 0.25),
        THCPreparedTerm(7, None, -0.75),
    ]

    assert build_select_data(terms, 3, 6) == [
        [False, True, False, False, False, True, False, True],
        [True, False, True, False, True, True, True, False],
        [False, False, False, True, True, False, False, False],
        [True, True, True, False, True, True, True, True],
    ]


def test_encode_givens_rotations_does_not_add_identity_rows() -> None:
    """Encode exactly the physical rotation rows supplied to the QROM."""
    rotations = np.array(
        [
            [0.0, 0.125, 0.25],
            [0.375, 0.5, 0.625],
            [0.75, 0.875, 0.0625],
            [0.1875, 0.3125, 0.4375],
            [0.5625, 0.6875, 0.8125],
        ]
    )

    encoded = encode_givens_rotations(rotations, precision_bits=6, n_indices=8)

    assert len(encoded) == len(rotations)
    assert all(len(row) == 3 for row in encoded)
    assert all(len(angle) == 6 for row in encoded for angle in row)
    with pytest.raises(ValueError, match="do not fit"):
        encode_givens_rotations(rotations, precision_bits=6, n_indices=4)


def test_one_body_sentinel_selects_little_endian_combined_qrom_row() -> None:
    """Map ``(mu, c=1)`` to the matching one-body rotation row.

    The Select data stores ``mu`` in little-endian order and sets the one-body flag
    ``c``. Appending that flag to the ``mu`` bits makes it the most-significant
    bit, so the joined QROM address is ``2**n_index_qubits + mu``.
    """
    n_index_qubits = 3
    mu = 4
    one_body_sentinel = 6
    terms = [THCPreparedTerm(mu, None, 0.5)]
    select_data = build_select_data(
        terms,
        n_index_qubits,
        one_body_sentinel=one_body_sentinel,
    )[0]
    mu_bits = select_data[:n_index_qubits]
    nu_bits = select_data[n_index_qubits : 2 * n_index_qubits]
    one_body_flag = select_data[2 * n_index_qubits]

    two_body_rotations = np.array(
        [
            [0.0, 0.125, 0.25],
            [0.375, 0.5, 0.625],
            [0.75, 0.875, 0.0625],
            [0.1875, 0.3125, 0.4375],
            [0.5625, 0.6875, 0.8125],
            [0.9375, 0.03125, 0.15625],
        ]
    )
    one_body_rotations = np.array(
        [
            [0.21875, 0.34375, 0.46875],
            [0.59375, 0.71875, 0.84375],
            [0.96875, 0.09375, 0.28125],
            [0.40625, 0.53125, 0.65625],
            [0.78125, 0.90625, 0.046875],
        ]
    )
    combined_data = encode_combined_givens_rotations(
        two_body_rotations,
        one_body_rotations,
        precision_bits=4,
        n_index_qubits=n_index_qubits,
    )
    expected_one_body_data = encode_givens_rotations(
        one_body_rotations,
        precision_bits=4,
        n_indices=2**n_index_qubits,
    )
    expected_two_body_data = encode_givens_rotations(
        two_body_rotations,
        precision_bits=4,
        n_indices=2**n_index_qubits,
    )

    joined_address = bits_to_int([*mu_bits, one_body_flag])
    assert bits_to_int(nu_bits) == one_body_sentinel
    assert one_body_flag
    assert joined_address == (2**n_index_qubits) + mu
    assert combined_data[mu] == expected_two_body_data[mu]
    assert combined_data[joined_address] == expected_one_body_data[mu]
    assert combined_data[6] == [[False] * 4 for _ in range(3)]
    assert combined_data[7] == [[False] * 4 for _ in range(3)]
