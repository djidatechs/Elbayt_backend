from fastapi import APIRouter ,Query , UploadFile  ,Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List , Optional
from pydantic import BaseModel
from sqlalchemy import  Column, Integer, String, Float, Enum , ForeignKey , LargeBinary
from sqlalchemy.orm import sessionmaker , relationship , Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.default import AbstractParams, BasePage, RawParams
import jwt
from .user import User
import base64
from db import engine , Base , get_db


router = APIRouter()



class RealEstate(Base):
    __tablename__ = "realestate"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(Enum("Sale", "Exchange", "Rent", "Vacation Rent", name="category_enum"))
    property_type = Column(String)
    surface = Column(Float)
    description = Column(String)
    price = Column(Float)
    contact_phone = Column(String)
    property_address = Column(String)

    photos = relationship("Photos", backref="realestate")

    user_id = Column(Integer, ForeignKey("users.id"))

    wilaya_id = Column(Integer, ForeignKey("wilayas.id"))

    commune_id = Column(Integer, ForeignKey("communes.id"))

class RealEstateCreate(BaseModel):
    category: str
    property_type: str
    surface: float
    description: str
    price: float
    contact_phone: str
    wilaya_id: int
    commune_id: int
    user: str
    property_address: str
    photos: List[str] = []



@router.post("/realestate/")
async def create_realestate(realestate: RealEstateCreate , db : Session = Depends(get_db)):
    
    user = db.query(User).filter(User.email == realestate.user).first()
    realestate_ = RealEstate(
        category=realestate.category,
        property_type=realestate.property_type,
        surface=realestate.surface,
        description=realestate.description,
        price=realestate.price,
        contact_phone=realestate.contact_phone,
        wilaya_id=realestate.wilaya_id,
        user_id=user.id,
        commune_id=realestate.commune_id,
        property_address=realestate.property_address,
    )
    db.add(realestate_)
    db.flush()


    for photo in realestate.photos:
        new_photo = Photos(data=photo, realestate_id=realestate_.id)
        db.add(new_photo)
    db.commit()
    

    

    return {"id": realestate_.id}


@router.delete("/realestate/{id}/remove")
async def remove_realestate(id: int , db : Session = Depends(get_db)):
    real_estate = db.query(RealEstate).filter_by(id=id).first()
    db.delete(real_estate)
    db.commit()
    return {"message": "Real estate deleted"}

@router.get("/realestate/{id}")
async def read_realestate_with_id(id: int , db : Session = Depends(get_db) ):
    realestate = db.query(RealEstate).get(id)
    return realestate

@router.get("/realestate")
async def read_real_estates_filter(
    page : int =1, 
    size : int = 4,
    db : Session = Depends(get_db),
    category: Optional[str] = Query(None, alias="category"),
    property_type: Optional[str] = Query(None, alias="property_type"),
    wilaya: Optional[str] = Query(None, alias="wilaya"),
    commune: Optional[str] = Query(None, alias="commune")
):
    

    
    filtered_listings = db.query(RealEstate).all()
    
    if category:
        filtered_listings = [listing for listing in filtered_listings if listing.category == category]
    if property_type:
        filtered_listings = [listing for listing in filtered_listings if listing.property_type == property_type]
    if commune:
        filtered_listings = [listing for listing in filtered_listings if commune == str(listing.commune_id)]
    elif wilaya:
        filtered_listings = [listing for listing in filtered_listings if wilaya ==str( listing.wilaya_id)]
    

    filtered_listings


    def paginate(array, size, page_number):
        start = (page_number - 1) * size
        end = start + size
        return array[start:end]
    return paginate(filtered_listings , size , page)


 # Replace with your own secret ke
async def get_current_user(db : Session = Depends(get_db)):

    return 



@router.get("/myrealestates")
async def read_my_realestates(email : str , db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    realestates = db.query(RealEstate).filter(RealEstate.user_id == user.id).all()
    
    if not realestates : 
            return {}
    return realestates

@router.get("/communes")
async def read_communes(wilaya : int  , db : Session = Depends(get_db)):
    communes = db.query(Communes).filter(Communes.wilaya_id == wilaya).all()
    return communes

@router.get("/wilayas/all")
async def read_communes( db : Session = Depends(get_db)):
    wil = db.query(Wilayas).all()
    return wil


@router.get("/wilayascommune")
async def read_wilayas(communeID : int  , db : Session = Depends(get_db)):
    commune = db.query(Communes).filter(Communes.id == communeID).first()
    wilaya = db.query(Wilayas).filter(Wilayas.id == commune.wilaya_id).first()
    
    return {"wilaya": wilaya.name , "commune" : commune.name}

@router.get("/photos_realestate")
async def read_realestate_photos(realestate : int  , db : Session = Depends(get_db)):
    photos = db.query(Photos).filter(Photos.realestate_id == realestate).all()
    return photos

class Photos(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    data = Column(String)
    realestate_id = Column(Integer, ForeignKey("realestate.id"))

class Wilayas(Base):
    __tablename__ = "wilayas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    communes = relationship("Communes", backref="wilayas")
    realestate = relationship("RealEstate", backref="wilayas")

  
class Communes(Base):
    __tablename__ = "communes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    wilaya_id = Column(Integer, ForeignKey("wilayas.id"))
    realestate = relationship("RealEstate", backref="communes")
  
#Base.metadata.create_all(bind=engine)



    