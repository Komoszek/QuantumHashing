from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.tools.monitor import job_monitor
import matplotlib.pyplot as plt
import math
from qiskit.circuit.library import RYGate
from PyQt6.QtWidgets import QMessageBox

class SwapTester:
    def __init__(self, first_message, second_message, control_qubits_count, k):
        self.backend = Aer.get_backend('qasm_simulator')
        self.k = k
        self.generate_circut(first_message, second_message,control_qubits_count);

    def generate_circut(self, first_message, second_message, control_qubits_count):
        quantumRegiter = QuantumRegister(2 * (control_qubits_count + 1) + 1, 'q')
        classicalRegister = ClassicalRegister(1, 'c')
        self.circuit = QuantumCircuit(quantumRegiter, classicalRegister)

        self.generate_message_circuit(0, control_qubits_count, first_message)
        self.generate_message_circuit(control_qubits_count + 1, control_qubits_count, second_message)

        first_result_qubit_index = control_qubits_count
        second_result_qubit_index = 2 * control_qubits_count + 1

        self.generate_swap_test_circuit(2 * (control_qubits_count + 1), first_result_qubit_index, second_result_qubit_index)

        self._measure_circuit = self.circuit.measure_all(inplace=False)

    def generate_message_circuit(self, first_qubit_index, control_qubits_count, message):
        last_qubit_index = first_qubit_index + control_qubits_count
        self.circuit.h(range(first_qubit_index, last_qubit_index))
        N = 2 ** len(message)
        K = 2 ** control_qubits_count
        bit = 1

        for i in range(len(message)):
            if message[i]:
                for j in range(K):
                    gate = RYGate((4 * math.pi * bit * self.k[j]) / N).control(last_qubit_index - first_qubit_index, ctrl_state=j)
                    qargs = range(first_qubit_index, last_qubit_index + 1)
                    self.circuit.append(gate, qargs)
            bit *= 2

    def generate_swap_test_circuit(self, test_qubit_index, first_result_qubit, second_result_qubit):
        self.circuit.h([test_qubit_index])
        for i in range(0, first_result_qubit + 1):
            self.circuit.cswap(test_qubit_index, i, second_result_qubit - first_result_qubit + i)
        self.circuit.h([test_qubit_index])
        self.circuit.measure([test_qubit_index], [0])

    def run_test(self, window):
        nShots = 1000
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

