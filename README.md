# Exploring new variational quantum circuit ansatze for solving SU(2) matrix models

This repo contains the Python codes for the paper `Exploring new variational quantum circuit ansatze for solving SU(2) matrix models', 	
\href{https://arxiv.org/abs/2503.13368}{arXiv:2503.13368 [quant-ph]}

Using IBM Qiskit, three types of variational quantum circuit ansatze were used to run the Variational Quantum Eigensolver (VQE) algorithms:
- EfficientSU2: https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.EfficientSU2
- TwoLocal: https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.TwoLocal
- EvolvedOperatorAnsatz: https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.EvolvedOperatorAnsatz

The structure of this repo is as follows:
- L=2_BMN_EvolvedOperator: $\Lambda=2$ supersymmetric $SU(2)$ matrix model, VQEs with EvolvedOperatorAnsatz quantum circuits
- L=2_EffSU2_TwoLocal:  $\Lambda=2$ bosonic $SU(2)$ matrix model, VQEs with TwoLocal+EfficientSU2 quantum circuits
- L=2_EvolvedOperator: $\Lambda=2$ bosonic $SU(2)$ matrix model, VQEs with EvolvedOperatorAnsatz quantum circuits
- L=4_EffSU2_TwoLocal: $\Lambda=4$ bosonic $SU(2)$ matrix model, VQEs with TwoLocal+EfficientSU2 quantum circuits
- L=4_EvolvedOperator:  $\Lambda=4$ bosonic $SU(2)$ matrix model, VQEs with EvolvedOperatorAnsatz quantum circuits
- utility:   Directory containing some utility scripts to run the Jupyter notebooks in other directories  

