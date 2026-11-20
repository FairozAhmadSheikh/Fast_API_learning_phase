from fastapi import APIRouter,status,Depends,Request,UploadFile,File
from src.users.dtos import UserSchema,LoginSchema,UserResponseSchema
from src.utils.db import get_db
from sqlalchemy.orm import Session
from src.users import controller
from src.utils.rate_limiter import limiter

user_router=APIRouter(prefix='/users')


@user_router.post('/register',response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED)
def register(body:UserSchema,db:Session=Depends(get_db)):
    return controller.register(body,db) 

@user_router.post('/login',status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
def login(request:Request,body:LoginSchema,db:Session=Depends(get_db)):
    return controller.login(body,db)

@user_router.get('/is_authenticated',response_model=UserResponseSchema,status_code=status.HTTP_200_OK)
def is_authenticated(request:Request,db:Session=Depends(get_db)):
    return controller.is_authenticated(request,db)

@user_router.post('/upload')
def upload(file:UploadFile=File(...)):
    return controller.upload(file)