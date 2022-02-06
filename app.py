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
    return "api root"


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
                            resp.message(f"{emojify(listlist_to_stringlist(matrix))}\n\nwoohoooo!!! damn you won the game, cheers 🍻 ")
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
                # return default response
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


