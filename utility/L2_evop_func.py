# Code written by HLD for the work arXiv: 2503.13368 [quant-ph, hep-th]
import numpy as np
import qiskit
from qiskit.quantum_info import Pauli
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import EvolvedOperatorAnsatz
from qiskit_algorithms import NumPyEigensolver

class L2_supersymmetric_EvOp():

    def __init__(self, coupling):
        self.ll = coupling
        self.file_link =f'../../utility/L2_BMN_l{self.ll}_Hpauli.txt'
        self.data_coeff, self.data_str = self.open_n_process()
        Hpauli = list(zip(self.data_str, self.data_coeff))
        self.H4q = SparsePauliOp.from_list(Hpauli)
        # exactly diagonalize the system using numpy routines
        solver = NumPyEigensolver(k=4)
        exact_solution = solver.compute_eigenvalues(self.H4q)
        #print("Exact Result of qubit hamiltonian:", np.real(exact_solution.eigenvalues))
        E_exact = np.round(np.real(exact_solution.eigenvalues)[0],6)
        print(f'{self.check_min_max()}')
        print(f'E_exact = {E_exact}')

        self.ind15, self.ops15, self.vals15 = self.get_k_largest_ops(15)
        self.ind20, self.ops20, self.vals20 = self.get_k_largest_ops(20)

        self.ops_Hp15 =[Pauli(f'{self.ops15[i]}') for i in range(len(self.ops15))]
        self.ops_Hp20 =[Pauli(f'{self.ops20[i]}') for i in range(len(self.ops20))]
        self.ops_H =[Pauli(f'{self.data_str[1:][i]}') for i in range(len(self.data_str[1:]))]

        ev_op_Hp15 = EvolvedOperatorAnsatz(self.ops_Hp15, reps=1, insert_barriers=True)
        ev_op_Hp20 = EvolvedOperatorAnsatz(self.ops_Hp20, reps=1, insert_barriers=True)
        ev_op_H = EvolvedOperatorAnsatz(self.ops_H, reps=1, insert_barriers=True)

        ev_op_Hp15_2f = EvolvedOperatorAnsatz(self.ops_Hp15, reps=2, insert_barriers=True)
        ev_op_Hp20_2f = EvolvedOperatorAnsatz(self.ops_Hp20, reps=2, insert_barriers=True)
        ev_op_H_2f = EvolvedOperatorAnsatz(self.ops_H, reps=2, insert_barriers=True)

        ev_op_Hp15_3f = EvolvedOperatorAnsatz(self.ops_Hp15, reps=3, insert_barriers=True)
        ev_op_Hp20_3f = EvolvedOperatorAnsatz(self.ops_Hp20, reps=3, insert_barriers=True)
        ev_op_H_3f = EvolvedOperatorAnsatz(self.ops_H, reps=3, insert_barriers=True)

        ev_op_Hp15_4f = EvolvedOperatorAnsatz(self.ops_Hp15, reps=4, insert_barriers=True)
        ev_op_Hp20_4f = EvolvedOperatorAnsatz(self.ops_Hp20, reps=4, insert_barriers=True)
        ev_op_H_4f = EvolvedOperatorAnsatz(self.ops_H, reps=4, insert_barriers=True)

        self.ansatz_list = [ev_op_Hp15, ev_op_Hp20, ev_op_H,
                       ev_op_Hp15_2f, ev_op_Hp20_2f, ev_op_H_2f,
                       ev_op_Hp15_3f, ev_op_Hp20_3f, ev_op_H_3f,
                       ev_op_Hp15_4f, ev_op_Hp20_4f, ev_op_H_4f]

        self.ansatz_names = ['ev_op_Hp15', 'ev_op_Hp20', 'ev_op_H',
                       'ev_op_Hp15_2f','ev_op_Hp20_2f','ev_op_H_2f',
                       'ev_op_Hp15_3f','ev_op_Hp20_3f','ev_op_H_3f',
                       'ev_op_Hp15_4f','ev_op_Hp20_4f','ev_op_H_4f']

        #print(f'number of params: {[ansatz_list[i].num_parameters for i in range(len(ansatz_list))]}')

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
