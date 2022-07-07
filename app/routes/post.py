from typing import List, Optional
from fastapi import  APIRouter, Response, status, Depends
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session


from .. import schemas,models, oauth2
from ..database import get_db

route = APIRouter(prefix='/post', tags=['Post'])


@route.get('/', response_model= List[schemas.PostOut])
#@route.get('/', response_model= List[schemas.Post])
def get_posts(db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),
limit: int = 10, skip:int = 0, search:Optional[str]=""):
    #cursor.execute("""SELECT * from post""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    #print(posts)
    #posts = posts.all
    return posts


@route.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user:int = Depends(
    oauth2.get_current_user)):
    #cursor.execute("""SELECT * from post where id = %s""",(str(id)))
    #post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()
    print(post)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post not found')
    return post


@route.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post:schemas.CreatePost, db: Session = Depends(get_db), current_user:int = Depends(
    oauth2.get_current_user)):
    #cursor.execute(""" INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #            (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    #print(current_user.id)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@route.put('/update/{id}', response_model=schemas.Post)
def update_post(id:int, post:schemas.CreatePost, db: Session = Depends(get_db), current_user:int = Depends(
    oauth2.get_current_user)):
    # cursor.execute(""" UPDATE post SET title=%s, content=%s, published=%s where id = %s RETURNING *""",
    #             (post.title, post.content, post.published, str(id)))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = db.query(models.Post).filter(models.Post.id == id)
    old_post = new_post.first()
    if old_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='Post not found')
    current_user_post = new_post.filter(models.Post.owner_id == current_user.id).first()
    print(current_user_post)
    if current_user_post is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User is not authorized")
    new_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return new_post.first()


@route.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user:int = Depends(
    oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    to_be_delete = post.first()
    if to_be_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    is_current_user_post = post.filter(models.Post.owner_id == current_user.id).first()
    if is_current_user_post is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized")
    post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT,content='Post deleted')