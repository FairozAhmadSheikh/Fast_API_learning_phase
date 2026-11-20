from fastapi import APIRouter,status,HTTPException,Depends
from src.posts.dtos import PostSchema
from src.posts.models import PostModel
from src.posts import controller
from src.utils.db import get_db
from sqlalchemy.orm import Session
from src.utils.helper_function import is_authenticated
from src.users.models import UserModel
from src.users.dtos import UserResponseSchema

task_route=APIRouter(prefix="/post")

@task_route.post('/create_post',status_code=status.HTTP_201_CREATED)
def create_post(body:PostSchema,db:Session=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controller.create_post(body,db,user)

@task_route.get('/get_all_posts')
def get_all_posts(db:Session=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controller.get_all_posts(db,user)

@task_route.get('/get_one_post/{post_id}')
def get_one_post(post_id:int,db:Session=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controller.get_one_post(post_id,db,user)

@task_route.post('/update_post/{post_id}')
def update_post(post_id:int,body:PostSchema,db:Session=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controller.update_post(post_id,body,db,user)

@task_route.delete('/delete_post/{post_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_task(post_id:int,db:Session=Depends(get_db),user:UserModel=Depends(is_authenticated)):
    return controller.delete_post(post_id,db,user)