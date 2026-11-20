from sqlalchemy.orm import Session
from sqlalchemy import Column,Integer,Boolean,String
from src.utils.db import Base


class UserModel(Base):
    __tablename__="user_table"
    user_id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    username=Column(String,nullable=False)
    email=Column(String,nullable=False)
    phone_number=Column(Integer,nullable=False)
    hash_password=Column(String,nullable=False)
    
