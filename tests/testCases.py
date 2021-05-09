import requests
from jsonschema import validate
import json

url = "http://127.0.0.1:8000/actors"
actorId = 9999

schemaResponse = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "response": {
      "type": "string"
    }
  },
  "required": [
    "response"
  ]
}

schemaGet = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "array",
  "items": [
    {
      "type": "object",
      "properties": {
        "actor_id": {
          "type": "integer"
        },
        "first_name": {
          "type": "string"
        },
        "last_name": {
          "type": "string"
        },
        "last_update": {
          "type": "string"
        }
      },
      "required": [
        "actor_id",
        "first_name",
        "last_name",
        "last_update"
      ]
    }
  ]
}

# Test POST (INSERT) for actors table
def test_addActor():
    requestData = {
                    "actor_id": actorId,
                    "first_name": "Add",
                    "last_name": "Actor"
                  }
    r = requests.post(url, data=json.dumps(requestData))
    assert r.status_code == 200
    assert r.headers["Content-Type"] == "application/json"

    rBody = r.json()
    validate(instance=rBody, schema=schemaResponse)

# Test GET for actors table
def test_getActorById():
    r = requests.get(url + "/" + str(actorId))
    assert r.status_code == 200
    assert r.headers["Content-Type"] == "application/json"

    rBody = r.json()
    # If the actor does not exist it will fail the test
    validate(instance=rBody, schema=schemaGet)

# Test PUT (UPDATE) for actors table
def test_updateActor():
    requestData = {
                    "first_name": "Ales12233",
                    "last_name": "Nabernik"
                  }
    r = requests.put(url + "/" + str(actorId), data=json.dumps(requestData))
    assert r.status_code == 200
    assert r.headers["Content-Type"] == "application/json"

    rBody = r.json()
    validate(instance=rBody, schema=schemaResponse)

# Test DELETE for actors table
def test_delActor():
    r = requests.delete(url + "/" + str(actorId))

    assert r.status_code == 200
    assert r.headers["Content-Type"] == "application/json"

    rBody = r.json()
    validate(instance=rBody, schema=schemaResponse)
