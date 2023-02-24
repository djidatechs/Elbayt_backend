
from sqlalchemy import  Column, Integer, VARCHAR, Float, Enum , ForeignKey , LargeBinary
from sqlalchemy.orm import relationship 
from db import Base , engine



class RealEstate(Base):
    __tablename__ = "realestate"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(Enum("Sale", "Exchange", "Rent", "Vacation Rent", name="category_enum"))
    property_type = Column(VARCHAR(100))
    surface = Column(Float)
    description = Column(VARCHAR(100))
    price = Column(Float)
    contact_phone = Column(VARCHAR(100))
    property_address = Column(VARCHAR(100))

    photos = relationship("Photos", backref="realestate")
    messages = relationship("Messages", backref="realestate")

    user_id = Column(Integer, ForeignKey("users.id"))

    wilaya_id = Column(Integer, ForeignKey("wilayas.id"))

    commune_id = Column(Integer, ForeignKey("communes.id"))

    commune_id = Column(Integer, ForeignKey("communes.id"))



class Photos(Base):
    __tablename__ = 'photos'
    id = Column(Integer, primary_key=True)
    data = Column(LargeBinary)
    realestate_id = Column(Integer, ForeignKey("realestate.id"))

class Wilayas(Base):
    __tablename__ = "wilayas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(100))
    communes = relationship("Communes", backref="wilayas")
    realestate = relationship("RealEstate", backref="wilayas")

  
class Communes(Base):
    __tablename__ = "communes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(100))
    wilaya_id = Column(Integer, ForeignKey("wilayas.id"))
    realestate = relationship("RealEstate", backref="communes")
  
class Messages(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(VARCHAR(100))
    name =  Column(VARCHAR(100))
    adress =  Column(VARCHAR(100))
    phone = Column(VARCHAR(100))
    email =  Column(VARCHAR(100))
    realestate_id = Column(Integer, ForeignKey("realestate.id"))
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    sender = relationship("User", foreign_keys=[sender_id])
    recipient = relationship("User", foreign_keys=[recipient_id])


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(VARCHAR(100))
    role = Column(Enum("user", "admin", name="role_types"), default="user")
    real_estates = relationship("RealEstate", backref="user")
    sent_messages = relationship("Messages", foreign_keys=[Messages.sender_id], backref="sender_user")
    received_messages = relationship("Messages", foreign_keys=[Messages.recipient_id], backref="recipient_user" , overlaps="recipient_user")


# Base.metadata.create_all(bind=engine)