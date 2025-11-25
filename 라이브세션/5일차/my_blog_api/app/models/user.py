from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from app.db.session import Base

class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(Integer, primary_key=True)
    username:Mapped[str]=mapped_column(String, unique=True, index=True)
    email:Mapped[str]=mapped_column(String, unique=True)
    password_hash:Mapped[str]=mapped_column(String)
