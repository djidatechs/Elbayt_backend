
from sqlalchemy import  Column, Integer, String, Float , ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Wilayas(Base):
    __tablename__ = "wilayas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    communes = relationship("Commune", back_populates="Wilayas")
  
class Communes(Base):
    __tablename__ = "communes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    wilaya_id = Column(Integer, ForeignKey("wilayas.id"))
    wilaya = relationship("Wilayas", back_populates="communes")
  