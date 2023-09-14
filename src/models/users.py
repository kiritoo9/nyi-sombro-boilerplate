from sqlalchemy import Column, String, Uuid, Boolean, Date, DateTime, Float
from src.configs.database import Base

class Users(Base):
	__tablename__ = "users"

	id = Column(Uuid, nullable=False, comment="", primary_key=True)
	email = Column(String, nullable=True, comment="")
	fullname = Column(String, nullable=True, comment="")
	password = Column(String, nullable=True, comment="")
	photo = Column(String, nullable=True, comment="")
	deleted = Column(Boolean, nullable=True, comment="")
	total = Column(Numeric, nullable=True, comment="")
	periode = Column(Integer, nullable=True, comment="")
	dibuat = Column(Date, nullable=True, comment="")
	created_date = Column(DateTime, nullable=True, comment="")
