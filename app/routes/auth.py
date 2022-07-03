from fastapi import  APIRouter, Response, status, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas,models, utils, oauth2
from ..database import get_db


route = APIRouter(prefix='/user', tags=['Authenticate'])

@route.post('/login', response_model=schemas.Token)
def login(credential:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credential.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='invalid credentials')
    plain_password = credential.password
    hashed_password = user.password
    if not utils.verify_password(credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='invalid credentials')

    access_token = oauth2.create_access_token({"user_id":user.id})
    return {"access_token":access_token, "token_type":"bearer"}
