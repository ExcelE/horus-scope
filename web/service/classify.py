import __init__

class Classify(Resource):
    def post(self):
        postedData = request.get_json()

        photo = request.files['photo']
        r = photo.save('temp.jpg')
        print("Saved image payload to jpg")
        
        try:
            username = postedData["username"]
            password = postedData["password"]
        except:
            return jsonify({
                "error": "Please supply both username and password",
                "status": 300
                })

        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        tokens = users.find({
            "Username":username
        })[0]["Tokens"]

        if tokens<=0:
            return jsonify(generateReturnDictionary(303, "Not Enough Tokens"))

        retArray = []
        with open('temp.jpg', 'r') as f:
            proc = subprocess.Popen('python3 classify_image.py --model_dir=. --image_file=./temp.jpg', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            ret = proc.communicate()[0]
            proc.wait()
            with open("text.txt") as g:
                loaded = json.load(g)
                keyLinks = []
                for key in loaded:
                    if loaded[key] > 0.001:
                        retArray.append(appendWiki(key, loaded[key]))

        users.update({
            "Username": username
        },{
            "$set":{
                "Tokens": tokens-1
            }
        })

        return jsonify(retArray)