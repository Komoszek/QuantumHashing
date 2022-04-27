from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.circuit.library import RYGate
from qiskit.visualization import plot_histogram
from qiskit import transpile
import matplotlib.pyplot as plt
import math
from qiskit import BasicAer

backend = BasicAer.get_backend('qasm_simulator')

class QuantumHash:
	def __init__(self, msg='', qubits_num=0):
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
		self._result = backend.run(transpile(self.circuit, backend), shots=shots).result()

	def generate_circuit(self):
		self.circuit = QuantumCircuit(self.qubits_num)
		control_qubits_num = self.control_qubits_num
		N = 2 ** control_qubits_num
		bit = 1
		self.circuit.h(range(0, control_qubits_num))

		for i in range(len(self.msg)):
			if self.msg[i] == '1':
				for j in range(N):
					gate = RYGate((4 * math.pi * bit * self.k[j]) / N).control(control_qubits_num, ctrl_state=j)
					self.circuit.append(gate, range(self.qubits_num))
			bit *= 2
		self.result = None

	def show_circuit(self, output='mpl'):
		if not self.constructed_circuit:
			self.generate_circuit()
		self.circuit.draw(output=output)
		plt.show()

	def show_histogram(self):
		plot_histogram(self.get_result().get_counts(self.circuit)) # no classical output

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

	@qubits_num.setter
	def qubits_num(self, value):
		self._qubits_num = value
		self.k = [i for i in range(2 ** self.control_qubits_num)] # replace with adding zeros and removing last elements
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