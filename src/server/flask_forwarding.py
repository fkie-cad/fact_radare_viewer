from flask import Flask
from flask_restful import Api

from scheduler.start_radare import RadareRunner
from server.endpoint import Retrieve


APP = Flask(__name__)
API = Api(APP)
RUNNER = RadareRunner()

API.add_resource(Retrieve, '/v1/retrieve', methods=['POST'], resource_class_kwargs={'runner': RUNNER})
