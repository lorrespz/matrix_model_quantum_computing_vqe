# Code written by HLD for the work arXiv: 2503.13368 [quant-ph, hep-th]
#VQE ALGORITHMS
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP, SPSA, COBYLA, NELDER_MEAD, L_BFGS_B, ADAM
from qiskit_algorithms.utils import algorithm_globals 
from qiskit_aer.primitives import Estimator as AerEstimator

import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

class VQE_run():
    def __init__(self, optimizer_, ansatz_, operator_,  iterations_, seed_ = 170):

        self.seed = seed_
        algorithm_globals.random_seed = self.seed
        self.noiseless_estimator = AerEstimator(
                run_options={"seed": self.seed, "shots": 1024},
                transpile_options={"seed_transpiler": self.seed},)
        self.iterations = iterations_
        self.optimizer = optimizer_(maxiter = self.iterations)
        self.ansatz = ansatz_
        self.operator = operator_

        #storing values
        self.counts = []
        self.values = []
        self.std = []
        self.params = []
        self.var = []
    def store_intermediate_result(self,eval_count, parameters, mean, std):
        self.counts.append(eval_count)
        self.values.append(mean)
        self.std.append(std)
        self.var.append(std['variance'])
        self.params.append(parameters)
    
    def run_qve_w_specified_optimizer(self):
        vqe = VQE(self.noiseless_estimator, self.ansatz, self.optimizer, callback=self.store_intermediate_result)
        #result_total = vqe.compute_minimum_eigenvalue(self.operator)
        result = vqe.compute_minimum_eigenvalue(self.operator).eigenvalue.real
        #standard error = sqrt(variance)/sqrt(number of shots)
        standard_error = np.sqrt(self.var[-1])/np.sqrt(1024)
        print(f"VQE result: {result:.5f}")
        print(f'VQE result with standard error: {self.values[-1]:.5f} +/- {standard_error:.5f}')
        print(f'Results range is ({self.values[-1]- standard_error:.5f} - {self.values[-1]+standard_error:.5f})')
        return result, standard_error

#This is for testing only !!!
class VQE_run_no_shots():
    def __init__(self, optimizer_, ansatz_, operator_,  iterations_, seed_ = 170):

        self.seed = seed_
        algorithm_globals.random_seed = self.seed
        self.noiseless_estimator = AerEstimator(
                run_options=None,
                transpile_options={"seed_transpiler": self.seed},)
        self.iterations = iterations_
        self.optimizer = optimizer_(maxiter = self.iterations)
        self.ansatz = ansatz_
        self.operator = operator_

        #storing values
        self.counts = []
        self.values = []
        self.std = []
        self.params = []
        self.var = []
    def store_intermediate_result(self,eval_count, parameters, mean, std):
        self.counts.append(eval_count)
        self.values.append(mean)
        self.std.append(std)
        self.var.append(std['variance'])
        self.params.append(parameters)
    
    def run_qve_w_specified_optimizer(self):
        vqe = VQE(self.noiseless_estimator, self.ansatz, self.optimizer, callback=self.store_intermediate_result)
        result_total = vqe.compute_minimum_eigenvalue(self.operator)
        result = vqe.compute_minimum_eigenvalue(self.operator).eigenvalue.real
        #standard error = sqrt(variance)/sqrt(number of shots)
        standard_error = np.sqrt(self.var[-1])/np.sqrt(1024)
        print(f"VQE result: {result:.5f}")
        print(f'VQE result with standard error: {self.values[-1]:.5f} +/- {standard_error:.5f}')
        print(f'Results range is ({self.values[-1]- standard_error:.5f} - {self.values[-1]+standard_error:.5f})')
        return result_total
