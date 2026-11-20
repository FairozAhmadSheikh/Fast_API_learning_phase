from sqlalchemy import Column,Integer,Boolean,String,ForeignKey
from src.utils.db import Base


class PostModel(Base):
    __tablename__="tasks_table"
    post_id=Column(Integer,primary_key=True)
    post_title=Column(String)
    post_description=Column(String)
    post_is_completed=Column(Boolean,default=False)
    user_id=Column(Integer,ForeignKey("user_table.user_id",ondelete='CASCADE'))