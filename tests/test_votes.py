import pytest
from app import models
from app import schemas

@pytest.fixture()
def test_vote(test_posts, test_user, session):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(f"/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 201

def test_vote_twice_on_post(authorized_client, test_posts, test_vote, test_user):
    res = authorized_client.post(f"/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409
    assert res.json().get("detail") == f"{test_user['email']} has already voted on post with id {test_posts[3].id}"

def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(f"/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201
    assert res.json().get("message") == "Vote deleted successfully"

def test_delete_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post(f"/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404
    assert res.json().get("detail") == "Vote not found"

def test_vote_post_non_exist(authorized_client):
    res = authorized_client.post("/vote/", json={"post_id": 999999, "dir": 1})
    assert res.status_code == 404
    assert res.json().get("detail") == "Post with id '999999' not found."

def test_vote_unauthorized_user(client, test_posts):
    res = client.post(f"/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 401