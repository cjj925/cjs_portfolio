from qiskit import QuantumCircuit # Qiskit to create quantum circuit
from qiskit_aer import AerSimulator # Qiskit AerSimulator to simulate quantum circuits on a classical computer

qc = QuantumCircuit(2, 2) # Quantum circuit with 2 qubits and 2 classical bits

qc.h(0) # Hadamard gate to qubit 0 which puts it into superposition
qc.cx(0, 1) # Controlled-NOT gate to qubit 0 and target qubit 1, this entangles qubit 0 and 1

qc.measure([0, 1], [0, 1]) # Measure qubits and stores results in classical bits

sim = AerSimulator() # AerSimulator to run the quantum circuit
result = sim.run(qc, shots=1000).result() # Run the circuit 1,000 times and store results
counts = result.get_counts() # Get results and list each one

print(counts) # Print results

