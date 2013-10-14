from collections import defaultdict
from flask.views import View, MethodView
from flask import request, jsonify, abort
from myapp import models
from myapp.models import db

def parse_request_to_create_object(request):
    """ given a json request object, return a default dict formatted to create objects
        Args: request:json object
        Returns: default dict with boolean default
    """

    inputDict              = defaultdict(bool)
    if "name" in request.json:
        inputDict["name"] = request.json["name"]
    if "tags" in request.json:
        inputDict["tags"] = request.json["tags"]
    if "project" in request.json:
        inputDict["project"] = request.json["project"]
    if "project" in request.json:
        inputDict["key"] = request.json["key"]

    return inputDict

##Base View Class (for POSTs and GETs)
class APIView(MethodView):
    """APIView is the base class for all the API views"""

    ##GET and POST both
    def get_model_name(self): raise NotImplementedError

    ##POST only
    def get_input_dict(self): raise NotImplementedError
    def create_item(self): raise NotImplementedError

    ##GET only
    def get_items(self): raise NotImplementedError

    def check_api_key(self, key):
        if key == "mykey":
            return True
        return False

    def validate_json_request(self, request):
        if not request.json:
            return False
        if not "name" in request.json:
            return False
        if not "key" in request.json:
            return False
        return self.check_api_key(request.json["key"])


    def post(self):
        if not self.validate_json_request(request):
            abort(400)
        modelName = self.get_model_name()
        item = self.create_item(self.get_input_dict())
        db.session.add(item)
        db.session.commit()
        return jsonify( { modelName: item.name } )

    def get(self):
        items = self.get_items()
        modelName = self.get_model_name()
        return jsonify( { modelName: items } )

class ThingsAPIView(APIView):
    """
    curl -i -H "Content-Type: application/json" -X POST -d '{"name":"pizza","key":"mykey" }' http://localhost:5000/api/v1/things
    """

    ##GET and POST both
    def get_model_name(self): return "things"


    ##POST only
    def get_input_dict(self):
        return parse_request_to_create_object(request)

    def create_item(self, inputDict):
        return models.get_or_create(db, models.Things, **inputDict)


    ##GET only
    def get_items(self): return [t.name for t in models.Things.query.all()]





