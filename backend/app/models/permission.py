from sqlalchemy import Column, Integer, String, Text
from ..db import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Permission(id={self.id}, name='{self.name}')>"
