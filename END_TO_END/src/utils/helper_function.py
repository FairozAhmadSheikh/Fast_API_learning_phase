from src.utils.db import get_db
from fastapi import Depends,Request,HTTPException,status
from sqlalchemy.orm import Session
import jwt 
from jwt.exceptions import InvalidTokenError
from src.utils.settings import settings
from src.users.models import UserModel

def is_authenticated(request:Request,db:Session=Depends(get_db)):
    token=request.headers.get("authorization")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not Authorized")
    token=token.split(' ')[-1]
    data=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
    user_id=data.get("_id")
    user=db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized")
    return user
    