from tests import client
from tests.test_user import login, register


def get_header(client):
    rv = login(client, "admin", "12345")
    data = rv.get_json()
    token = data["access_token"]
    return {"Authorization": f"Bearer {token}"}


def add_item(client):
    headers = get_header(client)
    return client.post("/items", headers=headers, json={
        "name": "book",
        "price": 20.0,
        "category": "stationary"
    })


def test_item_list_no_para_success(client):
    """Make sure getting an item list with no condition works"""
    rv = client.get("/items")
    data = rv.get_json()
    assert data["items"] == []
    add_item(client)
    rv = client.get("/items")
    data = rv.get_json()
    assert data["items"] != []
    assert data["prev_page"] is False
    assert data["next_page"] is False


def test_item_list_with_name_success(client):
    """Make sure getting an item list according to name works"""
    add_item(client)
    rv = client.get("/items?name=book")
    data = rv.get_json()
    assert data["items"][0]["name"] == "book"


def test_item_list_with_name_failure(client):
    """Make sure getting an item list doesn't work with a new name"""
    add_item(client)
    rv = client.get("/items?name=pen")
    data = rv.get_json()
    assert data["items"] == []


def test_pagination_success(client):
    """Make sure getting an item list with custom pagination works"""
    add_item(client)
    add_item(client)
    rv = client.get("/items?page=1")
    data = rv.get_json()
    assert data["items"][0]["name"] == "book"

    rv = client.get("/items?page=213&name=book")
    data = rv.get_json()
    assert data["items"][0]["name"] == "book"

    rv = client.get("/items?page=1&name=book&per_page=1")
    data = rv.get_json()
    assert data["next_page"] is True
    assert data["prev_page"] is False

    rv = client.get("/items?page=2&name=book&per_page=1")
    data = rv.get_json()
    assert data["prev_page"] is True
    assert data["next_page"] is False


def test_pagination_page_not_positive_failure(client):
    """Make sure pagination only works with a positive page number"""
    add_item(client)
    rv = client.get("/items?page=0")
    assert b"The page number has to be positive." in rv.data


def test_pagination_per_page_not_positive_failure(client):
    """Make sure pagination only works with a positive number of items per page"""
    add_item(client)
    rv = client.get("/items?page=1&per_page=-1")
    assert b"The number of items per page has to be positive." in rv.data


def test_pagination_query_string_typo_failure(client):
    """Make sure getting an item list validates parameters on query string"""
    add_item(client)
    rv = client.get("/items?page=1name=book")
    assert b"Not a valid integer." in rv.data


def test_add_item_success(client):
    """Make sure adding an item works"""
    rv = add_item(client)
    info = rv.get_json()
    assert info["name"] == "book"


def test_add_item_invalid_info_failure(client):
    """Make sure adding an item validates parameters on body"""
    headers = get_header(client)
    rv = client.post("/items", headers=headers, json={
        "name": "book",
        "price": "abc",
        "category": "stationary"
    })
    assert b"Not a valid number." in rv.data


def test_item_detail_success(client):
    """Make sure getting an item works """
    headers = get_header(client)
    id = add_item(client).get_json()["id"]
    rv = client.get(f"/items/{id}", headers=headers)
    info = rv.get_json()
    assert info["name"] == "book"


def test_item_detail_no_item_failure(client):
    """Make sure getting an item only works with existing items"""
    headers = get_header(client)
    id = add_item(client).get_json()["id"]
    rv = client.get(f"/items/{id + 1}", headers=headers)
    info = rv.get_json()
    assert info["msg"] == "Item not found!"


def test_edit_item_success(client):
    """Make sure editing an item works"""
    headers = get_header(client)
    id = add_item(client).get_json()["id"]
    rv = client.put(f"/items/{id}", headers=headers, json={
        "name": "book",
        "price": 19,
        "category": "stationary"
    })
    info = rv.get_json()
    assert info["msg"] == "Item updated!"

    rv = client.get(f"/items/{id}", headers=headers)
    info = rv.get_json()
    assert info["price"] == 19.0


def test_edit_item_no_item_failure(client):
    """Make sure editing an item only works with existing items"""
    headers = get_header(client)
    id = add_item(client).get_json()["id"]
    rv = client.put(f"/items/{id + 1}", headers=headers, json={
        "name": "book",
        "price": 19,
        "category": "stationary"
    })
    info = rv.get_json()
    assert info["msg"] == "Item not found!"


def test_edit_item_invalid_info_failure(client):
    """Make sure editing an item only works with existing items"""
    headers = get_header(client)
    id = add_item(client).get_json()["id"]
    rv = client.put(f"/items/{id}", headers=headers, json={
        "name": "book",
        "category": "stationary"
    })
    print(rv.data)
    assert b"'Missing data for required field." in rv.data


def test_delete_item_success(client):
    """Make sure deleting an item works"""
    headers = get_header(client)
    id = add_item(client).get_json()["id"]
    rv = client.delete(f"/items/{id}", headers=headers)
    info = rv.get_json()
    assert info["msg"] == "Item deleted!"


def test_delete_item_no_privilege_failure(client):
    """Make sure deleting an item needs authorization"""
    register(client, "tester", "password")
    rv = login(client, "tester", "password")
    data = rv.get_json()
    new_token = data["access_token"]
    headers = {"Authorization": f"Bearer {new_token}"}
    id = add_item(client).get_json()["id"]
    rv = client.delete(f"/items/{id}", headers=headers)
    info = rv.get_json()
    assert info["msg"] == "You need to be the owner!"
