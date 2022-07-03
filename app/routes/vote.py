from fastapi import  APIRouter, Response, status, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from .. import schemas,models, oauth2
from ..database import get_db

route = APIRouter(prefix='/vote', tags=['Vote'])

@route.get('/', status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post {vote.post_id} not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id,
    models.Vote.post_id==vote.post_id)
    vote_status = vote_query.first()
    if vote.vote_dir == 1:
        if vote_status:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=f'User {current_user.id} already voted for post {vote.post_id}')
        new_vote = models.Vote(user_id = current_user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        return {'message':'Successfully added vote'}    
    else:
        if vote_status is None:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=f'User {current_user.id} not voted for post {vote.post_id}')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message':'Successfully deleted vote'} 
    
