from fastapi import FastAPI
from . import models
from .routes import post, user, auth, vote
from .database import engine

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(post.route)
app.include_router(auth.route)
app.include_router(user.route)
app.include_router(vote.route)


