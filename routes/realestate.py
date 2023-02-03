from fastapi import APIRouter ,Query  ,Depends , Body
from typing import List , Optional
from pydantic import BaseModel
from sqlalchemy.orm import  Session , joinedload
import base64
from .high import RealEstate  , User , Photos , Messages , Communes , Wilayas 
from db import  get_db


router = APIRouter()


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
    photos:  List[str]



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
    print("\n\n\n")
    print("\n\n\n")
    print("\n\n\n")
    print(realestate.photos)
    print("\n\n\n")
    print("\n\n\n")
    print("\n\n\n")

    for photo in realestate.photos:
        decoded_photo = base64.b64decode(photo)
        photo_db = Photos(data=decoded_photo,realestate_id=realestate_.id)
        db.add(photo_db)
    

    db.commit()
    

    

    return {"id": realestate_.id}


@router.delete("/realestate/{id}/remove")
async def remove_realestate(id: int , db : Session = Depends(get_db)):
    real_estate = db.query(RealEstate).filter(RealEstate.id==id).first()
    db.delete(real_estate)
    db.commit()
    return {"message": "Real estate deleted"}

@router.get("/realestate/{id}")
async def read_realestate_with_id(id: int , db : Session = Depends(get_db) ):
    realestate = db.query(RealEstate).options(joinedload(RealEstate.photos)).get(id)
    realestate.encoded_photos = [{"id": photo.id, "data": base64.b64encode(photo.data).decode("utf-8")} for photo in realestate.photos]
    realestate.photos = []
    return realestate


@router.get("/realestate")
async def read_real_estates_filter(
    page : int =1, 
    size : int = 4,
    db : Session = Depends(get_db),
    category: Optional[str] = Query(None, alias="category"),
    property_type: Optional[str] = Query(None, alias="property_type"),
    wilaya: Optional[str] = Query(None, alias="wilaya"),
    commune: Optional[str] = Query(None, alias="commune"),
    nophotos: Optional[str] = Query(None, alias="nophotos"),
    onephoto : Optional[str] = Query(None, alias="onephoto")
):
    

    if nophotos :
        filtered_listings = db.query(RealEstate).all()
    else :
        filtered_listings = db.query(RealEstate).options(joinedload(RealEstate.photos)).all()
        if onephoto : 
             for realestate in filtered_listings:
                if realestate.photos : 
                    photo = realestate.photos[0]
                    photo = {"id": photo.id, "data": base64.b64encode(photo.data).decode("utf-8")}
                    realestate.encoded_photos = [photo]
                else :
                    realestate.encoded_photos = []
                realestate.photos = []
        else :                
            for realestate in filtered_listings:
                realestate.encoded_photos = [{"id": photo.id, "data": base64.b64encode(photo.data).decode("utf-8")} for photo in realestate.photos]
                realestate.photos = []

    
    if category:
        filtered_listings = [listing for listing in filtered_listings if listing.category == category]
    if property_type:
        filtered_listings = [listing for listing in filtered_listings if listing.property_type == property_type]
    if commune:
        filtered_listings = [listing for listing in filtered_listings if commune == str(listing.commune_id)]
    elif wilaya:
        filtered_listings = [listing for listing in filtered_listings if wilaya ==str( listing.wilaya_id)]
    
  

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
async def read_realestate_photos(realestate : int  , onlyone : str , db : Session = Depends(get_db)):
    photos = db.query(Photos).filter(Photos.realestate_id == realestate).all()
    if not photos:
        return []
    if onlyone : 
        photo = photos[0]
        photo = {"id": photo.id, "data": base64.b64encode(photo.data).decode("utf-8")}
        return [photo]

    else:
        photos = [{"id": photo.id, "data": base64.b64encode(photo.data).decode("utf-8")} for photo in photos]
    
        
    return photos


@router.get("/messages")
async def read_messages(  sender_id :Optional[int] = Query(None, alias="sender_id") ,  db : Session = Depends(get_db)):
    if sender_id:
        messages = db.query(Messages).filter(Messages.sender_id == sender_id).all()
        return messages
    return []


    
@router.post("/messages")
async def write_messages(data = Body(...),db : Session = Depends(get_db)):
    text  = data.get("text" )
    name  = data.get("name" )
    adress  = data.get("adress" )
    phone  = data.get("phone" )
    email = data.get("email")
    realestate_id  = data.get("realestate_id" )
    
    
    sender_id = db.query(User).filter(User.email == email).first()
    sender_id = sender_id.id
    print (sender_id)    
    recipient_id =  db.query(RealEstate).filter(RealEstate.id == int(realestate_id)).first()
    recipient_id = recipient_id.user_id

    Object = Messages (
        text=text ,
        name=name ,
        adress=adress ,
        phone=phone ,
        email=email ,
        realestate_id=realestate_id ,
        sender_id=sender_id ,
        recipient_id=recipient_id ,
    )

    db.add(Object)
    db.flush()
    db.commit()
    
    return {"ok" : True }



#Base.metadata.create_all(bind=engine)



    