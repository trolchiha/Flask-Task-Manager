import requests
import uuid
from . import ENDPOINT


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def create_user(payload):
    return requests.post(ENDPOINT + "/api/users", json=payload)

def update_user(user_id, payload):
    return requests.put(ENDPOINT + f"/api/user/{user_id}", json=payload)

def read_user(user_id):
    return requests.get(ENDPOINT + f"/api/user/{user_id}")

def delete_user(user_id):
    return requests.delete(ENDPOINT + f"/api/user/{user_id}")

def list_users():
    return requests.get(ENDPOINT + f"/api/users")

def new_user_payload():
    username = f"user_{uuid.uuid4().hex}"
    password = uuid.uuid4().hex
    return {
        "username": username,
        "password": password,
    }

def test_can_create_user():
    # create new user
    payload = new_user_payload()
    response = create_user(payload)
    assert response.status_code == 200

    # check if user was created by user id
    user_id = response.json()["id"]
    read_user_response = read_user(user_id)
    assert read_user_response.status_code == 200

    # check the data 
    read_user_data = read_user_response.json()
    assert read_user_data["username"] == payload["username"]
    assert read_user_data["password"] == payload["password"]
    
