# Dynamic Circuits Track

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
- [Terra 0.23.3](https://qiskit.org/documentation/stable/0.42/).
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

We have a reservation on the machine `ibm_TODO` for the duration of this session.
Use the `qiskit-ibm-provider` using the `instance` (hub/group/project) credentials `"hub_TODO/group_TODO/project_TODO"` to access this backend.

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

<!--
What we're interested in:

- mostly this is just a test that people know how to access our hardware _at all_, so we know what stage everyone in the room is at.
-->


### Task #2: Hello, dynamic circuits

*[Link to hints and solutions.](#Solutions-to-2-Hello-dynamic-circuits)*

We will now run our first circuit requiring the new dynamic-circuits capabilities.
We will create a circuit that uses a mid-circuit measurement and feed-forward control to reset a qubit.

When executing the circuit using `backend.run`, you must pass the keyword argument `dynamic=True`.

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

What we want to know:
- do people have any insight into what the transpiler might be doing that's non-optimal (in order to know what they could improve)
- do people know how to access dynamic-circuits enable dynamic decoupling
- do users know how to find issues with 


### Task #5: The `switch` statement

*[Link to hints and solutions.](#Solutions-to-5-The-switch-statement)*

To achieve this task with Qiskit alone, you will need to use [the advanced setup at the top of this document](#Advanced-users-setup). 
In particular, you will need the pre-release of Qiskit Terra 0.24.0 and the helper functions provided by this repository.
If you are familiar with using the direct submission of OpenQASM 3 strings to IBM hardware, you can use these methods too, though we would particularly appreciate feedback on the new `switch` support coming in Qiskit Terra 0.24.0.

Notes to implement:
- a circuit that needs only a single classical lookup, rather than several separate syncs
- possible example: create some `000 + 001 + 010 + 011 + ...` state, then use a `switch` to reverse the bitstring?
- will need to use `helpers.add_switch_support(backend)` helper defined in `lib/helpers.py` because IBM backends won't have support yet.

What we want to know:
- how difficult do people find constructing `switch`?
- how do they react on errors?
- how do they debug circuit on error?


### Task #6: Bitwise manipulations

*[Link to hints and solutions.](#Solutions-to-6-Bitwise-manipulations)*

This task goes beyond Qiskit's current capabilities.
You will need to use the direct submission of OpenQASM 3 strings to the IBM backends.

Notes to implement:
- brief introduction on how to submit raw strings
- some task that logically wants to manipulate the bits in a runtime condition for some more complex logic (e.g. `a && b` conditions)

What we're interested in:
- how people mix-and-match Qiskit and raw OQ3 strings when dealing with problems beyond Qiskit's current capabilities
- how people might try and use techniques to improve output quality in such situations
- interface design ideas from people about how we could implement this in Qiskit



## Hints and solutions

This section continues some hints and possible solutions for the tasks given above.
We are interested in how you go about solving problems as they arise, and how able you are to troubleshoot using our existing documentation, so please try doing whatever you'd normally do first (and note what problems you encounter!), and then use these as a secondary resort.

### Solutions to #1: Accessing dynamic-circuits backends

*[Link back to task.](#Task-1-Accessing-dynamic-circuits-backends)*

#### Accessing the backend

You must be using the package `qiskit-ibm-provider` and _not_ the now-deprecated `qiskit-ibmq-provider` (note `-ibm-` vs `-ibmq-`).
If you have saved credentials that grant you access to a dynamic-circuits machines other than `ibm_TODO`, you may use those instead, but we've got a reservation on this one.

```python
from qiskit_ibm_provider import IBMProvider

instance = "hub_TODO/group_TODO/project_TODO"
provider = IBMProvider(instance=instance)
backend = provider.get_backend("ibm_TODO")
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

instance = "hub_TODO/group_TODO/project_TODO"
provider = IBMProvider(instance=instance)
backend = provider.get_backend("ibm_TODO")

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


### Solutions to #3: If-then-else constructs

*[Link back to task.](#Task-3-If-then-else constructs)*


### Solutions to #4: Improving quality of complex circuits

*[Link back to task.](#Task-4-Improving-quality-of-complex-circuits)*


### Solutions to #5: The `switch` statement

*[Link back to task.](#Task-5-The-switch-statement)*


### Solutions to #6: Bitwise manipulations

*[Link back to task.](#Task-6-Bitwise-manipulations)*
