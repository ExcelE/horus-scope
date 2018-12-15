from .auth.common import *
from .engine.label_image import engine
from time import gmtime, strftime
import os

def stop(self):
    self.is_alive = False
    self.process.join()

INCEPTION = {
    "input": "Placeholder",
    "output": "final_result",
    "graph": "model/engine/inceptionv3_cars_graph.pb",
    "labels": "model/engine/inceptionv3_cars_labels.txt",
    "width": 299,
    "height": 299
}

MOBILENET = {
    "input": "Placeholder",
    "output": "final_result",
    "graph": "model/engine/mobinet_cars_graph.pb",
    "labels": "model/engine/mobinet_cars_labels.txt",
    "width": 224,
    "height": 224
}

class Classify(Resource):
    @jwt_required
    def post(self):
        print("posted", file=sys.stderr)
        username = get_jwt_identity()

        photo = request.files['photo']
        
        r = photo.save('temp.jpg')

        tokens = users.find({
            "Username":username
        })[0]["Tokens"]

        if tokens<=0:
            return generateReturnDictionary(303, "Not Enough Tokens"), 303

        retArray = []
        
        photoLoc = "temp.jpg"
        graphLoc = os.path.join(os.getcwd(), MOBILENET["graph"])
        labelLoc = os.path.join(os.getcwd(), MOBILENET["labels"])

        predictions = engine(photoLoc, graphLoc, labelLoc, 
                            MOBILENET["input"], MOBILENET["output"],
                            MOBILENET["height"], MOBILENET["width"])

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

        response = jsonify(retArray)
        response.status_code = 200

        return response
