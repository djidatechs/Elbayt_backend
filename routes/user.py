from fastapi import APIRouter, Body , Depends
import requests
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from db import Base , get_db
from .high import User

router =  APIRouter()

#Base.metadata.create_all(bind=engine)

@router.post("/google-oauth")
async def google_oauth(data = Body(...) ,db :  Session = Depends(get_db)):
    # Check if the origin header is present and matches the expected value
    code : str = data.get("code")
   
   

    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": "577253181136-vsp9pem3lhc62r9oajr579c9p1ihpokr.apps.googleusercontent.com",
            "client_secret": "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",
            "redirect_uri": "https://elbaytdz.netlify.app/signup",
            "grant_type": "authorization_code",
            },
            )

    access_token = response.json()
    access_token = access_token.get("access_token", None)#access "access_token" value and if there's no value makes it none with "None"
    print(access_token)



    # fetch user information
    response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={
        "Authorization": f"Bearer {access_token}",
        },
    )
    user_info = response.json()
    email = user_info.get("email",None)
    print(user_info)
    

    # check if user exists in the database
    user_look = db.query(User).filter(User.email == email).first()

    print ("this is userlook") 
    print(user_look)
    print(email)
    if user_look is not None :
        user_info["role"] = user_look.role
    else : 
        user_info["role"] = "user"
    
    
    if user_look is None and email is not None :
        # create a new user
        user = User(email=user_info['email'])
        print(user)
        db.add(user)
        db.commit()

    # Return the access token along with the proper CORS headers
  
    return {"access_token": access_token , "user_info" : user_info}


@router.get("/users")
async def read_users(  db : Session = Depends(get_db)):
    users = db.query(User).all()
    return users
@router.get("/users/{id}")
async def read_users(id: int,  db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    return user

@router.get("/me")
async def read_users(email: str ,   db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    return user

@router.put("/user/toadmin")
async def make_admin( id : int, db : Session = Depends(get_db)):
    query = db.query(User).filter(User.id == id)
    query.update({User.role: "admin"})
    db.commit()
    return {"massage" : "You have new admin"}


