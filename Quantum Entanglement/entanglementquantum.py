from qiskit import QuantumCircuit # Qiskit to create quantum circuit
from qiskit_aer import AerSimulator # Qiskit AerSimulator to simulate quantum circuits on a classical computer
from qiskit_aer.noise import NoiseModel, pauli_error # Qiskit noise modeling

qc = QuantumCircuit(2, 2) # Quantum circuit with 2 qubits and 2 classical bits

qc.h(0) # Hadamard gate to qubit 0 which puts it into superposition
qc.cx(0, 1) # Controlled-NOT gate to qubit 0 and target qubit 1, this entangles qubit 0 and 1
qc.measure([0, 1], [0, 1]) # Measure qubits and stores results in classical bits

sim = AerSimulator() # AerSimulator to run the quantum circuit

noise_model = NoiseModel() # Noise model
bit_flip = pauli_error([('X', 0.05), ('I', 0.95)]) # 'X' flips the bit with a 5% chance, 'I' leaves bit unchanged with a 95% chance
noise_model.add_all_qubit_quantum_error(bit_flip, "measure") # Apply bit_flip to all qubits

result = sim.run(qc, shots=1000, noise_model=noise_model).result() # Run the circuit 1,000 times and store results
counts = result.get_counts() # Get results and list each one

ordered_states = ['11', '00', '10', '01'] # Desired printed order

ordered_counts = { # Dictionary Comprehension
    state: counts.get(state, 0)
    for state in ordered_states
}

print(ordered_counts) # Print ordered results

