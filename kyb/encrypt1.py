import random 
from kyber import Kyber512
from polynomials import *
import numpy as np
from kyberFunctions1 import *
# #ENCRYPTION
# (maxInteger,maxDegree,qint)
def Enc(M,t,eV,message,grade,qint):
    errorVectorPolys=[]
    for i in range(0,2):
        errorVectorPolys.append(createRandomPolynomial(1,grade,qint))
    # r1= -1*x**3+1*x**2
    # r2= 1*x**3+1*x**2-1
    # print("randomVector1=",r1)
    # print("randomVector2=",r2)
    rvector=[]
    for i in range(0,2):
        rvector.append(createRandomPolynomial(1,grade,qint))
    rvector= np.array(rvector) 
    ePoly2=createRandomPolynomial(1,grade,qint)
    # errorPoly2=-1*x**3 - 1*x**2
    # print("error2Poly=",errorPoly2)

    mb=binToPoly(message,qint,grade)
    # print("mb=",mb)
    mq= mb*(qint//2)
    # print("mq=",mq)

    # # lets calculate u
    u=np.add(np.matmul(M.transpose(),rvector),eV)
    # print("U=", u )

    # # lets calculate v
    v= np.add(np.matmul(t.transpose(),rvector), np.add(ePoly2, mq))
    # print("v1=",v)
    return u,v