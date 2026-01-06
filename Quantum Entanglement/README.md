# Quantum Entanglement Simulation (Qiskit)

This program simulates a basic quantum circuit using Qiskit that creates and measures entanglement between two qubits. The circuit is simulated using Qiskit Aer.

This project illustrates fundamental quantum computing concepts such as superposition, entanglement, noise modeling, and quantum measurement in a short and simple way.

## What this program does
* Creates a quantum circuit with 2 qubits and 2 classical bits
* Applies Hadamard gate to place first qubit into superposition
* Applies Controlled-NOT gate to entanlge the two qubits
* Measures both qubits
* Applies noise to simulate real quantum hardware behavior
* Runs circuit 1,000 times on the Aer simulator
* Displays measurement results as counts in a ordered fashion

## Requirements
* Python 3.9+
* Qiskit
* Qiskit Aer

## Install dependencies with: pip install qiskit qiskit-aer

## Notes
* This program runs entirely on a classical computer
* Zero real quantum hardware is used
* Noise modeling is simulated

## Credit
Built using Qiskit, IBM's open-source quantum computing framework
