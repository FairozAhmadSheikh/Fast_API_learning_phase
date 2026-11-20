from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from src.posts.router import task_route
from src.utils.db import Base,engine
from src.users.router import user_router
from src.utils.rate_limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

Base.metadata.create_all(engine)


origins=['http://localhost:5173']

app=FastAPI(title="Instagram Cloned API")
app.state.limiter=limiter
app.add_exception_handler(RateLimitExceeded,
                          _rate_limit_exceeded_handler)

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_headers=['*'],
                   allow_methods=['*'])

# Additional Routes
app.include_router(task_route)
app.include_router(user_router)

 
@app.get("/")
@limiter.limit('5/minute')
def health(request:Request):
    return {"status":"OK"}