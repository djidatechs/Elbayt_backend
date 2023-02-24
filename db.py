from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker , relationship ,Session
Base = declarative_base()
engine = create_engine("postgresql://postgres:OjSHIzgkQx1HrJ1EQUmu@containers-us-west-163.railway.app:7660/railway")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()

# Base.metadata.create_all(bind=engine)