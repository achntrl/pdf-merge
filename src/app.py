from flask import Flask
from flask_restful import Api

from resources.merge import MergeResource


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


api = Api(app)
api.add_resource(MergeResource, '/merge')

# Default port:
if __name__ == '__main__':
    app.run()
