from .base import Base

from sqlalchemy import Column, Integer, String, JSON


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    permissions = Column(JSON)
