import random 
from kyber import Kyber512

import numpy as np

pk, sk = Kyber512.keygen()
c, key = Kyber512.enc(pk)
_key = Kyber512.dec(c, sk)
assert key == _key
print("ASSERT-->",key == _key)
print("PRIVATE_KEY-->",sk[:10])
print("PUBLIC_KEY-->",pk[:10])
print("c_KEY-->",c[:10])
print("key------->",key[:10])
print("_KEY-->",_key[:10])
print("----KEYGEN----")
key = Kyber512.dec(c, sk) 
print("key------->",key[:10])