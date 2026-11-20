from pydantic import BaseModel


class PostSchema(BaseModel):
    post_title:str
    post_description:str
    post_is_completed:bool
    
