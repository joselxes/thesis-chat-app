import random 
from kyber import Kyber512
from polynomials import *
import numpy as np
from kyberFunctions1 import *
from keygen1 import *
from encrypt1 import *
from decrypt1 import *
# from kyber import Kyber512
pk, sk = Kyber512.keygen()
c, key = Kyber512.enc(pk)
_key = Kyber512.dec(c, sk)
assert key == _key
print("ASSERT-->",key == _key)
print("PRIVATE_KEY-->",sk[:10])
print("PUBLIC_KEY-->",pk[:10])
print("c_KEY-->",c[:10])
print("key-->",key[:10])
print("_KEY-->",_key[:10])
print("----KEYGEN----")
start_range = 13
end_range = 3329

contTrue=0
contFalse=0
mensajeStr='hola mundo, queria agradecer por su paciencia en estos tiempos dificiles que nos encontramos. Gracias por el apoyo!!:)'
mensajeStr='HiWorld!'
mensajeStrb=b'hola mundo qwertyuiopasdfghjklzxcvbnm AAAAAAAAAAA BBBBBBBBBBBBBB CCCCCCCCCC DDDDDDDDDDDDDD'
resultArr=""
temporl=""
binaryArray=message2BinaryArray(mensajeStr)
print(len(binaryArray),len(mensajeStr))
# for tryi in range(0,1):
#     for element in binaryArray:
#         print("byte size",len(element)//8)
#         q=2*random.randint(start_range,end_range)
#         # print(q,element)
#         qhalf=q//2
#         polyGrade=len(element)
#         R = PolynomialRing(q, polyGrade)
#         x = R.gen()
#         secKs,MA=KeyGeneration(polyGrade,q)
#     #     # print("----ENCRYPTION----")
#         pubKt,ePolyVec=forgeTnp(MA,secKs,polyGrade,q)
#         polyu,polyv=Enc(MA,pubKt,ePolyVec,element,polyGrade,q)
#     #     # print("----dECRYPTION----")
#         decodedMessage=Dec( secKs, polyu, polyv,polyGrade,q) 
#         # print(polyu,polyv)
#         print(decodedMessage)
#         resultArr+=decodedMessage
#         # if ( messageToEnc == decodedMessage ):
#         #     contTrue+=1
#         # else:
#         #     contFalse+=1

#     print("|"+resultArr+"|","len=",len(resultArr))
#     resultArr=""
#     print("la q=",q)

#         print("q=",q)
#         print("completed",messageToEnc)
#         # print(R)
#         print("messageToEnc=",messageToEnc,"ActualMess=",decodedMessage)
#         print("x",decodedMessage,"x")
#         print( messageToEnc == decodedMessage )

# #     # input()
# print("|"+resultArr+"|","|"+mensajeStr+"|",resultArr==mensajeStr)
# print("Success=",contTrue)
# print("Fail   =",contFalse)
# # print(bin("hola mundo"))
# per=""
# j=0
# splittedMesage=[]
# while (len(per)<256 and j<len(mensajeStrb)):
#     per+=complete( bin( mensajeStrb[j] )[2:] )
#     # print( mensajeStrb[j] , bin( mensajeStrb[j] ) )
#     if (len(per)==256 or j+1>len(mensajeStrb)):
#         splittedMesage.append(per)
#         per=""
#         print(j,chr(mensajeStrb[j]))
#     j+=1
# splittedMesage.append(per)
# print( chr(mensajeStrb[j-1]) )
# print(splittedMesage)
# print(splittedMesage[0][:8])
# print(binToPoly(splittedMesage[0][:8]))
# print(binToPoly(splittedMesage[0][:8]).coeffs)
# # coeffs
# # def getMessage(mess2recover):
# #     final=""

# #     for i in range(0,len(mess2recover),8):
# #         final+=str(mess2recover[i:i+8])
# #     # print(int(final,2),"binary=",final)
