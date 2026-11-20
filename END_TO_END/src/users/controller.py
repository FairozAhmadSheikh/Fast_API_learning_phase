from src.users.models import UserModel
from src.users.dtos import UserSchema,LoginSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException,status,Request,UploadFile,File
import jwt 
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from datetime import datetime,timedelta,timezone
from src.utils.settings import settings
from sqlalchemy.orm import Session

password_hash=PasswordHash.recommended()

def create_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_pass,hash_pass):
    return password_hash.verify(plain_pass,hash_pass)

def register(body:UserSchema,db:Session):
    user=db.query(UserModel).filter(UserModel.username == body.username).first()
    email=db.query(UserModel).filter(UserModel.email==body.email).first()
    if user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Username Occupied")
    if email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Email already Exists")
    data=body.model_dump()
    hash_password=create_password_hash(data.get('password'))
    new_user=UserModel(
        name=data.get('name'),
        username=data.get('username'),
        email=data.get('email'),
        phone_number=data.get('phone_number'),
        hash_password=hash_password
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Something went wrong")

def login(body:LoginSchema,db:Session):
    user=db.query(UserModel).filter(UserModel.username==body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    if not verify_password(body.password,user.hash_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    exp_time=datetime.now(timezone.utc)+timedelta(minutes=settings.EXP_TIME)
    token=jwt.encode({"_id":user.user_id,"exp":exp_time},settings.SECRET_KEY,settings.ALGORITHM)

    return {"token":token}

def is_authenticated(request:Request,db:Session):
    token=request.headers.get("authorization")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not Authorized")
    token=token.split(' ')[-1]
    data=jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
    user_id=data.get("_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not Authorized")
    user_data=db.query(UserModel).filter(UserModel.user_id==user_id).first()

    return user_data

def upload(file:UploadFile=File(...)):
    return {
        "filename":file.filename,
        "file-type":file.content_type,
        "message":"File Uploaded Successfully"
    }