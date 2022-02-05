from errno import ENETRESET
import math
from random import gammavariate
import re
from turtle import color
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import firebase_admin
from firebase_admin import credentials, firestore

from helpers import emojify, listlist_to_stringlist, stringlist_to_listlist
from logics import botstep, winstatus, winstatusbot

app = Flask(__name__)


cred = credentials.Certificate("haunt-4-firebase-adminsdk-vrct0-0f6252fefc.json")
firebase_admin.initialize_app(cred)
db = firestore.client() 
collection = db.collection('users')
# doc = collection.document('rome')



@app.route("/")
def hello():
    return "heheh homeecjn"

@app.route("/sms", methods=['POST'])
def sms_reply():
    msg = request.form.get('Body')
    mobile = request.form.get('From').split('+')[1]
    name = request.form.get('ProfileName')
    

    resp = MessagingResponse()
    doc = collection.document(mobile).get()
    options = ["1","2","3","4","5","6","7"]
    # color = ['yellow', 'red']
    if doc.exists:
        
        if msg=="9":
            collection.document(mobile).delete()
            resp.message(f'successfully exited game')
            return str(resp)
        info = doc.to_dict()
        stage = info['stage']

        if stage == "choose_color":
            if msg not in ["1","2"]:
                resp.message(f"wrong input, try again lol\n\n~or press 9 to exit the game~")
                return resp
            else:
                collection.document(mobile).update({'stage':'gameon', 'color':int(msg)-1})
                # return 
        print(f'Document data: {doc.to_dict()}')
        matrix = info['game_state']
        equivalent = {'0': '🔴','1':'🟡','2':'⬛'}
        matrix_beautiful = ""
        for i in matrix:
            for j in i:
                matrix_beautiful+=equivalent[j]
            matrix_beautiful+="\n"
        matrix_beautiful+="1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣\n"

        if msg in options:
            msg = int(msg)
            for i in range(7):
                if matrix[msg][6-i]=="2":
                    hehe = list(matrix[msg])
                    hehe[6-i]='1'
                    print(hehe)
                    matrix[msg] = "".join(hehe)
                    # lol = "1111111"
                    collection.document(mobile).update({'game_state': matrix})
                    break

        resp.message(f"let's continue the game, {name}\nyour game state is\n\n{matrix_beautiful}\nEnter the number corresponding to the column you wanna put your color into\n\n\n~or press 9 to exit the game~")

    
    else:
        matrix = ["2222222","2222222","2222222","2222222","2222222","2222222","2222222"]
        collection.document(mobile).set({'name': name, 'game_state': matrix, 'stage': 'choose_color', 'color': 0})
        resp.message(f"welcome to the game, {name}\nWhich color would you like to take up to play?\n1: Yellow\n2: Red\n\n\n~or press 9 to exit the game~")



    
    # resp.message(f"aakash bot is happy that you said {msg}")

    return str(resp)

@app.route('/check')
def check():
    collection.document('hello').delete()
    return "hemlo"



@app.route("/message", methods=['POST'])
def message():
    options = ["0","1","2","3","4","5","6"]
    colors = ["red", "yellow"]
    msg = request.form.get('Body')
    mobile = request.form.get('From').split('+')[1]
    name = request.form.get('ProfileName')
    resp = MessagingResponse()
    doc = collection.document(mobile).get()

    if doc.exists:
        info = doc.to_dict()
        # check for exiting
        if msg == "9":
            collection.document(mobile).delete()
            resp.message(f'successfully exited game')
            return str(resp)

        # check stage
        if info['stage']=="choose_color":
            if msg not in ["1","2"]:
                resp.message(f"wrong input, try again lol")
                return str(resp)
            else:
                collection.document(mobile).update({'color':int(msg)-1, 'stage':'gamestarted'})
                resp.message(f"Your color is set to {colors[int(msg)-1]}\n\nEnter 'play' to start playing ✨✨")
                return str(resp)

        if msg == "play":
            matrix = info['game_state']
            # matrix = stringlist_to_listlist(matrix)
            # equivalent = {0: '🔴',1:'🟡',2:'⬛'}

            emojified = emojify(matrix)
            resp.message(f"Your game state is\n\n{emojified}\nEnter the number corresponding to the column you wanna put your color into\n\n\n~or press 9 to exit the game~")
            return str(resp)

        
        if msg in options:
            matrix = info['game_state']
            matrix = stringlist_to_listlist(matrix)
            print(matrix)
            # check if entering is valid
            if matrix[0][int(msg)] != 2:
                resp.message("wrong input, try again lol")
                return str(resp)
            else:
                print("here atleast")
                for x in range(6,-1,-1):
                    if matrix[x][int(msg)]==2:
                        print("dayummmm")
                        matrix[x][int(msg)]=info['color']
                        # check winstatus
                        didplayerwin = winstatus(matrix, info['color'])

                        if didplayerwin:
                            resp.message(f"{emojify(listlist_to_stringlist(matrix))}\n\nwoohoooo!!! damn you won the game, cheers!!")
                            collection.document(mobile).delete()
                            return str(resp)
                        if info['color'] ==1:
                            botclr = 0
                        if info['color']==0:
                            botclr = 1

                        # botEnter
                        newmatrix = botstep(matrix, botclr)
                        
                        didbotwin = winstatusbot(newmatrix, botclr)

# check isbotwinner
                        if didbotwin:
                            resp.message(f"{emojify(newmatrix )}\n\naw damn!! you lost, try again by entering anything")
                            collection.document(mobile).delete()
                            return str(resp) 

                        if not didbotwin:
                            # update to db
                            newmatrix = listlist_to_stringlist(newmatrix)
                            collection.document(mobile).update({'game_state': newmatrix})
                            emojified = emojify(newmatrix)
                            #  play baamzi
                            resp.message(f"Your game state is\n\n{emojified}\nEnter the number corresponding to the column you wanna put your color into\n\n\n~or press 9 to exit the game~")
                            return str(resp)
                           


                        

                        break
                # return response
                resp.message('some error occured')
                return str(resp)
            
        resp.message("wrong input you entered")
        return str(resp)
                    




        
        

        
        
        

        
        
       

    else:
        matrix = ["2222222","2222222","2222222","2222222","2222222","2222222","2222222"]
        collection.document(mobile).set({'name': name, 'game_state': matrix, 'stage': 'choose_color', 'color': 0})
        resp.message(f"welcome to the game, {name} ✨✨\nWhich color would you like to take up to play?\n1: Red\n2: Yellow\n\n\n~or press 9 to exit the game~")
        return str(resp)

        # create doc
        # initialise game
        # send response


if __name__ == "__main__":
    app.run(debug=True)


