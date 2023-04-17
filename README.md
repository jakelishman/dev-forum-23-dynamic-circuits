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


## Setup

Most of this session will use only release versions of Qiskit Terra (version 0.23.3), Qiskit Aer (version 0.12.0) and the IBM Provider (version 0.5.2).
You can install these with

```text
pip install qiskit-terra qiskit-aer qiskit-ibm-provider
```

You should feel free to use whatever developer environment you would usually use to interact with Qiskit.
This can be the IDE you typically use, Jupyter Lab (or the older notebook) or a command-line interface.
We are interested in pain points associated with any of these, though will likely be less able to offer immediate technical support for custom IDE setups.


### Advanced users' setup

** :bangbang: This will not work until Terra 0.24.0rc1 is released, scheduled on 2023-04-20 :bangbang: **

If you are familiar enough with the stack to try out use of the new `switch` operation, you will need to use the prerelease version of Qiskit Terra, 0.24.0rc1.
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

### #1: Accessing dynamic-circuits backends

*[Link to hints and solutions.](#Solutions-to-Accessing-dynamic-circuits-backends)*

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


### #2: Hello, dynamic circuits

*[Link to hints and solutions.](#Solutions-to-Hello-dynamic-circuits)*




## Hints and solutions

This section continues some hints and possible solutions for the tasks given above.
We are interested in how you go about solving problems as they arise, and how able you are to troubleshoot using our existing documentation, so please try doing whatever you'd normally do first (and note what problems you encounter!), and then use these as a secondary resort.

### Solutions to Accessing dynamic-circuits backends

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
result = job.result()
counts = result.get_counts()

print(counts)
```


### Solutions to Hello dynamic circuits
