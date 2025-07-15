from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func, select

router = APIRouter(prefix = "/posts", tags=["Posts"])

@router.get("/", response_model=list[schemas.PostResponseWithVotes])
def read_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: str | None = ""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(
        models.Post, 
        func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).order_by(models.Post.id).filter(
                models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts 

# Needs to be last in the list of endpoints because it is a path parameter
@router.get("/{id}", response_model=schemas.PostResponseWithVotes)
def read_post(id: int, response: Response, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, 
            func.count(models.Vote.post_id).label("votes")).join(
                models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).order_by(models.Post.id).filter(
                    models.Post.id == id).first()

    if post:
        return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id '{id}' not found."
    )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post_full(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if updated_post:
        if updated_post.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this post."
            )

        post_query.update(post.model_dump(), synchronize_session=False)
        db.commit()
        return post_query.first()
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id '{id}' not found."
    )

@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id '{id}' not found."
        )

    if existing_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post."
        )
    
    updated_data = post.model_dump(exclude_unset=True)

    if not updated_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update."
        )
        
    post_query.update(updated_data, synchronize_session=False)
    db.commit()

    return post_query.first()


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT, response_model=None)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if deleted_post:
        if deleted_post.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this post."
            )


        db.delete(deleted_post)
        db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id '{id}' not found."
        )