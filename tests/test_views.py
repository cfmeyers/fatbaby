import sys, unittest, json
sys.path.append("../")

from tests import TestCase
from myapp import models
from myapp.models import db, Things

API_V1              = "/api/v1/"
JSON_HEADERS = {'Content-type': 'application/json'}

def helper_add_item_to_db(db, model, **kwargs):
    item = models.get_or_create(db, model, **kwargs)
    db.session.add(item)
    db.session.commit()

def get_endpoint(resourceName, fully_qualified=False):
    return API_V1+resourceName.lower()

def table_is_empty(client, url, resourceName):
    response = client.get(url)
    return not response.json[resourceName.lower()]

def verify_my_item_in_db(modelName, client):
        model    = eval(modelName)
        resource = modelName.lower()
        url      = get_endpoint(resource)

        #verify no things in the db via the API
        response = client.get(url)
        assert table_is_empty(client, url, resource)

        #add a thing manually to the db
        helper_add_item_to_db(db, model, **{"name":"my item"})
        response2 = client.get(url)

        #verify there is a thing in the db via the API
        return response2.json[resource][0] == "my item"


class TestThingsAPIView(TestCase):

    def test_GET_Things_API(self):
        assert verify_my_item_in_db("Things", self.client)

    def test_POST_Things_API(self):
        url = get_endpoint("things")
        postData = json.dumps({'name':'my item'})
        data = {'name':'my item'}
        response = self.client.post(url, data=postData, headers=JSON_HEADERS)

        assert not table_is_empty(self.client, url, "things")










