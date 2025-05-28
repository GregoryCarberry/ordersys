from sqlalchemy import Column, Integer, String, Boolean
from ..db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    role = Column(String(50), nullable=False)
    can_grant_permissions = Column(Boolean, default=False)  # can this user grant perms?
    store_id = Column(Integer, nullable=True)  # optional store assignment

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
