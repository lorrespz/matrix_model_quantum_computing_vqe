#VQE ALGORITHMS
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP, SPSA, COBYLA, NELDER_MEAD, L_BFGS_B, ADAM
from qiskit_algorithms.utils import algorithm_globals 
from qiskit_aer.primitives import Estimator as AerEstimator

import numpy as np
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

class QVE():
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
    def store_intermediate_result(self,eval_count, parameters, mean, std):
        self.counts.append(eval_count)
        self.values.append(mean)
    
    def run_qve_w_specified_optimizer(self):
        vqe = VQE(self.noiseless_estimator, self.ansatz, self.optimizer, callback=self.store_intermediate_result)
        result = vqe.compute_minimum_eigenvalue(self.operator).eigenvalue.real
        print(f"VQE result: {result:.5f}")
        return result
