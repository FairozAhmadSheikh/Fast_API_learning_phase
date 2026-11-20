from src.posts.dtos import PostSchema
from src.posts.models import PostModel
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from src.users.models import UserModel


def create_post(body:PostSchema,db:Session,user:UserModel):
    
    data=body.model_dump()
    new_post=PostModel(
        post_title=data['post_title'],
        post_description=data['post_description'],
        post_is_completed=data['post_is_completed'],
        user_id=user.user_id
    )
    try:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong")


def get_all_posts(db:Session,user:UserModel):
    user_id=user.user_id
    data=db.query(PostModel).filter(PostModel.user_id ==user_id).all()
    if data != None:
        return data
    return "No Posts Yet"

def get_one_post(post_id:int,db:Session,user:UserModel):
    one_post=db.query(PostModel).filter(PostModel.post_id == post_id).first()
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Task ID")
    if one_post.user_id !=user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized")
    return one_post

def update_post(post_id:int,body:PostSchema,db:Session,user:UserModel):
    one_post=db.query(PostModel).filter(PostModel.post_id == post_id).first()
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Task ID")
    if one_post.user_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized")
    
    body=body.model_dump()

    for key,value in body.items():
        setattr(one_post,key,value)
    try:
        db.commit()
        db.refresh(one_post)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Something went wrong")

    return {'Message':"Task Updated Succesfully",
            'Updated':one_post}


def delete_post(post_id:int,db:Session,user:UserModel):
    one_post=db.query(PostModel).filter(PostModel.post_id == post_id).first()
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Task ID")
    if one_post.user_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized")
    db.delete(one_post)
    db.commit()
    return None