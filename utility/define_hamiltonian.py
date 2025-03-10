import qiskit
import numpy as np
import itertools

def bosonHamiltonians(numBosons, bosonMatrixDim, coupling=0.1):
    annOP = np.array(np.diagflat(np.sqrt(np.linspace(1,bosonMatrixDim-1,bosonMatrixDim-1)),k=1))   
    # Create the n x n identity matrix.
    iden = np.identity(bosonMatrixDim)
    
    # Create a list which holds the six bosons.
    # For the first boson, the Kronecker product starts with the annihilation operator.
    bosonList = [annOP]
    for bosons in range(0,numBosons-1):
        bosonList.append(iden)
    for i in range(0,numBosons):
        for j in range(0,numBosons-1):  
            # For the nth boson, the nth Kronecker product is with the annihilation operator.
            if j == i-1 and i != 0:
                bosonList[i] = np.kron(bosonList[i], annOP)
            # Else, the nth Kronecker product is with the identity matrix.
            else:
                bosonList[i] = np.kron(bosonList[i], iden)

    # Create the position operators. Normalized as in the notes
    x = []
    # x_I = 1/sqrt(2)(a_I + a^\dagger_I)
    for r in range(0, numBosons):
        x.append((1/np.sqrt(2))*(bosonList[r] + np.transpose(np.conjugate(bosonList[r]))))
    
    # Create the simple quadratic Hamiltonian.
    H2MM = 0
    for i in range(0,numBosons):
        # The free part: \sum a^\dagger_I a_I
        H2MM = H2MM + (np.transpose(np.conjugate(bosonList[i])) @ bosonList[i])
    # The constant of 1/2*Identity
    H2MM = H2MM + 0.5*numBosons*np.identity(bosonMatrixDim**(numBosons))

    # Create the full quartic SU(2) Hamiltonian.
    x_sq = []
    for i in x:
        x_sq.append(i @ i)

    H4MM1 = (H2MM + coupling*((x_sq[2] @ x_sq[3]) 
                              + (x_sq[2] @ x_sq[4]) 
                              + (x_sq[1] @ x_sq[3]) 
                              + (x_sq[1] @ x_sq[5])
                              + (x_sq[0] @ x_sq[4])
                              + (x_sq[0] @ x_sq[5])
                              - 2*((x[0] @ x[2]) @ (x[3] @ x[5]))
                              - 2*((x[0] @ x[1]) @ (x[3] @ x[4]))
                              - 2*((x[1] @ x[2]) @ (x[4] @ x[5]))))
    return H2MM, H4MM1

############################## Convert to PauliOp (L=2 only) ##############################
def vec_query(arr, my_dict):
    return np.vectorize(my_dict.__getitem__, otypes=[tuple])(arr)

def nested_kronecker_product(a):
    if len(a) == 2:
        return np.kron(a[0],a[1])
    else:
        return np.kron(a[0], nested_kronecker_product(a[1:]))

def Hilbert_Schmidt(mat1, mat2):
    return np.trace(mat1.conj().T @ mat2)

def decompose(Ham_arr, tol=5):
    # Define a dictionary with the four Pauli matrices:
    pms = {'I': np.array([[1, 0], [0, 1]], dtype=complex),
            'X': np.array([[0, 1], [1, 0]], dtype=complex),
            'Y': np.array([[0, -1j], [1j, 0]], dtype=complex),
            'Z': np.array([[1, 0], [0, -1]], dtype=complex)}
    pauli_keys = list(pms.keys()) # Keys of the dictionary
    nqb = int(np.log2(Ham_arr.shape[0])) # Determine the # of qubits needed
    output_string = '' # Initialize an empty string to which we can add our terms
    # Make all possible combinations of nqb Pauli matrices
    sigma_combinations = list(itertools.product(pauli_keys, repeat=nqb))
    # Loop through each unique combination of Pauli Matrices
    for ii in range(len(sigma_combinations)):
        # Take the full Pauli string
        pauli_str = ''.join(sigma_combinations[ii])
        #print(pauli_str)
        norm_factor = (1/(2**nqb))
        # Convert the Pauli string to list of arrays
        tmp_mat_list = vec_query(np.array(sigma_combinations[ii]), pms)
        # Evaluate the Kronecker product of the matrix array
        tmp_p_matrix = nested_kronecker_product(tmp_mat_list)
        hs_innerprod = Hilbert_Schmidt(tmp_p_matrix, Ham_arr)
        a_coeff = norm_factor * hs_innerprod
        # If the coefficient is non-zero, we want to use it!
        if a_coeff != 0.0:
            #Assert that coefficients less than 10**-tol are 0.
            min_val = 10**(-tol)
            if abs(a_coeff) < min_val:
                pass
            # If non-zero:
            else:
                output_string += str(np.round(a_coeff.real, tol))+"*"+pauli_str
                output_string += '+' # Add a plus sign for the next term!
    return output_string[:-1] # To ignore that extra plus sign


def get_pauli_op_w_coeffs(H_pauli_strings):
    op_list = H_pauli_strings.split('+')
    coeffs = []
    pauli_ops = []
    for sub_list in op_list:
        coeff, pauli_op = sub_list.split('*')
        coeffs.append(float(coeff))
        pauli_ops.append(pauli_op)
    return list(zip(pauli_ops, coeffs))