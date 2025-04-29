from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db import Base

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    items = Column(Text, nullable=False)
    status = Column(String(50), default='pending')
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    store = relationship("Store", back_populates="orders")
