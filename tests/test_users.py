from .database import session, client
from jose import jwt
from app.config import settings
from app import schemas
import pytest

# def test_root(client):
#     res = client.get("/")
#     assert res.json().get("greetings") == "Hello, Bro!!"
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "mishok123@gmail.com", "password": "nba2k25"})

    new_user = schemas.UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.email == "mishok123@gmail.com"

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code, detail", [
    ("wrongemail@gmail.com", "nba2k25", 403, "Invalid Username"),
    ("mishok123@gmail.com", "wrong_password", 403, "Invalid Password"),
    ("wrongemail123@gmail.com", "wrong_password", 403, "Invalid Username"),
    (None, "nba2k25", 403, "Invalid Username"),
    ("mishok123@gmail.com", None, 403, "Invalid Password")])
def test_incorrect_login(client, test_user, email, password, status_code, detail):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    assert res.json().get("detail") == detail