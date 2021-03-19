from tests import client
from tests.test_user import login, register


def get_header(client):
    rv = login(client, 'admin', '12345')
    data = rv.get_json()
    token = data["access_token"]
    return {"Authorization": f"Bearer {token}"}


def add_item(client):
    headers = get_header(client)
    return client.post('/items', headers=headers, json={
        "name": "book",
        "price": 20.0,
        "category": "stationary"
    })


def test_items(client):
    """ Make sure getting all items works """
    rv = add_item(client)
    info = rv.get_json()
    assert info["name"] == "book"

    rv = client.get('/items')
    data = rv.get_json()
    assert data["items"] != []

    rv = client.get('/items?prefix=pen')
    data = rv.get_json()
    assert data["items"] == []


def test_add_item_success(client):
    """ Make sure adding an item works """
    rv = add_item(client)
    info = rv.get_json()
    assert info["name"] == "book"


def test_add_item_failure(client):
    """ Make sure adding an item validates information """
    headers = get_header(client)
    rv = client.post('/items', headers=headers, json={
        "name": "book",
        "price": "abc",
        "category": "stationary"
    })
    assert b'Not a valid number' in rv.data


def test_item_detail(client):
    """ Make sure getting an item only works with existing items"""
    headers = get_header(client)
    id = add_item(client).get_json()["id"]
    rv = client.get(f'/items/{id}', headers=headers)
    info = rv.get_json()
    assert info["name"] == "book"

    rv = client.get(f'/items/{id + 1}', headers=headers)
    info = rv.get_json()
    assert info["msg"] == "Item not found!"


def test_edit_item_success(client):
    """ Make sure editing an item works """
    headers = get_header(client)
    id = add_item(client).get_json()["id"]
    rv = client.put(f'/items/{id}', headers=headers, json={
        "name": "book",
        "price": 19,
        "category": "stationary"
    })
    info = rv.get_json()
    assert info["msg"] == "Item updated!"

    rv = client.get(f'/items/{id}', headers=headers)
    info = rv.get_json()
    assert info["price"] == 19.0


def test_delete_item_failure(client):
    """ Make sure deleting an item needs authorization """
    register(client, 'tester', 'password')
    rv = login(client, 'tester', 'password')
    data = rv.get_json()
    new_token = data["access_token"]
    headers = {"Authorization": f"Bearer {new_token}"}
    id = add_item(client).get_json()["id"]
    rv = client.delete(f'/items/{id}', headers=headers)
    info = rv.get_json()
    assert info["msg"] == 'You need to be the owner!'


def test_delete_item_success(client):
    """ Make sure deleting an item works """
    headers = get_header(client)
    id = add_item(client).get_json()["id"]
    rv = client.delete(f'/items/{id}', headers=headers)
    info = rv.get_json()
    assert info["msg"] == 'Item deleted!'


def test_edit_item_failure(client):
    """ Make sure editing an item only works with existing items """
    headers = get_header(client)
    id = add_item(client).get_json()["id"]
    rv = client.put(f'/items/{id + 1}', headers=headers, json={
        "name": "book",
        "price": 19,
        "category": "stationary"
    })
    info = rv.get_json()
    assert info["msg"] == "Item not found!"
