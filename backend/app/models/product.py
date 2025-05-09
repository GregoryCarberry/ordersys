from sqlalchemy import Column, Integer, String, Boolean
from app.db import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    barcode = Column(String(100), unique=True, nullable=True)
    active = Column(Boolean, default=True)
    stock_quantity = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=10) 