from .auth.common import *
from .engine.label_image import engine
from time import gmtime, strftime
import os, base64
from PIL import Image

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
        username = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('photo', required=True, help="Needs to end in jpg or jpeg. Or check that there's no offending character(s) in your filename", location=['files', 'form', 'json'])
        args = parser.parse_args()

        photo = request.files['photo']

        print(allowed_file(photo.filename), file=sys.stderr)
        print(secure_filename(photo.filename), file=sys.stderr)

        if photo and allowed_file(photo.filename):
            checkDir(os.path.join('uploads', username))
            filename = secure_filename(photo.filename)
            photoDir = username + "/" + filename
            photoLoc = os.path.join(app.config['UPLOAD_FOLDER'], photoDir)
            photo.save(photoLoc)
        else:
            return {"msg": "Needs to end in jpg or jpeg. Or check that there's no offending character(s) in your filename"}, 400

        tokens = getToken(username)

        if (tokens <= 0):
            return generateReturnDictionary(303, "Not Enough Tokens"), 303
        
        retArray = []
        
        graphLoc = os.path.join(os.getcwd(), MOBILENET["graph"])
        labelLoc = os.path.join(os.getcwd(), MOBILENET["labels"])

        photoLocation = os.path.join("uploads", photoDir)

        predictions = engine(photoLocation, graphLoc, labelLoc, 
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

        with Image.open(photoLoc) as img:
            width, height = img.size
            
        size = (os.path.getsize(photoLoc) >> 10)

        newId = predictions_db.insert({
            "Username": username,
            "image": {
                "url": photoLocation,
                "height": height,
                "width": width,
                "size": size
            },
            "predictions": retArray,
            "dateCreated": datetime.utcnow()
        })

        retJson = {}

        retJson['image'] = {
                "url": photoLocation,
                "height": height,
                "width": width,
                "size": size
            }
            
        retJson['predictions'] = retArray
        retJson['id'] = str(newId)

        response = jsonify(retJson)
        response.status_code = 200

        return response
