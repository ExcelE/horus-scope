from model.auth.register import Register
from model.auth.login import Login
from model.auth.logout import Logout
from model.auth.refill import Refill
from model.classify import Classify
from model.auth.common import *

# Do not use in Production
app.secret_key = 'A0Zr98j/@9as@g89a!(82asdR~XHH!jmN]LWX/,?RT'

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(Register, '/register')
api.add_resource(Classify, '/classify')
api.add_resource(Refill, '/refill')

if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
