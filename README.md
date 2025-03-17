# Exploring new variational quantum circuit ansatze for solving SU(2) matrix models

This repo contains the Python codes for the paper `Exploring new variational quantum circuit ansatze for solving SU(2) matrix models'.

Using IBM Qiskit, three types of variational quantum circuit ansatze were used to run the Variational Quantum Eigensolver (VQE) algorithms:
- EfficientSU2: https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.EfficientSU2
- TwoLocal: https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.TwoLocal
- EvolvedOperatorAnsatz: https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.EvolvedOperatorAnsatz

The structure of this repo is as follows:

matrix_model_quantum_computing_vqe/
│
├── L=2_BMN_EvolvedOperator/  # $\Lambda=2$ supersymmetric $SU(2)$ matrix model, VQEs with EvolvedOperatorAnsatz quantum circuits
├── src/                    # Source code for the project
│   ├── __init__.py         # Makes src a Python module
│   ├── data.py             # Scripts to download or generate data
│   ├── model.py            # Scripts to create the machine learning model
│   ├── utils.py            # Utility scripts for transformation and data manipulation
│
├── L=2_EffSU2_TwoLocal/     # $\Lambda=2$ bosonic $SU(2)$ matrix model, VQEs with TwoLocal+EfficientSU2 circuits
├── L=2_EvolvedOperator/     # $\Lambda=2$ bosonic $SU(2)$ matrix model, VQEs with EvolvedOperatorAnsatz circuits
├── L=4_EffSU2_TwoLocal/     # $\Lambda=4$ bosonic $SU(2)$ matrix model, VQEs with TwoLocal+EfficientSU2 circuits
├── L=4_EvolvedOperator/      # $\Lambda=4$ bosonic $SU(2)$ matrix model, VQEs with EvolvedOperatorAnsatz circuits
├── utility        # Directory containing some utility scripts to run the Jupyter notebooks in other directories              # Specifies intentionally 
└── README.md               # README file
