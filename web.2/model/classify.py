from .auth.common import *
from .engine.label_image import engine
from time import gmtime, strftime
import os

def stop(self):
    self.is_alive = False
    self.process.join()

class Classify(Resource):
    def post(self):
        #postedData = request.get_json()
        if 'username' in session:
            photo = request.files['photo']
            r = photo.save('temp.jpg')

            username = escape(session['username'])

            tokens = users.find({
                "Username":username
            })[0]["Tokens"]

            if tokens<=0:
                return generateReturnDictionary(303, "Not Enough Tokens"), 303

            retArray = []
            
            photoLoc = "temp.jpg"
            graphLoc = os.path.join(os.getcwd(),"model/engine/retrained_graph.pb")
            labelLoc = os.path.join(os.getcwd(),"model/engine/retrained_labels.txt")

            predictions = engine(photoLoc, graphLoc, labelLoc)

            for key in predictions:
                if predictions[key] > 0.001:
                    retArray.append(appendWiki(key, predictions[key]))

            users.update({
                "Username": username
            },{
                "$set":{
                    "Tokens": tokens-1, 
                }
            })

            return retArray, 200

        else:
            return generateReturnDictionary(300, "Please log in first!"), 300