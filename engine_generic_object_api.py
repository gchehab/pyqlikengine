import json


class EngineGenericObjectApi:

    def __init__(self, socket):
        self.engine_socket = socket

    def get_layout(self, handle):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetLayout", "params": []})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def get_properties(self, handle):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetProperties", "params": []})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def get_hypercube_data(self, handle, path="/qHyperCubeDef", pages=[]):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetHyperCubeData",
                          "params": [path,pages]})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def get_hypercube_pivot_data(self, handle, path="/qHyperCubeDef", pages=[]):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetHyperCubePivotData",
                          "params": [path,pages]})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def get_list_object_data(self, handle, path="/qListObjectDef", pages=[]):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "GetListObjectData",
                          "params": [path, pages]})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]

    def expand_left(self, handle, path="/qHyperCubeDef", row=0, col=0, all=True):
        msg = json.dumps({"jsonrpc": "2.0", "id": 0, "handle": handle, "method": "ExpandLeft",
                          "params": [path, row, col, all]})
        response = json.loads(self.engine_socket.send_call(self.engine_socket, msg))
        try:
            return response["result"]
        except KeyError:
            return response["error"]