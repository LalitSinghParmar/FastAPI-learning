from typing import List
from fastapi import  APIRouter, Response, status, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from .. import schemas,models, utils
from ..database import get_db


route = APIRouter(prefix='/user', tags=['User'])

@route.post('/create', response_model=schemas.getUser, status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.User, db: Session = Depends(get_db)):
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@route.get('/{id}', response_model=schemas.getUser)
def get_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * from post where id = %s""",(str(id)))
    #post = cursor.fetchone()
    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail='User not found')
    return user