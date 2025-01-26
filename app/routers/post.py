from app import oauth2
from .. import models, schemas
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.orm import session
from fastapi import Response, status, HTTPException, Depends, APIRouter, Query
from typing import List, Optional

router = APIRouter(
    prefix='/posts',
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
def get_post(db: session = Depends(get_db), current_user : int =Depends(oauth2.get_current_user),  search: Optional[str]="", Limit: int = Query(2, alias="limit", ge=1)):
    # print(Limit)

   
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).all()

    print(result)

    return result


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: session = Depends(get_db)):

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: session = Depends(get_db), current_user : int =Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post



    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: session = Depends(get_db), current_user : int =Depends(oauth2.get_current_user)):
    #deleting post


    post = db.query(models.Post).filter(models.Post.id == id)
    if  post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
        
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, updated_post: schemas.CreatePost, db: session = Depends(get_db), current_user : int =Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.model_dump(), synchronize_session =False)
    db.commit()
    return post_query.first()