from flask import request
from flask_restful import Resource

from config import ROUTE_PORT_MAPPING
from scheduler.start_radare import OutOfPortsError


def extract_binary_from_request(input_request):
    data = input_request.data
    return data


class Retrieve(Resource):
    def __init__(self, runner):
        self._runner = runner

    def post(self):
        binary = extract_binary_from_request(request)

        try:
            port = self._runner.pseudo_start(binary)
        except OutOfPortsError as out_of_ports_error:
            return dict(error_message=str(out_of_ports_error)), 503
        except Exception as exception:
            return dict(error_message=str(exception)), 500

        return dict(endpoint=ROUTE_PORT_MAPPING[port]), 200
