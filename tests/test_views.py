import sys, unittest, json
sys.path.append("../")

from tests import TestCase, add_item_to_db
from myapp import models
from myapp.models import db, Things

PATH              = "/api/v1/"
JSON_HEADERS = {'Content-type': 'application/json'}

def get_response(client, resource, postData, headers):
    url = get_endpoint(resource)
    postJSON = json.dumps(postData)
    return client.post(url, data=postJSON, headers=headers)

def get_endpoint(resourceName, fully_qualified=False):
    return PATH+resourceName.lower()

def table_is_empty(client, resourceName):
    url = get_endpoint(resourceName)
    response = client.get(url)
    return not response.json[resourceName.lower()]

def verify_my_item_in_db(modelName, client):
        model    = eval(modelName)
        resource = modelName.lower()
        url      = get_endpoint(resource)

        #verify no things in the db via the API
        response = client.get(url)
        assert table_is_empty(client, resource)

        #add a thing manually to the db
        add_item_to_db(db, model, **{"name":"my item"})
        response2 = client.get(url)

        #verify there is a thing in the db via the API
        return response2.json[resource][0] == "my item"


class TestDirtyDiapersAPIView(TestCase):

    def test_POST_DirtyDiapers_API(self):
        url = get_endpoint("dirtydiapers")
        postData = json.dumps({'time':'now', 'key':'mykey'})
        response = self.client.post(url, data=postData, headers=JSON_HEADERS)

        assert not table_is_empty(self.client, "dirtydiapers")

def post_resource(client, resource, data={'time':'now', 'key':'mykey'}):
        get_response(client, resource, data, JSON_HEADERS)

class TestPOSTAPIViews(TestCase):

    def test_POST_WetDiapers_API(self):
        resource, data = "wetdiapers", {'time':'now', 'key':'mykey'}
        get_response(self.client, resource, data, JSON_HEADERS)
        assert not table_is_empty(self.client, resource)

    def test_POST_DirtyDiapers_API(self):
        resource, data = "dirtydiapers", {'time':'now', 'key':'mykey'}
        get_response(self.client, resource, data, JSON_HEADERS)
        assert not table_is_empty(self.client, resource)

    def test_POST_Weighings_API(self):
        resource, data = "weighings", {'time':'now', 'key':'mykey', 'ounces':'99'}
        get_response(self.client, resource, data, JSON_HEADERS)
        assert not table_is_empty(self.client, resource)

    def test_POST_Feedings_API(self):
        resource, data = "feedings", {'time':'now', 'key':'mykey', 'ounces':'12'}
        get_response(self.client, resource, data, JSON_HEADERS)
        assert not table_is_empty(self.client, resource)

    def test_POST_NapStarts_API(self):
        resource, data = "napstarts", {'time':'now', 'key':'mykey'}
        get_response(self.client, resource, data, JSON_HEADERS)
        assert not table_is_empty(self.client, resource)

    def test_POST_Wakings_API(self):
        resource, data = "wakings", {'time':'now', 'key':'mykey'}
        get_response(self.client, resource, data, JSON_HEADERS)
        assert not table_is_empty(self.client, resource)


class TestNapCreation(TestCase):
    pass













