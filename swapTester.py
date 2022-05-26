from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.tools.monitor import job_monitor
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QMessageBox

class SwapTester:
    def __init__(self, first_hash, second_hash):
        self.backend = Aer.get_backend('qasm_simulator')
        self.generate_circut(first_hash, second_hash)

    def generate_circut(self, first_hash, second_hash):
        qa = QuantumRegister(first_hash.qubits_num, 'qa')
        qb = QuantumRegister(second_hash.qubits_num, 'qb')
        q = QuantumRegister(1, 'q')
        c = ClassicalRegister(1, 'c')

        sub_circuit1 = first_hash.circuit.to_instruction(label='Hash 1')
        sub_circuit2 = second_hash.circuit.to_instruction(label='Hash 2')
        self.circuit = QuantumCircuit(qa, qb, q, c)

        self.circuit.append(sub_circuit1, [x for x in qa])
        self.circuit.append(sub_circuit2, [x for x in qb])

        first_result_qubit_index = first_hash.control_qubits_num
        second_result_qubit_index = 2 * first_hash.control_qubits_num + 1

        self.generate_swap_test_circuit(2 * (first_hash.control_qubits_num + 1), first_result_qubit_index, second_result_qubit_index)

    def generate_swap_test_circuit(self, test_qubit_index, first_result_qubit, second_result_qubit):
        self.circuit.h([test_qubit_index])
        for i in range(0, first_result_qubit + 1):
            self.circuit.cswap(test_qubit_index, i, second_result_qubit - first_result_qubit + i)
        self.circuit.h([test_qubit_index])
        self.circuit.measure([test_qubit_index], [0])

    def run_test(self, window, nShots = 1000):
        job = execute(self.circuit, self.backend, shots=nShots)

        job_monitor(job)

        result = job.result().get_counts()

        if '1' in result:
            areEqual = False;
        else:
            areEqual = True;

        ones = 0
        zeros = 0
        if '1' in result:
            ones = result['1']
        if '0' in result:
            zeros = result['0']

        QMessageBox.about(window, "Wynik swap testu", f"Czy sa rowne: {areEqual}\n Liczba testow: {nShots} \n 1 -> {ones} \n 0 -> {zeros}")

    def show_circuit(self):
        self.circuit.draw(output='mpl')
        plt.show()

