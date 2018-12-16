from .common import *
from flask_restful import reqparse
from bson import ObjectId, objectid

class Delete(Resource):
    @jwt_required
    def post(self):
        username = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True, help='The parameter id needs to be present!', location=['args', 'form', 'json'])
        args = parser.parse_args()

        idToRemove = str(args['id'])

        if (objectid.ObjectId.is_valid(idToRemove)):
            if (predictions_db.find({ "_id": ObjectId(idToRemove) }).count() > 0):
                predictions_db.remove(
                    { "_id": ObjectId(idToRemove) }
                )   
                return {"msg": "Removal success!"}, 200 

        return {"msg": "Removal failed. Item doesn't exist."}, 400