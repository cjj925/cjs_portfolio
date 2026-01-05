Quantum Entanglement Simulation (Qiskit)

This program simulates a basic quantum circuit using Qiskit that creates and measure entanglement between two qubits. The circuit is simulated using Qiskit Aer.

This project illustrates fundamental quantum computing concepts such as superposition, entanglement, and quantum measurement in a super short 15 lines of code.

What this proram does

* Creates a quantum circuit with 2 qubits and 2 classical bits
* Applies Hadamard gate to place first qubit into superposition
* Applies Controlled-NOT gate to entanlge the two qubits
* Measures both qubits
* Runs circuit 1,000 times on the Aer simulator
* Displays measurement results as counts

Requirements

* Python 3.9+
* Qiskit
* Qiskit Aer

Install dependencies with: pip install qiskit qiskit-aer

Credit

Built using Qiskit, IBM's open-source quantum computing framework
