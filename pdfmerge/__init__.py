from flask import Flask, render_template
from flask_restful import Api

from pdfmerge.resources.merge import MergeResource

import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/pid')
def pid():
    print(os.getpid(), flush=True)
    return ""


api = Api(app)
api.add_resource(MergeResource, '/merge')
