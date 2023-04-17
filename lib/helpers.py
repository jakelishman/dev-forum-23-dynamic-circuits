# This code is part of Qiskit.
#
# (C) Copyright IBM 2023.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import functools

from qiskit import qasm3
from qiskit.circuit import SwitchCaseOp, ControlFlowOp, QuantumCircuit
from qiskit_ibm_provider import IBMBackend


def _has_switch(circuit: QuantumCircuit) -> bool:
    """Does this circuit contain a `switch` instruction?"""
    for inst in circuit.data:
        if isinstance(inst.operation, SwitchCaseOp):
            return True
        if isinstance(inst.operation, ControlFlowOp):
            for block in inst.operation.blocks:
                if _has_switch(block):
                    return True
    return False


class _wrap_backend_run:
    """Wrap an IBM Provider `IBMBackend`'s `run` method with a callable that converts circuit inputs
    that contain `switch` statements into suitable OpenQASM 3 using Terra's pre-release exporter, to
    avoid issues caused by the full stack not yet being updated."""

    # This is a class rather than a function defining an inner function just to avoid any possible
    # issues with pickle - we don't want to waste time debugging our own helper.

    __wrapped__ = True

    def __init__(self, inner):
        self._inner = inner

    def __call__(self, circuit, *args, dynamic=False, **kwargs):
        if dynamic and isinstance(circuit, QuantumCircuit) and _has_switch(circuit):
            circuit = qasm3.dumps(
                circuit,
                disable_constants=True,
                experimental=qasm3.ExperimentalFeatures.SWITCH_CASE_V1,
            )
        return self._inner(circuit, *args, dynamic=dynamic, **kwargs)


def add_switch_support(backend: IBMBackend) -> IBMBackend:
    """Add support for the `switch` statement to an IBM backend.

    This includes adding support so that Qiskit's `transpile` method will know how to compile for
    the backend, and so the backend will accept circuits with `switch` statements in for its
    `backend.run(dynamic=True)` calls.  This mutates the given backend instance.

    For example, you can do::

        import helpers
        import qiskit_ibm_provider

        provider = qiskit_ibm_provider.IBMProvider()
        backend = helpers.add_switch_support(provider.get_backend("ibm_wellington"))

    and then use `backend` like normal."""
    # Hack #1: monkey-patch information about the `switch` statement into the backend's `Target`, so
    # the Terra transpiler knows about it.  Fixing this requires a deployment of the backends.
    if "switch_case" not in backend.target:
        backend.target.add_instruction(SwitchCaseOp, name="switch_case")

    # Hack #2: wrap the backend's `run` method to intercept runs of circuits that contain
    # `SwitchCaseOp` to manually submit them as OQ3 strings.  Fixing this requires the new version
    # of QPY to be deployed in Qiskit Runtime, and for the Runtime to learn to pass the experimental
    # feature flag that enables `switch`-statement exporting during its internal conversions.
    if not getattr(backend.run, "__wrapped__", False):
        backend.run = functools.wraps(backend.run)(_wrap_backend_run(backend.run))

    return backend
