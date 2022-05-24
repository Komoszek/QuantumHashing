from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.circuit.library import RYGate
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import math
from qiskit import Aer, execute

class QuantumHash:
    def __init__(self, backend=Aer.get_backend('qasm_simulator'), msg=[], qubits_num=0):
        self.backend = backend
        self._msg = msg
        self._qubits_num = qubits_num
        self.circuit = QuantumCircuit(self.qubits_num)
        self._k = []
        self._constructed_circuit = True
        self._result = None

    def get_result(self, recalculate=False):
        if recalculate or not self.constructed_circuit or self._result is None:
            self.recalculate_result()
        return self._result

    def recalculate_result(self, shots=1000):
        if not self.constructed_circuit:
            self.generate_circuit()
        self._result = execute(self.circuit.measure_all(inplace=False), self.backend, shots=shots).result()

    def generate_circuit(self):
        self.circuit = QuantumCircuit(self.qubits_num)
        control_qubits_num = self.control_qubits_num
        N = 2 ** len(self.msg)
        K = 2 ** control_qubits_num
        bit = 1
        self.circuit.h(range(0, control_qubits_num))

        print(self.qubits_num)

        for i in range(len(self.msg)):
            if self.msg[i]:
                for j in range(K):
                    gate = RYGate((4 * math.pi * bit * self.k[j]) / N).control(control_qubits_num, ctrl_state=j)
                    self.circuit.append(gate, range(self.qubits_num))
            bit *= 2
        self.result = None
        self.constructed_circuit = True
        self._measure_circuit = self.circuit.measure_all(inplace=False)

    def show_circuit(self, output='mpl'):
        if not self.constructed_circuit:
            self.generate_circuit()
        self.circuit.draw(output=output)
        plt.show()

    def show_histogram(self):
        res = self.get_result().get_counts(self.circuit.measure_all(inplace=False))
        plot_histogram(res, title='Hash histogram')
        plt.show()

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, value):
        self._msg = value

    @property
    def control_qubits_num(self):
        return self._qubits_num - 1

    @property
    def qubits_num(self):
        return self._qubits_num

    @control_qubits_num.setter
    def control_qubits_num(self, value):
        self.qubits_num = value + 1

    @qubits_num.setter
    def qubits_num(self, value):
        self._qubits_num = value
        self.k = [i for i in
                  range(2 ** self.control_qubits_num)]  # replace with adding zeros and removing last elements
        self.constructed_circuit = False

    @property
    def k(self):
        return self._k

    @k.setter
    def k(self, value):
        self._k = value
        self.constructed_circuit = False

    def set_single_k(self, new_k_val, i):
        self.k[i] = new_k_val
        self.constructed_circuit = False




'''
a = QuantumHash()
a.qubits_num = 4
a.msg = [0, 1, 0]
a.show_circuit()
a.show_histogram() # it will probably segfault if you try it without show_circuit()
'''
