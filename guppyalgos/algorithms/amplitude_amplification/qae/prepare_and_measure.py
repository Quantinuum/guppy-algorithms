r"""Prepare-and-measure amplitude estimation.

The simplest amplitude estimator: prepare the state :math:`A\ket{0}` and measure the
distinguished *target* qubit in the computational basis. Repeating this ``repeat`` times
and taking the fraction of :math:`\ket{1}` outcomes estimates the amplitude. This
carries no quantum speedup (it is equivalent to classical Monte Carlo sampling), but it
is a useful baseline and building block.

The state-preparation unitary :math:`A` is supplied as a higher-order argument, so both
functions compose directly into a larger workflow. Qubit allocation is handled
internally; the calling workflow only needs to record the returned value.
"""

from collections.abc import Callable
from typing import no_type_check

from guppylang import guppy
from guppylang.std.builtins import array, nat
from guppylang.std.quantum import discard_array, measure, qubit

from guppyalgos.utils import qarray


@guppy
@no_type_check
def prepare_and_measure_once[n: nat](
    state_prep: Callable[[array[qubit, n], qubit], None],
) -> bool:
    r"""Prepare :math:`A\ket{0}` and measure the target qubit once.

    Allocates an ``n``-qubit register together with a single target qubit, all in
    :math:`\ket{0}`, applies the state-preparation unitary ``state_prep`` (:math:`A`),
    and measures the target in the computational basis. The register is discarded.

    Args:
        state_prep: The state-preparation unitary :math:`A`, acting on the register
            (assumed to start in :math:`\ket{0}`) and the target qubit. It must flag the
            "good" subspace on the target qubit, i.e. arrange that measuring the target
            yields :math:`\ket{1}` with probability equal to the amplitude.

    Returns:
        The measured target outcome, ``True`` for :math:`\ket{1}` and ``False`` for
        :math:`\ket{0}`.

    """
    register = qarray(n)
    target = qubit()
    state_prep(register, target)
    outcome = measure(target).read()
    discard_array(register)
    return outcome


@guppy
@no_type_check
def prepare_and_measure[n: nat](
    state_prep: Callable[[array[qubit, n], qubit], None],
    repeat: nat,
) -> float:
    r"""Estimate the amplitude by repeated prepare-and-measure sampling.

    Runs :func:`prepare_and_measure_once` ``repeat`` times and returns the fraction of
    repetitions in which the target was measured in :math:`\ket{1}`, i.e.
    ``count(1) / repeat``. The estimate converges to the amplitude
    :math:`a = P(\text{target} = 1)` with standard error :math:`\sqrt{a(1-a)/repeat}`.

    Args:
        state_prep: The state-preparation unitary :math:`A`; see
            :func:`prepare_and_measure_once`.
        repeat: The number of prepare-and-measure repetitions. Must be at least ``1``.

    Returns:
        The estimated amplitude in ``[0, 1]``.

    """
    successes = 0
    for _ in range(repeat):
        successes += 1 if prepare_and_measure_once(state_prep) else 0
    return successes / repeat
