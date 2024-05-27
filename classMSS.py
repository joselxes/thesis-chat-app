import base64
import hashlib
class Message:
    def __init__(self,content=None,username=None,currentTime=None):
        self.content =content
        self.username = username
        self.currentTime = currentTime
        
        pass
def call(fixedString):
    newString=""
    print(fixedString,"=====================)")
    for i in range (0,len(fixedString)-1):
        if not(fixedString[i]==" " and fixedString[i+1]==" "):
            newString+=fixedString[i]
    print(fixedString,"=====================)",len(fixedString))
    if (fixedString[-1]!=" "):
        newString+=fixedString[-1]
    if (newString[0]==" "):
        newString=newString[1 : : ]
    return newString
def communicateList(newMembers,oldMembers):
    parejas=[]
    for i in range( 0, len(newMembers) ):
        for j in range( i+1, len(oldMembers) ):
            parejas.append([newMembers[i],oldMembers[j]])
        oldMembers.append(newMembers[i])
    newMembers=[]
    return parejas
def hash_string(string):
    # Convert the string to bytes (UTF-8 encoding)
    string_bytes = string.encode('utf-8')
    
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()
    
    # Update the hash object with the string bytes
    sha256_hash.update(string_bytes)
    
    # Get the hexadecimal representation of the hashed value
    hashed_string = sha256_hash.hexdigest()
    
    return hashed_string
def soloCanal(soloCanales):
    
  salasChat=[]
  for i in soloCanales:
    salasChat.append(i["canal"])
  return salasChat

def getIdSession(string1, string2):
    listStrings=sorted([string1,string2])
    sessionString=listStrings[0]+listStrings[1]
    idsession=hash_string(sessionString)
    return idsession[:10]
def addNewChat(userA,userB):
    idsession=getIdSession(userA,userB)
    return idsession,{"chat":[],"users":[userA,userB],}

def decode_data(encoded_data):
    return base64.b64decode(encoded_data)
def encode_data(data_bytes):
    return base64.b64encode(data_bytes).decode('utf-8')
