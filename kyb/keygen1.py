import random 
from kyber import Kyber512
from polynomials import *
import numpy as np
from kyberFunctions1 import *
#key generation
def KeyGeneration(grade,qint):
    s=[]
    for i in range(0,2):
        s.append(createRandomPolynomial1(1,grade,qint))

    matrixSize=2
    # s1 = -1*x**3 - 1*x**7+x
    # s2 = -1*x**3 - 1*x
    # print("s1=",[s1,s2])

    A=[]
    for i in range(0,matrixSize):
        A.append([])
        for j in range(0,matrixSize):
            A[i].append(createRandomPolynomial(qint//2,grade,qint))
            # print("A==",A)

    # em1 = 1*x**2   #em1
    # em2 = 1*x**2 -1*x   #em2
    return np.array(s), np.array(A)
    # return s1,s2,A