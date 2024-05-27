import os
import requests
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
import hashlib
# implementing Diffie Hellman
from binascii import hexlify
from hashlib import sha256
from os import urandom

class Message:
    def __init__(self,content=None,username=None,currentTime=None):
        self.content =content
        self.username = username
        self.currentTime = currentTime
        
        pass
def call(fixedString):
    newString=""
    for i in range (0,len(fixedString)-1):
        if not(fixedString[i]==" " and fixedString[i+1]==" "):
            newString+=fixedString[i]
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
def soloCanal(soloCanales):
    
  salasChat=[]
  for i in soloCanales:
    salasChat.append(i["canal"])
  return salasChat
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
def getIdSession(string1, string2):
    listStrings=sorted([string1,string2])
    sessionString=listStrings[0]+listStrings[1]
    idsession=hash_string(sessionString)
    return idsession[:10]
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.secret_key = 'BAD_SECRET_KEY'
socketio = SocketIO(app)
newUser=[]
users=["user1","user2"]
channelsA=[]
channelsA.append({"canal":"jose","chat":[["user1","jajaja","11:00"],["user2","jijiji","11:01"]],"users":["user1","user2"]})
chatsById={}
def addNewChat(userA,userB):
    idsession=getIdSession(userA,userB)
    return idsession,{"chat":[],"users":[userA,userB],}
def checkChats(currentUser):
    temp=""
    newChats=[]
    oldChats=[]
    for i in users:
        if i !=currentUser:
            temp=getIdSession(i,currentUser)
            if not(temp in chatsById):
                newChats.append([i,temp])
            else:
                oldChats.append([i,temp])
    if not (currentUser in users):
        users.append(currentUser)
    return oldChats,newChats

xd=getIdSession(users[0],users[1])
chatsById[xd]={"chat":[],"users":["user1","user2"],}
message1= Message(username="user1",content="jajajaja",currentTime="11:11")
message2= Message(username="user2",content="jajajaja",currentTime="11:12")
chatsById[xd]["chat"].append(message1) 
chatsById[xd]["chat"].append(message2)

@app.route("/")
def index():
    if "username" in session and session["username"] is not None:
        return redirect(url_for('chatList'))    

    return render_template("log.html")
    # return render_template("createRoom.html",nName="jose",channels=channels)

@app.route("/newChannels",methods=["POST"])
def newChannels():
    # print(123123132)
    if not("username" in session and session["username"] is not None):
        return jsonify({"success":False,"newChannel":"aaa"})
        # return redirect(url_for('chatlist')) 
    newChannel = call(request.form.get("newChannel"))
    channelsA.append({"canal":newChannel,"chat":[],"users":[]})
    return jsonify({"success":True,"newChannel":channelsA[-1]["canal"]})



@app.route("/chatList",methods=["GET","POST"])
def chatList():
    print(chatsById)
    if "username" in session and session["username"] is not None:
        session['oldChats'],session['newChats']=checkChats(session['username'])
        # print("old",session['oldChats'],session['newChats'],"\nidchats",chatsById)
        return render_template("chatLists.html",username=session['username'],
                               oldChats=session['oldChats'],
                               newChats=session['newChats'])   
        # return render_template("chatLists.html",username=session['username'],channels=soloCanal(channelsA),oldChats=session['oldChats'],newChats=session['newChats'])   
    elif request.method == "POST" :
        session['username']=request.form.get("username")
        session['oldChats'],session['newChats']=checkChats(session['username'])
        return render_template("chatLists.html",username=session['username'],
                               oldChats=session['oldChats'],
                               newChats=session['newChats'])    
        # print("old",session['oldChats'],session['newChats'],"\nidchats",chatsById)
        # return render_template("chatLists.html",username=session['username'],channels=soloCanal(channelsA),oldChats=session['oldChats'],newChats=session['newChats'])    
    else:
        return redirect(url_for('index'))#"error"

@app.route("/chatList/<Source>", methods=["GET","POST"] )
def chatRoom(Source):
    if Source in chatsById:
        if chatsById[Source]["users"][0]==session["username"]:
            session["otherUser"]=chatsById[Source]["users"][1]
        else:
            session["otherUser"]=chatsById[Source]["users"][0]
        return render_template("chatRoom.html",messages=chatsById[Source]["chat"],
                               source=Source,
                               username=session['username'],
                               otherUser=session["otherUser"])        
        # return jsonify({"success":True,"Source":Source})
    else:
        return jsonify({"success":False,"Source":Source})
    # for k in channelsA:
    #     if Source == k["canal"]:
    #         # print(session['username'],11111)
    #         print(k["chat"])
    #         return render_template("chatRoom.html",messages=k["chat"],source=Source,username=session['username'])

@app.route("/leave",methods=["GET","POST"] )
def leave():
    session.pop('username', default=None)
    return redirect(url_for('index'))    

@socketio.on("submit mss")
def submitMss(data):
    newMessage = Message(username=data["username"],content=data["content"],currentTime=data["currentTime"])

    channelid = data["channelid"]
    emmitMessageJson={'channelid':channelid,'username':newMessage.username,'content':newMessage.content,'currentTime':newMessage.currentTime    }

    if channelid in chatsById:
        chatsById[channelid]["chat"].append(newMessage)
    emit("announce mensaje", {"newMessage": emmitMessageJson,
                              }, broadcast=True)



@app.route("/newPriv",methods=["POST"])
def newPriv():
    # print("AAAAAAAAAAAAAAAAAAAAAAAA",not("username" in session and session["username"] is not None))
    if not("username" in session and session["username"] is not None):
        return jsonify({"success":False,"newChannel":"error"})
    ui=request.form.get("newChannel")
    userToAdd = call(ui)
    idChannel=getIdSession(session['username'],userToAdd)

    if not(idChannel in chatsById):
        chatsById[idChannel]={"chat":[],"users":[session['username'],userToAdd]}    
        print(chatsById[idChannel])
        return jsonify({"success":True,"toUser":userToAdd,"idChannel":idChannel})

    # if (newChannel in channels):
    return jsonify({"success":False,"newChannel":userToAdd})
    # else:
        # channels.append(newChannel)
        # return jsonify({"success":True,"newChannel":channels[-1]})





# if __name__ == "__main__":
#     socketio.run(app)










