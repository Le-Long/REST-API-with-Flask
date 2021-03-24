from tests import client


def login(client, username, password):
    return client.post("/login", json=dict(
        username=username,
        password=password
    ))


def logout(client, headers):
    return client.post("/logout", headers=headers)


def register(client, username, password):
    return client.post("/register", json=dict(
        username=username,
        password=password
    ))


def test_login_success(client):
    """Make sure login works"""
    rv = login(client, "admin", "Passw0rd")
    data = rv.get_json()
    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    rv = logout(client, headers)
    assert b"Successfully logged out!" in rv.data


def test_login_no_account_failure(client):
    """Make sure login only works with existing account"""
    rv = login(client, "wrongname", "Passw0rd")
    assert b"Please register first!" in rv.data


def test_logout_success(client):
    """Make sure logout works"""
    rv = login(client, "admin", "Passw0rd")
    data = rv.get_json()
    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    logout(client, headers)

    rv = client.post("/items", headers=headers, json={
        "name": "book",
        "price": 20.0,
        "category": "stationary"
    })
    assert b"You has already logged out!" in rv.data


def test_logout_not_yet_log_in_failure(client):
    """Make sure user who logout need to login first"""
    rv = client.post("/logout")
    assert b"You need to log in first!" in rv.data


def test_signup_success(client):
    """Make sure register works"""
    rv = register(client, "tester", "Passw0rd")
    assert b"User created successfully." in rv.data


def test_signup_username_exists_failure(client):
    """Make sure register only works with new username"""
    register(client, "tester", "Passw0rd")
    rv = register(client, "tester", "12345Hn")
    assert b"An user with that username already exists" in rv.data


def test_signup_info_not_fill_failure(client):
    """Make sure register can't create an user without username or password"""
    rv = register(client, "", "12345Hn")
    assert b"Length must be between 1 and 20." in rv.data

    rv = register(client, "tester", "")
    assert b"Length must be between 5 and 20." in rv.data
