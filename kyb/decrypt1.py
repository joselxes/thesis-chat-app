import random 
from kyber import Kyber512
from polynomials import *
import numpy as np
from kyberFunctions1 import *
# #DECRYPTION
def Dec( privKeys, polyu, polyv, maxDegree, qint):
    R = PolynomialRing(qint, maxDegree)
    x = R.gen()

    mn=np.subtract( polyv, np.matmul(privKeys.transpose(),polyu) )
    # print("mn---->\n",mn)
    # print("mn=",mn)
    mrounded=0
    for i in range (0,len(mn.coeffs)):
        mrounded+=closer(mn.coeffs[i],qint//2,qint)*x**i    
        # mb+=(int(numBin[i]))*x**(len(numBin)-i-1)

    # print("rounded=",mrounded)
    messrecover=np.array(mrounded.coeffs)//(qint//2)
    
    # print("mround=",mrounded.coeffs)
    # print("recover=",messrecover)
    finalstr,finalstrInt=fromPolyToString(messrecover)
    # print(finalstrInt)
    # print(finalstr,"xxxx",finalstrInt)
    return finalstr