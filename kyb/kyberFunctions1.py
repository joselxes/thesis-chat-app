import random 
from kyber import Kyber512
from polynomials import *
import numpy as np
#functions

def createRandomPolynomial(maxInteger,maxDegree,qint):
    R = PolynomialRing(qint, maxDegree)
    x = R.gen()
    randomPoly=0*x**0
    randCoeff=0
    # print("randomPoly",randomPoly)
    for i in range(0,maxDegree ):
        randCoeff=random.randint(-maxInteger,maxInteger )
        randomPoly+=( randCoeff*x**i)    
    # print("random poly=", randomPoly)
    return randomPoly
def createRandomPolynomial1(maxInteger,maxDegree,qint):
    R = PolynomialRing(qint, maxDegree)
    x = R.gen()
    randomPoly=0*x**0
    randCoeff=0
    # print("randomPoly",randomPoly)
    for i in range(0,maxDegree ):
        randCoeff=random.randint(0,maxInteger )
        randomPoly+=( randCoeff*x**i)    
    # print("random poly=", randomPoly)
    return randomPoly
def closer(num1,middle,top):
    topDist=top-num1
    middleDist=abs(middle-num1)

    if (  topDist<middleDist  or num1<middleDist) :
        return 0
    return middle
def binToPoly(binaryNumber,qint,maxDegree):
    R = PolynomialRing(qint, maxDegree)
    x = R.gen()
    binaryPoly=0
    for i in range(0,len(binaryNumber) ):
        binaryPoly+=(int(binaryNumber[i]))*x**(len(binaryNumber)-i-1)
    # print(binaryPoly)
    return binaryPoly
def getchar(binary_string): 
    # Convert binary string to decimal integer
    decimal_value = int(binary_string, 2)

    # Convert decimal value to ASCII character
    ascii_character = chr(decimal_value)
    
    # Getting the ASCII value
    return ascii_character
def complete(binString):
    filled=binString
    while(len(filled)%8!=0):
        filled="0"+filled
    return filled
def fromPolyToString(coefficientsList):
    # print(coefficientsList,"coeff")
    newStr=""
    newStrInt=[]
    newStrBinary=[]
    temp=[]
    for i in range(0,len(coefficientsList),8):
        # print(i,temp)
        temp=""
        for j in range(1,9):
            # print(coefficientsList[ (i+8) -j]) 
            temp+=str(coefficientsList[ (i+8) -j]) 
    

        newStrInt.append(int(temp, 2))
        # newStrBinary.append(temp)
        # print(chr(newStrInt[-1]),"imprimo temp")
        newStr=chr(newStrInt[-1])+newStr
    # print(newStrBinary)
    # print("salimoooooooooooos")
    return newStr,newStrInt
def message2BinaryArray(text):
    temporl=""
    message=[]
    for i in range(0,len(text),8):
        for j in range(0,8):
            if(i+j<len(text)):
                temporl+=complete(bin( ord( text[ i+ j] ) )[2:])
        message.append(temporl)
        temporl=""
    return message

def forgeT(M11,M12,M21,M22,privK1,privK2,grade):
    # errorPolyVector=[]
    ePolyV1=createRandomPolynomial(1,grade)
    ePolyV2=createRandomPolynomial(1,grade)
    # publicKeyt=[]
    publicKeyt1=(M11*privK1 + M12*privK2) + ePolyV1[0]
    publicKeyt2=(M21*privK1 + M22*privK2) + ePolyV2[1]
    return publicKeyt1,publicKeyt2,ePolyV1,ePolyV2
def forgeTnp(M,privK,grade,qint):
    errorPolyVector=[]
    errorPolyVector.append(createRandomPolynomial(1,grade,qint))
    errorPolyVector.append(createRandomPolynomial(1,grade,qint))
    errorPolyVector=np.array(errorPolyVector)
    # publicKeyt=[]
    # print("sizeA=",M.shape,"sizek=",privK.shape)
    publicKeyt= np.matmul(M,privK) 
    publicKeyt= np.add( publicKeyt , errorPolyVector)
    return publicKeyt,errorPolyVector