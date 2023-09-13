from sqlalchemy import Column, String, Uuid, Boolean
from src.configs.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, nullable=False)
    email = Column(String)
    fullname = Column(String)
    password = Column(String)
    photo = Column(String, comment="Filled by filename only")
    deleted = Column(Boolean, default=False)