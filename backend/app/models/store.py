# backend/app/models/store.py

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db import Base

class Store(Base):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    location = Column(String(255), nullable=True)
    active = Column(Boolean, default=True)

    # Relationship to Order model
    orders = relationship("Order", back_populates="store")
