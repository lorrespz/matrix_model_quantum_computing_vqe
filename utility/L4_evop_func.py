# Code written by HLD for the work arXiv: 2503.13368 [quant-ph, hep-th]
import numpy as np
import pandas as pd
import pylab
import matplotlib.pyplot as plt
import time

import qiskit
from qiskit.quantum_info import Pauli
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms import NumPyEigensolver
from qiskit.circuit.library import EvolvedOperatorAnsatz

class L4_evop():
	def __init__(self, _ll):
		self.ll = _ll
		self.file_link = f"../../utility/pauliH_L4_g{self.ll}.txt"

		self.data_coeff, self.data_str = self.open_n_process()
		self.Hpauli = list(zip(self.data_str, self.data_coeff))
		self.H4q = SparsePauliOp.from_list(self.Hpauli)
		self.solver = NumPyEigensolver(k=4)
		self.exact_solution = self.solver.compute_eigenvalues(self.H4q)
		#print("Exact Result of qubit hamiltonian:", np.real(exact_solution.eigenvalues))
		self.E_exact = np.round(np.real(self.exact_solution.eigenvalues)[0],5)
		print(f'{self.check_min_max()}')
		print(f'E_exact = {self.E_exact}')

		#get the indices of the N largest elements
		self.ind15, self.ops15, self.vals15 = self.get_k_largest_ops(15)
		self.ind20, self.ops20, self.vals20 = self.get_k_largest_ops(20)
		self.ind25, self.ops25, self.vals25 = self.get_k_largest_ops(25)
		self.ind30, self.ops30, self.vals30 = self.get_k_largest_ops(30)
		self.ind40, self.ops40, self.vals40 = self.get_k_largest_ops(40)

		self.ops_Hp15 =[Pauli(f'{self.ops15[i]}') for i in range(len(self.ops15))]
		self.ops_Hp20 =[Pauli(f'{self.ops20[i]}') for i in range(len(self.ops20))]
		self.ops_Hp25 =[Pauli(f'{self.ops25[i]}') for i in range(len(self.ops25))]
		self.ops_Hp30 =[Pauli(f'{self.ops30[i]}') for i in range(len(self.ops30))]
		self.ops_Hp40 =[Pauli(f'{self.ops40[i]}') for i in range(len(self.ops40))]

		ev_op_Hp15 = EvolvedOperatorAnsatz(self.ops_Hp15, reps=1, insert_barriers=True)
		ev_op_Hp20 = EvolvedOperatorAnsatz(self.ops_Hp20, reps=1, insert_barriers=True)
		ev_op_Hp25 = EvolvedOperatorAnsatz(self.ops_Hp25, reps=1, insert_barriers=True)
		ev_op_Hp30 = EvolvedOperatorAnsatz(self.ops_Hp30, reps=1, insert_barriers=True)
		ev_op_Hp40 = EvolvedOperatorAnsatz(self.ops_Hp40, reps=1, insert_barriers=True)

		ev_op_Hp15_2f = EvolvedOperatorAnsatz(self.ops_Hp15, reps=2, insert_barriers=True)
		ev_op_Hp20_2f = EvolvedOperatorAnsatz(self.ops_Hp20, reps=2, insert_barriers=True)
		ev_op_Hp25_2f = EvolvedOperatorAnsatz(self.ops_Hp25, reps=2, insert_barriers=True)
		ev_op_Hp30_2f = EvolvedOperatorAnsatz(self.ops_Hp30, reps=2, insert_barriers=True)
		ev_op_Hp40_2f = EvolvedOperatorAnsatz(self.ops_Hp40, reps=2, insert_barriers=True)

		self.ansatz_list = [ev_op_Hp15, ev_op_Hp20, ev_op_Hp25, ev_op_Hp30, ev_op_Hp40, 
	               ev_op_Hp15_2f, ev_op_Hp20_2f, ev_op_Hp25_2f, ev_op_Hp30_2f, ev_op_Hp40_2f]

		self.ansatz_names = ['ev_op_Hp15', 'ev_op_Hp20', 'ev_op_Hp25', 'ev_op_Hp30', 'ev_op_H40',
	               'ev_op_Hp15_2f','ev_op_Hp20_2f','ev_op_Hp25_2f', 'ev_op_Hp30_2f', 'ev_op_Hp40_2f']

	def open_n_process(self):
	    file = open(self.file_link, "r")
	    content = file.read()

	    data = content.split(',\n')
	    data[0] = data[0].split('\n')[1]
	    data[-1] = data[-1].split('\n')[0]

	    data_coeff = []
	    data_str = []
	    for i in range(len(data)):
	        data_coeff.append(float(data[i].split('*')[0]))
	        data_str.append(data[i].split('*')[1].split(' ')[1])
	    return data_coeff, data_str 

	def check_min_max(self):
	    print(f'Min absolute value is {np.round(np.min(np.abs(self.data_coeff[1:])),6)}')
	    print(f'Max absolute value is {np.round(np.max(np.abs(self.data_coeff[1:])),5)}')
	    print(f'Mean absolute value is {np.round(np.mean(np.abs(self.data_coeff[1:])),5)}')
    
	def get_k_largest_ops(self, k):
	    ind_list = np.argsort(np.abs(self.data_coeff[1:]))[-k:]
	    ops = [self.data_str[1:][i] for i in ind_list]
	    val= [np.round(self.data_coeff[1:][i],4) for i in ind_list]
	    return ind_list, ops, val

	