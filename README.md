# Dynamic Circuits Track

*Facilitators: Jake Lishman and Kevin Krsulich*

The purpose of this track is to gain familiarity with building and executing dynamic circuits on IBM hardware using Qiskit.
We hope to use your experiences to find out:

- pain points in constructing and working with dynamic circuits
- how users go about preparing a dynamic circuit to run on hardware
- how users interact with any errors in the process
- how users debug incorrect circuits or poor performance

This session will principally focus on capabilities accessible through Qiskit, though users should feel free to use and bring up any issues that arise from using lower-level access and features of the QSS stack, if they are familiar with them.

We are interested in all parts of your knowledge about how to go about achieving these tasks.
For this reason, the instructions begin fairly light, and we encourage you to try your normal methods to find how you should proceed.
At each step, we have included links to more complete "walkthrough" style content later on in the document to help if (when) you're unable to figure something out using only the published documentation.

For reference, these are links to public documentation for:
- [Terra 0.23.3](https://qiskit.org/documentation/stable/0.42/)
- [the current IBM Provider](https://qiskit.org/ecosystem/ibm-provider/)
- [using dynamic circuits with IBM hardware](https://quantum-computing.ibm.com/services/resources/docs/resources/manage/systems/dynamic-circuits/introduction)

Top-level contents:

- [Setup](#Setup)
- [Tasks](#Tasks)
- [Hints and solutions](#Hints-and-solutions)


## Setup

Most of this session will use only release versions of Qiskit Terra (version 0.23.3) and the IBM Provider (version 0.5.2).
You can install these with

```text
pip install qiskit-terra qiskit-ibm-provider
```

You should feel free to use whatever developer environment you would usually use to interact with Qiskit.
This can be the IDE you typically use, Jupyter Lab (or the older notebook) or a command-line interface.
We are interested in pain points associated with any of these, though will likely be less able to offer immediate technical support for custom IDE setups.


### Advanced users' setup

:bangbang: **This will not work until Terra 0.24.0rc1 is released, scheduled for 2023-04-20.** :bangbang:

If you are familiar enough with the stack to try out use of the new `switch` operation, you will need to use the prerelease version of Qiskit Terra, 0.24.0rc1 (see task 5 below).
You will likely want to do this in a separate virtual environment.
The prerelease of Qiskit Terra can be installed with
```text
pip install --upgrade --pre qiskit-terra
```
Since this is not fully deployed across the IBM stack yet, we have provided a couple of helper functions to bridge the gap.
You can install these by doing
```text
pip install .
```
from the root of this repository (this will also require that the pre-release of Terra is installed).
This will make a module called `helpers` available; this guide will cover details of the functions within it when appropriate.



## Tasks

At all stages throughout these tasks, please feel free to use whatever debugging tools you would usually use (whether external or built into Qiskit).
This includes circuit visualisations and exporting the circuit to other forms.
We are also interested in problems with using any of these tools.

### Task #1: Accessing dynamic-circuits backends

*[Link to hints and solutions.](#Solutions-to-1-Accessing-dynamic-circuits-backends)*

We have a reservation on the machine `ibmq_kolkata` for the duration of this session.
Use the `qiskit-ibm-provider` using the `instance` (hub/group/project) credentials `ibm-q-community/dev-forum-23/main` to access this backend.

Test that the backend works for regular (non-dynamic) circuits by creating a Bell-state creation circuit and measuring both qubits, running it on the device, and retrieving the counts.
One possible Bell circuit looks like this:
```python
from qiskit import QuantumCircuit

bell = QuantumCircuit(2, 2)
bell.h(0)
bell.cx(0, 1)
bell.measure([0, 1], [0, 1])
```

You should be able to print out the counts from the backend run, which ideally should be mostly an even split between `'00'` and `'11`'.

Dynamic circuit capabilities on IBM Hardware utilize a new system software stack, so being able to compare results from the new and legacy stacks can be a useful tool in debugging. Can you run the above against both stacks and compare their outputs?

<!--
What we're interested in:

- mostly this is just a test that people know how to access our hardware _at all_, so we know what stage everyone in the room is at.
-->


### Task #2: Hello, dynamic circuits

*[Link to hints and solutions.](#Solutions-to-2-Hello-dynamic-circuits)*

We will now run our first circuit requiring the new dynamic-circuits capabilities.
We will create a circuit that uses a mid-circuit measurement and feed-forward control to reset a qubit.

<!--
When executing the circuit using `backend.run`, you must pass the keyword argument `dynamic=True`.
-->

1. Create a circuit with one qubit and two clbits
2. Do a Hadamard gate on the qubit, then measure it into clbit 0.
3. If the measurement result is 1, apply an X gate on the qubit.
4. Measure the qubit again, into clbit 1.
5. Execute the circuit on the backend and retrieve the counts.

You should find that the results `00` and `01` happen with equal probability and everything else happens with little-to-no probability.

<!--
What we're interested in:

- debugging: how do users go about this?  Suggest circuit visualisations, OQ3 exporter.
- how do users find the builder interface to use?
-->

Follow up questions:

1. How long did it take to transpile your circuit?
2. Which device qubits were used to execute your circuit? What are their T1/T2 times, gate and readout fidelities?
3. What dit the transpiled circuit look like?
4. Can you generate and print an OpenQASM3 string representing the transpiled circuit?

### Task #3: If-then-else constructs

*[Link to hints and solutions.](#Solutions-to-3-If-then-else constructs)*

Notes to implement:
- some task that logically wants an `else` clause on the `if` statement.
- ideally the logic should want to condition multiple statements, so `c_if` is totally inappropriate

<!--
What we're interested in:

- how well do users find the `else` branch, and how easy/intuitive is it for them?
- do they understand the upgrade path from / reasons not to use `c_if` now (if they knew it before)?
- do users understand the current limitations on conditions in Qiskit / do they have suggestions for how to improve them?
-->


### Task #4: Improving quality of complex circuits

*[Link to hints and solutions.](#Solutions-to-4-Improving-quality-of-complex-circuits)*

Notes to implement:
- circuit should not have a perfect mapping to hardware coupling - routing 100% required
- first make a circuit that's complex and will have poor results
- looking to improve by:
  - choosing better initial qubits (if VF2Post doesn't do this for us)
  - adding dynamical decoupling
- ideally, the classical component could be reduced to a single classical jump iff implemented with a `switch`, to lead into task #5

<!--
What we're interested in:

- do people have any insight into what the transpiler might be doing that's non-optimal (in order to know what they could improve)
- do people know how to access dynamic-circuits enable dynamic decoupling
- do users know how to find issues with 
-->


### Task #5: The `switch` statement

*[Link to hints and solutions.](#Solutions-to-5-The-switch-statement)*

To achieve this task with Qiskit alone, you will need to use [the advanced setup at the top of this document](#Advanced-users-setup). 
In particular, you will need the pre-release of Qiskit Terra 0.24.0 and the helper functions provided by this repository.
If you are familiar with using the direct submission of OpenQASM 3 strings to IBM hardware, you can use these methods too, though we would particularly appreciate feedback on the new `switch` support coming in Qiskit Terra 0.24.0.

Notes to implement:
- a circuit that needs only a single classical lookup, rather than several separate syncs
- possible example: create some `000 + 001 + 010 + 011 + ...` state, then use a `switch` to reverse the bitstring?
- will need to use `helpers.add_switch_support(backend)` helper defined in `lib/helpers.py` because IBM backends won't have support yet.

<!--
What we're interested in:
- how difficult do people find constructing `switch`?
- how do they react on errors?
- how do they debug circuit on error?
-->


### Task #6: Bitwise manipulations

*[Link to hints and solutions.](#Solutions-to-6-Bitwise-manipulations)*

The natural solution to this task goes beyond Qiskit's current capabilities.
You will need to use the direct submission of OpenQASM 3 strings to the IBM backends.
See the first hint in the link above if you need guidance on how to do that.

We will create a long-distance teleportation circuit, which teleports the state of the top qubit to the bottom qubit.
The setup looks like this:

```text
                    ┌───┐ ┌─┐
─|ψ>─────────────■──┤ H ├─┤M├───────────────
     ┌───┐     ┌─┴─┐└───┘ └╥┘┌─┐
─|0>─┤ H ├──■──┤ X ├───────╫─┤M├────────────
     └───┘┌─┴─┐└───┘┌───┐  ║ └╥┘┌─┐
─|0>──────┤ X ├──■──┤ H ├──╫──╫─┤M├─────────
     ┌───┐└───┘┌─┴─┐└───┘  ║  ║ └╥┘┌─┐
─|0>─┤ H ├──■──┤ X ├───────╫──╫──╫─┤M├──────
     └───┘┌─┴─┐└───┘┌───┐  ║  ║  ║ └╥┘┌─┐
─|0>──────┤ X ├──■──┤ H ├──╫──╫──╫──╫─┤M├───
     ┌───┐└───┘┌─┴─┐└───┘  ║  ║  ║  ║ └╥┘┌─┐
─|0>─┤ H ├──■──┤ X ├───────╫──╫──╫──╫──╫─┤M├
     └───┘┌─┴─┐└───┘       ║  ║  ║  ║  ║ └╥┘
─|0>──────┤ X ├────────────╫──╫──╫──╫──╫──╫─
          └───┘            ║  ║  ║  ║  ║  ║
═══════════════════════════╩══╩══╩══╩══╩══╩═
                           0  1  2  3  4  5
```

You can implement the state to be teleported $\lvert\psi\rangle$ however you like.

To teleport the state from the top qubit to the bottom qubit, you should:
- apply an $X$ on the bottom qubit if the odd-numbered measurements have odd parity
- apply a $Z$ on the bottom qubit if the even-numbered measurements have odd parity

Run your result on Kolkata, and verify that you're able to get the results you expect.
We are interested in how you go about implementing the parity measure, any problems you encountered in doing any part fo this, and how you handled any errors that might have arisen.

<!--
What we're interested in:
- how you mix-and-match Qiskit and raw OQ3 strings when dealing with problems beyond Qiskit's current capabilities
- how easy it is to deal with any errors that arise at any point
- how you try to improve output quality in such situations
- any interface design ideas what these features should look like in Qiskit
-->


## Hints and solutions

This section continues some hints and possible solutions for the tasks given above.
We are interested in how you go about solving problems as they arise, and how able you are to troubleshoot using our existing documentation, so please try doing whatever you'd normally do first (and note what problems you encounter!), and then use these as a secondary resort.

### Solutions to #1: Accessing dynamic-circuits backends

*[Link back to task.](#Task-1-Accessing-dynamic-circuits-backends)*

#### Accessing the backend

You must be using the package `qiskit-ibm-provider` and _not_ the now-deprecated `qiskit-ibmq-provider` (note `-ibm-` vs `-ibmq-`).
If you have saved credentials that grant you access to a dynamic-circuits machines other than `ibmq_kolkata`, you may use those instead, but we've got a reservation on this one.

```python
from qiskit_ibm_provider import IBMProvider

instance = "ibm-q-community/dev-forum-23/main"
provider = IBMProvider(instance=instance)
backend = provider.get_backend("ibmq_kolkata")
```

#### Preparing a circuit to run on a backend

One of Qiskit's principal jobs is to compile the quantum components of a circuit to run on a backend.
This includes performing virtual-qubit layout and routing, and translating the quantum gates used into gates that the backend can execute.

This is done using `qiskit.transpile` with the `backend` you just created.
Failing to do this will cause the backend to reject the circuit.

```python
from qiskit import transpile

transpiled = transpile(qc, backend)
```

#### Running a transpiled circuit on a backend

The unified entry point for direct backend access is to use the `.run` method of a backend, passing a circuit transpiled for that backend.
The complete code to run the Bell-circuit example is:
```python
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_provider import IBMProvider

instance = "ibm-q-community/dev-forum-23/main"
provider = IBMProvider(instance=instance)
backend = provider.get_backend("ibmq_kolkata")

bell = QuantumCircuit(2, 2)
bell.h(0)
bell.cx(0, 1)
bell.measure([0, 1], [0, 1])

transpiled = transpile(bell, backend)
job = backend.run(transpiled)
print(f"Job id: {job.job_id()}")
result = job.result()
counts = result.get_counts()

print(counts)
```


### Solutions to #2: Hello dynamic circuits

*[Link back to task.](#Task-2-Hello-dynamic-circuits)*

#### Creation of the circuit

The conditional logic can be done using either the legacy `.c_if` path, or the modern `with qc.if_test` builder interface.
We strongly recommend using the `with qc.if_test` form for everything; `.c_if` is due to be deprecated, can only handle conditioning single instructions (not blocks), and cannot represent an `else` condition.

```python
from qiskit import QuantumCircuit

qc = QuantumCircuit(1, 2)
qc.h(0)
qc.measure(0, 0)
with qc.if_test((0, True)):
    qc.x(0)
qc.measure(0, 1)
```


#### Executing the circuit on hardware

You _must_ remember to pass `dynamic=True` to `backend.run` when trying to execute a dynamic circuit.

```python
transpiled = transpile(qc, backend)

job = backend.run(transpiled, dynamic=True)
print(f"Job id: {job.job_id()}")
result = job.result()
print(result.get_counts())
```

#### Inspecting the transpiled circuit

Details about the layout are stored on the transpiled circuit.
This includes the initial and final mappings of virtual to physical qubits.
These two mappings (and all intermediate states of the circuit) may not be the same, if routing (swap-mapping) was necessary to map the circuit to the target backend's topology.

```python
print(transpiled.layout)
```

The `target` property of backends contains the full information that the Qiskit transpiler uses to reason about the device.
This includes both properties of the qubits themselves:

```python
print(backend.target.qubit_properties[0])
```

and properties of various instructions, organised by opcode (name) and the physical qubits that they are available on.

```python
print(backend.target['sx'][(0,)])
```

You can print out an OpenQASM 3 representation of a circuit using the Qiskit `qiskit.qasm3` module.
The function `dumps` is the simplest entry point, which returns a string.

```python
print(
    qiskit.qasm3.dumps(
        transpiled,
        includes=[],
        disable_constants=True,
        basis_gates=backend.configuration().basis_gates,
    )
)
```


### Solutions to #3: If-then-else constructs

*[Link back to task.](#Task-3-If-then-else constructs)*

For a bit-flip repitition code, with a randomly introduced error:

```python
qr_data = qk.QuantumRegister(3, 'data')
qr_anc = qk.QuantumRegister(2, 'ancilla')

cr_rand = qk.ClassicalRegister(2, 'rand')
cr_anc = qk.ClassicalRegister(2, 'anc')
cr_data = qk.ClassicalRegister(3, 'out')

qc = qk.QuantumCircuit(qr_data, qr_anc, cr_rand, cr_anc, cr_data)

qc.h(qr_anc)
qc.measure(qr_anc, cr_rand)

qc.reset(qr_anc)

qc.barrier()

qc.h(qr_data[0])
qc.cx(qr_data[0], qr_data[1])
qc.cx(qr_data[0], qr_data[2])

# Can replace the above stanza with the below to help
# the transpiler find a good layout, but if enabled,
# gives a backend compilation error.
# qc.h(qr_data[0])
# qc.cx(qr_data[0], qr_anc[0])
# qc.cx(qr_anc[0], qr_data[1])
# qc.cx(qr_data[1], qr_anc[0])
# qc.cx(qr_data[0], qr_anc[1])
# qc.cx(qr_anc[1], qr_data[2])
# qc.cx(qr_data[2], qr_anc[1])

with qc.if_test((cr_rand, 0)):
    qc.x(qr_data[0])
with qc.if_test((cr_rand, 1)):
    qc.x(qr_data[1])
with qc.if_test((cr_rand, 2)):
    qc.x(qr_data[2])
with qc.if_test((cr_rand, 3)):
    qc.id(qr_data)

# Alternative to above. Maybe shorter.
# Had raised an error on qasm3.dumps, but can't reproduce now.
#with qc.if_test((cr_rand, 0)) as else_:
#    qc.x(qr_data[0])
#with else_:
#    with qc.if_test((cr_rand, 1)) as else_:
#        qc.x(qr_data[1])
#    with else_:
#        with qc.if_test((cr_rand, 2)) as else_:
#            qc.x(qr_data[2])
#        with else_:
#            qc.id(qr_data)

qc.cx(qr_data[0], qr_anc[0])
qc.cx(qr_data[1], qr_anc[0])
qc.cx(qr_data[0], qr_anc[1])
qc.cx(qr_data[2], qr_anc[1])

qc.measure(qr_anc, cr_anc)

with qc.if_test((cr_anc, 3)):
    qc.x(qr_data[0])
with qc.if_test((cr_anc, 1)):
    qc.x(qr_data[1])
with qc.if_test((cr_anc, 2)):
    qc.x(qr_data[2])

qc.measure(qr_data, cr_data)
```

```python
from qiskit.result import marginal_counts
marginal_counts(
   job.result(),
   [4,5,6],
   format_marginal=True
).get_counts()
```


### Solutions to #4: Improving quality of complex circuits

*[Link back to task.](#Task-4-Improving-quality-of-complex-circuits)*

```python
# From https://qiskit.org/ecosystem/ibm-provider/stubs/qiskit_ibm_provider.transpiler.passes.scheduling.html#module-qiskit_ibm_provider.transpiler.passes.scheduling
from qiskit.transpiler import PassManager
from qiskit.circuit.library import XGate

from qiskit_ibm_provider.transpiler.passes.scheduling import (
    DynamicCircuitInstructionDurations,
    ALAPScheduleAnalysis,
    PadDynamicalDecoupling,
)

# Use this duration class to get appropriate durations for dynamic
# circuit backend scheduling
durations = DynamicCircuitInstructionDurations.from_backend(nairobi)
# Configure the as-late-as-possible scheduling pass
dd_sequence = [XGate(), XGate()]
pm = PassManager(
    [
        ALAPScheduleAnalysis(durations),
        PadDynamicalDecoupling(durations, dd_sequence),
    ]
)

scheuled = pm.run(transpiled_circuit)
# qss_compiler.compile.QSSCompilationFailure: Failure during compilation
# Warning: OpenQASM 3 parse error
# File: -, Line: 1, Col: 1
# Possible loss of precision in calculating multiple-precision Pi.
# warning: 
# OPENQASM 3;
# ^

```
### Solutions to #5: The `switch` statement

*[Link back to task.](#Task-5-The-switch-statement)*


### Solutions to #6: Bitwise manipulations

*[Link back to task.](#Task-6-Bitwise-manipulations)*

#### Running a raw OpenQASM 3 string on a dynamic-circuits backend

In principle, you just pass a valid OpenQASM 3 program in a string to `backend.run`, such as:
```python
my_program = """
    OPENQASM 3.0;
    include "stdgates.inc";
    bit[2] out;
    sx $0;
    cx $0, $1;
    out[0] = measure $0;
    out[1] = measure $1;
"""

job = backend.run(my_program, dynamic=True)
```

You have to follow several rules about the OpenQASM 3 program you can output, though:

- you cannot use virtual qubits; all references must be physical qubits (`$0`, `$1`, etc)
- you can only use the basis gates of the machine (no calling `h`, for example)
- you must obey the coupling constraints of the hardware

Part of Qiskit's job in the stack is to resolve all these rules, but bitwise manipulations can't yet be represented in Qiskit.


#### Displaying backend-suitable OpenQASM 3 code for a Qiskit circuit

You might have begun this task by building up part of the circuit in Qiskit, then wanting to modify Qiskit's OpenQASM 3 code to do the rest manually.
The defaults of `qiskit.qasm3.dumps` will not necessarily generate a suitable circuit; you likely will want to pass `disable_constants=True` as well.

The OpenQASM 3 exporter will output physical qubits iff the circuit has been transpiled to a particular layout (the circuit has a non-`None` `.layout` attribute).
The minimal command to fix a particular layout is `transpile(qc, initial_layout=[...])`, where the `initial_layout` is a list of integers mapping virtual to physical qubits.
For example, `initial_layout=[1, 2, 0]` will place the 0th virtual qubit on physical qubit `$1`, the 1st virtual on `$2`, and the 2nd virtual on `$0`.

To convert the basis gates as well, you would need to pass the backend to the `transpile` call as well.
You can still include `initial_layout`.

Putting it all together:
```python
# Note, this isn't the teleportation circuit.
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)

transpiled = transpile(qc, backend, initial_layout=[1, 2, 0])
print(qasm3.dumps(transpiled, disable_constants=True))
```

```qasm3
OPENQASM 3;
include "stdgates.inc";
rz(1.5707963267949) $1;
sx $1;
rz(1.5707963267949) $1;
cx $1, $2;
cx $1, $0;
```


#### Creation of the teleporter

You can set the initial state to anything you like.
Just as an example, we will initialize the top qubit in a state $\sqrt{\frac14}\lvert0\rangle + \sqrt{\frac34}\lvert1\rangle$.
I used `initial_layout=[0, 1, 2, 3, 5, 8, 9]` just because these qubits form a topological line on Kolkata.
You may want to investigate which line of qubits have the best error rates and use those instead.
(You can also just let `transpile` pick for you, or choose qubits that _aren't_ in a line and let the transpiler handle the swap-mapping problem on your behalf.)

```python
import numpy as np
from qiskit import QuantumCircuit, transpile, qasm3

n_bits = 7
qc = QuantumCircuit(n_bits, n_bits)
qc.initialize(np.sqrt([0.25, 0.75]), 0)
for i in range(1, n_bits, 2):
    # First layer
    qc.h(i)
    qc.cx(i, i + 1)

    # Second layer
    qc.cx(i - 1, i)
    qc.h(i - 1)

qc.measure(range(n_bits - 1), range(n_bits - 1))

transpiled = transpile(qc, backend, initial_layout=[0, 1, 2, 3, 5, 8, 9])
print(qasm3.dumps(transpiled, disable_constants=True))
```

```qasm3
OPENQASM 3;
include "stdgates.inc";
bit[7] c;
rz(-3.141592653589793) $0;
sx $0;
rz(1.0471975511965983) $0;
sx $0;
rz(1.5707963267949) $1;
sx $1;
rz(1.5707963267949) $1;
cx $1, $2;
cx $0, $1;
rz(1.5707963267949) $0;
sx $0;
rz(1.5707963267949) $0;
rz(1.5707963267949) $3;
sx $3;
rz(1.5707963267949) $3;
cx $3, $5;
cx $2, $3;
rz(1.5707963267949) $2;
sx $2;
rz(1.5707963267949) $2;
rz(1.5707963267949) $8;
sx $8;
rz(1.5707963267949) $8;
cx $8, $9;
cx $5, $8;
rz(1.5707963267949) $5;
sx $5;
rz(1.5707963267949) $5;
c[0] = measure $0;
c[1] = measure $1;
c[2] = measure $2;
c[3] = measure $3;
c[4] = measure $5;
c[5] = measure $8;
```

This circuit is just the base; it makes the circuit as drawn in the task, although I doctored the drawing slightly, so if you use `QuantumCircuit.draw()`, yours probably won't look _exactly_ identical.


#### Teleportation via parity-checked feed-forward

The following OpenQASM 3 can be appended to the output in the previous hint to make one possible implementation of the feed-forward teleporter.

```qasm3
if (c[1] ^ c[3] ^ c[5]) {
    x $9;
}
if (c[0] ^ c[2] ^ c[4]) {
    rz(3.14159265358979) $9;
}
```

You also probably want to add a `c[6] = measure $9;` line at the end to measure the state of your output.
Note that the physical qubit might be different if you didn't use the same `initial_layout` as my example.

It's also possible that the quality of the results might be improved if you do a bit more bit-twiddling to reduce the branch point to a single classical branching point using a `switch` statement.
Logically this is something like
```qasm3
int[32] discriminator = (int[32](c[1] ^ c[3] ^ c[5]) << 1) + int[32](c[0] ^ c[2] ^ c[4]);
switch (discriminator) {
    case 1: {
        rz(3.14159265358979) $9;
    }
    break;
    case 2: {
        x $9;
    }
    break;
    case 3: {
        x $9;
        rz(3.14159265358979) $9;
    }
    break;
    default: {
    }
    break;
}
```


#### Teleportation via hardcoded switch

It's technically possible to do the same feed-forward with a Qiskit-generated `switch` statement as well, even without bit-twiddling.
(In reality, you'd almost certainly want to do the parity checks to reduce the size of the table.)
First we need to generate a large lookup table:

```python
def parity_checks(distance):
    """For a teleportation distance (the number of 'cx' per layer), get all the possible measured
    values that require both `x` and `z`, just `x`, and just `z`."""
    parity = lambda x: f"{x:b}".count("1") % 2  # or `int.bit_count`, if you're using Python 3.11+

    x_mask = 0
    z_mask = 0
    for _ in range(distance):
        x_mask <<= 2
        x_mask |= 0b01
        z_mask <<= 2
        z_mask |= 0b10
    both = []
    xs = []
    zs = []
    for i in range(1 << (2 * distance)):
        bits = f"{i:b}"[::-1]
        if parity(i & x_mask) and parity(i & z_mask):
            both.append(i)
        elif parity(i & x_mask):
            xs.append(i)
        elif parity(i & z_mask):
            zs.append(i)
    return both, xs, zs
```

Now we use the lookup table in a single switch statement:

```python
import numpy as np
from qiskit import QuantumCircuit, transpile, qasm3, QuantumRegister, ClassicalRegister

n_bits = 7
qubits = QuantumRegister(n_bits)
midmeasures = ClassicalRegister(n_bits - 1)
outmeasure = ClassicalRegister(1)

qc = QuantumCircuit(qubits, midmeasures, outmeasure)
qc.initialize(np.sqrt([0.25, 0.75]), 0)
for i in range(1, n_bits, 2):
    # First layer
    qc.h(i)
    qc.cx(i, i + 1)

    # Second layer
    qc.cx(i - 1, i)
    qc.h(i - 1)

qc.measure(qubits[:-1], midmeasures)

both, xs, zs = parity_checks((n_bits - 1) // 2)
with qc.switch(midmeasures) as case:
    with case(*both):
        qc.x(n_bits - 1)
        qc.z(n_bits - 1)
    with case(*xs):
        qc.x(n_bits - 1)
    with case(*zs):
        qc.z(n_bits - 1)
    with case(case.DEFAULT):
        pass

transpiled = transpile(qc, backend, initial_layout=[0, 1, 2, 3, 5, 8, 9])
print(
    qasm3.dumps(
        transpiled, disable_constants=True, experimental=qasm3.ExperimentalFeatures.SWITCH_CASE_V1
    )
)
```

This gives

```qasm3
OPENQASM 3;
include "stdgates.inc";
bit[6] c0;
bit[1] c1;
int switch_dummy;
rz(-3.141592653589793) $0;
sx $0;
rz(1.0471975511965983) $0;
sx $0;
rz(1.5707963267949) $1;
sx $1;
rz(1.5707963267949) $1;
cx $1, $2;
cx $0, $1;
rz(1.5707963267949) $0;
sx $0;
rz(1.5707963267949) $0;
rz(1.5707963267949) $3;
sx $3;
rz(1.5707963267949) $3;
cx $3, $5;
cx $2, $3;
rz(1.5707963267949) $2;
sx $2;
rz(1.5707963267949) $2;
rz(1.5707963267949) $8;
sx $8;
rz(1.5707963267949) $8;
cx $8, $9;
cx $5, $8;
rz(1.5707963267949) $5;
sx $5;
rz(1.5707963267949) $5;
c0[0] = measure $0;
c0[1] = measure $1;
c0[2] = measure $2;
c0[3] = measure $3;
c0[4] = measure $5;
c0[5] = measure $8;
switch_dummy = c0;
switch (switch_dummy) {
  case 3:
  case 6:
  case 9:
  case 12:
  case 18:
  case 23:
  case 24:
  case 29:
  case 33:
  case 36:
  case 43:
  case 46:
  case 48:
  case 53:
  case 58:
  case 63: {
    x $9;
    rz(3.14159265358979) $9;
  }
  break;
  case 1:
  case 4:
  case 11:
  case 14:
  case 16:
  case 21:
  case 26:
  case 31:
  case 35:
  case 38:
  case 41:
  case 44:
  case 50:
  case 55:
  case 56:
  case 61: {
    x $9;
  }
  break;
  case 2:
  case 7:
  case 8:
  case 13:
  case 19:
  case 22:
  case 25:
  case 28:
  case 32:
  case 37:
  case 42:
  case 47:
  case 49:
  case 52:
  case 59:
  case 62: {
    rz(-3.141592653589793) $9;
  }
  break;
  default: {
  }
  break;
}
```
