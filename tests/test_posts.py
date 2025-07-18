from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)

def unauthorized_user_get_all_posts(client):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostResponseWithVotes(**res.json())
    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/999999")
    assert res.status_code == 404
    assert res.json().get("detail") == "Post with id '999999' not found."


@pytest.mark.parametrize("title, content, published", [
    ("New Post Title", "Content of the new post", True),
    ("Another Post", "Content for another post", False),
    ("Third Post", "Content of the third post", True)])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    print(f"CREATED POST{res.json()}")
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner.id == test_user['id']


def test_create_post_default_published(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "Default Published Post", "content": "Content of the default published post"})
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "Default Published Post"
    assert created_post.content == "Content of the default published post"
    assert created_post.published is True

def test_unauthorized_user_create_post(client):
    res = client.post("/posts/", json={"title": "Unauthorized Post", "content": "Content of the unauthorized post"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401 

def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_posts):
    res = authorized_client.delete("/posts/999999")
    assert res.status_code == 404
    assert res.json().get("detail") == "Post with id '999999' not found."

def test_delete_other_user_post(authorized_client, test_posts, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
    assert res.json().get("detail") == "Not authorized to delete this post."

def test_update_full_post(authorized_client, test_posts, test_user):
    updated_data = {
        "title": "Updated Title",
        "content": "Updated content",
        "published": False
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=updated_data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == updated_data['title']
    assert updated_post.content == updated_data['content']
    assert updated_post.published is False

def test_update_full_other_user_post(authorized_client, test_posts, test_user2):
    updated_data = {
        "title": "Updated Title",
        "content": "Updated content",
        "published": False
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=updated_data)
    assert res.status_code == 403
    assert res.json().get("detail") == "Not authorized to update this post."

def test_unauthorized_user_update_full_post(client, test_posts):
    updated_data = {
        "title": "Unauthorized Update",
        "content": "Content of the unauthorized update"
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=updated_data)
    assert res.status_code == 401

def test_update_full_post_not_exist(authorized_client, test_posts):
    updated_data = {
        "title": "Non-existent Post",
        "content": "Content of the non-existent post"
    }
    res = authorized_client.put("/posts/999999", json=updated_data)
    assert res.status_code == 404
    assert res.json().get("detail") == "Post with id '999999' not found."

def test_update_partial_post(authorized_client, test_posts):
    updated_data = {
        "title": "Partially Updated Title"
    }
    res = authorized_client.patch(f"/posts/{test_posts[0].id}", json=updated_data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == updated_data['title']
    assert updated_post.content == test_posts[0].content
    assert updated_post.published is True

def test_update_partial_other_user_post(authorized_client, test_posts, test_user2):
    updated_data = {
        "title": "Partially Updated Title"
    }
    res = authorized_client.patch(f"/posts/{test_posts[3].id}", json=updated_data)
    assert res.status_code == 403
    assert res.json().get("detail") == "Not authorized to update this post."

def test_unauthorized_user_update_partial_post(client, test_posts):
    updated_data = {
        "title": "Unauthorized Partial Update"
    }
    res = client.patch(f"/posts/{test_posts[0].id}", json=updated_data)
    assert res.status_code == 401

def test_update_partial_post_not_exist(authorized_client, test_posts):
    updated_data = {
        "title": "Non-existent Post Partial Update"
    }
    res = authorized_client.patch("/posts/999999", json=updated_data)
    assert res.status_code == 404
    assert res.json().get("detail") == "Post with id '999999' not found."