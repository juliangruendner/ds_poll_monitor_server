from flask import Flask
from flask_restful_swagger_2 import Api
from resources.userResource import UserListResource, UserResource, UserLoginResource
from resources import exampleResource
from resources import controlResource
from flask_cors import CORS
from rdb.rdb import connect_to_db, create_all, create_admin_user
import json
import logging
import logging.config
logging.config.dictConfig(json.load(open("logging_config.json", "r")))


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app,
          add_api_spec_resource=True, api_version='0.0', api_spec_url='/api/swagger', schemes=["http"],  #, "https", {"securitySchemes": {"basicAuth": {"type": "http"}}}],
          security=[{"basicAuth": []}], security_definitions={"basicAuth": {"type": "basic"}})  # Wrap the Api and add /api/swagger endpoint


connect_to_db(app)
# create_all()   //comment in to create all tables for models on startup
# create_admin_user()  //creates admin user

api.add_resource(UserListResource, '/users', endpoint='users')
api.add_resource(UserLoginResource, '/users/login', endpoint='user_login')
api.add_resource(UserResource, '/users/<int:user_id>', endpoint='user')
api.add_resource(exampleResource.ExampleList, '/example', endpoint='examples')
api.add_resource(exampleResource.Example, '/example/<int:example_id>', endpoint='example')
api.add_resource(controlResource.ControlList, '/control', endpoint='control')

if __name__ == '__main__':
    # set false in production mode
    app.run(debug=True, host='0.0.0.0', port=5000)


