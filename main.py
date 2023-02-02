
from fastapi import FastAPI 
from routes import realestate , user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
 "http://localhost:3000"
 , "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(realestate.router)
app.include_router(user.router)