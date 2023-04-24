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

Dynamic circuit capabilities on IBM Hardware utilize a new system software stack, so being able to compare results from the new and legacy stacks can be a useful tool in debugging. Run the circuit above against both stacks and compare the relative device performance.

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
3. Add a runtime check that, if the measurement result is 1, will apply an X gate on the qubit.
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
2. Which device qubits were used to execute your circuit?
   What are their T1/T2 times, gate and readout fidelities?
3. What did the transpiled circuit look like?
4. Can you generate and print an OpenQASM 3 string representing the transpiled circuit?


### Task #3: If-then-else constructs

*[Link to hints and solutions.](#Solutions-to-3-If-then-else-constructs)*

In this task, we will create an approximation of a repeat-until-success circuit that returns how many iterations it took to create the desired state.
For simplicity we will repeatedly create and measure a two-qubit state until we get the result `0b11`, at which point we will record the iteration number.

(Note: IBM backends don't yet fully support `for` or `while` loops, so you should hard-code your iterations into the circuit using `if` statements.)

1. Create a circuit with two data qubits, two mid-circuit measurement clbits, and two clbits to record iteration count.
2. Create a state $\sqrt p\lvert00\rangle + \sqrt{1 - p}\lvert11\rangle$ for some probability $p$.
   Measure both qubits into the mid-circuit measurement clbits.
3. If the result is `11`, store the iteration count into the data clbits.
   If it isn't, reset your qubits and repeat steps 2 and 3 up to two more times.

Record your results over several shots.
Does the distribution of your iteration counts agree with the statistics you expect from the value of $p$ you chose, and the error rates of the qubits, gates and measurements you used?

<!--
What we're interested in:

- how well do users find the `else` branch, and how easy/intuitive is it for them?
- do they understand the upgrade path from / reasons not to use `c_if` now (if they knew it before)?
- do users understand the current limitations on conditions in Qiskit / do they have suggestions for how to improve them?
-->


### Task #4: Improving quality of complex circuits

*[Link to hints and solutions.](#Solutions-to-4-Improving-quality-of-complex-circuits)*

You don't necessarily have to do this task in the order we have put it.

This is quite a free-form task.
We are interested in how you go about improving results you've got from dynamic circuits pathways.

Take either a previous circuit, or one from your own work, that did not give high quality results.
If you don't have one, two possible examples to explore:

- Create two separate Bell pairs. Randomly choose one of them, and apply some randomised benchmarking sequence on it, leaving the other untouched.  Measure both Bell pairs separately afterwards.  How does the fidelity of the untouched one hold up?
- Create a circuit that may do one of 8 things, based on a random number generated by the circuit.  Does the fidelity scale with the number of qubits?

What can you do to improve the quality of the results that you saw?

<!--
What we're interested in:

- do people have any insight into what the transpiler might be doing that's non-optimal (in order to know what they could improve)?
- do people know how to access dynamic-circuits enable dynamic decoupling?
- do users know how to find issues with their results?
-->


### Task #5: The `switch` statement

*[Link to hints and solutions.](#Solutions-to-5-The-switch-statement)*

To achieve this task with Qiskit alone, you will need to use [the advanced setup at the top of this document](#Advanced-users-setup). 
In particular, you will need the pre-release of Qiskit Terra 0.24.0 and the helper functions provided by this repository.
If you are familiar with using the direct submission of OpenQASM 3 strings to IBM hardware, you can use these methods too, though we would particularly appreciate feedback on the new `switch` support coming in Qiskit Terra 0.24.0.

A preliminary: once you have got your advanced setup installed, you need to use the helper library to upgrade your backend.
This is just temporary; it will not be necessary once the roll-out of Terra 0.24.0 across the IBM stack is complete.
To upgrade a backend you have already retrieved from `qiskit_ibm_provider`, you should do:
```python
import helpers

backend = helpers.add_switch_support(backend)
```
You can then use `backend` like you did before, both with Qiskit's `transpile` and passing the result of that to `backend.run`.
If you want to do more advanced debugging, you may want to examine the code of the `add_switch_support` function to see how this hack is achieved.

This task is to simulate random noise on a bit-flip code, and then measure and correct a syndrome.
This should all be done in the same circuit.

1. Create a circuit with 3 data qubits and corresponding clbits, 2 ancillary qubits and clbits, and a third 2-clbit register to store the randomness.
2. Use the ancillary qubits to generate two random bits of classical data in the "random" register.
   Reset the qubits after.
3. Create a GHZ state on the data qubits.
   See the first hint for just the physics, if needed.
4. Using the result of the randomness $n$, apply a bit-flip to data qubit $n$.
   Do nothing if the result is out of range.
   Pretend we don't know which qubit was flipped.
5. Use the ancillary qubits to determine which qubit was flipped, and reverse the flip.
   See the second hint for just the physics, or the later "step 5" hint for the solution.
6. Measure all the data qubits.
   Run the circuit on Kolkata, and reduce your results down so that you _only_ see the measurement from the data qubits.

You should try and use the `switch` statement in Qiskit for the quantum parts of this.
Unfortunately, the documentation for Terra 0.24.0rc1 isn't deployed publicly, but you can use the Python built-in `help` function to look at `QuantumCircuit.switch` for some guidance.
The solutions for this section contain full worked examples, but we're interested in how you get on without using them, if possible.


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

*[Link back to task.](#Task-3-If-then-else-constructs)*

#### Creating if statements in Qiskit

`QuantumCircuit` has two `if`-related methods: `if_test` and `if_else`.
Of these, `if_test` can be used in two distinct calling conventions: a low-level manual construction form (`if_else` only has this), and a "builder" form which can also produce `else` blocks.
As a user, you will almost always want to use the builder form.
To do that, use `QuantumCircuit.if_test(condition)` as a Python context manager:

```python
qr = QuantumRegister(2)
cr = ClassicalRegister(2, "test")
qc = QuantumCircuit(qr, cr)

with qc.if_test((cr, 0)):
    # These are only executed if `cr == 0` at runtime.
    qc.h(0)
    qc.cx(0, 1)
```

The condition is a 2-tuple whose first element is a `ClassicalRegister` or `Clbit`, and whose second element is an integer.
The condition represents an equality condition only.
This is the same form as the old `c_if`.

You can add an `else` block like this:
```python
with qc.if_test((cr, 0)) as else_:
    # Only if `cr` is 0
    qc.h(0)
    qc.cx(0, 1)
with else_:
    # If `cr` is anything else.
    qc.h(1)
    qc.cx(1, 0)
```

These can be nested, but beware when nesting `else` statements; the `else_` object here is just a Python name, and so you might accidentally overwrite it if you use the same name in a nested scope.
You can call each `else_` variable anything.


#### How to record iteration count

Qiskit currently doesn't have a way to directly assign a classical value to bits that should be returned from the circuit.
You could record the iteration count by hardcoding the relevant `x` flips on the data qubits, then measuring the result into the iteration clbit store.


#### I'm not getting my iteration count back!

If all the measurements into a clbit are conditional, you might not see this clbit in the returned values from the IBM backends (but come to the "Rethinking dynamic circuits IO" working session to learn more!).
If this is the case, you might need to conditionally prepare two special "iteration counter" qubits, and unconditionally measure them at the end.


#### Example implementation

There are lots of ways of doing this, some of which have pitfalls in the current IBM stack, which we're also interested in seeing you debug.
This is one possible example, using a nested `if/else` structure:

```python
from math import pi
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

qr = QuantumRegister(2)
iteration = QuantumRegister(2, "iteration")
cr = ClassicalRegister(2)

qc = QuantumCircuit(qr, cr, iteration)

# Prepare state.
qc.rx(3 * pi / 13, 0)
qc.cx(0, 1)
qc.measure(qr, cr)

with qc.if_test((cr, 3)) as else_:
    # Set up iteration counter to 1.
    qc.x(iteration[0])
    # Success!
with else_:
    # Iteration 2
    qc.reset(qr)
    qc.rx(3 * pi / 13, 0)
    qc.cx(0, 1)
    qc.measure(qr, cr)
    with qc.if_test((cr, 3)) as else_:
        qc.x(iteration[1])
    with else_:
        # Iteration 3
        qc.reset(qr)
        qc.rx(3 * pi / 13, 0)
        qc.cx(0, 1)
        qc.measure(qr, cr)
        with qc.if_test((cr, 3)) as else_:
            qc.x(iteration[0])
            qc.x(iteration[1])

qc.measure(iteration, cr)
```

### Solutions to #4: Improving quality of complex circuits

*[Link back to task.](#Task-4-Improving-quality-of-complex-circuits)*

This is one area where we're particularly interested in seeing what people try, and what people have done.
There aren't many hints here; we're mostly after feedback.

One possibility is to use dynamic decoupling.
If so, you need to use the custom dynamic decoupling routines in `qiskit_ibm_provider`, since they can apply the scheduling rules that the IBM backends require; not all this information can currently be fed to Terra via the `Target` object, and we anticipate the scheduling problem becoming much more of a backend concern as more classical processing is done.
This is one way of applying scheduling:

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

scheduled = pm.run(transpiled_circuit)
```


### Solutions to #5: The `switch` statement

*[Link back to task.](#Task-5-The-switch-statement)*

#### Creating a GHZ state

A GHZ state has the form $\bigl(\lvert00\cdots0\rangle + \lvert11\cdots1\rangle\rangle\bigr)/2$.
You can make one by applying a Hadamard on one qubit, then using that as the control of a `cx` on each other qubit.


#### Using ancillas to reverse a bitflip on a GHZ state

Assume a starting state $\lvert000\rangle + \lvert111\rangle$, and two ancillary qubits initially in $\lvert00\rangle$.
If we do
```qasm3
qubit[3] data;
qubit[2] ancilla;
bit[2] syndrome;

cx data[0], ancilla[0];
cx data[1], ancilla[0];

cx data[0], ancilla[1];
cx data[2], ancilla[1];

syndrome = measure ancilla;
```
we can determine which of the data qubits was flipped, without disturbing the state.
If either pair acting on the same ancilla are in an equal state, the ancilla will remain $\lvert0\rangle$.
If both ancillas are $\lvert1\rangle$, it must be the shared qubit that is flipped.
If only one ancilla is $\lvert1\rangle$, it must be the qubit unique to that ancilla that is flipped.

Notably, this doesn't disturb the GHZ state; we didn't get any information on which $Z$ state any individual qubit is in, just a parity check.
You can extend this idea to other input states and larger states.


#### Construction of the circuit (steps 1 to 3)

```python
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

# Step 1: set up registers.
data = QuantumRegister(3, "data")
anc = QuantumRegister(2, "anc")
rand = ClassicalRegister(2, "rand")
syndrome = ClassicalRegister(2, "syndrome")
out = ClassicalRegister(3, "out")
qc = QuantumCircuit(data, anc, rand, syndrome, out)


# Step 2: Hadamard each ancilla and measure to get a random bit.
qc.h(anc)
qc.measure(anc, rand)
qc.reset(anc)
qc.barrier()


# Step 3: prepare the GHZ state.
qc.h(data[0])
qc.cx(data[0], data[1])
qc.cx(data[0], data[2])
qc.barrier()
```

#### Apply a bit-flip using the randomness (step 4)

This _can_ be done with a sequence of `if` statements, or a bunch of chained `else if` statements, but that's inefficient in the control hardware.
Instead, use a `switch` statement.

First hint: the QSS stack requires a "default" case.
You will still need to create one in Qiskit; you can make a no-op with the Python statement `pass` (or use an explicit `id` gate, if you like).

Using the new `switch` builder interface in Qiskit, this looks like (following on from the previous hint):

```python
with qc.switch(rand) as case:
    with case(0):
        qc.x(data[0])
    with case(1):
        qc.x(data[1])
    with case(2):
        qc.x(data[2])
    with case(case.DEFAULT):
        pass
```

#### Use the ancillary qubits to flip back (step 5)

For the intuition behind this, see the second hint in this section.

```python
qc.cx(data[0], anc[0])
qc.cx(data[1], anc[0])
qc.cx(data[0], anc[1])
qc.cx(data[2], anc[1])

qc.measure(anc, syndrome)

with qc.switch(syndrome) as case:
    with case(3):
        qc.x(data[0])
    with case(1):
        qc.x(data[1])
    with case(2):
        qc.x(data[2])
    with case(case.DEFAULT):
        pass

qc.measure(data, out)
```

#### Reducing the results down (step 6)

Let's say we've transpiled our circuit, submitted the job and got the `job.result()` result back in `result`.
Qiskit has built-in capabilities to marginalise results down to only some bits of interest.
You need to know the indices of the clbits you're interested in.
In this case, they're the last three bits in the circuit, so `[4, 5, 6]`.

```python
from qiskit.result import marginal_counts

marginal_counts(result, [4, 5, 6], format_marginal=True).get_counts()
```


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
You can still include `initial_layout`, but the transpiler will pick for you if you don't.

Putting it together:
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


#### Teleportation via Qiskit `switch` (not a good idea!)

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
