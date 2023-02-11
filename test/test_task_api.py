from . import *
from .test_user_api import *

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def create_task(payload):
    return requests.post(ENDPOINT + "/api/tasks", json=payload)

def update_task(task_id, payload):
    return requests.put(ENDPOINT + f"/api/task/{task_id}", json=payload)

def read_task(task_id):
    return requests.get(ENDPOINT + f"/api/task/{task_id}")

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/api/task/{task_id}")

def list_tasks():
    return requests.get(ENDPOINT + f"/api/tasks")

def new_task_payload():

    # create new user
    user_payload = new_user_payload()
    response = create_user(user_payload)
    user_id = response.json()["id"]

    data = f"some data {uuid.uuid4().hex}"

    return {
        "data": data,
        "status": False,
        "user_id": user_id,
    }


def test_can_create_task():
    # create new task
    payload = new_task_payload()
    response = create_task(payload)
    assert response.status_code == 200
    
    # check if task was created by task id
    task_id = response.json()["id"]
    read_task_response = read_task(task_id)
    assert read_task_response.status_code == 200

    # validate the data 
    read_task_data = read_task_response.json()
    assert read_task_data["data"] == payload["data"]
    assert read_task_data["status"] == payload["status"]
    assert read_task_data["user_id"] == payload["user_id"]

    
def test_can_update_task():
    # create new task
    payload = new_task_payload()
    response = create_task(payload)
    assert response.status_code == 200
    user_id = response.json()["id"]

    # update the task
    new_payload = new_task_payload()
    update_task_response = update_task(user_id, new_payload)
    assert update_task_response.status_code == 200

    # validate changes
    update_task_data = update_task_response.json()
    assert update_task_data["data"] == new_payload["data"]
    assert update_task_data["status"] == new_payload["status"]
    assert update_task_data["user_id"] == new_payload["user_id"]

    
def test_can_delete_task():
    # create task
    payload = new_task_payload()
    response = create_task(payload)
    assert response.status_code == 200
    task_id = response.json()["id"]

    # delete the task
    delete_task_response = delete_user(task_id)
    assert delete_task_response.status_code == 200
    
    # get the task and check that it's not found
    read_task_response = read_user(task_id)
    assert read_task_response.status_code == 404
    