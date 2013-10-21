from collections import defaultdict
from flask.views import View, MethodView
from flask import request, jsonify, abort
from myapp import models
from myapp.models import db
from datetime import datetime
import myapp.utils as utils


def get_admin_user(db):
    return db.session.query(models.Users)\
        .filter(models.Users.name=='admin').first()

def get_nap_starts(db):
    """returns only the NapStarts rows that are not connected to a Nap"""
    return db.session.query(models.NapStarts).filter(models.NapStarts.nap==None).all()


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
    if "time" in request.json:
        inputDict["time"] = datetime.utcnow()
    if "ounces" in request.json:
        inputDict["ounces"] = float(request.json["ounces"])

    return inputDict

##Base View Class (for POSTs and GETs)
class APIView(MethodView):
    """APIView is the base class for all the API views"""
    APIKEY = "monkey patch this value"

    ##GET and POST both
    def get_model_name(self): raise NotImplementedError

    ##POST only
    def get_input_dict(self): raise NotImplementedError
    def create_item(self): raise NotImplementedError

    ##GET only
    def get_items(self): raise NotImplementedError

    def check_api_key(self, key):
        # if key == "mykey":
        if key == self.APIKEY:
            return True
        return False

    def validate_json_request(self, request):
        if not request.json:
            return False
        if not "key" in request.json:
            return False
        return self.check_api_key(request.json["key"])


    def post(self):

        if not self.validate_json_request(request):
            abort(400)
        modelName = self.get_model_name()
        item = self.create_item(self.get_input_dict())
        admin = get_admin_user(db)
        if admin:
            item.user = admin
        db.session.add(item)
        db.session.commit()
        return jsonify( { modelName: "posted!" } )

    def get(self):
        items = self.get_items()
        modelName = self.get_model_name()
        return jsonify( { modelName: items } )


class DirtyDiapersAPIView(APIView):
    """
    curl -i -H "Content-Type: application/json" -X POST -d '{"time":"now","key":"mykey" }' http://localhost:5000/api/v1/dirtydiapers

    """
    def get_items(self): return [t.time for t in models.DirtyDiapers.query.all()]
    def get_model_name(self): return "dirtydiapers"
    def get_input_dict(self): return parse_request_to_create_object(request)
    def create_item(self, inputDict):
        return models.get_or_create(db, models.DirtyDiapers, **inputDict)

class WetDiapersAPIView(APIView):
    """
    curl -i -H "Content-Type: application/json" -X POST -d '{"time":"now","key":"mykey" }' http://localhost:5000/api/v1/wetdiapers

    """
    def get_items(self): return [t.time for t in models.WetDiapers.query.all()]
    def get_model_name(self): return "wetdiapers"
    def get_input_dict(self): return parse_request_to_create_object(request)
    def create_item(self, inputDict):
        return models.get_or_create(db, models.WetDiapers, **inputDict)

class FeedingsAPIView(APIView):
    """
    curl -i -H "Content-Type: application/json" -X POST -d '{"time":"now","key":"mykey", "ounces":"12" }' http://localhost:5000/api/v1/feedings

    """
    def get_items(self): return [t.time for t in models.Feedings.query.all()]
    def get_model_name(self): return "feedings"
    def get_input_dict(self): return parse_request_to_create_object(request)
    def create_item(self, inputDict):
        return models.get_or_create(db, models.Feedings, **inputDict)


class WeighingsAPIView(APIView):
    """
    curl -i -H "Content-Type: application/json" -X POST -d '{"time":"now","key":"mykey", "ounces":"12" }' http://localhost:5000/api/v1/weighings

    """
    def get_items(self): return [t.time for t in models.Weighings.query.all()]
    def get_model_name(self): return "weighings"
    def get_input_dict(self): return parse_request_to_create_object(request)
    def create_item(self, inputDict):
        return models.get_or_create(db, models.Weighings, **inputDict)

class NapStartsAPIView(APIView):
    """
    curl -i -H "Content-Type: application/json" -X POST -d '{"time":"now","key":"mykey"}' http://localhost:5000/api/v1/napstarts

    """
    def get_items(self): return [t.time for t in models.NapStarts.query.all()]
    def get_model_name(self): return "napstarts"
    def get_input_dict(self): return parse_request_to_create_object(request)
    def create_item(self, inputDict):
        return models.get_or_create(db, models.NapStarts, **inputDict)


class WakingsAPIView(APIView):
    """
    curl -i -H "Content-Type: application/json" -X POST -d '{"time":"now","key":"mykey"}' http://localhost:5000/api/v1/wakings

    """


    def get_items(self): return [t.time for t in models.Wakings.query.all()]
    def get_model_name(self): return "wakings"
    def get_input_dict(self): return parse_request_to_create_object(request)
    def create_item(self, inputDict):
        starts = get_nap_starts(db)
        stop = models.Wakings(**inputDict)
        matchedStart = utils.match_waking_with_napstart(starts, stop)
        if matchedStart:
            db.session.add(stop)
            db.session.commit()
            nap = models.get_or_create(db, models.Naps, start=matchedStart, end=stop)
            return nap
        return stop





