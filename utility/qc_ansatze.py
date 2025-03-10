
import numpy as np
import pylab
import matplotlib.pyplot as plt
from qiskit.circuit.library import TwoLocal, EfficientSU2

num_qubits = 6

############### TWO-LOCAL###############
def TL_ansatz(n_q, r_g='ry', e_g='crx', e_p='circular', fold=1):
	qc = TwoLocal(num_qubits=n_q, rotation_blocks=r_g, entanglement_blocks=e_g,
	              entanglement=e_p, reps=fold, insert_barriers = True)
	print(f'Circuit ansatz with {qc.num_parameters} parameters')	
	return qc

############### EFFICIENT-SU2 ###############

def ef_ansatz(n_q, r_g='ry',  e_p='circular', fold=1):
	qc = EfficientSU2(num_qubits=n_q, su2_gates=r_g, entanglement=e_p, reps=fold, insert_barriers = True)
	print(f'Circuit ansatz with {qc.num_parameters} parameters')
	qc.decompose().draw(output='mpl',fold=1)
	return qc


