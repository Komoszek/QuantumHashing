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
		self.msg = msg
		self.qubits_num = qubits_num
		self.circuit = QuantumCircuit(self.qubits_num)
		self.k = []
		self.constructed_circuit = True
		self.result = None

	def get_result(self, recalculate=False):
		if recalculate or not self.constructed_circuit or self.result is None:
			self.recalculate_result()
		return self.result

	def recalculate_result(self, shots=1000):
		if not self.constructed_circuit:
			self.generate_circuit()
		self.result = backend.run(transpile(self.circuit, backend), shots=shots).result()

	def get_control_qubits_num(self):
		return self.qubits_num - 1

	def generate_circuit(self):
		self.circuit = QuantumCircuit(self.qubits_num)
		control_qubits_num = self.get_control_qubits_num()
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
			self.generateCircuit()
		self.circuit.draw(output=output)
		plt.show()

	def show_histogram(self):
		plot_histogram(self.get_result().get_counts(self.circuit))

	def set_msg(self, msg):
		self.msg = msg
		self.constructed_circuit = False

	def set_qubits_num(self, num):
		self.qubits_num = num
		self.set_k(range(2 ** self.get_control_qubits_num())) # replace with adding zeros and removing last elements
		self.constructed_circuit = False
	
	def set_k(self, new_k):
		self.k = new_k
		self.constructed_circuit = False
	
	def set_single_k(self, new_k_val, i):
		self.k[i] = new_k_val
		self.constructed_circuit = False

