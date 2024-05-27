import os
import requests
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit

# kybe
from kyber import Kyber512

from flask_cors import CORS
from diffie import DiffieHellman
from classMSS import *

def checkChats(currentUser):
    temp=""
    newChats=[]
    oldChats=[]
    for i in users:
        if i !=currentUser:
            # print(i,currentUser,type(i),type(currentUser))
            temp=getIdSession(i,currentUser)
            if not(temp in chatsById):
                newChats.append([i,temp])
            else:
                oldChats.append([i,temp])
    if not (currentUser in users):
        users.append(currentUser)
    # print (oldChats,newChats,",============================")
    return oldChats,newChats

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.secret_key = 'BAD_SECRET_KEY'
socketio = SocketIO(app)
cors=CORS(app)

newUser=[]
users=[]
usersPublicKeys={}
chatsById={}
channelsA=[]
channelsA.append({"canal":"jose","chat":[["user1","jajaja","11:00"],["user2","jijiji","11:01"]],"users":["user1","user2"]})

checkChats("user1")
checkChats("user2")
# dfh = DiffieHellman()
# private_key, public_key = dfh.get_private_key(), dfh.generate_public_key()
public_key, private_key = Kyber512.keygen()
encrypted_key, key = Kyber512.enc(public_key)
usersPublicKeys["user1"]={"private_key":private_key,"public_key":public_key,"encrypted_key":encrypted_key}

public_key, private_key = Kyber512.keygen()
encrypted_key, key = Kyber512.enc(public_key)
usersPublicKeys["user2"]={"private_key":private_key,"public_key":public_key,"encrypted_key":encrypted_key}

# public_key, private_key="",""
# encrypted_key, key="",""
print(users)
# print(usersPublicKeys)


xd=getIdSession(users[0],users[1])
chatsById[xd]={"chat":[],"users":["user1","user2"],"encrypted_key":encrypted_key}
message1= Message(username="user1",content="jajajaja",currentTime="11:11")
message2= Message(username="user2",content="jajajaja",currentTime="11:12")
chatsById[xd]["chat"].append(message1) 
chatsById[xd]["chat"].append(message2)

@app.route("/")
def index():
    if "username" in session and session["username"] is not None:
        return redirect(url_for('chatList'))    

    return render_template("log.html")


@app.route("/newChannels",methods=["POST"])
def newChannels():
    if not("username" in session and session["username"] is not None):
        return jsonify({"success":False,"newChannel":"aaa"})

    newChannel = call(request.form.get("newChannel"))
    channelsA.append({"canal":newChannel,"chat":[],"users":[]})
    # print(channelsA[-1]["canal"],channelsA[-1]["chat"])
    return jsonify({"success":True,"newChannel":channelsA[-1]["canal"]})



@app.route("/chatList",methods=["GET","POST"])
def chatList():
    # print(usersPublicKeys)
    # print(chatsById)
    if "username" in session and session["username"] is not None:
        session['oldChats'],session['newChats']=checkChats(session['username'])

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

@app.route("/leave",methods=["GET","POST"] )
def leave():
    session.pop('username', default=None)
    return redirect(url_for('index'))    

@socketio.on("submit mss")
def submitMss(data):
    newMessage = Message(username=data["username"],content=data["content"],currentTime=data["currentTime"])
    print("------------",newMessage.content)
    channelid = data["channelid"]
    emmitMessageJson={'channelid':channelid,'username':newMessage.username,'content':newMessage.content,'currentTime':newMessage.currentTime    }

    if channelid in chatsById:
        chatsById[channelid]["chat"].append(newMessage)
    emit("announce mensaje", {"newMessage": emmitMessageJson,
                              }, broadcast=True)

@app.route("/newPriv",methods=["POST"])
def newPriv():
    if not("username" in session and session["username"] is not None):
        return jsonify({"success":False,"newChannel":"error"})
    ui=request.form.get("newChannel")
    print(ui,"ui------------------------",)
    userToAdd = call(ui)
    print(userToAdd,"ui------------------------",)
    idChannel=getIdSession(session['username'],userToAdd)
    encrypted_key, key = Kyber512.enc(usersPublicKeys[userToAdd]["public_key"])
    print("encryption with public key of user:",userToAdd)
    print("newPriv/ enc_key====>",encode_data(encrypted_key)[:10])
    print("newPriv/     key====>",encode_data(key)[:10])


    # generate shared key
    print("ANTES de entrar al IFFF aquiiiiiiiiiiiiiiiii",type(key))
    if not(idChannel in chatsById):
        chatsById[idChannel]={"chat":[],"users":[session['username'],userToAdd],"encrypted_key":encrypted_key}    
        print("al  salir IFFF aquiiiiiiiiiiiiiiiii",encode_data(key))
        return jsonify({"success":True,"toUser":userToAdd,"idChannel":idChannel,"key":encode_data(key)})

    return jsonify({"success":False,"newChannel":userToAdd})

@app.route("/generate_keys", methods=["POST"])
def generate_keys():
    print("---------generate_keys---------",not(session["username"]in usersPublicKeys))
    if not(session["username"]in usersPublicKeys):
        print("entraaaaamos")

        
        public_key, private_key = Kyber512.keygen()


        print("\n---",encode_data(private_key)[:10], encode_data(public_key[:10]))
        # print("key---->", key[:10])

        # print("key---->", key[:10])
        # print("public_key======>", public_key[0:10], "\nprivate_key=====>",private_key[:10])
        usersPublicKeys[session["username"]]={"private_key":private_key,"public_key":public_key}
        # print("nnnnnnnnnnnnnnnnnnnn\n",usersPublicKeys[session["username"]],"\nnnnnnnnnnnnnnnnnnnnn")
        return jsonify({"success":True,"private_key": encode_data(private_key), "public_key": encode_data(public_key)})
    return jsonify({"message": "Invalid JSON data in request body"}), 400
    # if (session["username"]in usersPublicKeys):
    #     try:
    #         print("------------------",1)
    #         # Parse JSON data from the request body
    #         data = request.json
    #         print("------------------",2)
    #         if not data:
    #             return jsonify({"message": "Invalid JSON data in request body"}), 400
    #         print("------------------",3)
    #         # Retrieve private key and receiver from the JSON data
    #         user_private_key = decode_data(data.get("private_key"))
    #         print("------------------",4)
    #         user_public_key = decode_data(data.get("public_key"))
    #         print("------------------",5)
    #         # Validate input data
    #         if not user_public_key or not user_private_key:
    #             print("------------------",6)
    #             return jsonify({"message": "Missing required fields in JSON data"}), 400
    #         print("------------------",7)
    #         print(session["username"],"private_key_xxxxxxxxxxx",usersPublicKeys[session["username"]]["private_key"][:5])
    #         usersPublicKeys[session["username"]]={"private_key":user_private_key,"public_key":user_public_key,}
    #         print(session["username"],"private_key_xxxxxxxxxxx",usersPublicKeys[session["username"]]["private_key"][:5])
    #         return jsonify({"success":True,"message":"No problema "}), 200
    #     except Exception as e:
    #         return jsonify({"message": str(e)}), 500



@app.route("/generate_shared_key", methods=["POST"])
def generate_shared_key():

    try:

        # Parse JSON data from the request body
        print("1-----------")
        data = request.json
        print("2-----------")
        if not data:

            return jsonify({"message": "Invalid JSON data in request body"}), 400

        # Retrieve private key and receiver from the JSON data
        local_private_key = decode_data(data.get("private_key"))
        print("3-----------",)        
        idChannel = data.get("chatIdSession")
        print("4-----------")
        receiver=chatsById[idChannel]["users"][0]
        print("5-----------")
        if receiver==session["username"]:            
            print("6-----------")
            receiver=chatsById[idChannel]["users"][1]


        # Validate input data
        if not local_private_key or not receiver:
            return jsonify({"message": "Missing required fields in JSON data"}), 400

        # Ensure receiver's public key exists

        if receiver not in usersPublicKeys:
            return jsonify({"message": "Receiver's public key not found"}), 400
        # # Retrieve receiver's public key
        # remote_public_key = usersPublicKeys[receiver]["public_key"]


        # # Generate shared key using Diffie-Hellman
        # shared_key = DiffieHellman.generate_shared_key_static(local_private_key, remote_public_key)

        # # Return the shared key----





        encrypted_key=chatsById[idChannel]["encrypted_key"]
        print("7-----------")
        # Generate shared key using Diffie-Hellman
        _key = Kyber512.dec(encrypted_key, local_private_key)

        print("decRyption with private key of user:",)
        print("newPriv/ enc_key====>",encode_data(encrypted_key)[:10])
        print("newPriv/     key====>",encode_data(_key)[:10])

        # Return the shared key


        return jsonify({"shared_key": encode_data(_key)}), 200

    except Exception as e:
        print("TRY EXCEPTION =>eeeeeeeeee exception")
        return jsonify({"message": str(e)}), 500



@app.route("/myProfile", methods=["POST","GET"])
def myProfile():
    return render_template("myProfile.html",username=session["username"],)
    # return render_template("myProfile.html",mykeys=[usersPublicKeys[session["username"]],987654321])
    return render_template("myProfile.html",username=session["username"],mykeys=[usersPublicKeys[ session['username'] ]["private_key"],
                                                    usersPublicKeys[ session['username'] ]["public_key"]])
    # return render_template("myProfile.html",mykeys=[123456789,987654321])


# if __name__ == "__main__":
#     socketio.run(app)




















